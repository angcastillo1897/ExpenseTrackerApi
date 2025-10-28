# Data access (SQLAlchemy queries, CRUD)
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.categories.models import Category
from src.domain.categories.types import CategoryCreateRequest


async def create_category(
    db: AsyncSession, user_id: int, category_data: CategoryCreateRequest
):
    db_category = Category(
        user_id=user_id, **category_data.model_dump(exclude_unset=True)
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_user_categories(
    db: AsyncSession, user_id: int, transaction_type: Optional[str]
) -> List[Category]:
    query = select(Category).where(Category.user_id == user_id)
    if transaction_type:
        query = query.where(Category.transaction_type == transaction_type)
    result = await db.execute(query)
    return result.scalars().all()


async def update_category(
    db: AsyncSession, category_id: int, user_id: int, update_data: dict
):
    result = await db.execute(
        update(Category)
        .where(Category.id == category_id, Category.user_id == user_id)
        .values(**update_data)
        .returning(Category)
    )
    await db.commit()
    return result.scalar_one_or_none()
