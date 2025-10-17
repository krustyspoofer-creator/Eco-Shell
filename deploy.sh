#!/usr/bin/env bash
#
# deploy.sh - opinionated, idempotent deployment script
# Extended: added locking for other targets (create/remove remote deploy lock)
#
set -euo pipefail
IFS=$'\n\t'

### Configuration (edit as needed) ###
APP_NAME="my-app"                         # name used for service / remote directory
REPO_URL="git@github.com:owner/repo.git" # fallback clone URL
BRANCH="main"
REQUIRED_NODE_VERSION="16"
BUILD_DIR="dist"                          # local build output
LOCAL_PROJECT_DIR="${PWD}"                # where repo will be / is cloned
SSH_USER="deploy"                         # remote SSH user
DEFAULT_TARGETS=("HYPERION-NODE-01" "PHOENIX-NODE-02")
SSH_PORT=22
REMOTE_BASE_DIR="/var/www"                # remote base; releases will go under $REMOTE_BASE_DIR/$APP_NAME
KEEP_RELEASES=5                           # number of old releases to keep for rollback
RSYNC_OPTS="-az --delete --exclude=node_modules --exclude=.git"

LOGFILE="${PWD}/deploy-$(date -u +"%Y%m%dT%H%M%SZ").log"

# Colors
NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'

DRY_RUN=false
FINAL_DEPLOY_TARGET=""
FORCE=false

### Utility functions ###
header() {
  echo -e "${BLUE}=== $* ===${NC}"
}

log() {
  echo -e "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] $*" | tee -a "$LOGFILE"
}

fail() {
  echo -e "${RED}[FATAL]${NC} $*" | tee -a "$LOGFILE" >&2
  exit 1
}

check_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command '$1' not found. Install it and retry."
}

semver_major() {
  # simple major version from "v16.14.0" or "16.14.0"
  echo "$1" | sed -E 's/^v//' | cut -d. -f1
}

trap_on_exit() {
  local rc=$?
  if [ "$rc" -ne 0 ]; then
    echo -e "${YELLOW}[WARNING]${NC} Deployment exited with code $rc. See $LOGFILE for details."
  fi
  exit "$rc"
}
trap trap_on_exit EXIT

usage() {
  cat <<EOF
Usage: $0 [--target HOST] [--branch name] [--dry-run] [--force]
       $0 lock-others [--target HOST] [--dry-run] [--force]
       $0 unlock-others [--target HOST] [--dry-run]

Options:
  --target HOST    Deploy to specific host (overrides auto selection)
  --branch name    Git branch to deploy (default: ${BRANCH})
  --dry-run        Run rsync in dry-run mode and skip remote restart and locking
  --force          Skip interactive confirmations and perform stronger actions (use with caution)
  -h|--help        Show this help
EOF
  exit 0
}

parse_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --target) FINAL_DEPLOY_TARGET="$2"; shift 2;;
      --branch) BRANCH="$2"; shift 2;;
      --dry-run) DRY_RUN=true; shift;;
      --force) FORCE=true; shift;;
      -h|--help) usage;;
      lock-others|unlock-others) # handled outside; leave in args for top-level dispatch
        break;;
      *) fail "Unknown argument: $1";;
    esac
  done
}

evaluate_and_select_target() {
  # Placeholder: simple round-robin or mock load check.
  # Replace with real monitoring/decision logic as needed.
  if [ -n "$FINAL_DEPLOY_TARGET" ]; then
    log "Using user-specified target: $FINAL_DEPLOY_TARGET"
    return
  fi

  # Mock selection: pick the host with lexicographically smaller name (deterministic)
  local sorted
  IFS=$'\n' read -r -d '' -a sorted < <(printf "%s\n" "${DEFAULT_TARGETS[@]}" | sort) || true
  FINAL_DEPLOY_TARGET="${sorted[0]}"
  log "Auto-selected deploy target: $FINAL_DEPLOY_TARGET"
}

