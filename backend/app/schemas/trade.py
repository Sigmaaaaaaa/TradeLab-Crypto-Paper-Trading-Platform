# backend/app/schemas/trade.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class BuyOrderRequest(BaseModel):
    symbol: str
    quantity: float = Field(..., gt=0)


class SellOrderRequest(BaseModel):
    symbol: str
    quantity: float = Field(..., gt=0)


class OrderResponse(BaseModel):
    id: int
    symbol: str
    side: str
    quantity: float
    price: float
    pnl: float
    created_at: datetime

    class Config:
        from_attributes = True


class PositionResponse(BaseModel):
    id: int
    symbol: str
    quantity: float
    average_price: float
    # unrealized_pnl will be calculated on the fly by the frontend
    # using the latest LTP from WebSocket

    class Config:
        from_attributes = True


class PortfolioResponse(BaseModel):
    balance: float
    positions: List[PositionResponse]
    recent_orders: List[OrderResponse]