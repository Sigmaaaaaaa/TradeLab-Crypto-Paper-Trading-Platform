# backend/app/schemas/watchlist.py

from pydantic import BaseModel
from typing import List


class WatchlistItemCreate(BaseModel):
    symbol: str


class WatchlistItemResponse(BaseModel):
    id: int
    symbol: str
    # live price will be filled by frontend via WebSocket
    # we keep the schema simple

    class Config:
        from_attributes = True


class WatchlistResponse(BaseModel):
    items: List[WatchlistItemResponse]