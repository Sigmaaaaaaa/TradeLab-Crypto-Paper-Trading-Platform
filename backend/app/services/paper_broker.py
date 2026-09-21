# backend/app/services/paper_broker.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.trade import Order, Position, OrderSide
from app.utils.validators import validate_symbol


class PaperBroker:
    """
    Simple paper trading engine.
    - BUY  → deduct cash, update (or create) position with weighted average price
    - SELL → add cash, reduce position, calculate realized P&L
    """

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def _get_or_create_position(self, symbol: str) -> Position:
        position = (
            self.db.query(Position)
            .filter(Position.user_id == self.user.id, Position.symbol == symbol)
            .first()
        )
        if not position:
            position = Position(
                user_id=self.user.id,
                symbol=symbol,
                quantity=0.0,
                average_price=0.0
            )
            self.db.add(position)
            self.db.flush()
        return position

    def buy(self, symbol: str, quantity: float, price: float) -> Order:
        symbol = validate_symbol(symbol)
        
        if quantity <= 0 or price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity and price must be positive"
            )
        
        cost = quantity * price
        
        if self.user.balance < cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient balance. Need {cost:.2f}, have {self.user.balance:.2f}"
            )
        
        # Update balance
        self.user.balance -= cost
        
        # Update position (weighted average)
        position = self._get_or_create_position(symbol)
        
        total_qty = position.quantity + quantity
        if total_qty > 0:
            # new average = (old_qty * old_avg + new_qty * new_price) / total_qty
            position.average_price = (
                (position.quantity * position.average_price) + (quantity * price)
            ) / total_qty
        position.quantity = total_qty
        
        # Record the order
        order = Order(
            user_id=self.user.id,
            symbol=symbol,
            side=OrderSide.BUY,
            quantity=quantity,
            price=price,
            pnl=0.0
        )
        self.db.add(order)
        
        self.db.commit()
        self.db.refresh(order)
        self.db.refresh(self.user)
        self.db.refresh(position)
        
        return order

    def sell(self, symbol: str, quantity: float, price: float) -> Order:
        symbol = validate_symbol(symbol)
        
        if quantity <= 0 or price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity and price must be positive"
            )
        
        position = (
            self.db.query(Position)
            .filter(Position.user_id == self.user.id, Position.symbol == symbol)
            .first()
        )
        
        if not position or position.quantity < quantity:
            available = position.quantity if position else 0.0
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough quantity to sell. Available: {available}"
            )
        
        # Calculate realized P&L
        pnl = (price - position.average_price) * quantity
        
        # Update balance
        proceeds = quantity * price
        self.user.balance += proceeds
        
        # Update position
        position.quantity -= quantity
        if position.quantity == 0:
            position.average_price = 0.0
        
        # Record the order
        order = Order(
            user_id=self.user.id,
            symbol=symbol,
            side=OrderSide.SELL,
            quantity=quantity,
            price=price,
            pnl=pnl
        )
        self.db.add(order)
        
        self.db.commit()
        self.db.refresh(order)
        self.db.refresh(self.user)
        self.db.refresh(position)
        
        return order

    def get_portfolio(self):
        """Return current balance + open positions + recent orders."""
        positions = (
            self.db.query(Position)
            .filter(Position.user_id == self.user.id, Position.quantity > 0)
            .all()
        )
        
        recent_orders = (
            self.db.query(Order)
            .filter(Order.user_id == self.user.id)
            .order_by(Order.created_at.desc())
            .limit(20)
            .all()
        )
        
        return {
            "balance": self.user.balance,
            "positions": positions,
            "recent_orders": recent_orders
        }