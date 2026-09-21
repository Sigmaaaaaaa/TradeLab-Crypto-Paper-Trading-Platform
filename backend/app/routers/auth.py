# backend/app/routers/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_token_for_user,
    get_current_user
)
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user and return JWT + user info.
    """
    user = register_user(db, data)
    token = create_token_for_user(user)
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            balance=user.balance
        )
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email + password and return JWT + user info.
    """
    user = authenticate_user(db, data)
    token = create_token_for_user(user)
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            balance=user.balance
        )
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Return the currently authenticated user.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        balance=current_user.balance
    )