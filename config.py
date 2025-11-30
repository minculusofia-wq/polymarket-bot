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
