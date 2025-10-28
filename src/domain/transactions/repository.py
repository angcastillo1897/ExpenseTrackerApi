from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import delete, extract, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.transactions.models import Transaction
from src.domain.transactions.types import TransactionCreateRequest


async def create_transaction(
    db: AsyncSession, user_id: int, data: TransactionCreateRequest
) -> Transaction:
    db_transaction = Transaction(
        amount=data.amount,
        description=data.description,
        date=data.date or None,
        is_recurring=data.is_recurring or False,
        transaction_type=data.transaction_type,
        category_id=data.category_id,
        account_id=data.account_id,
        user_id=user_id,
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


async def update_transaction(
    db: AsyncSession, transaction_id: int, user_id: int, update_data: dict
) -> Optional[Transaction]:
    result = await db.execute(
        update(Transaction)
        .where(Transaction.id == transaction_id, Transaction.user_id == user_id)
        .values(**update_data)
        .returning(Transaction)
    )
    await db.commit()
    return result.scalar_one_or_none()


async def delete_transaction(
    db: AsyncSession, transaction_id: int, user_id: int
) -> None:
    await db.execute(
        delete(Transaction).where(
            Transaction.id == transaction_id, Transaction.user_id == user_id
        )
    )
    await db.commit()


async def get_transactions(
    db, user_id: int, filter_type: str, date: str, transaction_type: str = None
) -> dict:
    base_query = select(Transaction).where(Transaction.user_id == user_id)
    dt = datetime.strptime(date, "%Y-%m-%d")
    if filter_type == "day":
        base_query = base_query.where(
            extract("year", Transaction.date) == dt.year,
            extract("month", Transaction.date) == dt.month,
            extract("day", Transaction.date) == dt.day,
        )
    elif filter_type == "week":
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        base_query = base_query.where(
            Transaction.date >= start, Transaction.date <= end
        )
    elif filter_type == "month":
        base_query = base_query.where(
            extract("year", Transaction.date) == dt.year,
            extract("month", Transaction.date) == dt.month,
        )
    elif filter_type == "year":
        base_query = base_query.where(extract("year", Transaction.date) == dt.year)
    if transaction_type:
        base_query = base_query.where(Transaction.transaction_type == transaction_type)

    # base_query = base_query.group_by(Transaction.category_id)
    result = await db.execute(base_query)
    print("RESULT:", result)
    return result
    # Query for summary by category
    # summary_query = select(
    #     Transaction.category_id,
    #     func.sum(Transaction.amount).label("total_amount")
    # ).where(Transaction.user_id == user_id)
    # if filter_type == "day":
    #     summary_query = summary_query.where(
    #         extract("year", Transaction.date) == dt.year,
    #         extract("month", Transaction.date) == dt.month,
    #         extract("day", Transaction.date) == dt.day,
    #     )
    # elif filter_type == "week":
    #     start = dt - timedelta(days=dt.weekday())
    #     end = start + timedelta(days=6)
    #     summary_query = summary_query.where(Transaction.date >= start, Transaction.date <= end)
    # elif filter_type == "month":
    #     summary_query = summary_query.where(
    #         extract("year", Transaction.date) == dt.year,
    #         extract("month", Transaction.date) == dt.month,
    #     )
    # elif filter_type == "year":
    #     summary_query = summary_query.where(extract("year", Transaction.date) == dt.year)
    # if transaction_type:
    #     summary_query = summary_query.where(Transaction.transaction_type == transaction_type)
    # summary_query = summary_query.group_by(Transaction.category_id)
    # summary_result = await db.execute(summary_query)
    # summary = {row.category_id: row.total_amount for row in summary_result}
    # # Group transactions by category_id
    # grouped = {}
    # for tx in transactions:
    #     grouped.setdefault(tx.category_id, []).append(tx)
    # return {"grouped": grouped, "summary": summary}
