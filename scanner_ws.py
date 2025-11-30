import asyncio
import json
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
analyzer = WhaleAnalyzer()
trader = Trader()

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

async def main():
    print("--- Starting Real-Time Scanner (WebSocket) ---")
    
    # Initialize WS
    ws = PolymarketWS(on_trade_message)
    
    # Start WS loop
    await ws.connect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
