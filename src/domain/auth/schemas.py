# DTOs / validation (Pydantic).
from pydantic import BaseModel, EmailStr

from src.domain.users.schemas import UserSerializer


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class RegisterResponse(BaseModel):
    user: UserSerializer
    access_token: str
    refresh_token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user: UserSerializer
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
