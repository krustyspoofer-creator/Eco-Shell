from concurrent import futures
import logging
import grpc

import plugin_pb2
import plugin_pb2_grpc


def process_plugin_request(request):
    """
    Process the plugin request and return a result string.
    
    Args:
        request: PluginRequest containing plugin_name, plugin_data, and parameters
        
    Returns:
        str: Result of plugin processing
    """
    # Log only non-sensitive metadata
    data_size = len(request.plugin_data) if request.plugin_data else 0
    param_count = len(request.parameters) if request.parameters else 0
    logging.info(f"Processing plugin: {request.plugin_name} (data_size: {data_size} bytes, params: {param_count})")
    
    # Simple plugin processing logic
    if not request.plugin_name:
        return "Error: No plugin name provided"
    
    result = f"Plugin '{request.plugin_name}' executed successfully"
    
    if request.plugin_data:
        result += f" with {len(request.plugin_data)} bytes of data"
    
    if request.parameters:
        result += f" ({param_count} parameter(s))"
    
    return result


class PluginService(plugin_pb2_grpc.PluginServiceServicer):
    """
    Implementation of the PluginService gRPC service.
    """
    
    def ExecutePlugin(self, request, context):
        """
        Process the plugin request and return the result.
        
        Args:
            request: PluginRequest from the client
            context: gRPC context
            
        Returns:
            PluginResponse with execution result
        """
        try:
            # Process the plugin request
            result = process_plugin_request(request)
            
            # Return successful response
            return plugin_pb2.PluginResponse(
                result=result,
                success=True,
                error_message=""
            )
        except Exception as e:
            # Handle errors gracefully
            logging.error(f"Error processing plugin request: {str(e)}")
            return plugin_pb2.PluginResponse(
                result="",
                success=False,
                error_message=str(e)
            )


def serve():
    """
    Start the gRPC server and listen for plugin requests.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    plugin_pb2_grpc.add_PluginServiceServicer_to_server(PluginService(), server)
    server.add_insecure_port('[::]:50051')
    
    logging.info("Starting PluginService on port 50051...")
    server.start()
    logging.info("PluginService is running")
    
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    serve()
