#!/usr/bin/env bash
# balorg/examples/integration_example.sh
# Example of integrating Balorg with EcoShell

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BALORG_HOME="$(dirname "$SCRIPT_DIR")"
ECOSHELL_ROOT="$(dirname "$BALORG_HOME")"

echo "==================================="
echo "Balorg + EcoShell Integration Demo"
echo "==================================="
echo ""

# Initialize Balorg
echo "1. Initializing Balorg..."
"$BALORG_HOME/balorgctl" init
echo ""

# Create an integration injection
echo "2. Creating EcoShell integration injection..."
"$BALORG_HOME/balorgctl" injection create eco_integration '
echo "[Balorg-EcoShell] Integration active"
echo "[Balorg-EcoShell] Checking EcoShell components..."

if [[ -f "Boot.Sh" ]]; then
    echo "  ✓ Boot.Sh found"
fi

if [[ -f "Fallback_loop.sh" ]]; then
    echo "  ✓ Fallback_loop.sh found"
fi

if [[ -f "Overlay_injector.sh" ]]; then
    echo "  ✓ Overlay_injector.sh found"
fi

echo "[Balorg-EcoShell] Integration check complete"
'
echo ""

# Execute the integration
echo "3. Executing integration check..."
cd "$ECOSHELL_ROOT"
"$BALORG_HOME/balorgctl" injection execute eco_integration
echo ""

# Run EcoShell analyzer plugin
echo "4. Running EcoShell analyzer plugin..."
bash "$BALORG_HOME/plugins/echo_analyzer.sh" "test"
echo ""

# Create a combined injection
echo "5. Creating combined Balorg-EcoShell injection..."
"$BALORG_HOME/balorgctl" injection create balorg_echo_combo '
echo "[Combo] Running Balorg + EcoShell stack"
echo "[Combo] Setting environment..."
export OVERLAY_ID="BalorgEcho"
export BALORG_MODE="bash"
echo "[Combo] Environment configured:"
echo "  OVERLAY_ID: $OVERLAY_ID"
echo "  BALORG_MODE: $BALORG_MODE"
echo "[Combo] Stack ready for deployment"
'
echo ""

# Execute combo injection
echo "6. Executing combo injection..."
"$BALORG_HOME/balorgctl" injection execute balorg_echo_combo
echo ""

echo "==================================="
echo "Integration Demo Complete! ✓"
echo "==================================="
echo ""
echo "Balorg is now integrated with EcoShell!"
echo "You can:"
echo "  - Use Balorg plugins to analyze EcoShell"
echo "  - Create injections that interact with EcoShell components"
echo "  - Combine Balorg and EcoShell functionality"
echo ""
