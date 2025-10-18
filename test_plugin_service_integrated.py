"""Integration test for the plugin service with auto-started server."""
import pytest
import grpc
import subprocess
import time
import sys
import os

from balorg import plugin_service_pb2
from balorg import plugin_service_pb2_grpc


@pytest.fixture(scope="module")
def grpc_server():
    """Start the gRPC server for testing."""
    # Set PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, '-m', 'balorg.server'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(2)
    
    yield server_process
    
    # Cleanup
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()


def test_execute_plugin_with_auto_server(grpc_server):
    """Test plugin execution with auto-started server."""
    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')
    stub = plugin_service_pb2_grpc.PluginServiceStub(channel)

    # Create a plugin request
    request = plugin_service_pb2.PluginRequest(
        plugin_name='example_plugin',
        plugin_data='example_data'
    )

    try:
        # Execute the plugin
        response = stub.ExecutePlugin(request)
        assert response is not None
        assert response.result == 'expected_result'
    except grpc.RpcError as e:
        pytest.fail(f"gRPC error: {e}")
    finally:
        channel.close()


def test_execute_plugin_unknown(grpc_server):
    """Test plugin execution with unknown plugin."""
    channel = grpc.insecure_channel('localhost:50051')
    stub = plugin_service_pb2_grpc.PluginServiceStub(channel)

    request = plugin_service_pb2.PluginRequest(
        plugin_name='unknown_plugin',
        plugin_data='test_data'
    )

    try:
        response = stub.ExecutePlugin(request)
        assert response is not None
        assert 'Unknown plugin' in response.result
    except grpc.RpcError as e:
        pytest.fail(f"gRPC error: {e}")
    finally:
        channel.close()


def test_execute_plugin_different_data(grpc_server):
    """Test plugin execution with different data."""
    channel = grpc.insecure_channel('localhost:50051')
    stub = plugin_service_pb2_grpc.PluginServiceStub(channel)

    request = plugin_service_pb2.PluginRequest(
        plugin_name='example_plugin',
        plugin_data='different_data'
    )

    try:
        response = stub.ExecutePlugin(request)
        assert response is not None
        assert 'Processed:' in response.result
    except grpc.RpcError as e:
        pytest.fail(f"gRPC error: {e}")
    finally:
        channel.close()
