import time
import requests
import json

time.sleep(2)

# Test 1: Just restaurants in Florence (not hotels + museums)
print("TEST 1: Restaurants only in Florence")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'can u recommend me some restaurants in firenze', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    types = [r['type'] for r in data['recommendations']]
    print(f"  Got {len(data['recommendations'])} recommendations")
    print(f"  Types found: {set(types)}")
    if set(types) == {'restaurant'}:
        print("  ✓ PASS: Only restaurants!")
    else:
        print("  ✗ FAIL: Got mixed types")
    print()

# Test 2: Budget restaurants
print("TEST 2: Budget restaurants in Florence")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'budget restaurants in firenze', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    print(f"  Budget filter: {data.get('budget', 'N/A')}")
    print(f"  Got {len(data['recommendations'])} recommendations")
    for r in data['recommendations'][:2]:
        print(f"    - {r['name']}: {r['details']}")
    if data.get('budget') == 'budget':
        print("  ✓ PASS: Budget detected!")
    print()

# Test 3: Luxury restaurants (should get fewer if truly filtering)
print("TEST 3: Luxury restaurants in Florence")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': '5-star luxury fine dining restaurants in firenze', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    print(f"  Budget filter: {data.get('budget', 'N/A')}")
    print(f"  Got {len(data['recommendations'])} recommendations")
    for r in data['recommendations'][:2]:
        print(f"    - {r['name']}: {r['details']}")
    if data.get('budget') == 'luxury':
        print("  ✓ PASS: Luxury detected!")
    print()

# Test 4: More than 2 items
print("TEST 4: Check number of items returned (should be more than 2)")
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'show me hotels in rome', 'language': 'en'},
    timeout=5
)
if response.status_code == 200:
    data = response.json()
    num = len(data['recommendations'])
    print(f"  Got {num} recommendations")
    if num > 2:
        print(f"  ✓ PASS: More than 2! ({num})")
    else:
        print(f"  ✗ FAIL: Still only {num}")
