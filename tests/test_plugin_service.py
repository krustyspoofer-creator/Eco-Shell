import pytest
import grpc
from balorg import plugin_service_pb2
from balorg import plugin_service_pb2_grpc

def test_execute_plugin():
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

    # Verify the response
    assert response.result == 'expected_result'
