#!/usr/bin/env bash
# balorg/utils/env_helper.sh
# Environment and system information utilities

get_system_info() {
    echo "System Information:"
    echo "  OS: $(uname -s)"
    echo "  Kernel: $(uname -r)"
    echo "  Hostname: $(hostname)"
    echo "  User: $(whoami)"
}

get_balorg_home() {
    echo "${BALORG_HOME:-$HOME/balorg}"
}

set_balorg_env() {
    export BALORG_HOME="${BALORG_HOME:-$HOME/balorg}"
    export BALORG_MODE="${BALORG_MODE:-bash}"
    echo "[Balorg] Environment initialized"
    echo "  BALORG_HOME: $BALORG_HOME"
    echo "  BALORG_MODE: $BALORG_MODE"
}

check_dependencies() {
    local deps=("bash" "socat" "jq" "curl")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo "[Warning] Missing dependencies: ${missing[*]}"
        return 1
    fi
    
    echo "[✓] All dependencies available"
    return 0
}

# Export functions
export -f get_system_info
export -f get_balorg_home
export -f set_balorg_env
export -f check_dependencies
