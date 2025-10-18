"""gRPC Plugin Service Server Implementation."""
import grpc
from concurrent import futures
import time

from . import plugin_service_pb2
from . import plugin_service_pb2_grpc


class PluginServiceServicer(plugin_service_pb2_grpc.PluginServiceServicer):
    """Implementation of the PluginService."""

    def ExecutePlugin(self, request, context):
        """Execute a plugin based on the request.
        
        Args:
            request: PluginRequest containing plugin_name and plugin_data
            context: gRPC context
            
        Returns:
            PluginResponse with the result
        """
        # Example plugin logic
        if request.plugin_name == 'example_plugin':
            if request.plugin_data == 'example_data':
                return plugin_service_pb2.PluginResponse(result='expected_result')
            else:
                return plugin_service_pb2.PluginResponse(result=f'Processed: {request.plugin_data}')
        else:
            return plugin_service_pb2.PluginResponse(result=f'Unknown plugin: {request.plugin_name}')


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
    print(f"Server started on port {port}")
    return server


if __name__ == '__main__':
    server = serve()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
