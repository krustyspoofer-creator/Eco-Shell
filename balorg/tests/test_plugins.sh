#!/usr/bin/env bash
# balorg/tests/test_plugins.sh
# Test suite for individual plugins

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BALORG_HOME="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$BALORG_HOME/plugins"

echo "==================================="
echo "Plugin Test Suite"
echo "==================================="
echo ""

# Test each plugin directly
plugins=("example_plugin" "system_info" "echo_analyzer" "log_aggregator")

for plugin in "${plugins[@]}"; do
    plugin_path="$PLUGIN_DIR/${plugin}.sh"
    
    echo "Testing plugin: $plugin"
    
    if [[ ! -f "$plugin_path" ]]; then
        echo "  ✗ Plugin file not found: $plugin_path"
        continue
    fi
    
    if [[ ! -x "$plugin_path" ]]; then
        echo "  ✗ Plugin not executable: $plugin_path"
        continue
    fi
    
    # Run plugin with test data
    output=$(bash "$plugin_path" "test_data" 2>&1)
    exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        echo "  ✓ Plugin executed successfully"
        echo "  Output preview:"
        echo "$output" | head -5 | sed 's/^/    /'
    else
        echo "  ✗ Plugin execution failed (exit code: $exit_code)"
        echo "  Output:"
        echo "$output" | sed 's/^/    /'
    fi
    
    echo ""
done

echo "==================================="
echo "Plugin tests complete"
echo "==================================="
