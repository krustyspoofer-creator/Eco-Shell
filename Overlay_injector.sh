#!/bin/bash
# Injects spoofed overlay into target shell
export SPOOF_ID="EchoShell"
export AUTHOR_TAG="ForgedByNull"

echo "[+] Injecting spoofed overlay: $SPOOF_ID"
touch /tmp/overlay_injected
echo "Injected by $AUTHOR_TAG" >> /tmp/overlay_injected
