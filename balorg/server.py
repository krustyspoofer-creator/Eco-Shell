"""
gRPC Plugin Service Server Implementation
"""
import grpc
from concurrent import futures
from balorg import plugin_service_pb2
from balorg import plugin_service_pb2_grpc


class PluginServiceServicer(plugin_service_pb2_grpc.PluginServiceServicer):
    """Implementation of the PluginService."""
    
    def ExecutePlugin(self, request, context):
        """Execute a plugin based on the request.
        
        Args:
            request: PluginRequest containing plugin_name and plugin_data
            context: gRPC context
            
        Returns:
            PluginResponse containing the result
        """
        plugin_name = request.plugin_name
        plugin_data = request.plugin_data
        
        # Example plugin logic - can be extended
        if plugin_name == 'example_plugin' and plugin_data == 'example_data':
            result = 'expected_result'
        else:
            result = f'Executed plugin: {plugin_name} with data: {plugin_data}'
        
        return plugin_service_pb2.PluginResponse(result=result)


def serve(port=50051):
    """Start the gRPC server.
    
    Args:
        port: Port number to listen on (default: 50051)
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    plugin_service_pb2_grpc.add_PluginServiceServicer_to_server(
        PluginServiceServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'Plugin Service server started on port {port}')
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print('Server stopped')


if __name__ == '__main__':
    serve()
