#!/usr/bin/env bash
# balorg/core/injection_manager.sh
# Balorg AI Injection Framework (Bash version)

INJECTION_DIR="${BALORG_HOME:-$(dirname "$(dirname "$(readlink -f "$0")"))")}/injections"
LOG_DIR="${BALORG_HOME:-$(dirname "$(dirname "$(readlink -f "$0")"))")}/logs"
mkdir -p "$INJECTION_DIR" "$LOG_DIR"

create_injection() {
    local injection_name="$1"
    local injection_code="$2"
    local injection_path="${INJECTION_DIR}/${injection_name}.sh"
    
    echo "[Balorg] Creating injection: $injection_name"
    echo "#!/usr/bin/env bash" > "$injection_path"
    echo "# Injection: $injection_name" >> "$injection_path"
    echo "# Created: $(date)" >> "$injection_path"
    echo "" >> "$injection_path"
    echo "$injection_code" >> "$injection_path"
    chmod +x "$injection_path"
    
    echo "[Balorg] Injection created at: $injection_path"
}

execute_injection() {
    local injection_name="$1"
    local injection_path="${INJECTION_DIR}/${injection_name}.sh"
    
    if [[ ! -f "$injection_path" ]]; then
        echo "Error: Injection '$injection_name' not found" >&2
        return 1
    fi
    
    echo "[Balorg] Executing injection: $injection_name"
    bash "$injection_path" 2>&1 | tee -a "$LOG_DIR/injection_${injection_name}.log"
}

list_injections() {
    echo "[Balorg] Available injections:"
    ls -1 "$INJECTION_DIR"/*.sh 2>/dev/null | xargs -n 1 basename | sed 's/\.sh$//' || echo "  (none)"
}

remove_injection() {
    local injection_name="$1"
    local injection_path="${INJECTION_DIR}/${injection_name}.sh"
    
    if [[ -f "$injection_path" ]]; then
        rm "$injection_path"
        echo "[Balorg] Injection '$injection_name' removed"
    else
        echo "Error: Injection '$injection_name' not found" >&2
        return 1
    fi
}

# CLI interface
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    case "$1" in
        create)
            create_injection "$2" "$3"
            ;;
        execute)
            execute_injection "$2"
            ;;
        list)
            list_injections
            ;;
        remove)
            remove_injection "$2"
            ;;
        *)
            echo "Usage: $0 {create|execute|list|remove} [args...]"
            echo ""
            echo "Commands:"
            echo "  create <name> <code>  - Create new injection"
            echo "  execute <name>        - Execute injection"
            echo "  list                  - List all injections"
            echo "  remove <name>         - Remove injection"
            exit 1
            ;;
    esac
fi
