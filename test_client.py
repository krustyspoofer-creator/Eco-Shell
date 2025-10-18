"""
Test client for the PluginService
"""
import grpc
import plugin_pb2
import plugin_pb2_grpc


def run_test_client():
    """
    Connect to the PluginService and send test requests.
    """
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = plugin_pb2_grpc.PluginServiceStub(channel)
        
        # Test 1: Basic plugin execution
        print("\nTest 1: Basic plugin execution")
        request = plugin_pb2.PluginRequest(
            plugin_name="test_plugin",
            plugin_data="sample data",
            parameters={"key1": "value1", "key2": "value2"}
        )
        response = stub.ExecutePlugin(request)
        print(f"Success: {response.success}")
        print(f"Result: {response.result}")
        print(f"Error: {response.error_message}")
        
        # Test 2: Plugin with no parameters
        print("\nTest 2: Plugin with no parameters")
        request = plugin_pb2.PluginRequest(
            plugin_name="simple_plugin"
        )
        response = stub.ExecutePlugin(request)
        print(f"Success: {response.success}")
        print(f"Result: {response.result}")
        
        # Test 3: Empty plugin name (should handle gracefully)
        print("\nTest 3: Empty plugin name")
        request = plugin_pb2.PluginRequest(
            plugin_name=""
        )
        response = stub.ExecutePlugin(request)
        print(f"Success: {response.success}")
        print(f"Result: {response.result}")


if __name__ == '__main__':
    print("Connecting to PluginService on localhost:50051...")
    try:
        run_test_client()
        print("\nAll tests completed successfully!")
    except grpc.RpcError as e:
        print(f"\nError: Could not connect to server. Make sure the server is running.")
        print(f"Details: {e}")
