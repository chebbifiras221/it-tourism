#!/usr/bin/env python3
import requests
import time

time.sleep(2)

try:
    r = requests.post('http://localhost:8000/api/chat', json={'message': 'hotel in rome', 'language': 'en'}, timeout=15)
    print('Status:', r.status_code)
    data = r.json()
    print('\nResponse:')
    print(data['response'][:300])
    print('\nRecommendations count:', len(data.get('recommendations', [])))
    if data.get('recommendations'):
        for rec in data['recommendations']:
            print(f"  {rec['icon']} {rec['name']}")
            if rec.get('link'):
                print(f"    Link: {rec['link']}")
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to backend on port 8000")
except Exception as e:
    print(f"ERROR: {e}")