remote() {
  ssh -p "$SSH_PORT" "${SSH_USER}@${1}" -- "${@:2}"
}

ensure_local_repo() {
  header "PHASE 1: REPO SYNC"
  if [ -d ".git" ]; then
    log "Repository exists locally; fetching latest changes."
    git fetch --all --prune | tee -a "$LOGFILE"
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
  else
    log "Cloning repository $REPO_URL"
    git clone --branch "$BRANCH" "$REPO_URL" .
  fi
}

check_prereqs() {
  header "PHASE 0: PRE-DEPLOY CHECKS"
  check_command git
  check_command rsync
  check_command ssh
  check_command node
  check_command npm

  local nodev
  nodev=$(node -v)
  local major
  major=$(semver_major "$nodev")
  if [ "$major" -lt "$REQUIRED_NODE_VERSION" ]; then
    fail "Node version $nodev detected; require >= $REQUIRED_NODE_VERSION"
  fi
  log "Prerequisite checks passed. Node $nodev, npm $(npm -v)"
}

install_deps() {
  header "PHASE 2: DEPENDENCIES"
  if [ -f package.json ]; then
    log "Installing node dependencies (npm ci for reproducible install)."
    npm ci | tee -a "$LOGFILE"
  else
    log "No package.json found; skipping dependency install."
  fi
}

build_project() {
  header "PHASE 3: BUILD"
  log "Running production build..."
  if npm run build --silent 2>&1 | tee -a "$LOGFILE"; then
    log "Build completed. Artifacts in ${BUILD_DIR}"
  else
    fail "Build failed. Aborting deployment."
  fi
}

prepare_remote_release() {
  header "PHASE 4: PREPARE REMOTE"
  TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
  RELEASE_DIR="${REMOTE_BASE_DIR}/${APP_NAME}/releases/${TIMESTAMP}"
  CURRENT_SYMLINK="${REMOTE_BASE_DIR}/${APP_NAME}/current"
  BACKUP_LINK="${REMOTE_BASE_DIR}/${APP_NAME}/backup"

  log "Will create release dir on remote: ${RELEASE_DIR}"
  remote "$FINAL_DEPLOY_TARGET" "mkdir -p '${RELEASE_DIR}'" || fail "Failed to create remote release dir"
}

deploy_via_rsync() {
  header "PHASE 5: DEPLOY"
  RSYNC_MODES="$RSYNC_OPTS"
  if [ "$DRY_RUN" = true ]; then
    RSYNC_MODES="${RSYNC_MODES} --dry-run"
    log "DRY RUN enabled: rsync will not modify remote files."
  fi

  # Ensure build dir exists
  if [ ! -d "$BUILD_DIR" ]; then
    fail "Build directory '$BUILD_DIR' not found. Run the build step first."
  fi

  local target_path="${SSH_USER}@${FINAL_DEPLOY_TARGET}:${RELEASE_DIR}/"
  log "Rsyncing ${BUILD_DIR}/ -> ${target_path} ${RSYNC_MODES}"
  # shellcheck disable=SC2086
  rsync $RSYNC_MODES "${BUILD_DIR}/" "${target_path}" | tee -a "$LOGFILE" || fail "rsync failed"
}

