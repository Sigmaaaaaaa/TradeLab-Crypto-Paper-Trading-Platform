# backend/app/utils/validators.py

from fastapi import HTTPException, status

from app.config import ALLOWED_SYMBOLS


def validate_symbol(symbol: str) -> str:
    """
    Normalize and validate a trading symbol.
    - Converts to uppercase
    - Checks against ALLOWED_SYMBOLS
    """
    if not symbol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Symbol is required"
        )
    
    symbol = symbol.strip().upper()
    
    if symbol not in ALLOWED_SYMBOLS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol '{symbol}' is not supported. Allowed: {', '.join(ALLOWED_SYMBOLS)}"
        )
    
    return symbol