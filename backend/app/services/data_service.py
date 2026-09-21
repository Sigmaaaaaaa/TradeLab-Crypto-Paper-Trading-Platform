# backend/app/services/data_service.py

from typing import List, Dict, Any
import yfinance as yf
from datetime import datetime, timedelta

from app.config import ALLOWED_SYMBOLS
from app.utils.validators import validate_symbol


# Map our symbols to yfinance tickers
# Binance pairs → Yahoo Finance crypto tickers
YFINANCE_MAP = {
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "BNBUSDT": "BNB-USD",
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


def search_symbols(query: str) -> List[str]:
    """
    Simple search: return symbols that contain the query (case-insensitive).
    """
    if not query:
        return ALLOWED_SYMBOLS[:10]  # return first 10 if empty
    
    q = query.strip().upper()
    results = [s for s in ALLOWED_SYMBOLS if q in s]
    return results


def get_historical_candles(
    symbol: str,
    interval: str = "1h",
    limit: int = 200
) -> List[Dict[str, Any]]:
    """
    Fetch historical OHLCV candles using yfinance.
    
    Supported intervals: 1m, 5m, 15m, 1h, 1d
    Returns list of dicts ready for lightweight-charts:
    [
      { "time": 1690000000, "open": 25000, "high": 25500, "low": 24800, "close": 25200 },
      ...
    ]
    """
    symbol = validate_symbol(symbol)
    
    yf_symbol = YFINANCE_MAP.get(symbol)
    if not yf_symbol:
        return []
    
    # Map our interval to yfinance interval + period
    interval_map = {
        "1m":  ("1m",  "1d"),
        "5m":  ("5m",  "5d"),
        "15m": ("15m", "5d"),
        "1h":  ("1h",  "1mo"),
        "1d":  ("1d",  "1y"),
    }
    
    yf_interval, period = interval_map.get(interval, ("1h", "1mo"))
    
    try:
        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(period=period, interval=yf_interval)
        
        if df.empty:
            return []
        
        # Keep only the last `limit` candles
        df = df.tail(limit)
        
        candles = []
        for index, row in df.iterrows():
            # lightweight-charts expects Unix timestamp (seconds)
            timestamp = int(index.timestamp())
            candles.append({
                "time": timestamp,
                "open": round(float(row["Open"]), 4),
                "high": round(float(row["High"]), 4),
                "low": round(float(row["Low"]), 4),
                "close": round(float(row["Close"]), 4),
            })
        
        return candles
    
    except Exception as e:
        print(f"[data_service] Error fetching history for {symbol}: {e}")
        return []