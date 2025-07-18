# Ollama Utils Examples

This directory contains example scripts demonstrating the usage of the ollama-utils package.

## Prerequisites

1. **Install ollama-utils**:
   ```bash
   # Using uv (recommended)
   uv add ollama-utils
   
   # Or using pip
   pip install ollama-utils
   ```

2. **Install and run Ollama**:
   ```bash
   # Install Ollama from https://ollama.com
   ollama serve
   ```

3. **Pull a model**:
   ```bash
   ollama pull llama3.2:latest
   ```

## Examples

### 1. Basic Usage (`basic_usage.py`)
Demonstrates core functionality including:
- Listing models
- Text generation
- Chat conversations
- Streaming responses
- Parameter customization

**Run:**
```bash
# If installed globally
python basic_usage.py

# If using uv in a project
uv run python basic_usage.py
```

### 2. Streamlit Integration (`streamlit_example.py`)
Shows how to build Streamlit applications with ollama-utils:
- Text generator page
- Chat interface
- Full chat UI using built-in components

**Run:**
```bash
# If installed globally
streamlit run streamlit_example.py

# If using uv in a project
uv run streamlit run streamlit_example.py
```

### 3. Model Management (`model_management.py`)
Demonstrates model management operations:
- Listing models
- Showing model details
- Checking installation status
- Interactive management menu

**Run:**
```bash
# If installed globally
python model_management.py

# If using uv in a project
uv run python model_management.py
```

## Code Snippets

### Quick Text Generation
```python
from ollama_utils import generate_with_model

response = generate_with_model("llama3.2:latest", "Hello, world!")
print(response)
```

### Streaming Generation
```python
from ollama_utils import generate_with_model

for chunk in generate_with_model("llama3.2:latest", "Tell me a story", stream=True):
    print(chunk, end="", flush=True)
```

### Simple Chat
```python
from ollama_utils import chat_with_model

messages = [{"role": "user", "content": "What is Python?"}]
response = chat_with_model("llama3.2:latest", messages)
print(response)
```

### Streamlit Chat UI
```python
import streamlit as st
from ollama_utils.streamlit_helpers import chat_ui

st.title("My Chat App")
chat_ui()  # That's it!
```

## Tips

1. **Model Selection**: Use `list_models()` to see available models
2. **Error Handling**: Always check if models are installed before using them
3. **Streaming**: Use streaming for better user experience with long responses
4. **Parameters**: Experiment with temperature, top_p, and other parameters
5. **Streamlit**: The built-in `chat_ui()` provides a complete chat interface

## Troubleshooting

- **"No models found"**: Install a model using `ollama pull <model-name>`
- **Connection errors**: Make sure Ollama is running (`ollama serve`)
- **Import errors**: Install streamlit if using Streamlit examples:
  ```bash
  # Using uv
  uv add streamlit
  
  # Using pip
  pip install streamlit
  ```