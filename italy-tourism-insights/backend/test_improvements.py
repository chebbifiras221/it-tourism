import time
import requests
import json

time.sleep(2)

print("=" * 60)
print("STRICT INTENT MATCHING TESTS")
print("=" * 60)

# Test 1: ONLY restaurants
print("\n1. RESTAURANTS ONLY (should get only 🍝, not 🏨 or 🏛️)")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'recommend restaurants in rome', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    types = [r['type'] for r in data['recommendations']]
    print(f"   Types: {set(types)}")
    print(f"   Count: {len(data['recommendations'])}")
    if set(types) == {'restaurant'}:
        print("   ✅ PASS - Only restaurants!")
    else:
        print("   ❌ FAIL - Mixed types")
        for r in data['recommendations']:
            print(f"      - {r['type']}: {r['name']}")

# Test 2: ONLY hotels
print("\n2. HOTELS ONLY (should get only 🏨, not 🍝 or 🏛️)")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'where to stay in venice', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    types = [r['type'] for r in data['recommendations']]
    print(f"   Types: {set(types)}")
    print(f"   Count: {len(data['recommendations'])}")
    if set(types) == {'hotel'}:
        print("   ✅ PASS - Only hotels!")
    else:
        print("   ❌ FAIL - Mixed types")

# Test 3: ONLY museums/culture
print("\n3. MUSEUMS ONLY (should get only 🏛️, not 🍝 or 🏨)")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'what museums in florence', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    types = [r['type'] for r in data['recommendations']]
    print(f"   Types: {set(types)}")
    print(f"   Count: {len(data['recommendations'])}")
    if set(types) == {'culture'}:
        print("   ✅ PASS - Only museums!")
    else:
        print("   ❌ FAIL - Mixed types")

print("\n" + "=" * 60)
print("NON-TOURISM FILTERING TESTS")
print("=" * 60)

# Test 4: Tech topic (should reject)
print("\n4. NON-TOURISM: Programming question")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'how to write python code', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    msg_type = data.get('message_type', 'unknown')
    print(f"   Response type: {msg_type}")
    print(f"   Message: {data['response'][:80]}...")
    if msg_type == 'rejection':
        print("   ✅ PASS - Rejected!")
    else:
        print("   ❌ FAIL - Should reject")

# Test 5: Personal topic (should reject)
print("\n5. NON-TOURISM: Personal question")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'my relationship is broken', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    msg_type = data.get('message_type', 'unknown')
    print(f"   Response type: {msg_type}")
    if msg_type == 'rejection':
        print("   ✅ PASS - Rejected!")
    else:
        print("   ❌ FAIL - Should reject")

# Test 6: Sports topic (should reject)
print("\n6. NON-TOURISM: Sports question")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'who won the football match', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    msg_type = data.get('message_type', 'unknown')
    print(f"   Response type: {msg_type}")
    if msg_type == 'rejection':
        print("   ✅ PASS - Rejected!")
    else:
        print("   ❌ FAIL - Should reject")

# Test 7: Tourism-related should accept
print("\n7. TOURISM: Valid question")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'best hotels in naples', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    msg_type = data.get('message_type', 'unknown')
    print(f"   Response type: {msg_type}")
    print(f"   Got {len(data['recommendations'])} recommendations")
    if msg_type != 'rejection' and len(data['recommendations']) > 0:
        print("   ✅ PASS - Accepted tourism question!")
    else:
        print("   ❌ FAIL - Should accept tourism")

print("\n" + "=" * 60)
