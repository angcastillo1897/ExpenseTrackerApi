from fastapi import APIRouter, status

from src.core.dependencies.async_bd import AsyncSessionDepends
from src.core.dependencies.auth_user import AuthUserDepends
from src.domain.accounts.types import (
    AccountCreateRequest,
    AccountResponse,
    AccountUpdateRequest,
)

from .service import (
    create_account_service,
    get_user_accounts_service,
    update_account_service,
)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account_endpoint(
    account: AccountCreateRequest,
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    return await create_account_service(db, user.id, account)


@router.get("/", response_model=list[AccountResponse])
async def get_user_accounts_endpoint(
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    return await get_user_accounts_service(db, user.id)


@router.patch("/{account_id}", response_model=AccountResponse)
async def update_account_endpoint(
    account_id: int,
    update_data: AccountUpdateRequest,
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    return await update_account_service(db, account_id, user.id, update_data)
