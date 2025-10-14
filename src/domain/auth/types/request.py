from typing import Optional

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    device_info: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_info: Optional[str] = None


class RefreshRequest(BaseModel):
    refresh_token: str
    device_info: Optional[str] = None


class LogoutRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
