from dotenv import load_dotenv
load_dotenv()

from chatbot import recommender
import json

result = recommender.chat('I need a luxury hotel in Rome')
print('Response snippet:')
print(result['response'][:800])
print('\n' + '='*60)
print('Parsed recommendations:')
for rec in result['recommendations']:
    print(f"\n{rec['icon']} {rec['name']}")
    if rec['link']:
        print(f"  Link: {rec['link']}")
    if rec['details']:
        print(f"  Details: {rec['details']}")
