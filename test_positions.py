import requests
import json

DATA_API_URL = "https://data-api.polymarket.com"

def get_positions(user_address):
    print(f"--- Fetching Positions for {user_address} ---")
    try:
        url = f"{DATA_API_URL}/positions?user={user_address}&limit=5"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def main():
    # Example address from leaderboard research (standtrade)
    # We don't have the address, just the name "standtrade". 
    # But the leaderboard response might have had an address or profileID?
    # Let's check the leaderboard response structure again from previous step.
    # It had "builder": "standtrade", no address visible in the snippet I saw.
    # Wait, the /holders endpoint returned "proxyWallet".
    
    # Let's try to find a real address.
    # I'll use a known Polymarket contract or try to search for a user.
    # Or I can try to fetch the leaderboard again and see if I missed a field.
    
    # For now, let's try to fetch leaderboard again and print FULL object.
    url = f"{DATA_API_URL}/v1/builders/leaderboard?timePeriod=ALL&limit=1"
    resp = requests.get(url)
    if resp.status_code == 200:
        item = resp.json()[0]
        print("Leaderboard Item:", json.dumps(item, indent=2))
        # If no address, this approach is blocked unless we can resolve name -> address.
        
    # Alternative: Use the /holders endpoint on a VERY active market to get a real address.
    # I need a real active market ID.
    # Let's try to get a market with high volume from CLOB.
    
    pass

if __name__ == "__main__":
    main()
