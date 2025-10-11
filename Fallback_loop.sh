#!/bin/bash
# Sovereign Fallback Loop
export HEAL_KEY="echo_heal"

echo "[+] Activating fallback loop: $HEAL_KEY"
if ! pgrep -f daemon_reflect.sh > /dev/null; then
  nohup bash ./daemon/daemon_reflect.sh &
  echo "[+] Daemon restored"
else
  echo "[✓] Daemon already active"
fi
