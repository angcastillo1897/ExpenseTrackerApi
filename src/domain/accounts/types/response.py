from typing import Optional

from src.core.base_schema import CamelModel


class AccountResponse(CamelModel):
    id: int
    name: str
    amount: float
    icon_name: Optional[str]
    icon_bg_color: Optional[str]
    currency: str
    include_in_total: bool
    user_id: int
