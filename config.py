import os
from dotenv import load_dotenv

load_dotenv()

# Network Configuration
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Polymarket API
CLOB_API_URL = "https://clob.polymarket.com"
DATA_API_URL = "https://data-api.polymarket.com"
GAMMA_API_URL = "https://gamma-api.polymarket.com"

# Trading Settings
PAPER_TRADING = True  # Set to False for real trading
MAX_POSITION_SIZE_USD = 10.0  # Max amount per trade
STOP_LOSS_PERCENT = 0.15  # 15% stop loss
TAKE_PROFIT_PERCENT = 0.30  # 30% take profit
MAX_OPEN_POSITIONS = 5
DAILY_LOSS_LIMIT_USD = 50.0

# Whale Selection
MIN_WHALE_SCORE = 60
MIN_WHALE_WIN_RATE = 0.55  # Not yet implemented in analyzer, placeholder
FOLLOW_TAGS = ["Mega Whale", "High Frequency"]
IGNORE_TAGS = ["Sniper"]  # Snipers might be too fast to copy

# System
SCAN_INTERVAL = 60
LOG_LEVEL = "INFO"

# External Data Sources (Option A)
NEWS_API_KEY = "2c1f916ed0da45749065edd092d08f80"
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "polymarket-bot:v1.0 (by /u/yourusername)"

# Advanced APIs
LUNARCRUSH_API_KEY = "tlqgx82dyber5ffbhijwvdqb7omimu20mdxov5ela"
SERPAPI_KEY = "fee7d2335de3adba052c9afc8fde3de15140305606c43ccf62e302798ae931c5"
HELIUS_API_KEY = "be5c8bc3-cb64-4141-b691-8ee754b2d3e4"

# Convergent Signals
MIN_WHALES_FOR_SIGNAL = 2
MIN_SOURCES_FOR_SIGNAL = 1
