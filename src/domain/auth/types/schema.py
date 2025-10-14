from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TokensBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


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
