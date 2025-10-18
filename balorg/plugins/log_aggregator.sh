#!/usr/bin/env bash
# balorg/plugins/log_aggregator.sh
# Log aggregation and analysis plugin

data="$1"
log_dir="${BALORG_HOME:-$(dirname "$(dirname "$(readlink -f "$0")"))")}/logs"

echo "[log_aggregator] Aggregating logs from: $log_dir"

if [[ ! -d "$log_dir" ]]; then
    echo "[log_aggregator] Log directory not found"
    exit 1
fi

echo "=== Log Summary ==="
log_count=$(ls -1 "$log_dir"/*.log 2>/dev/null | wc -l)
echo "Total logs: $log_count"

if [[ $log_count -gt 0 ]]; then
    echo ""
    echo "Recent activity:"
    for log in "$log_dir"/*.log; do
        if [[ -f "$log" ]]; then
            log_name=$(basename "$log")
            line_count=$(wc -l < "$log")
            last_modified=$(stat -c %y "$log" 2>/dev/null || stat -f %Sm "$log" 2>/dev/null || echo "unknown")
            echo "  - $log_name: $line_count lines (modified: $last_modified)"
        fi
    done
fi

echo "[log_aggregator] Aggregation complete."
