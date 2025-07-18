# models.py
import requests

def list_models():
    """Return a list of locally installed Ollama models."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        return response.json().get("models", [])
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to list models: {str(e)}"}

def pull_model(model_name):
    """Pull a model from the Ollama registry."""
    try:
        response = requests.post("http://localhost:11434/api/pull", json={
            "name": model_name,
            "stream": False
        })
        response.raise_for_status()
        return {"success": True, "output": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

def delete_model(model_name):
    """Remove a model from the local cache."""
    try:
        response = requests.delete("http://localhost:11434/api/delete", json={
            "model": model_name
        })
        response.raise_for_status()
        return {"success": True, "output": "Model deleted successfully"}
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response.status_code == 404:
            return {"success": False, "error": "Model not found"}
        return {"success": False, "error": str(e)}

def show_model(model_name):
    """Show metadata for a specific model."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        
        for model in models:
            if model.get("name") == model_name:
                # Format the output to match CLI behavior
                output = f"Model: {model.get('name', 'N/A')}\n"
                output += f"Size: {model.get('size', 0) / 1e9:.1f}GB\n"
                output += f"Modified: {model.get('modified_at', 'N/A')}\n"
                output += f"Digest: {model.get('digest', 'N/A')}\n"
                
                details = model.get('details', {})
                if details:
                    output += f"\nDetails:\n"
                    output += f"  Format: {details.get('format', 'N/A')}\n"
                    output += f"  Family: {details.get('family', 'N/A')}\n"
                    output += f"  Parameter Size: {details.get('parameter_size', 'N/A')}\n"
                    output += f"  Quantization: {details.get('quantization_level', 'N/A')}\n"
                
                return output
        
        return f"Error showing model info: Model '{model_name}' not found"
    except requests.exceptions.RequestException as e:
        return f"Error showing model info: {str(e)}"

def is_model_installed(model_name):
    """Check if a model is already installed locally."""
    models = list_models()
    if isinstance(models, list):
        return any(m['name'] == model_name for m in models)
    return False
