from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.accounts.repository import (
    create_account,
    get_user_accounts,
    update_account,
)
from src.domain.accounts.types import (
    AccountCreateRequest,
    AccountResponse,
    AccountUpdateRequest,
)


async def create_account_service(
    db: AsyncSession, user_id: int, account_data: AccountCreateRequest
) -> AccountResponse:
    db_account = await create_account(db, user_id, account_data)
    return AccountResponse.model_validate(db_account)


async def get_user_accounts_service(
    db: AsyncSession, user_id: int
) -> List[AccountResponse]:
    db_accounts = await get_user_accounts(db, user_id)
    return [AccountResponse.model_validate(acc) for acc in db_accounts]


async def update_account_service(
    db: AsyncSession, account_id: int, user_id: int, update_data: AccountUpdateRequest
) -> AccountResponse:
    update_dict = update_data.model_dump(exclude_unset=True)
    db_account = await update_account(db, account_id, user_id, update_dict)
    return AccountResponse.model_validate(db_account)
