import requests
import json

url = "https://data-api.polymarket.com/trades?limit=2"
response = requests.get(url)

if response.status_code == 200:
    trades = response.json()
    if trades and len(trades) > 0:
        print("First Trade Keys:", list(trades[0].keys()))
        print("\nFirst Trade Sample:")
        print(json.dumps(trades[0], indent=2))
else:
    print(f"Error: {response.status_code}")