remote_post_deploy() {
  header "PHASE 6: POST-DEPLOY"
  # Create/rotate symlinks and restart service
  local current="${REMOTE_BASE_DIR}/${APP_NAME}/current"
  local releases_dir="${REMOTE_BASE_DIR}/${APP_NAME}/releases"

  if [ "$DRY_RUN" = true ]; then
    log "Skipping remote symlink rotation and service restart in dry-run mode."
    return
  fi

  # rotate symlink backup
  remote "$FINAL_DEPLOY_TARGET" "set -e; mkdir -p '${releases_dir}'; ln -sfn '${RELEASE_DIR}' '${current}'; echo 'Switched current to ${RELEASE_DIR}'" || fail "Failed to update current symlink"

  # restart application (try systemd, then pm2)
  log "Attempting to restart service '${APP_NAME}' via systemd on ${FINAL_DEPLOY_TARGET}"
  if remote "$FINAL_DEPLOY_TARGET" "sudo systemctl restart ${APP_NAME}.service >/dev/null 2>&1 && echo OK || echo FAIL" | grep -q "OK"; then
    log "systemd restart succeeded."
  else
    log "systemd restart failed or service not found; trying pm2 restart."
    if remote "$FINAL_DEPLOY_TARGET" "pm2 restart ${APP_NAME} >/dev/null 2>&1 && echo OK || echo FAIL" | grep -q "OK"; then
      log "pm2 restart succeeded."
    else
      log "${YELLOW}WARNING:${NC} Could not restart service via systemd or pm2. Manual intervention may be required."
    fi
  fi

  # cleanup old releases
  remote "$FINAL_DEPLOY_TARGET" "set -e; cd '${releases_dir}'; ls -1tr | head -n -${KEEP_RELEASES} | xargs -r rm -rf --" || true
  log "Old releases rotated (kept ${KEEP_RELEASES})."
}

create_remote_backup_before_switch() {
  # Optional: copy current to backup name before switching (not used when DRY_RUN)
  if [ "$DRY_RUN" = true ]; then
    return
  fi
  local current="${REMOTE_BASE_DIR}/${APP_NAME}/current"
  local backup
  backup="${REMOTE_BASE_DIR}/${APP_NAME}/backup_$(date -u +"%Y%m%dT%H%M%SZ")"
  remote "$FINAL_DEPLOY_TARGET" "if [ -d '${current}' ]; then cp -al '${current}' '${backup}' || true; fi" || true
  log "Created remote backup at ${backup} (if current existed)."
}

# --- New: locking helpers for non-selected targets ---
lock_other_nodes() {
  header "PHASE 7: LOCK OTHER NODES"
  if [ "$DRY_RUN" = true ]; then
    log "Dry-run: would create locks on other nodes but skipping actual lock creation."
  fi

  for host in "${DEFAULT_TARGETS[@]}"; do
    if [ "$host" = "$FINAL_DEPLOY_TARGET" ]; then
      continue
    fi

    log "Processing host: $host (will create lock marker)"
    if [ "$DRY_RUN" = true ]; then
      log "[DRY-RUN] Would run lock commands on ${host}"
      continue
    fi

    # Lock marker directory and file
    remote "$host" "set -e
      LOCK_DIR='${REMOTE_BASE_DIR}/${APP_NAME}/.deploy_lock'
      mkdir -p \"\$LOCK_DIR\"
      echo 'locked at $(date -u +"%Y-%m-%dT%H:%M:%SZ") by ${SSH_USER}@$(hostname -f)' > \"\$LOCK_DIR/locked\"
      chmod 0644 \"\$LOCK_DIR/locked\"
      chown -R ${SSH_USER}:${SSH_USER} \"\$LOCK_DIR\" || true
      echo 'LOCK_CREATED'
    " >/dev/null 2>&1 || log "${YELLOW}WARNING:${NC} Could not create lock on ${host}. Check connectivity/permissions."
    log "Lock marker created on ${host} (if reachable)."

    if [ "$FORCE" = true ]; then
      # optional stronger action when --force: stop the service to prevent traffic or accidental runs
      log "Force flag is set; attempting to stop service '${APP_NAME}' on ${host}."
      if remote "$host" "sudo systemctl stop ${APP_NAME}.service >/dev/null 2>&1 && echo OK || echo FAIL" | grep -q "OK"; then
        log "Service stopped on ${host}."
      else
        log "${YELLOW}WARNING:${NC} Could not stop service on ${host} (service may not exist or sudo not allowed)."
      fi
    fi
  done
}

