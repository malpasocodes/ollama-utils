# streamlit_helpers.py
import streamlit as st
from .models import list_models

def model_selector(label="Select a local model", sidebar=True):
    """Dropdown selector for available local Ollama models."""
    models = list_models()
    if isinstance(models, list) and len(models) > 0:
        model_names = [m['name'] for m in models]
        if sidebar:
            return st.sidebar.selectbox(label, model_names)
        else:
            return st.selectbox(label, model_names)
    else:
        error_msg = "No models found. Please install a model using 'ollama pull <model-name>'"
        if sidebar:
            st.sidebar.error(error_msg)
        else:
            st.error(error_msg)
        return None

def chat_ui(model_name=None, streaming=True):
    """
    Complete chat UI with message history and streaming support.
    
    Args:
        model_name: Model to use (if None, uses model_selector)
        streaming: Enable streaming responses for better UX
    """
    from .chat import chat_with_model
    
    st.title("🧠 Local LLM Chat")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Model selection
    if model_name is None:
        model_name = model_selector()
        if model_name is None:
            return  # No models available
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            if streaming:
                # Streaming response
                response_placeholder = st.empty()
                full_response = ""
                
                try:
                    for chunk in chat_with_model(model_name, st.session_state.messages, stream=True):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                except Exception as e:
                    full_response = f"Error: {str(e)}"
                    response_placeholder.error(full_response)
            else:
                # Non-streaming response
                with st.spinner("Thinking..."):
                    full_response = chat_with_model(model_name, st.session_state.messages, stream=False)
                st.markdown(full_response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### Chat Controls")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            max_tokens = st.number_input("Max Tokens", 100, 4000, 1000, 100)
            st.session_state.chat_options = {
                "temperature": temperature,
                "num_predict": max_tokens
            }