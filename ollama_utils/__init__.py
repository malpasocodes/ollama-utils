"""
Ollama Utils - Python utilities for integrating Ollama with Streamlit and building LLM applications.

This package provides a simple, pythonic interface to Ollama's API with built-in Streamlit components
for rapid prototyping of LLM applications.

Basic usage:
    from ollama_utils import generate_with_model, chat_with_model
    
    # Generate text
    response = generate_with_model("llama3.2:latest", "Hello world!")
    
    # Chat conversation
    messages = [{"role": "user", "content": "Hello!"}]
    response = chat_with_model("llama3.2:latest", messages)
"""

__version__ = "0.1.0"
__author__ = "Alfred Essa"
__email__ = "malpaso@alfredcodes.com"
__license__ = "MIT"

# Core functions
from .models import list_models, pull_model, delete_model, show_model, is_model_installed
from .chat import chat_with_model, generate_with_model

# Streamlit helpers (optional import)
try:
    from .streamlit_helpers import model_selector, chat_ui
except ImportError:
    # Streamlit not installed, skip these imports
    pass

# Define what gets imported with "from ollama_utils import *"
__all__ = [
    # Core functions
    "list_models",
    "pull_model", 
    "delete_model",
    "show_model",
    "is_model_installed",
    "chat_with_model",
    "generate_with_model",
    # Streamlit helpers (if available)
    "model_selector",
    "chat_ui",
    # Package metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
