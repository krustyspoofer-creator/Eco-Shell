"""
Unit tests for the PluginService
"""
import unittest
from unittest.mock import Mock, patch
import grpc

import plugin_pb2
import plugin_pb2_grpc
from plugin_service import PluginService, process_plugin_request


class TestPluginService(unittest.TestCase):
    """Test cases for PluginService"""
    
    def test_process_plugin_request_basic(self):
        """Test basic plugin request processing"""
        request = plugin_pb2.PluginRequest(
            plugin_name="test_plugin",
            plugin_data="test data"
        )
        result = process_plugin_request(request)
        
        self.assertIn("test_plugin", result)
        self.assertIn("executed successfully", result)
    
    def test_process_plugin_request_with_parameters(self):
        """Test plugin request with parameters"""
        request = plugin_pb2.PluginRequest(
            plugin_name="param_plugin",
            plugin_data="data",
            parameters={"key1": "value1", "key2": "value2"}
        )
        result = process_plugin_request(request)
        
        self.assertIn("param_plugin", result)
        self.assertIn("2 parameter(s)", result)
    
    def test_process_plugin_request_empty_name(self):
        """Test plugin request with empty name"""
        request = plugin_pb2.PluginRequest(
            plugin_name=""
        )
        result = process_plugin_request(request)
        
        self.assertIn("Error", result)
    
    def test_execute_plugin_success(self):
        """Test ExecutePlugin method success case"""
        service = PluginService()
        request = plugin_pb2.PluginRequest(
            plugin_name="test_plugin"
        )
        context = Mock()
        
        response = service.ExecutePlugin(request, context)
        
        self.assertTrue(response.success)
        self.assertIn("test_plugin", response.result)
        self.assertEqual(response.error_message, "")
    
    def test_execute_plugin_with_exception(self):
        """Test ExecutePlugin method with exception"""
        service = PluginService()
        request = plugin_pb2.PluginRequest(
            plugin_name="test_plugin"
        )
        context = Mock()
        
        # Mock process_plugin_request to raise an exception
        with patch('plugin_service.process_plugin_request', side_effect=Exception("Test error")):
            response = service.ExecutePlugin(request, context)
        
        self.assertFalse(response.success)
        self.assertEqual(response.result, "")
        self.assertIn("Test error", response.error_message)


if __name__ == '__main__':
    unittest.main()
