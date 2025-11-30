import requests
import json

BASE_URL = "https://data-api.polymarket.com"

def get_leaderboard():
    print("\n--- Fetching Leaderboard ---")
    try:
        url = f"{BASE_URL}/v1/builders/leaderboard?timePeriod=ALL&limit=5"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def get_top_markets():
    print("\n--- Fetching Top Markets from DATA API ---")
    try:
        # Try Data API markets endpoint
        url = "https://data-api.polymarket.com/markets?limit=10&active=true&closed=false" 
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Data API usually returns a list directly or inside 'data'
            if isinstance(data, dict) and 'data' in data:
                data = data['data']
            
            if len(data) > 0:
                print(f"Found {len(data)} markets.")
                print("Market Keys:", list(data[0].keys()))
                print("First Market Sample:", json.dumps(data[0], indent=2))
                return data[0]['condition_id'] if 'condition_id' in data[0] else None
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
            # Fallback: Try /events which might contain volume
            print("Trying /events endpoint...")
            url = "https://data-api.polymarket.com/events?limit=5&active=true&closed=false"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    print("Event Keys:", list(data[0].keys()))
                    print("First Event Sample:", json.dumps(data[0], indent=2))
    except Exception as e:
        print(f"Exception: {e}")
    return None

def main():
    get_leaderboard()
    market_id = get_top_markets()
    
    if market_id:
        print(f"\n--- Fetching Holders for Event/Market {market_id} ---")
        # Note: /holders might need a market ID (condition ID) not event ID.
        # Let's try to see if we can find a condition ID from the event data first.
        pass

if __name__ == "__main__":
    main()
