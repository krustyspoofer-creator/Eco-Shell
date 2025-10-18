#!/bin/bash
# Echo Knowledge Graph - Quick Start Guide
#
# This script helps you get started with the Echo Knowledge Graph system

echo "================================================================================"
echo "                      Echo Knowledge Graph - Quick Start"
echo "================================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "knowledge_graph_schema.yaml" ]; then
    echo "Error: Please run this script from the echo_knowledge directory"
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

# Install dependencies
echo "Step 1: Installing dependencies..."
pip3 install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Display menu
echo "What would you like to do?"
echo ""
echo "1. View Knowledge Graph Statistics"
echo "2. Run Collaboration Query (find AI labs for Balorg)"
echo "3. Discover Workflow Automation Stacks"
echo "4. Analyze Research Trends"
echo "5. Run Complete Demo (all phases)"
echo "6. Test Reasoning Engine"
echo "7. Test Data Ingestion Pipeline"
echo "8. Exit"
echo ""
read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo ""
        echo "Running: Knowledge Graph Statistics"
        echo "-----------------------------------"
        python3 echo_kg_cli.py stats
        ;;
    2)
        echo ""
        echo "Running: Collaboration Opportunities Query"
        echo "------------------------------------------"
        python3 echo_kg_cli.py query collaboration \
            --domains "Workflow Automation,AI Privacy & Safety" \
            --focus "workflow_automation"
        ;;
    3)
        echo ""
        echo "Running: Workflow Automation Stacks Discovery"
        echo "---------------------------------------------"
        python3 echo_kg_cli.py query workflow_stacks
        ;;
    4)
        echo ""
        echo "Running: Research Trends Analysis"
        echo "--------------------------------"
        python3 echo_kg_cli.py query research_trends --since-year 2023
        ;;
    5)
        echo ""
        echo "Running: Complete Demonstration"
        echo "------------------------------"
        echo "Note: This demo is interactive. Press Enter to advance through phases."
        echo ""
        python3 demo_use_case.py
        ;;
    6)
        echo ""
        echo "Running: Reasoning Engine Test"
        echo "-----------------------------"
        python3 reasoning_engine.py
        ;;
    7)
        echo ""
        echo "Running: Data Ingestion Pipeline Test"
        echo "------------------------------------"
        python3 data_ingestion.py
        ;;
    8)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "================================================================================"
echo "For more information, see README.md"
echo "================================================================================"
