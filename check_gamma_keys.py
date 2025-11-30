import requests
import json

def main():
    url = "https://gamma-api.polymarket.com/events?limit=1&active=true&closed=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            event = data[0]
            print("Event Keys:", list(event.keys()))
            markets = event.get('markets', [])
            if len(markets) > 0:
                market = markets[0]
                print("Nested Market Keys:", list(market.keys()))
                print(f"Nested Condition ID: {market.get('conditionId')}")
                print(f"Nested CLOB Token IDs: {market.get('clobTokenIds')}")
                print(f"Nested Tokens: {market.get('tokens')}")
            else:
                print("No markets in event")
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    main()
