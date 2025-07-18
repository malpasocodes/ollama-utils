"""
Model management example using ollama-utils.

This script demonstrates how to manage Ollama models using the ollama-utils package.
"""

from ollama_utils import (
    list_models, 
    pull_model, 
    delete_model, 
    show_model,
    is_model_installed
)
import json

def main():
    print("🔧 Ollama Utils - Model Management Examples\n")
    
    # 1. List all models
    print("1. Listing all installed models:")
    models = list_models()
    
    if isinstance(models, list):
        if models:
            print(f"   Found {len(models)} models:\n")
            for i, model in enumerate(models, 1):
                print(f"   {i}. {model['name']}")
                print(f"      Size: {model['size'] / 1e9:.1f}GB")
                print(f"      Modified: {model['modified_at']}")
                print(f"      Family: {model['details']['family']}")
                print()
        else:
            print("   No models found.")
    else:
        print(f"   Error: {models}")
        return
    
    # 2. Show detailed model information
    if models:
        model_name = models[0]['name']
        print(f"2. Detailed information for {model_name}:")
        info = show_model(model_name)
        print(f"   {info}")
        
        # 3. Check if model is installed
        print(f"3. Checking if {model_name} is installed:")
        is_installed = is_model_installed(model_name)
        print(f"   Installed: {'✅ Yes' if is_installed else '❌ No'}")
        
        # 4. Check a non-existent model
        fake_model = "non-existent-model:latest"
        print(f"4. Checking if {fake_model} is installed:")
        is_installed = is_model_installed(fake_model)
        print(f"   Installed: {'✅ Yes' if is_installed else '❌ No'}")
    
    # 5. Example of pulling a model (commented out to avoid actual download)
    print("\n5. Example of pulling a model:")
    print("   # This would download a model - commented out for demo")
    print("   # result = pull_model('llama3.2:1b')")
    print("   # if result['success']:")
    print("   #     print('Model pulled successfully!')")
    print("   # else:")
    print("   #     print(f'Error: {result[\"error\"]}')")
    
    # 6. Example of deleting a model (commented out for safety)
    print("\n6. Example of deleting a model:")
    print("   # This would delete a model - commented out for safety")
    print("   # result = delete_model('model-name:tag')")
    print("   # if result['success']:")
    print("   #     print('Model deleted successfully!')")
    print("   # else:")
    print("   #     print(f'Error: {result[\"error\"]}')")
    
    # 7. Interactive model management
    print("\n7. Interactive model management:")
    interactive_management()

def interactive_management():
    """Interactive model management menu."""
    while True:
        print("\n" + "="*50)
        print("Interactive Model Management")
        print("="*50)
        print("1. List models")
        print("2. Show model details")
        print("3. Check if model is installed")
        print("4. Pull a model")
        print("5. Delete a model")
        print("6. Exit")
        print("="*50)
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                models = list_models()
                if isinstance(models, list):
                    if models:
                        print(f"\nFound {len(models)} models:")
                        for i, model in enumerate(models, 1):
                            print(f"{i}. {model['name']} ({model['size'] / 1e9:.1f}GB)")
                    else:
                        print("No models found.")
                else:
                    print(f"Error: {models}")
            
            elif choice == "2":
                model_name = input("Enter model name: ").strip()
                if model_name:
                    info = show_model(model_name)
                    print(f"\n{info}")
                else:
                    print("Please enter a model name.")
            
            elif choice == "3":
                model_name = input("Enter model name: ").strip()
                if model_name:
                    is_installed = is_model_installed(model_name)
                    status = "✅ Installed" if is_installed else "❌ Not installed"
                    print(f"\n{model_name}: {status}")
                else:
                    print("Please enter a model name.")
            
            elif choice == "4":
                model_name = input("Enter model name to pull: ").strip()
                if model_name:
                    confirm = input(f"Are you sure you want to pull {model_name}? (y/N): ").strip().lower()
                    if confirm == 'y':
                        print(f"Pulling {model_name}... This may take a while.")
                        result = pull_model(model_name)
                        if result.get("success"):
                            print("✅ Model pulled successfully!")
                        else:
                            print(f"❌ Error: {result.get('error')}")
                    else:
                        print("Operation cancelled.")
                else:
                    print("Please enter a model name.")
            
            elif choice == "5":
                # List current models first
                models = list_models()
                if isinstance(models, list) and models:
                    print("\nCurrent models:")
                    for i, model in enumerate(models, 1):
                        print(f"{i}. {model['name']}")
                    
                    model_name = input("Enter model name to delete: ").strip()
                    if model_name:
                        confirm = input(f"Are you sure you want to delete {model_name}? (y/N): ").strip().lower()
                        if confirm == 'y':
                            result = delete_model(model_name)
                            if result.get("success"):
                                print("✅ Model deleted successfully!")
                            else:
                                print(f"❌ Error: {result.get('error')}")
                        else:
                            print("Operation cancelled.")
                    else:
                        print("Please enter a model name.")
                else:
                    print("No models available to delete.")
            
            elif choice == "6":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please enter 1-6.")
        
        except KeyboardInterrupt:
            print("\nOperation interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()