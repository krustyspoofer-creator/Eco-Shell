#!/bin/bash
# Script to run the gRPC plugin service server

cd "$(dirname "$0")"
python -m balorg.server
