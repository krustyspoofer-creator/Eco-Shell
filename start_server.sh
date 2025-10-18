#!/bin/bash
# Start the gRPC plugin service server

cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)"

echo "Starting gRPC Plugin Service on port 50051..."
python -m balorg.server
