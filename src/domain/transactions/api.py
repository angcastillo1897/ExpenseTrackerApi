from fastapi import APIRouter, status

from src.core.dependencies.async_bd import AsyncSessionDepends
from src.core.dependencies.auth_user import AuthUserDepends
from src.domain.transactions.types import (
    TransactionCreateRequest,
    TransactionGetRequestDepends,
    TransactionResponse,
    TransactionUpdateRequest,
)

from .service import (
    create_transaction_service,
    delete_transaction_service,
    get_transactions_service,
    update_transaction_service,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
async def create_transaction_endpoint(
    transaction: TransactionCreateRequest,
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    return await create_transaction_service(db, user.id, transaction)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction_endpoint(
    transaction_id: int,
    update_data: TransactionUpdateRequest,
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    return await update_transaction_service(db, transaction_id, user.id, update_data)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction_endpoint(
    transaction_id: int,
    db: AsyncSessionDepends,
    user: AuthUserDepends,
):
    await delete_transaction_service(db, transaction_id, user.id)


@router.get("/", response_model=list[TransactionResponse])
async def get_transactions_endpoint(
    db: AsyncSessionDepends,
    user: AuthUserDepends,
    filters: TransactionGetRequestDepends,
):
    return await get_transactions_service(db, user.id, filters)
