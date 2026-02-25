import os
import sys
import time

time.sleep(1)

# Check if .env is loaded
print("=" * 60)
print("DEBUGGING GEMINI API SETUP")
print("=" * 60)

# Manually load dotenv like app.py does
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"✓ API Key loaded: {api_key[:20]}..." if api_key else "✗ API Key NOT found")

# Try initializing TouristRecommender
print("\n" + "=" * 60)
print("Initializing TouristRecommender...")
print("=" * 60)

try:
    from chatbot import TouristRecommender
    recommender = TouristRecommender()
    print("✓ TouristRecommender initialized successfully")
    
    # Try a simple chat
    print("\n" + "=" * 60)
    print("Testing chat with Gemini...")
    print("=" * 60)
    
    result = recommender.chat("Hello, what can you do?")
    print(f"Response type: {result.get('type')}")
    print(f"Response length: {len(result.get('response', ''))}")
    print(f"First 100 chars: {result.get('response', '')[:100]}")
    
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
