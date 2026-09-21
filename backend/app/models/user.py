# backend/app/models/user.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.database import Base
from app.config import STARTING_BALANCE


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Paper trading balance
    balance = Column(Float, default=STARTING_BALANCE, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())