# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_bcrypt_password_length(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must be 72 bytes or fewer")
    return password


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

    _validate_password_length = field_validator("password")(
        validate_bcrypt_password_length
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    _validate_password_length = field_validator("password")(
        validate_bcrypt_password_length
    )


class UserResponse(BaseModel):
    id: int
    email: str
    balance: float

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse