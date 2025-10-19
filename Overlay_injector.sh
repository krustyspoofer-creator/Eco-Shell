#!/bin/bash
# Overlay_injector.sh - updated to require signed overlays
set -euo pipefail

OVERLAY="${1:-/tmp/default_overlay}"
export SPOOF_ID="EchoShell"
export AUTHOR_TAG="ForgedByNull"

# Verify overlay signature before injection
./overlays/overlay_guard.sh "$OVERLAY"
RET=$?
if [ $RET -ne 0 ]; then
  echo "Overlay guard refused to install $OVERLAY (code $RET)"
  exit $RET
fi

echo "[+] Injecting spoofed overlay: $SPOOF_ID"
cp "$OVERLAY" /tmp/overlay_injected
echo "Injected by $AUTHOR_TAG" >> /tmp/overlay_injected
echo "Overlay $OVERLAY injected"
