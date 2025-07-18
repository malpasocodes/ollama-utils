"""
Streamlit example using ollama-utils.

Run with: streamlit run streamlit_example.py
"""

import streamlit as st
from ollama_utils import generate_with_model, chat_with_model
from ollama_utils.streamlit_helpers import model_selector, chat_ui

def main():
    st.set_page_config(page_title="Ollama Utils Streamlit Example", page_icon="🤖")
    
    st.title("🤖 Ollama Utils Streamlit Example")
    st.markdown("This app demonstrates different ways to use ollama-utils with Streamlit.")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page:", [
        "Text Generator",
        "Chat Interface", 
        "Full Chat UI"
    ])
    
    if page == "Text Generator":
        text_generator_page()
    elif page == "Chat Interface":
        chat_interface_page()
    elif page == "Full Chat UI":
        full_chat_ui_page()

def text_generator_page():
    st.header("📝 Text Generator")
    st.markdown("Generate text using different models and parameters.")
    
    # Model selection
    model = model_selector(sidebar=False)
    
    if model:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            prompt = st.text_area(
                "Enter your prompt:", 
                "Write a short poem about artificial intelligence",
                height=100
            )
        
        with col2:
            st.markdown("**Settings**")
            streaming = st.checkbox("Enable streaming", value=True)
            temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
            max_tokens = st.number_input("Max tokens", 50, 1000, 300)
        
        if st.button("Generate", type="primary"):
            if prompt:
                st.divider()
                
                if streaming:
                    st.markdown("**Generated Text:**")
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    try:
                        for chunk in generate_with_model(
                            model, 
                            prompt, 
                            stream=True,
                            temperature=temperature,
                            num_predict=max_tokens
                        ):
                            full_response += chunk
                            response_placeholder.markdown(full_response + "▌")
                        
                        response_placeholder.markdown(full_response)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    with st.spinner("Generating..."):
                        try:
                            response = generate_with_model(
                                model,
                                prompt,
                                temperature=temperature,
                                num_predict=max_tokens
                            )
                            st.markdown("**Generated Text:**")
                            st.markdown(response)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please install a model first using `ollama pull <model-name>`")

def chat_interface_page():
    st.header("💬 Chat Interface")
    st.markdown("Have a conversation with your model.")
    
    # Model selection
    model = model_selector(sidebar=False)
    
    if model:
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("What would you like to talk about?"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                try:
                    for chunk in chat_with_model(
                        model, 
                        st.session_state.messages, 
                        stream=True,
                        temperature=0.7
                    ):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    
                    response_placeholder.markdown(full_response)
                    
                    # Add assistant response to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_response
                    })
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Chat controls
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    else:
        st.warning("Please install a model first using `ollama pull <model-name>`")

def full_chat_ui_page():
    st.header("🚀 Full Chat UI")
    st.markdown("This uses the pre-built `chat_ui()` function from ollama-utils.")
    
    # Use the built-in chat UI
    chat_ui(streaming=True)

if __name__ == "__main__":
    main()