# DTOs / validation (Pydantic).
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.domain.users.schemas import UserSerializer


class TokensBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    device_info: Optional[str] = None


class RegisterResponse(TokensBase):
    user: UserSerializer


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_info: Optional[str] = None


class LoginResponse(TokensBase):
    user: UserSerializer


class CreateRefreshToken(BaseModel):
    user_id: int
    token_hash: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    expires_at: datetime


class CreatePasswordResetToken(BaseModel):
    user_id: int
    token_hash: str
    expires_at: datetime


class RefreshRequest(BaseModel):
    refresh_token: str
    device_info: Optional[str] = None


# class RefreshResponse(BaseModel):
#     access_token: str
#     token_type: str = "Bearer"
class LogoutRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
