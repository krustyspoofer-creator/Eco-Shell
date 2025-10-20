#!/usr/bin/env python3
"""
Balorg Resources Monitoring System
System resource monitoring with persona overlay
"""

import psutil
import time
import os
import sys

# 🛡️ Persona Overlay
BALORG_SIGIL = "[BALORG-MONITOR]"
KYEEL_ACCESS = os.getenv("KYEEL_ACCESS", "false")

def sovereign_check():
    """Check for authorized access"""
    if KYEEL_ACCESS.lower() != "true":
        print(f"{BALORG_SIGIL} Unauthorized access. Persona enforcement active.")
        sys.exit(1)

def resource_snapshot():
    """Get system resource snapshot"""
    cpu = psutil.cpu_percent(percpu=True)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    uptime = time.time() - psutil.boot_time()

    print(f"\n{BALORG_SIGIL} SYSTEM STATUS")
    print(f"🧠 CPU Cores: {cpu}")
    print(f"🧠 Memory: {mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB ({mem.percent}%)")
    print(f"🧠 Swap: {swap.used / (1024**3):.2f} GB / {swap.total / (1024**3):.2f} GB ({swap.percent}%)")
    print(f"🧠 Uptime: {uptime // 3600:.0f}h {(uptime % 3600) // 60:.0f}m")

def process_scan():
    """Scan active processes"""
    print(f"\n{BALORG_SIGIL} ACTIVE PROCESSES")
    print(f"{'PID':<8} {'Name':<30} {'CPU%':<8} {'MEM%':<8}")
    print("-" * 60)
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            if info['cpu_percent'] > 0 or info['memory_percent'] > 1.0:
                print(f"{info['pid']:<8} {info['name'][:28]:<30} {info['cpu_percent']:<8.1f} {info['memory_percent']:<8.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def manifest():
    """Main monitoring function"""
    sovereign_check()
    resource_snapshot()
    process_scan()
    print(f"\n{BALORG_SIGIL} Manifest complete. Sovereign logic enforced.\n")

if __name__ == "__main__":
    print(f"{BALORG_SIGIL} Starting monitoring system...")
    manifest()
