from typing import List, Optional

from fastapi import APIRouter, Query, status

from src.core.dependencies.async_bd import AsyncSessionDepends
from src.core.dependencies.auth_user import AuthUserDepends
from src.domain.categories.types import (
    CategoryCreateRequest,
    CategoryResponse,
    CategoryUpdateRequest,
)

from .service import (
    create_category_service,
    get_user_categories_service,
    update_category_service,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(
    category: CategoryCreateRequest,
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    return await create_category_service(db, user.id, category)


@router.get("/", response_model=List[CategoryResponse])
async def get_user_categories_endpoint(
    db: AsyncSessionDepends,
    user: AuthUserDepends,
    transaction_type: Optional[str] = Query(
        None, description="Filter by transaction type: income or expense"
    ),
):
    return await get_user_categories_service(db, user.id, transaction_type)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category_endpoint(
    category_id: int,
    update_data: CategoryUpdateRequest,
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    return await update_category_service(db, category_id, user.id, update_data)
