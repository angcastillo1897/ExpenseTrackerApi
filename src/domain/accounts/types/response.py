from typing import Optional

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    name: str
    amount: float
    icon_name: Optional[str]
    icon_bg_color: Optional[str]
    currency: str
    include_in_total: bool
    user_id: int

    class Config:
        from_attributes = True
