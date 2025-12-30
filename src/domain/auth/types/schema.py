from datetime import datetime
from typing import Optional

from src.core.base_schema import CamelModel


class TokensBase(CamelModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class CreateRefreshToken(CamelModel):
    user_id: int
    token_hash: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    expires_at: datetime


class CreatePasswordResetToken(CamelModel):
    user_id: int
    token_hash: str
    expires_at: datetime
