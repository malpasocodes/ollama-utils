# Ollama Utils

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library providing convenient utilities for integrating [Ollama](https://ollama.com) with Streamlit and Python applications. This package offers a simple, pythonic interface to Ollama's API with built-in Streamlit components for rapid prototyping of LLM applications.

## Features

-  **Full HTTP API Integration** - No CLI dependencies
- =� **Streaming Support** - Real-time response streaming
- <� **Parameter Control** - Fine-tune model behavior (temperature, top_p, etc.)
- =� **Streamlit Components** - Ready-to-use UI components
- = **Model Management** - List, pull, delete, and inspect models
- =� **Chat Interface** - Multi-turn conversations
- <� **Simple API** - Easy to use, well-documented functions

## Installation

### Using uv (recommended)
```bash
uv add ollama-utils
```

### Using pip
```bash
pip install ollama-utils
```

## Prerequisites

1. **Install Ollama**: Download from [ollama.com](https://ollama.com)

2. **Start Ollama server**:
   ```bash
   ollama serve
   ```

3. **Pull a model**:
   ```bash
   ollama pull llama3.2:latest
   ```

## Quick Start

### Basic Text Generation

```python
from ollama_utils import generate_with_model

# Simple generation
response = generate_with_model("llama3.2:latest", "Write a haiku about Python")
print(response)

# With custom parameters
response = generate_with_model(
    "llama3.2:latest", 
    "Explain quantum computing",
    temperature=0.7,
    num_predict=500
)
```

### Chat Conversations

```python
from ollama_utils import chat_with_model

messages = [
    {"role": "user", "content": "Hello! What's the weather like?"},
    {"role": "assistant", "content": "I don't have access to real-time weather data, but I can help you with weather-related questions!"},
    {"role": "user", "content": "What should I wear in 70�F weather?"}
]

response = chat_with_model("llama3.2:latest", messages)
print(response)
```

### Streaming Responses

```python
from ollama_utils import generate_with_model

# Stream generation
for chunk in generate_with_model("llama3.2:latest", "Tell me a story", stream=True):
    print(chunk, end="", flush=True)

# Stream chat
for chunk in chat_with_model("llama3.2:latest", messages, stream=True):
    print(chunk, end="", flush=True)
```

### Model Management

```python
from ollama_utils import list_models, pull_model, delete_model, show_model

# List available models
models = list_models()
for model in models:
    print(f"Model: {model['name']}, Size: {model['size']}")

# Pull a new model
result = pull_model("mistral:latest")
if result["success"]:
    print("Model pulled successfully!")

# Get model info
info = show_model("llama3.2:latest")
print(info)
```

## Streamlit Integration

### Quick Chat Interface

```python
import streamlit as st
from ollama_utils.streamlit_helpers import chat_ui

st.title("My LLM Chat App")

# This creates a complete chat interface!
chat_ui()
```

### Custom Streamlit App

```python
import streamlit as st
from ollama_utils.streamlit_helpers import model_selector
from ollama_utils import generate_with_model

st.title("LLM Text Generator")

# Model selection dropdown
model = model_selector()

# Text input
prompt = st.text_area("Enter your prompt:")

if st.button("Generate"):
    if model and prompt:
        # Generate with streaming
        response_placeholder = st.empty()
        full_response = ""
        
        for chunk in generate_with_model(model, prompt, stream=True):
            full_response += chunk
            response_placeholder.markdown(full_response + "�")
        
        response_placeholder.markdown(full_response)
```

## API Reference

### Core Functions

#### `generate_with_model(model_name, prompt, stream=False, **kwargs)`
Generate text using the `/api/generate` endpoint.

**Parameters:**
- `model_name` (str): Name of the model (e.g., "llama3.2:latest")
- `prompt` (str): Input prompt
- `stream` (bool): Enable streaming responses
- `**kwargs`: Additional parameters (temperature, top_p, num_predict, etc.)

**Returns:**
- If `stream=False`: Complete response as string
- If `stream=True`: Generator yielding response chunks

#### `chat_with_model(model_name, messages, stream=False, **kwargs)`
Multi-turn chat using the `/api/chat` endpoint.

**Parameters:**
- `model_name` (str): Name of the model
- `messages` (List[dict]): List of messages with "role" and "content" keys
- `stream` (bool): Enable streaming responses
- `**kwargs`: Additional parameters

**Returns:**
- If `stream=False`: Complete response as string
- If `stream=True`: Generator yielding response chunks

#### `list_models()`
List all locally installed models.

**Returns:**
- List of model dictionaries with metadata

#### `pull_model(model_name)`
Download a model from Ollama registry.

**Parameters:**
- `model_name` (str): Name of the model to pull

**Returns:**
- Dictionary with "success" and "output"/"error" keys

#### `delete_model(model_name)`
Remove a model from local cache.

**Parameters:**
- `model_name` (str): Name of the model to delete

**Returns:**
- Dictionary with "success" and "output"/"error" keys

#### `show_model(model_name)`
Display detailed information about a model.

**Parameters:**
- `model_name` (str): Name of the model

**Returns:**
- Formatted string with model information

#### `is_model_installed(model_name)`
Check if a model is installed locally.

**Parameters:**
- `model_name` (str): Name of the model

**Returns:**
- Boolean indicating if the model is installed

### Streamlit Helpers

#### `model_selector(label="Select a local model", sidebar=True)`
Create a dropdown selector for available models.

**Parameters:**
- `label` (str): Label for the selector
- `sidebar` (bool): Whether to place in sidebar

**Returns:**
- Selected model name or None

#### `chat_ui(model_name=None, streaming=True)`
Complete chat interface with history and controls.

**Parameters:**
- `model_name` (str, optional): Model to use (if None, shows selector)
- `streaming` (bool): Enable streaming responses

## Advanced Usage

### Custom Parameters

```python
# Fine-tune model behavior
response = generate_with_model(
    "llama3.2:latest",
    "Explain machine learning",
    temperature=0.8,      # Creativity (0.0-2.0)
    top_p=0.9,           # Nucleus sampling (0.0-1.0)
    top_k=40,            # Top-k sampling (1-100)
    repeat_penalty=1.1,   # Repetition penalty (0.0-2.0)
    num_predict=1000,     # Max tokens to generate
)
```

### Error Handling

```python
from ollama_utils import chat_with_model

try:
    response = chat_with_model("nonexistent-model", messages)
    if response.startswith("Chat error"):
        print(f"Error occurred: {response}")
    else:
        print(f"Response: {response}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Demo Application

Run the included demo to test all features:

```bash
git clone https://github.com/malpasocodes/ollama-utils.git
cd ollama-utils
uv sync
uv run streamlit run demo_app.py
```

The demo includes:
- Model management interface
- Text generation testing
- Chat interface
- API parameter testing
- Full chat UI demonstration

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- `requests` library
- `streamlit` library (for Streamlit helpers)

## Contributing

1. Fork the repository
2. Clone and set up development environment:
   ```bash
   git clone https://github.com/your-username/ollama-utils.git
   cd ollama-utils
   uv sync
   ```
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Run tests: `uv run pytest`
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/malpasocodes/ollama-utils/issues)
- **Discussions**: [GitHub Discussions](https://github.com/malpasocodes/ollama-utils/discussions)
- **Documentation**: [API Reference](https://github.com/malpasocodes/ollama-utils#api-reference)

## Changelog

### 0.1.0
- Initial release
- Full HTTP API integration
- Streaming support
- Streamlit helpers
- Model management functions
- Chat and generation capabilities