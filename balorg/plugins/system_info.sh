#!/usr/bin/env bash
# balorg/plugins/system_info.sh
# System information collector plugin

data="$1"
echo "[system_info] Collecting system information..."

echo "=== System Information ==="
echo "OS: $(uname -s)"
echo "Kernel: $(uname -r)"
echo "Hostname: $(hostname)"
echo "User: $(whoami)"
echo "Uptime: $(uptime -p 2>/dev/null || uptime)"
echo "Load: $(uptime | awk -F'load average:' '{print $2}')"

if command -v free &> /dev/null; then
    echo "Memory: $(free -h | grep Mem | awk '{print "Used: "$3" / Total: "$2}')"
fi

echo "[system_info] Collection complete."
