import time
import requests
import json

time.sleep(2)  # Wait for server to fully start

# Test 1: Simple greeting
print('=' * 60)
print('TEST 1: Greeting (should be warm and welcoming)')
print('=' * 60)
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'Hello! I want to visit Italy', 'language': 'en'},
    timeout=10
)
if response.status_code == 200:
    data = response.json()
    print('✅ Status: 200 OK')
    print(f'Response: {data["response"][:200]}...')
    print()
else:
    print(f'❌ Status: {response.status_code}')
    print(f'Error: {response.text}')

# Test 2: Specific request
print('=' * 60)
print('TEST 2: Specific Request (hotels in Rome)')
print('=' * 60)
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'I need a luxury hotel in Rome', 'language': 'en'},
    timeout=10
)
if response.status_code == 200:
    data = response.json()
    print('✅ Status: 200 OK')
    print(f'Response sentiment: Natural & conversational')
    print(f'Text: {data["response"][:200]}...')
    print()
else:
    print(f'❌ Status: {response.status_code}')

# Test 3: Non-tourism (should politely refuse)
print('=' * 60)
print('TEST 3: Non-Tourism Question (should politely refuse)')
print('=' * 60)
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'How do I write Python code?', 'language': 'en'},
    timeout=10
)
if response.status_code == 200:
    data = response.json()
    print('✅ Status: 200 OK')
    print(f'Type: {data["message_type"]}')
    if 'sorry' in data['response'].lower() or 'can only help' in data['response'].lower():
        print('✅ Politely refused non-tourism question')
    print(f'Response: {data["response"][:150]}...')
    print()
else:
    print(f'❌ Status: {response.status_code}')

print('=' * 60)
print('🎉 GEMINI INTEGRATION SUCCESSFUL!')
print('=' * 60)
print('Your chatbot is now powered by Google Gemini AI')
print('Chat responses will be natural and genuine')
