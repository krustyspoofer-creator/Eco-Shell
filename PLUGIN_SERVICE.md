# Balorg Plugin Service

A gRPC-based plugin service implementation for the Eco-Shell project.

## Overview

The Balorg plugin service provides a gRPC interface for executing plugins. It uses Protocol Buffers for efficient message serialization and gRPC for high-performance RPC communication.

## Components

- **`balorg/plugin_service.proto`**: Protocol Buffer definition for the plugin service
- **`balorg/plugin_service_pb2.py`**: Generated Python protobuf code
- **`balorg/plugin_service_pb2_grpc.py`**: Generated Python gRPC code
- **`balorg/server.py`**: gRPC server implementation
- **`test_plugin_service.py`**: Test cases for the plugin service

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

Start the gRPC server on port 50051:

```bash
./start_server.sh
```

Or manually:

```bash
export PYTHONPATH=$(pwd)
python -m balorg.server
```

## Running Tests

Run the test suite:

```bash
./run_tests.sh
```

Or manually:

```bash
export PYTHONPATH=$(pwd)
pytest test_plugin_service.py -v
```

## Usage

The plugin service accepts a `PluginRequest` with the following fields:
- `plugin_name`: Name of the plugin to execute
- `plugin_data`: Data to pass to the plugin

Example:
```python
import grpc
from balorg import plugin_service_pb2
from balorg import plugin_service_pb2_grpc

# Create a gRPC channel
channel = grpc.insecure_channel('localhost:50051')
stub = plugin_service_pb2_grpc.PluginServiceStub(channel)

# Create a plugin request
request = plugin_service_pb2.PluginRequest(
    plugin_name='example_plugin',
    plugin_data='example_data'
)

# Execute the plugin
response = stub.ExecutePlugin(request)
print(f"Result: {response.result}")
```

## Regenerating gRPC Code

If you modify the `.proto` file, regenerate the Python code:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. balorg/plugin_service.proto
```

## Architecture

The service uses a simple request-response pattern:
1. Client sends a `PluginRequest` to the server
2. Server processes the request and executes the specified plugin
3. Server returns a `PluginResponse` with the result

The current implementation includes an example plugin that returns `'expected_result'` when given:
- `plugin_name='example_plugin'`
- `plugin_data='example_data'`
