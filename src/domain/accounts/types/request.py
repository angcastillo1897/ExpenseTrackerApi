from typing import Optional

from pydantic import BaseModel


class AccountCreateRequest(BaseModel):
    name: str
    amount: float = 0.0
    icon_name: str
    icon_bg_color: str
    currency: str = "PEN"
    include_in_total: bool = True


class AccountUpdateRequest(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    icon_name: Optional[str] = None
    icon_bg_color: Optional[str] = None
    currency: Optional[str] = None
    include_in_total: Optional[bool] = None
