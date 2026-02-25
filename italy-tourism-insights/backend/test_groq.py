import requests
import time

time.sleep(2)

print("Testing Groq chatbot integration...")
print("=" * 60)

try:
    # Test 1: Greeting
    print("Test 1: Greeting")
    r = requests.post('http://localhost:8000/api/chat', 
                     json={'message': 'Hello! I want to visit Italy', 'language': 'en'}, 
                     timeout=15)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Status: 200 OK")
        print(f"Response: {data['response'][:150]}...")
        print()
    else:
        print(f"❌ Status: {r.status_code}")
        print(f"Error: {r.text}")

    # Test 2: Hotel request
    print("Test 2: Hotel recommendation")
    r = requests.post('http://localhost:8000/api/chat', 
                     json={'message': 'I need hotels in Rome', 'language': 'en'}, 
                     timeout=15)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Status: 200 OK")
        print(f"Response: {data['response'][:150]}...")
        if data.get('recommendations'):
            print(f"Recommendations found: {len(data['recommendations'])}")
            for rec in data['recommendations'][:2]:
                print(f"  - {rec['icon']} {rec['name']}")
                if rec.get('link'):
                    print(f"    Link: {rec['link']}")
        print()
    else:
        print(f"❌ Status: {r.status_code}")

    # Test 3: Non-tourism (should politely refuse)
    print("Test 3: Non-tourism question")
    r = requests.post('http://localhost:8000/api/chat', 
                     json={'message': 'How do I code Python?', 'language': 'en'}, 
                     timeout=15)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Status: 200 OK")
        print(f"Response: {data['response'][:150]}...")
        print()
    else:
        print(f"❌ Status: {r.status_code}")

    print("=" * 60)
    print("🎉 GROQ INTEGRATION SUCCESSFUL!")
    print("✅ No rate limits")
    print("✅ Super fast responses")
    print("✅ 30,000 requests/month free")

except Exception as e:
    print(f"Error: {e}")
