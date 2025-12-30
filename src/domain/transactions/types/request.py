from datetime import datetime
from typing import Annotated, Literal, Optional

from fastapi import Depends
from pydantic import Field

from src.core.base_schema import CamelModel


class TransactionCreateRequest(CamelModel):
    amount: float
    description: Optional[str] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = False
    transaction_type: Literal["income", "expense"]
    currency: str = "PEN"
    category_id: int
    account_id: int


class TransactionUpdateRequest(CamelModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    currency: Optional[str] = None
    transaction_type: Optional[Literal["income", "expense"]] = None
    category_id: Optional[int] = None
    account_id: Optional[int] = None


class TransactionGetRequest(CamelModel):
    filter_type: Literal["day", "week", "month", "year"] = Field(
        default="day",
        description="Filter by day, week, month, or year",
    )
    date: str = Field(
        ...,
        description="Date in YYYY-MM-DD format for filtering",
        pattern=r"^\d{4}-\d{2}-\d{2}$",  # Validates YYYY-MM-DD format
    )
    transaction_type: Optional[Literal["income", "expense"]] = Field(
        default=None, description="Filter by transaction type: income or expense"
    )


TransactionGetRequestDepends = Annotated[TransactionGetRequest, Depends()]
