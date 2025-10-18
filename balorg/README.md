# gRPC Plugin Service

This directory contains the implementation of a gRPC-based plugin service for Eco-Shell.

## Structure

- `plugin_service_pb2.py` - Generated protobuf message definitions
- `plugin_service_pb2_grpc.py` - Generated gRPC service definitions
- `server.py` - Implementation of the gRPC plugin service server

## Running the Server

To start the plugin service server:

```bash
python -m balorg.server
```

The server will listen on port 50051 by default.

## Testing

Run the tests with:

```bash
pytest tests/test_plugin_service.py
```

Make sure the server is running before executing the tests.

## Usage Example

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
