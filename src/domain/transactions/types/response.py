from datetime import datetime
from typing import Optional

from src.core.base_schema import CamelModel


class TransactionResponse(CamelModel):
    id: int
    amount: float
    currency: str
    description: Optional[str]
    date: datetime
    is_recurring: bool
    transaction_type: str
    category_id: int
    account_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
