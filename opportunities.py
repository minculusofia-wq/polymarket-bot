import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Constants
GAMMA_API_URL = "https://gamma-api.polymarket.com"
DATA_API_URL = "https://data-api.polymarket.com"
OPPORTUNITIES_FILE = "opportunities.json"

# Keywords to monitor
KEYWORDS = {
    "crypto": ["bitcoin", "btc", "ethereum", "eth", "crypto", "binance", "coinbase"],
    "politics": ["trump", "biden", "election", "president", "congress", "senate"],
    "sports": ["nfl", "nba", "super bowl", "world cup", "champions league"],
    "tech": ["apple", "google", "meta", "tesla", "ai", "chatgpt"],
    "finance": ["fed", "interest rate", "stock market", "recession", "inflation"]
}

def get_trending_markets():
    """Get markets with high recent volume."""
    try:
        url = f"{GAMMA_API_URL}/markets?active=true&closed=false&limit=100"
        response = requests.get(url)
        if response.status_code == 200:
            markets = response.json()
            # Sort by volume
            trending = sorted(markets, key=lambda x: float(x.get('volume', 0)), reverse=True)[:10]
            return trending
        return []
    except Exception as e:
        print(f"Error fetching trending markets: {e}")
        return []

def detect_price_movements():
    """Detect significant price changes in last hour."""
    opportunities = []
    try:
        # Get recent trades
        url = f"{DATA_API_URL}/trades?limit=500"
        response = requests.get(url)
        if response.status_code != 200:
            return opportunities
            
        trades = response.json()
        
        # Group by market
        market_prices = defaultdict(list)
        for trade in trades:
            market_id = trade.get('conditionId')
            price = float(trade.get('price', 0))
            timestamp = trade.get('timestamp', 0)
            
            if market_id and price:
                market_prices[market_id].append({'price': price, 'time': timestamp})
        
        # Detect movements
        for market_id, prices in market_prices.items():
            if len(prices) < 5:
                continue
                
            prices.sort(key=lambda x: x['time'])
            first_price = prices[0]['price']
            last_price = prices[-1]['price']
            
            change = abs(last_price - first_price) / first_price if first_price > 0 else 0
            
            if change > 0.10:  # 10% movement
                opportunities.append({
                    "type": "price_movement",
                    "market_id": market_id,
                    "change": f"{change * 100:.1f}%",
                    "direction": "📈" if last_price > first_price else "📉",
                    "detected_at": datetime.now().isoformat()
                })
    except Exception as e:
        print(f"Error detecting price movements: {e}")
    
    return opportunities

def scan_keywords():
    """Scan markets for important keywords."""
    opportunities = []
    try:
        markets = get_trending_markets()
        
        for market in markets:
            question = market.get('question', '').lower()
            
            for category, keywords in KEYWORDS.items():
                for keyword in keywords:
                    if keyword in question:
                        opportunities.append({
                            "type": "keyword",
                            "category": category,
                            "keyword": keyword,
                            "question": market.get('question'),
                            "market_id": market.get('id'),
                            "volume": float(market.get('volume', 0)),
                            "detected_at": datetime.now().isoformat()
                        })
                        break  # Only one keyword per market
    except Exception as e:
        print(f"Error scanning keywords: {e}")
    
    return opportunities

def find_opportunities():
    """Main function to find all opportunities."""
    print("🔍 Scanning for opportunities...")
    
    opportunities = {
        "trending": get_trending_markets()[:5],
        "price_movements": detect_price_movements(),
        "keywords": scan_keywords()[:10],
        "last_update": datetime.now().isoformat()
    }
    
    # Save to file
    with open(OPPORTUNITIES_FILE, 'w') as f:
        json.dump(opportunities, f, indent=2)
    
    print(f"✅ Found {len(opportunities['price_movements'])} price movements")
    print(f"✅ Found {len(opportunities['keywords'])} keyword matches")
    
    return opportunities

if __name__ == "__main__":
    find_opportunities()
