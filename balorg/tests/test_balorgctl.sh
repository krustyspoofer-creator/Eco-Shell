#!/usr/bin/env bash
# balorg/tests/test_balorgctl.sh
# Test suite for balorgctl and Balorg framework

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BALORG_HOME="$(dirname "$SCRIPT_DIR")"
export BALORG_HOME

echo "==================================="
echo "Balorg Framework Test Suite"
echo "==================================="
echo ""

# Test 1: Check balorgctl exists and is executable
echo "Test 1: Check balorgctl..."
if [[ -x "$BALORG_HOME/balorgctl" ]]; then
    echo "  ✓ balorgctl is executable"
else
    echo "  ✗ balorgctl not found or not executable"
    exit 1
fi

# Test 2: Test init command
echo ""
echo "Test 2: Test initialization..."
"$BALORG_HOME/balorgctl" init > /tmp/balorg_test_init.log 2>&1
if [[ $? -eq 0 ]]; then
    echo "  ✓ Initialization successful"
else
    echo "  ✗ Initialization failed"
    cat /tmp/balorg_test_init.log
    exit 1
fi

# Test 3: Check directory structure
echo ""
echo "Test 3: Check directory structure..."
dirs=("core" "plugins" "injections" "api" "utils" "logs" "tests")
all_exist=true
for dir in "${dirs[@]}"; do
    if [[ -d "$BALORG_HOME/$dir" ]]; then
        echo "  ✓ $dir/ exists"
    else
        echo "  ✗ $dir/ missing"
        all_exist=false
    fi
done

if ! $all_exist; then
    exit 1
fi

# Test 4: Test plugin list
echo ""
echo "Test 4: Test plugin listing..."
plugin_list=$("$BALORG_HOME/balorgctl" plugin list)
if [[ $? -eq 0 ]]; then
    echo "  ✓ Plugin list command works"
    echo "  Available plugins:"
    echo "$plugin_list" | sed 's/^/    /'
else
    echo "  ✗ Plugin list failed"
    exit 1
fi

# Test 5: Test injection creation
echo ""
echo "Test 5: Test injection creation..."
"$BALORG_HOME/balorgctl" injection create test_injection 'echo "Test injection executed"' > /tmp/balorg_test_injection.log 2>&1
if [[ $? -eq 0 ]]; then
    echo "  ✓ Injection creation successful"
else
    echo "  ✗ Injection creation failed"
    cat /tmp/balorg_test_injection.log
    exit 1
fi

# Test 6: Test injection execution
echo ""
echo "Test 6: Test injection execution..."
result=$("$BALORG_HOME/balorgctl" injection execute test_injection 2>&1)
if [[ $result == *"Test injection executed"* ]]; then
    echo "  ✓ Injection execution successful"
else
    echo "  ✗ Injection execution failed"
    echo "  Result: $result"
    exit 1
fi

# Test 7: Test injection removal
echo ""
echo "Test 7: Test injection removal..."
"$BALORG_HOME/balorgctl" injection remove test_injection > /tmp/balorg_test_remove.log 2>&1
if [[ $? -eq 0 ]]; then
    echo "  ✓ Injection removal successful"
else
    echo "  ✗ Injection removal failed"
    cat /tmp/balorg_test_remove.log
    exit 1
fi

# Test 8: Test utilities
echo ""
echo "Test 8: Test utility functions..."
source "$BALORG_HOME/utils/env_helper.sh"
if get_system_info > /dev/null 2>&1; then
    echo "  ✓ Environment utilities work"
else
    echo "  ✗ Environment utilities failed"
    exit 1
fi

# Test 9: Test JSON utilities (if jq is available)
echo ""
echo "Test 9: Test JSON utilities..."
if command -v jq &> /dev/null; then
    source "$BALORG_HOME/utils/json_helper.sh"
    test_json='{"name":"Balorg","version":"1.0"}'
    if json_validate "$test_json"; then
        name=$(json_get "$test_json" ".name")
        if [[ "$name" == "Balorg" ]]; then
            echo "  ✓ JSON utilities work"
        else
            echo "  ✗ JSON parsing incorrect"
            exit 1
        fi
    else
        echo "  ✗ JSON validation failed"
        exit 1
    fi
else
    echo "  ⊘ jq not installed, skipping JSON tests"
fi

# Cleanup
echo ""
echo "Cleaning up test files..."
rm -f /tmp/balorg_test_*.log

echo ""
echo "==================================="
echo "All tests passed! ✓"
echo "==================================="
