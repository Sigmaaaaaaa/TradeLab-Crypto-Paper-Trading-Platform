# backend/app/routers/symbols.py

from fastapi import APIRouter, Query
from typing import List

from app.services.data_service import search_symbols

router = APIRouter(prefix="/api/symbols", tags=["symbols"])


@router.get("", response_model=List[str])
def search(q: str = Query("", description="Search query, e.g. BTC or ETH")):
    """
    Search for trading pairs.
    Returns a list of matching symbols from the allowed list.
    """
    return search_symbols(q)