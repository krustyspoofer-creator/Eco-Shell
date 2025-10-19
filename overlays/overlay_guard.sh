#!/bin/bash
# overlay_guard.sh - require signed overlays; refuse injection if signature invalid
set -euo pipefail

OVERLAY_PATH="$1"
PUBKEY_PATH="overlays/sig-public.pem"
LOGFILE="overlays/overlay_guard.log"

if [ ! -f "$OVERLAY_PATH" ]; then
  echo "Overlay not found: $OVERLAY_PATH" >&2
  exit 2
fi

if [ ! -f "$PUBKEY_PATH" ]; then
  echo "Public key missing ($PUBKEY_PATH). Refusing to inject overlays." | tee -a "$LOGFILE"
  exit 3
fi

SIG_PATH="$OVERLAY_PATH.sig"
if [ ! -f "$SIG_PATH" ]; then
  echo "Signature missing for $OVERLAY_PATH. Refusing to inject." | tee -a "$LOGFILE"
  exit 4
fi

# verify signature using openssl
if ! openssl dgst -sha256 -verify "$PUBKEY_PATH" -signature "$SIG_PATH" "$OVERLAY_PATH" >/dev/null 2>&1; then
  echo "Signature verification failed for $OVERLAY_PATH" | tee -a "$LOGFILE"
  exit 5
fi

echo "Signature valid for $OVERLAY_PATH" >> "$LOGFILE"
exit 0
