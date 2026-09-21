# backend/app/routers/history.py

from fastapi import APIRouter, Query
from typing import List, Dict, Any

from app.services.data_service import get_historical_candles
from app.utils.validators import validate_symbol

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/{symbol}")
def get_history(
    symbol: str,
    interval: str = Query("1h", description="Candle interval: 1m, 5m, 15m, 1h, 1d"),
    limit: int = Query(200, ge=10, le=1000, description="Number of candles")
) -> List[Dict[str, Any]]:
    """
    Return historical candlestick data for a symbol.
    Data is fetched from Yahoo Finance via yfinance.
    """
    symbol = validate_symbol(symbol)
    
    allowed_intervals = {"1m", "5m", "15m", "1h", "1d"}
    if interval not in allowed_intervals:
        interval = "1h"
    
    candles = get_historical_candles(symbol=symbol, interval=interval, limit=limit)
    return candles