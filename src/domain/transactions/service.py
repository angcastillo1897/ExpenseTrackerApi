from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.transactions.repository import (
    create_transaction,
    delete_transaction,
    get_transactions,
    update_transaction,
)
from src.domain.transactions.types import (
    TransactionCreateRequest,
    TransactionGetRequestDepends,
    TransactionResponse,
    TransactionUpdateRequest,
)


async def create_transaction_service(
    db: AsyncSession, user_id: int, data: TransactionCreateRequest
) -> TransactionResponse:
    db_transaction = await create_transaction(db, user_id, data)
    return TransactionResponse.model_validate(db_transaction)


async def update_transaction_service(
    db: AsyncSession,
    transaction_id: int,
    user_id: int,
    update_data: TransactionUpdateRequest,
) -> Optional[TransactionResponse]:
    update_dict = update_data.model_dump(exclude_unset=True)
    db_transaction = await update_transaction(db, transaction_id, user_id, update_dict)
    if db_transaction:
        return TransactionResponse.model_validate(db_transaction)
    return None


async def delete_transaction_service(
    db: AsyncSession, transaction_id: int, user_id: int
) -> None:
    await delete_transaction(db, transaction_id, user_id)


async def get_transactions_service(
    db, user_id: int, filters: TransactionGetRequestDepends
) -> any:
    filter_type = filters.filter_type
    date = filters.date
    transaction_type = filters.transaction_type
    db_transactions = await get_transactions(
        db, user_id, filter_type, date, transaction_type
    )

    #!!! need to improve

    # print("DB TRANSACTIONS:", db_transactions)

    # transactions_list =[TransactionResponse.model_validate(tx) for tx in db_transactions]

    # #* group transactions by category
    # transaction_list_grouped =

    return []
