# backend/app/routers/trades.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.trade import (
    BuyOrderRequest,
    SellOrderRequest,
    OrderResponse,
    PortfolioResponse,
    PositionResponse
)
from app.services.auth_service import get_current_user
from app.services.paper_broker import PaperBroker
from app.services.ws_manager import manager  # to get latest price

router = APIRouter(prefix="/api/trades", tags=["trades"])


def _get_latest_price(symbol: str) -> float:
    """Get the most recent price from the WebSocket cache."""
    price = manager.latest_prices.get(symbol.upper())
    if price is None or price <= 0:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No live price available for {symbol}. Try again in a moment."
        )
    return price


@router.post("/buy", response_model=OrderResponse)
def buy(
    data: BuyOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Place a paper BUY order at the current live price.
    """
    price = _get_latest_price(data.symbol)
    broker = PaperBroker(db, current_user)
    order = broker.buy(data.symbol, data.quantity, price)
    
    return OrderResponse(
        id=order.id,
        symbol=order.symbol,
        side=order.side.value,
        quantity=order.quantity,
        price=order.price,
        pnl=order.pnl,
        created_at=order.created_at
    )


@router.post("/sell", response_model=OrderResponse)
def sell(
    data: SellOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Place a paper SELL order at the current live price.
    """
    price = _get_latest_price(data.symbol)
    broker = PaperBroker(db, current_user)
    order = broker.sell(data.symbol, data.quantity, price)
    
    return OrderResponse(
        id=order.id,
        symbol=order.symbol,
        side=order.side.value,
        quantity=order.quantity,
        price=order.price,
        pnl=order.pnl,
        created_at=order.created_at
    )


@router.get("/portfolio", response_model=PortfolioResponse)
def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Return current balance, open positions and recent orders.
    """
    broker = PaperBroker(db, current_user)
    data = broker.get_portfolio()
    
    return PortfolioResponse(
        balance=data["balance"],
        positions=[
            PositionResponse(
                id=p.id,
                symbol=p.symbol,
                quantity=p.quantity,
                average_price=p.average_price
            ) for p in data["positions"]
        ],
        recent_orders=[
            OrderResponse(
                id=o.id,
                symbol=o.symbol,
                side=o.side.value,
                quantity=o.quantity,
                price=o.price,
                pnl=o.pnl,
                created_at=o.created_at
            ) for o in data["recent_orders"]
        ]
    )