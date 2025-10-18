"""Integration test for the plugin service with auto-started server."""
import pytest
import grpc
import subprocess
import time
import sys
import os
from pathlib import Path

from balorg import plugin_service_pb2
from balorg import plugin_service_pb2_grpc


@pytest.fixture(scope="module")
def grpc_server():
    """Start the gRPC server for testing."""
    # Set PYTHONPATH to project root (parent directory of this file)
    env = os.environ.copy()
    project_root = Path(__file__).parent.resolve()
    env['PYTHONPATH'] = str(project_root)
    
    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, '-m', 'balorg.server'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start with retry mechanism
    max_retries = 10
    retry_delay = 0.5
    channel = None
    
    for attempt in range(max_retries):
        try:
            channel = grpc.insecure_channel('localhost:50051')
            # Try to connect to verify server is ready
            stub = plugin_service_pb2_grpc.PluginServiceStub(channel)
            request = plugin_service_pb2.PluginRequest(
                plugin_name='health_check',
                plugin_data=''
            )
            stub.ExecutePlugin(request, timeout=1)
            channel.close()
            break
        except grpc.RpcError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                if channel:
                    channel.close()
                server_process.terminate()
                raise RuntimeError("Server failed to start within expected time")
    
    yield server_process
    
    # Cleanup
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()


@pytest.fixture
def grpc_channel(grpc_server):
    """Create a gRPC channel for testing."""
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()


def test_execute_plugin_with_auto_server(grpc_channel):
    """Test plugin execution with auto-started server."""
    stub = plugin_service_pb2_grpc.PluginServiceStub(grpc_channel)

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


def test_execute_plugin_unknown(grpc_channel):
    """Test plugin execution with unknown plugin."""
    stub = plugin_service_pb2_grpc.PluginServiceStub(grpc_channel)

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


def test_execute_plugin_different_data(grpc_channel):
    """Test plugin execution with different data."""
    stub = plugin_service_pb2_grpc.PluginServiceStub(grpc_channel)

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
