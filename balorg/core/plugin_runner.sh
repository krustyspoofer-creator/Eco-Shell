#!/usr/bin/env bash
# balorg/core/plugin_runner.sh
# Balorg AI Plugin Executor (Bash version)

PLUGIN_DIR="${BALORG_HOME:-$(dirname "$(dirname "$(readlink -f "$0")"))")}/plugins"
LOG_DIR="${BALORG_HOME:-$(dirname "$(dirname "$(readlink -f "$0")"))")}/logs"
mkdir -p "$LOG_DIR"

process_plugin_request() {
    local plugin_name="$1"
    local plugin_data="$2"

    local plugin_path="${PLUGIN_DIR}/${plugin_name}.sh"
    if [[ ! -f "$plugin_path" ]]; then
        echo "Error: Plugin '$plugin_name' not found" >&2
        exit 1
    fi

    echo "[Balorg] Executing plugin: $plugin_name"
    bash "$plugin_path" "$plugin_data" 2>&1 | tee -a "$LOG_DIR/${plugin_name}.log"
}

serve_plugins() {
    echo "[Balorg] Plugin service running (Bash mode)"
    echo "[Balorg] Listening on TCP port 50051"
    while read -r line; do
        plugin_name=$(echo "$line" | cut -d' ' -f1)
        plugin_data=$(echo "$line" | cut -d' ' -f2-)
        process_plugin_request "$plugin_name" "$plugin_data"
    done < <(socat - TCP-LISTEN:50051,reuseaddr,fork)
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    serve_plugins
fi