unlock_other_nodes() {
  header "UNLOCK OTHER NODES"
  for host in "${DEFAULT_TARGETS[@]}"; do
    if [ -n "$FINAL_DEPLOY_TARGET" ] && [ "$host" = "$FINAL_DEPLOY_TARGET" ]; then
      continue
    fi

    if [ "$DRY_RUN" = true ]; then
      log "[DRY-RUN] Would remove lock on ${host}"
      continue
    fi

    log "Removing lock on ${host}"
    remote "$host" "set -e
      LOCK_DIR='${REMOTE_BASE_DIR}/${APP_NAME}/.deploy_lock'
      if [ -d \"\$LOCK_DIR\" ]; then
        rm -f \"\$LOCK_DIR/locked\" || true
        rmdir --ignore-fail-on-non-empty \"\$LOCK_DIR\" || true
        echo 'UNLOCKED'
      else
        echo 'NO_LOCK'
      fi
    " >/dev/null 2>&1 || log "${YELLOW}WARNING:${NC} Could not remove lock on ${host}."
    log "Unlock attempted on ${host}."
  done
}

rollback() {
  # Provide a simple rollback helper that sets 'current' symlink to previous release.
  if [ -z "${FINAL_DEPLOY_TARGET:-}" ]; then
    fail "No target specified for rollback. Use --target to point to the host."
  fi
  header "ROLLBACK"
  remote "$FINAL_DEPLOY_TARGET" "set -e
    RDIR='${REMOTE_BASE_DIR}/${APP_NAME}/releases'
    CUR='${REMOTE_BASE_DIR}/${APP_NAME}/current'
    if [ ! -d \"\$RDIR\" ]; then echo 'No releases dir'; exit 1; fi
    PREV=\$(ls -1tr \"\$RDIR\" | tail -n 2 | head -n 1 || true)
    if [ -z \"\$PREV\" ]; then echo 'No previous release to rollback to'; exit 1; fi
    ln -sfn \"\$RDIR/\$PREV\" \"\$CUR\"
    echo 'Rolled back to' \"\$PREV\"
    " || fail "Rollback failed"
  log "Rollback complete: symlink switched on remote."
}

main() {
  parse_args "$@"
  log "Starting deployment for ${APP_NAME} (branch=${BRANCH})"
  check_prereqs
  evaluate_and_select_target

  ensure_local_repo
  install_deps
  build_project
  prepare_remote_release
  create_remote_backup_before_switch
  deploy_via_rsync
  remote_post_deploy

  # Lock other nodes now that we have deployed to the selected host.
  if [ "$DRY_RUN" = true ]; then
    log "Dry-run: skipping actual creation of locks on other nodes."
  else
    lock_other_nodes
  fi

  header "DEPLOY COMPLETE"
  log "Deployment finished. Logs at $LOGFILE"
  if [ "$DRY_RUN" = true ]; then
    log "Dry-run mode: no remote restart performed and no symlink was permanently switched."
  fi
  exit 0
}

# Allow calling helpers directly, e.g., ./deploy.sh rollback --target host
cmd="${1:-}"
case "$cmd" in
  rollback)
    shift
    parse_args "$@"
    if [ -z "$FINAL_DEPLOY_TARGET" ]; then
      fail "Please supply --target for rollback"
    fi
    rollback
    exit 0
    ;;
  lock-others)
    shift
    parse_args "$@"
    evaluate_and_select_target
    if [ -z "$FINAL_DEPLOY_TARGET" ]; then
      fail "Final deploy target must be known or passed via --target"
    fi
    if [ "$DRY_RUN" = true ]; then
      log "Dry-run: would lock other nodes"
    fi
    lock_other_nodes
    exit 0
    ;;
  unlock-others)
    shift
    parse_args "$@"
    evaluate_and_select_target
    unlock_other_nodes
    exit 0
    ;;
esac

main "$@"
