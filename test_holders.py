import requests
import json

# Token ID from Gamma Events
token_id = "60487116984468020978247225474488676749601001829886755968952521846780452448915"

url = f"https://data-api.polymarket.com/holders?market={token_id}"
print(f"Testing: {url}")

response = requests.get(url)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Response Type: {type(data)}")
    print(f"Length: {len(data) if isinstance(data, list) else 'N/A'}")
    if data:
        print(json.dumps(data[:2] if isinstance(data, list) else data, indent=2))
else:
    print(f"Error: {response.text}")
