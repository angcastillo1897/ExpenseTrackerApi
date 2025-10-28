from typing import List, Optional

# Business logic (rules, validations, orchestration)
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.categories.repository import (
    create_category,
    get_user_categories,
    update_category,
)
from src.domain.categories.types import (
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)


async def create_category_service(
    db: AsyncSession, user_id: int, category_data: CategoryCreateRequest
) -> CategoryResponse:
    db_category = await create_category(db, user_id, category_data)
    return CategoryResponse.model_validate(db_category)


async def get_user_categories_service(
    db: AsyncSession, user_id: int, transaction_type: Optional[str]
) -> List[CategoryResponse]:
    db_categories = await get_user_categories(db, user_id, transaction_type)
    return [CategoryResponse.model_validate(cat) for cat in db_categories]


async def update_category_service(
    db: AsyncSession, category_id: int, user_id: int, update_data: CategoryUpdateRequest
) -> CategoryResponse:
    update_dict = update_data.model_dump(exclude_unset=True)
    db_category = await get_user_categories(db, user_id, None)
    # Check if category exists for user
    found = [cat for cat in db_category if cat.id == category_id]
    if not found:
        raise Exception("Category not found or not owned by user")
    updated = await update_category(db, category_id, user_id, update_dict)
    return CategoryResponse.model_validate(updated)
