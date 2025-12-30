from typing import Optional

from pydantic import EmailStr

from src.core.base_schema import CamelModel


class RegisterRequest(CamelModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    device_info: Optional[str] = None


class LoginRequest(CamelModel):
    email: EmailStr
    password: str
    device_info: Optional[str] = None


class RefreshRequest(CamelModel):
    refresh_token: str
    device_info: Optional[str] = None


class LogoutRequest(CamelModel):
    refresh_token: str


class ForgotPasswordRequest(CamelModel):
    email: EmailStr


class ResetPasswordRequest(CamelModel):
    token: str
    new_password: str
