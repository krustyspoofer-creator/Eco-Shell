#!/usr/bin/env bash

# --- Balorg Proxy Module Configuration & Utilities ---

# Use HOME/balorg as fallback if BALORG_HOME is not set
BALORG_BASE="${BALORG_HOME:-$HOME/balorg}"
BALORG_REGISTRY_DIR="$BALORG_BASE/registry"
BALORG_LOGS_DIR="$BALORG_BASE/logs"
PROXY_FILE="$BALORG_REGISTRY_DIR/proxies.txt"
LOG_FILE="$BALORG_LOGS_DIR/proxy.log"

# Ensures directories exist and logs the output
balorg_log() {
    mkdir -p "$BALORG_LOGS_DIR"
    echo "[Balorg] [$(date +%Y-%m-%d\ %H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

# Checks if a given proxy is live by testing connectivity to ipinfo.io
# Returns 0 (success) if a connection is established within 5 seconds, 1 otherwise.
validate_proxy() {
    local proxy_url="$1"
    # Suppress output, connect timeout 5s, check status code
    curl -x "$proxy_url" -s --connect-timeout 5 https://ipinfo.io/ip >/dev/null 2>&1
}

# --- Core Balorg Proxy Functions ---

# Function: Update Proxy List from a remote source
update_proxies() {
    balorg_log "Starting proxy list update from ProxyScrape API..."
    
    mkdir -p "$BALORG_REGISTRY_DIR"
    
    # Download fresh list, overwriting the old file
    curl -s "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all" > "$PROXY_FILE"
    local count
    count=$(wc -l < "$PROXY_FILE" 2>/dev/null || echo 0)
    
    if [[ "$count" -gt 0 ]]; then
        balorg_log "SUCCESS: Updated proxies list with $count entries."
        return 0
    else
        balorg_log "FAILURE: Proxy list updated, but found 0 entries. Check source URL."
        return 1
    fi
}

# Function: Rotate to a new, validated proxy
proxy_rotate() {
    balorg_log "Starting proxy rotation (max 5 attempts)..."

    if [[ ! -f "$PROXY_FILE" ]]; then
        balorg_log "FATAL: No proxies.txt found in $BALORG_REGISTRY_DIR. Run update_proxies first."
        return 1
    fi

    local proxy
    local attempt=0
    local max_attempts=5

    while [[ "$attempt" -lt "$max_attempts" ]]; do
        attempt=$((attempt + 1))
        
        # Randomly select a proxy
        proxy=$(shuf -n1 "$PROXY_FILE")
        
        balorg_log "Attempt $attempt: Testing $proxy..."

        if validate_proxy "$proxy"; then
            # Apply the working proxy to the environment
            export http_proxy="$proxy"
            export https_proxy="$proxy"
            balorg_log "SUCCESS: Rotated to LIVE proxy: $proxy"
            return 0
        else
            balorg_log "WARN: Proxy $proxy failed validation. Trying next..."
        fi
    done

    # If the loop finishes without finding a live proxy
    balorg_log "FAILURE: No live proxies found after $max_attempts attempts."
    return 1
}

# Function: Display the current proxy status
proxy_status() {
    local current_proxy="${http_proxy:-[NONE SET]}"
    echo "--- Balorg Proxy Status ---"
    echo "Current http_proxy:  $current_proxy"
    echo "Current https_proxy: $https_proxy"
    echo "Proxy list file:     $PROXY_FILE"
    echo "Log file:            $LOG_FILE"
}

# Function: Test the currently exported proxy (if one is set)
proxy_test() {
    if [[ -z "$http_proxy" ]]; then
        echo "[Balorg] Current proxy is NOT set. Direct connection test:"
        curl -s https://ipinfo.io/ip
        return 0
    fi
    
    echo "[Balorg] Testing CURRENTLY EXPORTED proxy: $http_proxy"
    
    if validate_proxy "$http_proxy"; then
        echo "SUCCESS: The current proxy is LIVE."
    else
        echo "FAILURE: The current proxy is DEAD or too slow."
    fi
}

# --- Command Line Integration Example (for balorgctl) ---
# To use these functions, you would typically source this file 
# or integrate the case statement into your main balorgctl script.

# if [[ "$1" == "proxy" ]]; then
#   case "$2" in
#     update) update_proxies ;;
#     rotate) proxy_rotate ;;
#     status) proxy_status ;;
#     test)   proxy_test ;;
#     *) echo "Usage: balorgctl proxy {update|rotate|status|test}" ;;
#   esac
# fi
