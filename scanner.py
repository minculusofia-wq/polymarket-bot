import requests
import json
import os
from datetime import datetime
from collections import defaultdict

# Constants
DATA_API_URL = "https://data-api.polymarket.com"
WHALES_FILE = "whales.json"
MIN_VOLUME_THRESHOLD = 100  # Minimum USD volume to be considered a "whale"

def get_recent_trades(limit=1000):
    """Fetch recent trades from Data API."""
    print(f"Fetching {limit} recent trades...")
    try:
        url = f"{DATA_API_URL}/trades?limit={limit}"
        response = requests.get(url)
        if response.status_code == 200:
            trades = response.json()
            print(f"Retrieved {len(trades)} trades")
            return trades
        else:
            print(f"Error fetching trades: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception fetching trades: {e}")
        return []

def aggregate_traders(trades):
    """Aggregate trades by wallet address to identify whales."""
    print("Analyzing trades...")
    
    trader_stats = defaultdict(lambda: {
        "total_volume": 0.0,
        "trade_count": 0,
        "markets": set(),
        "first_seen": None,
        "last_trade": None
    })
    
    for trade in trades:
        # Get trader address
        address = trade.get('proxyWallet')
        
        if not address:
            continue
        
        # Get trade details
        market_id = trade.get('conditionId')
        # Volume in USD (price * size)
        price = float(trade.get('price', 0))
        size = float(trade.get('size', 0))
        volume = price * size
        
        timestamp = trade.get('timestamp')
        
        # Update trader stats
        trader_stats[address]["total_volume"] += volume
        trader_stats[address]["trade_count"] += 1
        if market_id:
            trader_stats[address]["markets"].add(market_id)
        if timestamp:
            trader_stats[address]["last_trade"] = timestamp
            if not trader_stats[address]["first_seen"]:
                trader_stats[address]["first_seen"] = timestamp
    
    # Convert sets to lists for JSON serialization
    for address in trader_stats:
        trader_stats[address]["markets"] = list(trader_stats[address]["markets"])
    
    return dict(trader_stats)

def filter_whales(trader_stats, min_volume=MIN_VOLUME_THRESHOLD):
    """Filter traders to identify whales based on volume threshold."""
    whales = {
        address: stats 
        for address, stats in trader_stats.items() 
        if stats["total_volume"] >= min_volume
    }
    
    # Sort by volume
    whales = dict(sorted(whales.items(), key=lambda x: x[1]["total_volume"], reverse=True))
    
    return whales

def load_whales():
    """Load existing whale data if available."""
    if os.path.exists(WHALES_FILE):
        try:
            with open(WHALES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def merge_whale_data(existing, new_whales):
    """Merge new whale data with existing data."""
    for address, stats in new_whales.items():
        if address in existing:
            # Update existing whale
            existing[address]["total_volume"] = stats["total_volume"]
            existing[address]["trade_count"] = stats["trade_count"]
            existing[address]["last_trade"] = stats["last_trade"]
            # Merge markets
            existing_markets = set(existing[address].get("markets", []))
            new_markets = set(stats["markets"])
            existing[address]["markets"] = list(existing_markets | new_markets)
        else:
            # Add new whale
            existing[address] = stats
    
    return existing

def save_whales(whales_data):
    """Save whale data to JSON file."""
    with open(WHALES_FILE, 'w') as f:
        json.dump(whales_data, f, indent=2)
    print(f"Saved {len(whales_data)} wallets to {WHALES_FILE}")

def main():
    print("--- Starting Whale Scanner (Trades-Based) ---")
    
    # 1. Get Recent Trades
    trades = get_recent_trades(limit=1000)
    
    if not trades:
        print("No trades retrieved. Exiting.")
        return
    
    # 2. Aggregate by Trader
    trader_stats = aggregate_traders(trades)
    print(f"Analyzed {len(trader_stats)} unique traders")
    
    # 3. Filter for Whales
    new_whales = filter_whales(trader_stats, min_volume=MIN_VOLUME_THRESHOLD)
    print(f"Identified {len(new_whales)} whales (volume >= ${MIN_VOLUME_THRESHOLD})")
    
    # 4. Merge with Existing Data
    existing_whales = load_whales()
    merged_whales = merge_whale_data(existing_whales, new_whales)
    
    # 5. Save Results
    save_whales(merged_whales)
    
    # 6. Print Top 5 Whales
    print("\n--- Top 5 Whales by Volume ---")
    for i, (address, stats) in enumerate(list(merged_whales.items())[:5], 1):
        print(f"{i}. {address[:10]}... - ${stats['total_volume']:.2f} ({stats['trade_count']} trades)")
    
    print("\n--- Scan Complete ---")

if __name__ == "__main__":
    main()
