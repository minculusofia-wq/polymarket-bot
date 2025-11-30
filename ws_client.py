import asyncio
import websockets
import json
import time
import ssl
import certifi

class PolymarketWS:
    def __init__(self, on_message_callback):
        self.uri = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
        self.on_message_callback = on_message_callback
        self.running = False
        
        # Create SSL context that works on Mac
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        # If that fails, we can try:
        # self.ssl_context = ssl._create_unverified_context()

    async def connect(self):
        self.running = True
        while self.running:
            try:
                print(f"Connecting to WebSocket: {self.uri}")
                async with websockets.connect(self.uri, ssl=self.ssl_context) as websocket:
                    print("Connected to Polymarket WebSocket")
                    
                    # Subscribe to trades (for all markets - wildcard not supported directly, 
                    # so we might need to subscribe to specific assets or use a firehose if available.
                    # Polymarket CLOB WS documentation says we need to subscribe to specific assets.
                    # However, for a general scanner, we want EVERYTHING.
                    # If firehose isn't available, we might need to stick to polling for discovery 
                    # and WS for specific tracking. 
                    # Let's check if there's a way to get all trades.
                    # Documentation suggests subscribing to specific assets.
                    # WORKAROUND: For this implementation, we will subscribe to the top markets found by the scanner.
                    
                    # Actually, let's try to subscribe to a known active market to test.
                    # In a real production bot, we would dynamically manage subscriptions.
                    
                    # Payload for subscription (Example)
                    # {
                    #     "assets_ids": ["..."],
                    #     "type": "market"
                    # }
                    
                    # Since we can't easily subscribe to ALL markets, we will implement a hybrid approach:
                    # 1. Polling scanner finds active markets.
                    # 2. WS Client subscribes to those markets for real-time updates.
                    
                    # For now, let's just keep the connection alive and handle messages.
                    # We will need the scanner to pass asset IDs to subscribe to.
                    
                    await self.listen(websocket)
            except Exception as e:
                print(f"WebSocket connection error: {e}")
                await asyncio.sleep(5)

    async def subscribe(self, websocket, asset_ids):
        if not asset_ids:
            return
            
        payload = {
            "assets_ids": asset_ids,
            "type": "market"
        }
        await websocket.send(json.dumps(payload))
        print(f"Subscribed to {len(asset_ids)} assets")

    async def listen(self, websocket):
        async for message in websocket:
            try:
                data = json.loads(message)
                # Process message
                if self.on_message_callback:
                    await self.on_message_callback(data)
            except Exception as e:
                print(f"Error processing message: {e}")

    def start(self):
        asyncio.run(self.connect())
