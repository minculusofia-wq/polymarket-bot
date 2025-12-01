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

import time
from whale_analyzer import WhaleAnalyzer
from trader import Trader
import config

# ... (Previous imports remain)

# Constants
DATA_API_URL = "https://data-api.polymarket.com"
WHALES_FILE = "whales.json"
MIN_VOLUME_THRESHOLD = 100
SCAN_INTERVAL = config.SCAN_INTERVAL

def load_whitelist():
    """Load whitelist from JSON file."""
    if os.path.exists("whitelist.json"):
        try:
            with open("whitelist.json", 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def main():
    print("--- Starting Polymarket Bot (Scanner + Trader) ---")
    analyzer = WhaleAnalyzer()
    trader = Trader()
    
    last_scan_time = time.time() - 3600 # Start by looking at last hour
    
    while True:
        try:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scanning market...")
            whitelist = load_whitelist()
            
            # 1. Get Recent Trades
            trades = get_recent_trades(limit=1000)
            
            if trades:
                current_scan_time = time.time()
                
                # 2. Aggregate & Analyze Whales (Background Task)
                trader_stats = aggregate_traders(trades)
                new_whales = filter_whales(trader_stats, min_volume=MIN_VOLUME_THRESHOLD)
                existing_whales = load_whales()
                merged_whales = merge_whale_data(existing_whales, new_whales)
                ranked_whales = analyzer.rank_whales(merged_whales)
                save_whales(ranked_whales)
                
                # 3. Check for Copy-Trade Opportunities
                # Filter for trades that happened AFTER the last scan
                # Note: API returns trades sorted by time desc
                
                print("Checking for copy-trade opportunities...")
                for trade in trades:
                    timestamp = trade.get('timestamp')
                    if not timestamp or timestamp <= last_scan_time:
                        continue
                        
                    address = trade.get('proxyWallet')
                    if not address:
                        continue
                        
                    # Check if address is a high-ranking whale OR whitelisted
                    whale_data = ranked_whales.get(address)
                    is_whitelisted = address in whitelist
                    
                    if is_whitelisted or (whale_data and whale_data.get('score', 0) >= config.MIN_WHALE_SCORE):
                        # Found a trade from a top whale or whitelisted wallet!
                        if is_whitelisted:
                            print(f"!!! WHITELISTED TRADER DETECTED: {address[:8]}...")
                        
                        market_id = trade.get('conditionId')
                        outcome = trade.get('outcome')
                        size = float(trade.get('size', 0))
                        price = float(trade.get('price', 0))
                        amount_usd = size * price
                        
                        print(f"!!! WHALE DETECTED: {address[:8]}... bought {amount_usd:.2f} of {outcome}")
                        
                        # Execute Copy Trade
                        trader.execute_copy_trade(address, market_id, outcome, amount_usd)
                
                last_scan_time = current_scan_time
            
            print(f"Waiting {SCAN_INTERVAL} seconds...")
            time.sleep(SCAN_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nStopping bot...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
def check_whale_exits(trader):
    """
    Check if followed whales have exited their positions.
    If AUTO_COPY_SELLS is True, liquidate corresponding positions.
    """
    import config
    
    # Check if feature is enabled (handle missing config safely)
    if not getattr(config, 'AUTO_COPY_SELLS', False):
        return

    open_positions = [p for pid, p in trader.positions.items() if p['status'] == 'OPEN' and p.get('whale')]
    
    if not open_positions:
        return

    print(f"Checking exits for {len(open_positions)} positions...")
    
    # Fetch recent trades to check for whale sells
    recent_trades = get_recent_trades(limit=500)
    
    for pid, position in trader.positions.items():
        if position['status'] != 'OPEN' or not position.get('whale'):
            continue
            
        whale_address = position['whale']
        market_id = position['market_id']
        outcome = position['outcome']
        
        # Look for SELL trades from this whale on this market
        whale_sells = [
            t for t in recent_trades 
            if t.get('proxyWallet') == whale_address 
            and t.get('conditionId') == market_id
            and t.get('side') == 'SELL'
            # Check timestamp to ensure it's a new trade (after our entry)
            # This is a simplified check; ideally compare timestamps properly
        ]
        
        if whale_sells:
            print(f"🚨 DETECTED WHALE EXIT: {whale_address} sold on {market_id}")
            trader.liquidate_position(pid, reason=f"Auto-Copy Sell (Whale {whale_address[:6]} exited)")
