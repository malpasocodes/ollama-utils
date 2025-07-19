#!/usr/bin/env python3
"""
Local testing script for ollama-utils package.

This script tests the installed package to ensure all functionality works
before publishing to PyPI.
"""

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import ollama_utils
        print(f"  ✅ ollama_utils imported - version {ollama_utils.__version__}")
        
        from ollama_utils import (
            list_models, pull_model, delete_model, show_model, is_model_installed,
            chat_with_model, generate_with_model
        )
        print("  ✅ Core functions imported")
        
        # Test optional Streamlit imports
        try:
            from ollama_utils import model_selector, chat_ui
            print("  ✅ Streamlit helpers imported")
        except ImportError as e:
            print(f"  ⚠️  Streamlit helpers not available: {e}")
            print("     This is expected if Streamlit is not installed")
        
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_model_functions():
    """Test model management functions."""
    print("\n🧪 Testing model management functions...")
    
    try:
        from ollama_utils import list_models, is_model_installed, show_model
        
        # Test list_models
        print("  Testing list_models()...")
        models = list_models()
        if isinstance(models, list):
            print(f"    ✅ Found {len(models)} models")
            if models:
                first_model = models[0]['name']
                print(f"    First model: {first_model}")
                
                # Test is_model_installed
                print("  Testing is_model_installed()...")
                is_installed = is_model_installed(first_model)
                print(f"    ✅ {first_model} installed: {is_installed}")
                
                # Test show_model
                print("  Testing show_model()...")
                info = show_model(first_model)
                print(f"    ✅ Model info retrieved (length: {len(info)} chars)")
                
            else:
                print("    ⚠️  No models found - you may need to install a model")
        else:
            print(f"    ❌ Error: {models}")
            return False
            
        return True
    except Exception as e:
        print(f"  ❌ Model functions failed: {e}")
        return False

def test_chat_functions():
    """Test chat and generation functions."""
    print("\n🧪 Testing chat and generation functions...")
    
    try:
        from ollama_utils import generate_with_model, chat_with_model, list_models
        
        # Get available models
        models = list_models()
        if not isinstance(models, list) or not models:
            print("    ⚠️  No models available for testing")
            return True
        
        model_name = models[0]['name']
        print(f"  Using model: {model_name}")
        
        # Test basic generation
        print("  Testing generate_with_model()...")
        response = generate_with_model(model_name, "Say 'Hello, world!' in exactly those words.")
        if isinstance(response, str) and len(response) > 0:
            print(f"    ✅ Generation successful: {response[:50]}...")
        else:
            print(f"    ❌ Generation failed: {response}")
            return False
        
        # Test chat
        print("  Testing chat_with_model()...")
        messages = [{"role": "user", "content": "Say 'Testing!' in exactly that word."}]
        response = chat_with_model(model_name, messages)
        if isinstance(response, str) and len(response) > 0:
            print(f"    ✅ Chat successful: {response[:50]}...")
        else:
            print(f"    ❌ Chat failed: {response}")
            return False
        
        # Test with parameters
        print("  Testing with custom parameters...")
        response = generate_with_model(
            model_name, 
            "Count: 1, 2, 3", 
            temperature=0.1,
            num_predict=20
        )
        if isinstance(response, str):
            print(f"    ✅ Parameters work: {response[:30]}...")
        else:
            print(f"    ❌ Parameters failed: {response}")
            return False
            
        return True
    except Exception as e:
        print(f"  ❌ Chat functions failed: {e}")
        return False

def test_package_metadata():
    """Test package metadata and structure."""
    print("\n🧪 Testing package metadata...")
    
    try:
        import ollama_utils
        
        # Test metadata
        attrs = ['__version__', '__author__', '__email__', '__license__']
        for attr in attrs:
            if hasattr(ollama_utils, attr):
                value = getattr(ollama_utils, attr)
                print(f"  ✅ {attr}: {value}")
            else:
                print(f"  ⚠️  Missing {attr}")
        
        # Test __all__
        if hasattr(ollama_utils, '__all__'):
            print(f"  ✅ __all__ defined with {len(ollama_utils.__all__)} exports")
        else:
            print(f"  ⚠️  __all__ not defined")
        
        return True
    except Exception as e:
        print(f"  ❌ Metadata test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing ollama-utils package locally\n")
    
    tests = [
        test_imports,
        test_package_metadata,
        test_model_functions,
        test_chat_functions,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! Package is ready for use.")
        print("\n🎯 Try running the examples:")
        print("   python examples/basic_usage.py")
        print("   uv run streamlit run examples/streamlit_example.py")
    else:
        print("❌ Some tests failed. Check the output above.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)