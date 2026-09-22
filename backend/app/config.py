# backend/app/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the backend
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "app.db"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
# Supabase may provide the legacy postgres:// prefix.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Paper trading starting balance (in INR)
STARTING_BALANCE = 100000.0

# Coinbase Exchange public market-data WebSocket.
COINBASE_WS_URL = "wss://ws-feed.exchange.coinbase.com"

# Application symbols mapped to Coinbase product IDs. Symbols remain in the
# BTCUSDT format throughout the API and frontend.
COINBASE_PRODUCTS = {
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "SOLUSDT": "SOL-USD",
    "XRPUSDT": "XRP-USD",
    "ADAUSDT": "ADA-USD",
    "DOGEUSDT": "DOGE-USD",
    "AVAXUSDT": "AVAX-USD",
    "DOTUSDT": "DOT-USD",
    "LINKUSDT": "LINK-USD",
    "MATICUSDT": "MATIC-USD",
    "LTCUSDT": "LTC-USD",
    "UNIUSDT": "UNI-USD",
    "ATOMUSDT": "ATOM-USD",
    "NEARUSDT": "NEAR-USD",
}

# Allowed crypto pairs (for search + live data)
ALLOWED_SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "DOTUSDT",
    "LINKUSDT",
    "MATICUSDT",
    "LTCUSDT",
    "UNIUSDT",
    "ATOMUSDT",
    "NEARUSDT",
]