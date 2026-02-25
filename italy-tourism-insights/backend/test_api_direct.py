import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Testing with API key: {api_key[:20]}...")

import google.generativeai as genai
print(f"\nUsing google-generativeai version: {genai.__version__}")

# Configure the API
genai.configure(api_key=api_key)

# Try to get the model
try:
    print("\nAttempting to create model...")
    model = genai.GenerativeModel("gemini-pro")
    print("✓ Model created")
    
    print("\nAttempting to send message...")
    response = model.generate_content("Hello, what is 2+2?")
    print(f"✓ Response received: {response.text[:100]}")
    
except Exception as e:
    print(f"✗ Error: {type(e).__name__}")
    print(f"Message: {str(e)}")
    import traceback
    traceback.print_exc()
