from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionResponse(BaseModel):
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

    class Config:
        from_attributes = True
