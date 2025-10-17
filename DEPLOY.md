# Deployment Script Documentation

## Overview

`deploy.sh` is an opinionated, idempotent deployment script that supports automated deployments with locking mechanisms for multi-node environments.

## Features

- **Automated Deployment**: Builds and deploys Node.js applications to remote servers
- **Target Selection**: Auto-selects deployment targets or allows manual specification
- **Locking Mechanism**: Prevents accidental deployments to non-selected nodes
- **Rollback Support**: Easy rollback to previous releases
- **Dry-run Mode**: Test deployments without making actual changes
- **Release Management**: Keeps configurable number of old releases for rollback

## Configuration

Edit the configuration section at the top of `deploy.sh`:

```bash
APP_NAME="my-app"                         # Application name
REPO_URL="git@github.com:owner/repo.git" # Git repository URL
BRANCH="main"                             # Default branch to deploy
REQUIRED_NODE_VERSION="16"                # Minimum Node.js version
BUILD_DIR="dist"                          # Local build output directory
SSH_USER="deploy"                         # Remote SSH user
DEFAULT_TARGETS=("HYPERION-NODE-01" "PHOENIX-NODE-02")  # Available targets
SSH_PORT=22                               # SSH port
REMOTE_BASE_DIR="/var/www"                # Remote base directory
KEEP_RELEASES=5                           # Number of old releases to keep
```

## Usage

### Standard Deployment

Deploy to auto-selected target:
```bash
./deploy.sh
```

Deploy to specific target:
```bash
./deploy.sh --target HYPERION-NODE-01
```

Deploy specific branch:
```bash
./deploy.sh --branch feature/new-feature
```

Dry-run (no actual changes):
```bash
./deploy.sh --dry-run
```

Force deployment (with service stops):
```bash
./deploy.sh --force
```

### Lock Management

Lock non-selected nodes:
```bash
./deploy.sh lock-others --target HYPERION-NODE-01
```

Unlock other nodes:
```bash
./deploy.sh unlock-others
```

### Rollback

Rollback to previous release:
```bash
./deploy.sh rollback --target HYPERION-NODE-01
```

## Deployment Phases

1. **PHASE 0: PRE-DEPLOY CHECKS** - Verify prerequisites (git, rsync, ssh, node, npm)
2. **PHASE 1: REPO SYNC** - Clone or update local repository
3. **PHASE 2: DEPENDENCIES** - Install npm dependencies with `npm ci`
4. **PHASE 3: BUILD** - Run production build
5. **PHASE 4: PREPARE REMOTE** - Create timestamped release directory on remote
6. **PHASE 5: DEPLOY** - Rsync build artifacts to remote
7. **PHASE 6: POST-DEPLOY** - Rotate symlinks, restart service, cleanup old releases
8. **PHASE 7: LOCK OTHER NODES** - Create lock markers on non-selected nodes

## Locking Mechanism

The script creates `.deploy_lock` directories on non-selected nodes to prevent accidental deployments:

- Lock marker: `${REMOTE_BASE_DIR}/${APP_NAME}/.deploy_lock/locked`
- With `--force`: Also stops the service on locked nodes
- Unlocking removes the lock marker files

## Release Structure

Remote directory structure:
```
/var/www/my-app/
├── releases/
│   ├── 20231017T120000Z/
│   ├── 20231017T140000Z/
│   └── 20231017T160000Z/
├── current -> releases/20231017T160000Z/
└── .deploy_lock/
    └── locked
```

## Service Management

The script attempts to restart services using:
1. systemd: `sudo systemctl restart ${APP_NAME}.service`
2. pm2: `pm2 restart ${APP_NAME}` (fallback)

## Logging

All deployment operations are logged to:
```
deploy-YYYYMMDDTHHMMSSZ.log
```

## Requirements

- bash 4.0+
- git
- rsync
- ssh
- node (>= configured version)
- npm
- Remote: systemd or pm2 (optional, for service restart)

## Error Handling

- Exit on error (`set -euo pipefail`)
- Trap on exit for error reporting
- Graceful handling of missing services
- Warnings for non-critical failures

## Best Practices

1. Always test with `--dry-run` first
2. Review logs after deployment
3. Keep `KEEP_RELEASES` >= 3 for safe rollback
4. Use `--force` cautiously (stops services on locked nodes)
5. Verify SSH access and sudo permissions before deployment
