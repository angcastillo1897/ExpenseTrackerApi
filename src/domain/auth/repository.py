# Data access (SQLAlchemy queries, CRUD).
from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth import schemas as auth_schemas

from . import models


async def create_refresh_token(
    db: AsyncSession, refresh_token_data: auth_schemas.CreateRefreshToken
):
    db_refresh_token = models.User(**refresh_token_data)
    db.add(db_refresh_token)
    await db.commit()
    await db.refresh(db_refresh_token)
    return db_refresh_token


async def count_active_refresh_token_by_user(db: AsyncSession, user_id: int) -> int:
    token_count = 0
    result = await db.execute(
        select(func.count(models.RefreshToken.id)).where(
            models.RefreshToken.user_id == user_id,
            models.RefreshToken.is_active,
            models.RefreshToken.expires_at > datetime.now(),
        )
    )
    token_count = result.scalar()

    return token_count


async def get_oldest_refresh_token_by_user(db: AsyncSession, user_id: int):
    oldest_refresh_token = await db.execute(
        select(models.RefreshToken)
        .where(models.RefreshToken.user_id == user_id, models.RefreshToken.is_active)
        .order_by(models.RefreshToken.last_used.asc())
        .limit(1)
    )
    return oldest_refresh_token.scalar_one_or_none()


async def delete_refresh_token(
    db: AsyncSession, refresh_token: models.RefreshToken
) -> None:
    await db.delete(refresh_token)
    await db.commit()


async def delete_user_expired_tokens(db: AsyncSession, user_id: int) -> None:
    await db.execute(
        delete(models.RefreshToken).where(
            models.RefreshToken.user_id == user_id,
            models.RefreshToken.expires_at < datetime.now(),
        )
    )
    await db.commit()


async def get_refresh_token_from_db(db: AsyncSession, token_hash: str):
    result = await db.execute(
        select(models.RefreshToken).where(
            models.RefreshToken.token_hash == token_hash,
            models.RefreshToken.is_active,
            models.RefreshToken.expires_at > datetime.now(),
        )
    )
    return result.scalar_one_or_none()
