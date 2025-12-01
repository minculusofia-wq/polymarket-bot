import asyncio
import json
import os
import time
from datetime import datetime
from ws_client import PolymarketWS
from scanner import get_recent_trades, aggregate_traders, filter_whales, load_whales, merge_whale_data, save_whales
from whale_analyzer import WhaleAnalyzer
from trader import Trader
import config

# Global state
active_assets = []
whales_cache = {}
whitelist_cache = set()
active_traders_cache = {}
analyzer = WhaleAnalyzer()
trader = Trader()

def load_whitelist():
    """Load whitelist from JSON file."""
    if os.path.exists("whitelist.json"):
        try:
            with open("whitelist.json", 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def load_active_traders():
    """Load active traders state from JSON file."""
    if os.path.exists("active_traders.json"):
        try:
            with open("active_traders.json", 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def is_trader_active(address):
    """Check if a trader is both whitelisted AND active."""
    global whitelist_cache, active_traders_cache
    
    # Must be in whitelist
    if address not in whitelist_cache:
        return False
    
    # Check active state (default to True if not set)
    return active_traders_cache.get(address, True)

async def on_trade_message(data):
    """Handle incoming WebSocket messages."""
    if isinstance(data, list):
        for item in data:
            process_trade_event(item)
    else:
        process_trade_event(data)

def process_trade_event(event):
    """Process a single trade event."""
    if event.get('event_type') != 'last_trade_price':
        return

    # Check if trader is whitelisted or a whale
    # Note: WS trade messages don't always contain the maker/taker address directly in the public feed.
    # The public 'last_trade_price' event usually only has price, size, side, asset_id.
    # To copy trade via WS, we need the maker/taker address, which might require a different subscription or API call.
    # However, assuming we CAN get the address (e.g. from a different message type or enriched data):
    
    # For this implementation, we'll simulate address check if available, 
    # but acknowledge limitation of public WS feed for copy-trading specific wallets without extra data.
    
    # If we are just scanning for high volume, we continue as is.
    # If we want to copy specific wallets, we might need to poll /trades endpoint rapidly or use a private feed if available.
    
    # Let's refresh whitelist and active traders periodically
    global whitelist_cache, active_traders_cache
    if int(time.time()) % 60 == 0:
        whitelist_cache = load_whitelist()
        active_traders_cache = load_active_traders()

    asset_id = event.get('asset_id')
    price = float(event.get('price', 0))
    size = float(event.get('size', 0))
    
    volume = price * size
    if volume > 1000: # Significant trade
        print(f"!!! HIGH VOLUME DETECTED via WS: ${volume:.2f} on {asset_id}")

async def update_subscriptions(ws_client):
    """Periodically update market subscriptions."""
    # Since we don't have get_active_markets, we can't easily subscribe to specific assets yet.
    # For this demo, we will rely on the fact that we might need to implement get_active_markets
    # or just skip subscription updates if we can't get the list.
    # Let's verify if we can get active markets from Gamma API directly here.
    pass

from opportunities import find_opportunities

# ... (existing imports)

async def run_opportunities_scanner():
    """Run opportunities scanner periodically."""
    from opportunities import find_opportunities
    from convergent_signals import analyze_convergence, save_signals
    import config
    
    while True:
        try:
            print("🔍 Scanning opportunities...")
            find_opportunities()
            
            print("🎯 Analyzing convergent signals...")
            # Use 0 thresholds to capture ALL signals, allowing frontend to filter
            signals = analyze_convergence(
                min_whales=0,
                min_sources=0
            )
            save_signals(signals)
            print(f"✅ Found {len(signals)} convergent signals")
            
            # Auto-Copy Sells Check
            from scanner import check_whale_exits
            from scanner_ws import trader # Import the global trader instance
            check_whale_exits(trader)
            
        except Exception as e:
            print(f"Error in opportunities scanner: {e}")
        
        await asyncio.sleep(60)  # Run every 60 seconds

async def main():
    print("--- Starting Real-Time Scanner (WebSocket) ---")
    
    # Initialize WS
    ws = PolymarketWS(on_trade_message)
    
    # Start background tasks
    asyncio.create_task(run_opportunities_scanner())
    
    # Start WS loop
    await ws.connect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
