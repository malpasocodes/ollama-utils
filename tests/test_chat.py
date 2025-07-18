"""
Unit tests for ollama_utils.chat module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from ollama_utils.chat import chat_with_model, generate_with_model


class TestChatWithModel:
    """Test the chat_with_model function."""
    
    @patch('ollama_utils.chat.requests.post')
    def test_chat_with_model_success(self, mock_post):
        """Test successful chat."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "Hello! How can I help you?"}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "Hello"}]
        result = chat_with_model("llama3.2:latest", messages)
        
        assert result == "Hello! How can I help you?"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2:latest",
                "messages": messages,
                "stream": False
            },
            stream=False
        )
    
    @patch('ollama_utils.chat.requests.post')
    def test_chat_with_model_with_options(self, mock_post):
        """Test chat with custom options."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"content": "Response with options"}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "Hello"}]
        result = chat_with_model(
            "llama3.2:latest", 
            messages, 
            temperature=0.8, 
            top_p=0.9
        )
        
        assert result == "Response with options"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2:latest",
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.8, "top_p": 0.9}
            },
            stream=False
        )
    
    @patch('ollama_utils.chat.requests.post')
    def test_chat_with_model_streaming(self, mock_post):
        """Test streaming chat."""
        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'{"message": {"content": "Hello"}}',
            b'{"message": {"content": " there"}}',
            b'{"message": {"content": "!"}}'
        ]
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "Hello"}]
        result = chat_with_model("llama3.2:latest", messages, stream=True)
        
        # Result should be a generator
        chunks = list(result)
        assert chunks == ["Hello", " there", "!"]
        
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2:latest",
                "messages": messages,
                "stream": True
            },
            stream=True
        )
    
    @patch('ollama_utils.chat.requests.post')
    def test_chat_with_model_error(self, mock_post):
        """Test chat with error."""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Connection failed")
        
        messages = [{"role": "user", "content": "Hello"}]
        result = chat_with_model("llama3.2:latest", messages)
        
        assert isinstance(result, str)
        assert "Chat error" in result
        assert "Connection failed" in result


class TestGenerateWithModel:
    """Test the generate_with_model function."""
    
    @patch('ollama_utils.chat.requests.post')
    def test_generate_with_model_success(self, mock_post):
        """Test successful generation."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "This is a generated response."
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = generate_with_model("llama3.2:latest", "Hello world")
        
        assert result == "This is a generated response."
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": "Hello world",
                "stream": False
            },
            stream=False
        )
    
    @patch('ollama_utils.chat.requests.post')
    def test_generate_with_model_with_options(self, mock_post):
        """Test generation with custom options."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": "Generated with options"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = generate_with_model(
            "llama3.2:latest", 
            "Hello world",
            temperature=0.5,
            num_predict=100
        )
        
        assert result == "Generated with options"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": "Hello world",
                "stream": False,
                "options": {"temperature": 0.5, "num_predict": 100}
            },
            stream=False
        )
    
    @patch('ollama_utils.chat.requests.post')
    def test_generate_with_model_streaming(self, mock_post):
        """Test streaming generation."""
        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'{"response": "Hello"}',
            b'{"response": " world"}',
            b'{"response": "!"}'
        ]
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = generate_with_model("llama3.2:latest", "Hello", stream=True)
        
        # Result should be a generator
        chunks = list(result)
        assert chunks == ["Hello", " world", "!"]
        
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": "Hello",
                "stream": True
            },
            stream=True
        )
    
    @patch('ollama_utils.chat.requests.post')
    def test_generate_with_model_error(self, mock_post):
        """Test generation with error."""
        import requests
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_error = requests.exceptions.RequestException("500 Server Error")
        mock_error.response = mock_response
        mock_post.side_effect = mock_error
        
        result = generate_with_model("llama3.2:latest", "Hello")
        
        assert isinstance(result, str)
        assert "Generation error" in result
        assert "500" in result
        assert "Internal Server Error" in result
    
    @patch('ollama_utils.chat.requests.post')
    def test_generate_with_model_empty_response_in_stream(self, mock_post):
        """Test streaming generation with empty response chunks."""
        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'{"response": "Hello"}',
            b'{"response": ""}',  # Empty response
            b'{"response": " world"}'
        ]
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = generate_with_model("llama3.2:latest", "Hello", stream=True)
        
        # Should filter out empty responses
        chunks = list(result)
        assert chunks == ["Hello", " world"]


if __name__ == "__main__":
    pytest.main([__file__])