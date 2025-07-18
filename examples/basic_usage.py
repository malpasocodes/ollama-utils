"""
Basic usage examples for ollama-utils.

This script demonstrates the core functionality of the ollama-utils package.
"""

from ollama_utils import (
    list_models, 
    generate_with_model, 
    chat_with_model,
    is_model_installed
)

def main():
    print("🤖 Ollama Utils - Basic Usage Examples\n")
    
    # 1. List available models
    print("1. Listing available models:")
    models = list_models()
    if isinstance(models, list):
        print(f"   Found {len(models)} models:")
        for model in models[:3]:  # Show first 3
            print(f"   - {model['name']} ({model['size'] / 1e9:.1f}GB)")
        if len(models) > 3:
            print(f"   ... and {len(models) - 3} more")
    else:
        print(f"   Error: {models}")
        return
    
    # Use the first available model
    if not models:
        print("❌ No models available. Please install a model first.")
        return
    
    model_name = models[0]['name']
    print(f"\n📱 Using model: {model_name}")
    
    # 2. Check if model is installed
    print(f"\n2. Checking if {model_name} is installed:")
    if is_model_installed(model_name):
        print("   ✅ Model is installed")
    else:
        print("   ❌ Model is not installed")
    
    # 3. Simple text generation
    print("\n3. Simple text generation:")
    prompt = "Write a haiku about programming"
    print(f"   Prompt: {prompt}")
    print("   Response:", end=" ")
    
    response = generate_with_model(model_name, prompt, temperature=0.7)
    print(f"{response}")
    
    # 4. Generation with custom parameters
    print("\n4. Generation with custom parameters:")
    prompt = "Explain Python in one sentence"
    print(f"   Prompt: {prompt}")
    print("   Response:", end=" ")
    
    response = generate_with_model(
        model_name, 
        prompt,
        temperature=0.3,  # Lower temperature for more focused response
        num_predict=50    # Limit tokens
    )
    print(f"{response}")
    
    # 5. Chat conversation
    print("\n5. Chat conversation:")
    messages = [
        {"role": "user", "content": "Hello! What's your favorite color?"}
    ]
    
    print("   User: Hello! What's your favorite color?")
    response = chat_with_model(model_name, messages)
    print(f"   Assistant: {response}")
    
    # Continue the conversation
    messages.append({"role": "assistant", "content": response})
    messages.append({"role": "user", "content": "Why do you like that color?"})
    
    print("   User: Why do you like that color?")
    response = chat_with_model(model_name, messages)
    print(f"   Assistant: {response}")
    
    # 6. Streaming example
    print("\n6. Streaming generation:")
    prompt = "Count from 1 to 10"
    print(f"   Prompt: {prompt}")
    print("   Streaming response: ", end="", flush=True)
    
    for chunk in generate_with_model(model_name, prompt, stream=True):
        print(chunk, end="", flush=True)
    
    print("\n\n✅ All examples completed!")

if __name__ == "__main__":
    main()