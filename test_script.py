from ollama_utils import list_models, generate_with_model

print("Installed models:")
print(list_models())

print("Generating response:")
response = generate_with_model("llama3.2:latest", "What is the capital of France?")
print(response)