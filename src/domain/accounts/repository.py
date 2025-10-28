from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.accounts.models import Account
from src.domain.accounts.types import AccountCreateRequest


async def create_account(
    db: AsyncSession, user_id: int, account_data: AccountCreateRequest
):
    db_account = Account(
        name=account_data.name,
        amount=account_data.amount,
        icon_name=account_data.icon_name,
        icon_bg_color=account_data.icon_bg_color,
        currency=account_data.currency,
        include_in_total=account_data.include_in_total,
        user_id=user_id,
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


async def get_user_accounts(db: AsyncSession, user_id: int):
    result = await db.execute(select(Account).where(Account.user_id == user_id))
    return result.scalars().all()


async def update_account(
    db: AsyncSession, account_id: int, user_id: int, update_data: dict
):
    result = await db.execute(
        Account.__table__.update()
        .where(Account.id == account_id, Account.user_id == user_id)
        .values(**update_data)
        .returning(Account)
    )
    await db.commit()
    return result.scalar_one_or_none()
