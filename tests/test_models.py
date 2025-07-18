"""
Unit tests for ollama_utils.models module.
"""

import pytest
from unittest.mock import Mock, patch
import json

from ollama_utils.models import (
    list_models, 
    pull_model, 
    delete_model, 
    show_model, 
    is_model_installed
)


class TestListModels:
    """Test the list_models function."""
    
    @patch('ollama_utils.models.requests.get')
    def test_list_models_success(self, mock_get):
        """Test successful model listing."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "models": [
                {
                    "name": "llama3.2:latest",
                    "size": 2000000000,
                    "modified_at": "2024-01-01T00:00:00Z",
                    "digest": "abc123",
                    "details": {"family": "llama", "format": "gguf"}
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = list_models()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "llama3.2:latest"
        mock_get.assert_called_once_with("http://localhost:11434/api/tags")
    
    @patch('ollama_utils.models.requests.get')
    def test_list_models_empty(self, mock_get):
        """Test empty model list."""
        mock_response = Mock()
        mock_response.json.return_value = {"models": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = list_models()
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('ollama_utils.models.requests.get')
    def test_list_models_connection_error(self, mock_get):
        """Test connection error handling."""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Connection failed")
        
        result = list_models()
        
        assert isinstance(result, dict)
        assert "error" in result
        assert "Connection failed" in result["error"]


class TestIsModelInstalled:
    """Test the is_model_installed function."""
    
    @patch('ollama_utils.models.list_models')
    def test_model_is_installed(self, mock_list_models):
        """Test when model is installed."""
        mock_list_models.return_value = [
            {"name": "llama3.2:latest"},
            {"name": "mistral:latest"}
        ]
        
        result = is_model_installed("llama3.2:latest")
        
        assert result is True
    
    @patch('ollama_utils.models.list_models')
    def test_model_not_installed(self, mock_list_models):
        """Test when model is not installed."""
        mock_list_models.return_value = [
            {"name": "llama3.2:latest"}
        ]
        
        result = is_model_installed("mistral:latest")
        
        assert result is False
    
    @patch('ollama_utils.models.list_models')
    def test_model_list_error(self, mock_list_models):
        """Test when list_models returns error."""
        mock_list_models.return_value = {"error": "Connection failed"}
        
        result = is_model_installed("llama3.2:latest")
        
        assert result is False


class TestPullModel:
    """Test the pull_model function."""
    
    @patch('ollama_utils.models.requests.post')
    def test_pull_model_success(self, mock_post):
        """Test successful model pull."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = pull_model("llama3.2:latest")
        
        assert result["success"] is True
        assert "output" in result
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/pull",
            json={"name": "llama3.2:latest", "stream": False}
        )
    
    @patch('ollama_utils.models.requests.post')
    def test_pull_model_error(self, mock_post):
        """Test pull model with error."""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        
        result = pull_model("llama3.2:latest")
        
        assert result["success"] is False
        assert "error" in result
        assert "Network error" in result["error"]


class TestDeleteModel:
    """Test the delete_model function."""
    
    @patch('ollama_utils.models.requests.delete')
    def test_delete_model_success(self, mock_delete):
        """Test successful model deletion."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        result = delete_model("llama3.2:latest")
        
        assert result["success"] is True
        assert "output" in result
        mock_delete.assert_called_once_with(
            "http://localhost:11434/api/delete",
            json={"model": "llama3.2:latest"}
        )
    
    @patch('ollama_utils.models.requests.delete')
    def test_delete_model_not_found(self, mock_delete):
        """Test delete model when model not found."""
        import requests
        mock_response = Mock()
        mock_response.status_code = 404
        mock_error = requests.exceptions.RequestException("404 Not Found")
        mock_error.response = mock_response
        mock_delete.side_effect = mock_error
        
        result = delete_model("nonexistent:latest")
        
        assert result["success"] is False
        assert "Model not found" in result["error"]


class TestShowModel:
    """Test the show_model function."""
    
    @patch('ollama_utils.models.requests.get')
    def test_show_model_success(self, mock_get):
        """Test successful show model."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "models": [
                {
                    "name": "llama3.2:latest",
                    "size": 2000000000,
                    "modified_at": "2024-01-01T00:00:00Z",
                    "digest": "abc123",
                    "details": {
                        "family": "llama",
                        "format": "gguf",
                        "parameter_size": "3.2B",
                        "quantization_level": "Q4_K_M"
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = show_model("llama3.2:latest")
        
        assert isinstance(result, str)
        assert "llama3.2:latest" in result
        assert "2.0GB" in result
        assert "llama" in result
    
    @patch('ollama_utils.models.requests.get')
    def test_show_model_not_found(self, mock_get):
        """Test show model when model not found."""
        mock_response = Mock()
        mock_response.json.return_value = {"models": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = show_model("nonexistent:latest")
        
        assert isinstance(result, str)
        assert "not found" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__])