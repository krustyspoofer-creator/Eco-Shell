# Plugin Service

A gRPC-based plugin service for Eco-Shell that enables remote plugin execution.

## Overview

The PluginService provides a gRPC server that accepts plugin execution requests and returns results. It's designed to be extensible and can process various types of plugins with custom parameters.

## Architecture

### Components

1. **plugin.proto** - Protocol Buffer definition for the service
2. **plugin_service.py** - Main server implementation
3. **test_client.py** - Example client for testing
4. **test_plugin_service.py** - Unit tests

### Service Definition

The service exposes one RPC method:
- `ExecutePlugin(PluginRequest) returns (PluginResponse)`

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Generate the gRPC stubs (if needed):

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. plugin.proto
```

## Usage

### Starting the Server

Run the plugin service server:

```bash
python plugin_service.py
```

The server will start on port 50051 and wait for incoming requests.

### Using the Test Client

In a separate terminal, run the test client:

```bash
python test_client.py
```

This will send several test requests to the server and display the results.

### Running Tests

Run the unit tests:

```bash
python -m unittest test_plugin_service.py -v
```

## API Reference

### PluginRequest

- `plugin_name` (string): Name of the plugin to execute
- `plugin_data` (string): Data to pass to the plugin
- `parameters` (map<string, string>): Key-value parameters for the plugin

### PluginResponse

- `result` (string): Result of the plugin execution
- `success` (bool): Whether the execution was successful
- `error_message` (string): Error message if execution failed

## Example

```python
import grpc
import plugin_pb2
import plugin_pb2_grpc

# Create a channel and stub
channel = grpc.insecure_channel('localhost:50051')
stub = plugin_pb2_grpc.PluginServiceStub(channel)

# Create a request
request = plugin_pb2.PluginRequest(
    plugin_name="my_plugin",
    plugin_data="sample data",
    parameters={"key": "value"}
)

# Execute the plugin
response = stub.ExecutePlugin(request)
print(f"Success: {response.success}")
print(f"Result: {response.result}")
```

## Extension

To add custom plugin processing logic, modify the `process_plugin_request()` function in `plugin_service.py`. This function receives the plugin request and should return a string result.

## Configuration

- **Port**: Default is 50051, can be changed in the `serve()` function
- **Max Workers**: Default thread pool size is 10, adjustable in `serve()`
- **Logging**: Configured in the `__main__` block

## Security Note

This implementation uses an insecure channel for simplicity. For production use, implement proper TLS/SSL encryption and authentication.
