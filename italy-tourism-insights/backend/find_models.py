import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API key: {api_key[:20]}...")

import google.generativeai as genai
genai.configure(api_key=api_key)

print("\nAvailable models:")
print("=" * 60)

try:
    # List all available models
    for model in genai.list_models():
        print(f"- {model.name}")
        if 'supported_generation_methods' in dir(model):
            methods = model.supported_generation_methods
            if methods:
                print(f"  Methods: {', '.join(methods)}")
except Exception as e:
    print(f"Error listing models: {e}")

# Try to find generative models
print("\n" + "=" * 60)
print("Attempting to use gemini-1.5-pro...")
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content("What is 2+2?")
    print(f"✓ Success! Response: {response.text[:100]}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nAttempting to use gemini-1.5-flash...")
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("What is 2+2?")
    print(f"✓ Success! Response: {response.text[:100]}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\nAttempting to use gemini-pro-vision...")
try:
    model = genai.GenerativeModel("gemini-pro-vision")
    print(f"✓ gemini-pro-vision available")
except Exception as e:
    print(f"✗ Error: {e}")
