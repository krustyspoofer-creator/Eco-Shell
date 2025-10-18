#!/usr/bin/env bash
# balorg/QUICKSTART.sh
# Quick start script for Balorg AI Framework

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         BALORG AI - Quick Start Guide                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Initialize
echo "Step 1: Initializing Balorg..."
./balorgctl init
echo ""

# Step 2: Check status
echo "Step 2: Checking system status..."
./balorgctl status
echo ""

# Step 3: List plugins
echo "Step 3: Available plugins:"
./balorgctl plugin list
echo ""

# Step 4: Run example plugin
echo "Step 4: Running example plugin..."
bash plugins/example_plugin.sh "Quick Start Test"
echo ""

# Step 5: Create test injection
echo "Step 5: Creating test injection..."
./balorgctl injection create quickstart_test 'echo "Balorg AI is operational!"'
echo ""

# Step 6: Execute injection
echo "Step 6: Executing injection..."
./balorgctl injection execute quickstart_test
echo ""

# Step 7: Clean up
echo "Step 7: Cleaning up..."
./balorgctl injection remove quickstart_test
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         Quick Start Complete! ✓                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  - Explore plugins: ./balorgctl plugin list"
echo "  - Create injections: ./balorgctl injection create <name> '<code>'"
echo "  - Start service: ./balorgctl serve"
echo "  - Read documentation: cat README.md"
echo ""
