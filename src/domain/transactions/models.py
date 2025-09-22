from sqlalchemy import String, Float, DateTime,func ,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.utils.db_connection import Model as Base
from datetime import datetime
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.domain.users.models import User
    from src.domain.categories.models import Category

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    amount: Mapped[float]=mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(400),nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    is_recurring: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")