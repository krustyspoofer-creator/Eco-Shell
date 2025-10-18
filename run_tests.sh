#!/bin/bash
# Run the plugin service tests

cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)"

echo "Running plugin service tests..."
pytest test_plugin_service.py -v
