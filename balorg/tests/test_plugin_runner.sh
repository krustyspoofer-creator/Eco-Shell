#!/usr/bin/env bash
# balorg/tests/test_plugin_runner.sh
# Test script for Balorg plugin runner

echo "example_plugin test_payload" | socat - TCP:localhost:50051
