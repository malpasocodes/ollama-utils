# chat.py
import requests
import json

def chat_with_model(model_name, messages, stream=False, **kwargs):
    """
    Interact with a model via Ollama's /api/chat endpoint.
    
    Args:
        model_name: Name of the model to use
        messages: List of {"role": "user"|"assistant", "content": "..."}
        stream: If True, returns a generator of response chunks
        **kwargs: Additional parameters (temperature, top_p, top_k, etc.)
    
    Returns:
        If stream=False: Complete response content as string
        If stream=True: Generator yielding response chunks
    """
    try:
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": stream
        }
        
        # Add any additional parameters
        if kwargs:
            payload["options"] = kwargs
        
        response = requests.post("http://localhost:11434/api/chat", 
                               json=payload,
                               stream=stream)
        response.raise_for_status()
        
        if stream:
            # Return generator for streaming responses
            def generate():
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if chunk.get("message", {}).get("content"):
                            yield chunk["message"]["content"]
            return generate()
        else:
            # Return complete response
            return response.json()["message"]["content"]
    except requests.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            return f"Chat error ({e.response.status_code}): {e.response.text}"
        return f"Chat error: {e}"

def generate_with_model(model_name, prompt, stream=False, **kwargs):
    """
    Generate a response from a model using the /api/generate endpoint.
    
    Args:
        model_name: Name of the model to use
        prompt: Text prompt for generation
        stream: If True, returns a generator of response chunks
        **kwargs: Additional parameters (temperature, top_p, top_k, etc.)
    
    Returns:
        If stream=False: Complete response as string
        If stream=True: Generator yielding response chunks
    """
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": stream
        }
        
        # Add any additional parameters
        if kwargs:
            payload["options"] = kwargs
            
        response = requests.post("http://localhost:11434/api/generate", 
                               json=payload,
                               stream=stream)
        response.raise_for_status()
        
        if stream:
            # Return generator for streaming responses
            def generate():
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if chunk.get("response"):
                            yield chunk["response"]
            return generate()
        else:
            # Return complete response
            return response.json()["response"]
    except requests.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            return f"Generation error ({e.response.status_code}): {e.response.text}"
        return f"Generation error: {e}"
