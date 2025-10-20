#!/usr/bin/env python3
"""
Balorg Mining System
Resource extraction and data mining
"""

import os
import platform
import socket
from datetime import datetime

BALORG_SIGIL = "[BALORG-MINE]"

class BalorgMiner:
    def __init__(self, log_dir="../logs", data_dir="../data"):
        self.log_dir = log_dir
        self.data_dir = data_dir
        os.makedirs(log_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(f"{self.log_dir}/mining.log", "a") as f:
            f.write(log_msg + "\n")
            
    def mine_system_info(self):
        """Extract system information"""
        self.log(f"{BALORG_SIGIL} Mining system information...")
        
        info = {
            "system": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": socket.gethostname(),
        }
        
        info_file = f"{self.data_dir}/system_info.txt"
        with open(info_file, "w") as f:
            for key, value in info.items():
                f.write(f"{key}: {value}\n")
                
        self.log(f"{BALORG_SIGIL} System info saved to {info_file}")
        return info
        
    def run(self):
        """Run mining operation"""
        self.log(f"{BALORG_SIGIL} Initializing mining operations...")
        self.mine_system_info()
        self.log(f"{BALORG_SIGIL} Mining operation complete.")

if __name__ == "__main__":
    miner = BalorgMiner()
    miner.run()
