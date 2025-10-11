#!/bin/bash
# EchoShell Boot Invocation
export OVERLAY_ID="EchoShell"
export TRIGGER_KEY="echo_invoke"

echo "[+] Booting EchoShell with trigger: $TRIGGER_KEY"
bash ./fallback_loop.sh
