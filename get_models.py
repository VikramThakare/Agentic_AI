import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

req = urllib.request.Request(
    'https://api.groq.com/openai/v1/models',
    headers={
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'curl/7.68.0'
    }
)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        for model in data.get("data", []):
            print(model.get("id"))
except Exception as e:
    print(f"Error: {e}")
