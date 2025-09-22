from sqlalchemy import ForeignKey,String,Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.utils.db_connection import Model as Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.domain.users.models import User
    from src.domain.transactions.models import Transaction

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]= mapped_column(String(100))
    type: Mapped[str] = mapped_column(
        Enum("income", "expense", name="category_type"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")