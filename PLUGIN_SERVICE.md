# gRPC Plugin Service Documentation

## Overview

This implementation provides a gRPC-based plugin service for the Eco-Shell project. The service allows executing plugins via a simple RPC interface defined using Protocol Buffers.

## Architecture

The implementation consists of several components:

### 1. Protocol Buffer Definition (`protos/plugin_service.proto`)
Defines the service interface and message types:
- `PluginService` - The gRPC service with `ExecutePlugin` method
- `PluginRequest` - Contains `plugin_name` and `plugin_data` fields
- `PluginResponse` - Contains the execution `result`

### 2. Generated Code (`balorg/`)
- `plugin_service_pb2.py` - Generated message classes
- `plugin_service_pb2_grpc.py` - Generated service stubs and server code

### 3. Server Implementation (`balorg/server.py`)
- `PluginServiceServicer` - Implements the service logic
- `serve()` - Starts the gRPC server on port 50051

### 4. Tests (`tests/test_plugin_service.py`)
- Validates the plugin service functionality
- Ensures the server responds correctly to requests

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

You can start the server in multiple ways:

**Option 1: Using the provided script**
```bash
./run_server.sh
```

**Option 2: Using Python module**
```bash
python -m balorg.server
```

**Option 3: Programmatically**
```python
from balorg.server import serve
serve(port=50051)
```

### Running Tests

Make sure the server is running, then execute:

```bash
pytest tests/test_plugin_service.py
```

### Client Usage

```python
import grpc
from balorg import plugin_service_pb2
from balorg import plugin_service_pb2_grpc

# Connect to the server
channel = grpc.insecure_channel('localhost:50051')
stub = plugin_service_pb2_grpc.PluginServiceStub(channel)

# Make a request
request = plugin_service_pb2.PluginRequest(
    plugin_name='example_plugin',
    plugin_data='example_data'
)
response = stub.ExecutePlugin(request)

print(f"Result: {response.result}")
```

## Extending the Service

To add more plugin functionality:

1. Update the `ExecutePlugin` method in `balorg/server.py`
2. Add your plugin logic based on the `plugin_name`
3. Return the appropriate result in the `PluginResponse`

Example:
```python
def ExecutePlugin(self, request, context):
    plugin_name = request.plugin_name
    plugin_data = request.plugin_data
    
    if plugin_name == 'my_plugin':
        # Your plugin logic here
        result = process_data(plugin_data)
    else:
        result = f'Unknown plugin: {plugin_name}'
    
    return plugin_service_pb2.PluginResponse(result=result)
```

## Security Considerations

- The current implementation uses insecure channels for simplicity
- For production use, consider:
  - Adding TLS/SSL encryption
  - Implementing authentication and authorization
  - Input validation and sanitization
  - Rate limiting

## Troubleshooting

**Server won't start:**
- Check if port 50051 is already in use: `lsof -i :50051`
- Try a different port: modify the `serve()` call

**Tests failing:**
- Ensure the server is running before executing tests
- Verify network connectivity to localhost:50051
- Check server logs for error messages

## Dependencies

- `grpcio==1.59.0` - gRPC runtime
- `grpcio-tools==1.59.0` - Protocol buffer compiler
- `protobuf==4.25.0` - Protocol buffers
- `pytest==7.4.3` - Testing framework
