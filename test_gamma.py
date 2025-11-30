import requests
import json

def main():
    print("--- Testing Gamma API ---")
    try:
        # Gamma API events
        url = "https://gamma-api.polymarket.com/events?limit=5&active=true&closed=false"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Gamma Events: {len(data)}")
            if len(data) > 0:
                print(json.dumps(data[0], indent=2))
        else:
            print(f"Gamma Events Error: {response.status_code}")

        # Gamma API markets
        url = "https://gamma-api.polymarket.com/markets?limit=5&active=true&closed=false"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Gamma Markets: {len(data)}")
            if len(data) > 0:
                print(json.dumps(data[0], indent=2))
        else:
            print(f"Gamma Markets Error: {response.status_code}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
