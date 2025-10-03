# Data access (SQLAlchemy queries, CRUD).

from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth import models as auth_models
from src.domain.auth import schemas as auth_schemas
from src.domain.users import models as user_models


async def create_user(
    db: AsyncSession, user: auth_schemas.RegisterRequest, hashed_password: str
):
    db_user = user_models.User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(user_models.User).where(user_models.User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(user_models.User).where(user_models.User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_reset_password_token(db: AsyncSession, token: str):
    result_query = await db.execute(
        select(user_models.User, auth_models.PasswordResetToken)
        .join(
            auth_models.PasswordResetToken,
            user_models.User.id == auth_models.PasswordResetToken.user_id,
        )
        .where(
            auth_models.PasswordResetToken.token_hash == token,
            auth_models.PasswordResetToken.expires_at > datetime.now(timezone.utc),
            auth_models.PasswordResetToken.is_used == False,
        )
        .limit(1)
    )
    if first_item := result_query.first():
        user, reset_token = first_item
        return {
            "user_id": user.id,
            "reset_token": reset_token.token_hash,
            "expires_at": reset_token.expires_at,
        }

    return None


async def update_user_password(
    db: AsyncSession, user_id: int, new_hashed_password: str
):
    await db.execute(
        update(user_models.User)
        .where(user_models.User.id == user_id)
        .values(hashed_password=new_hashed_password)
    )
    await db.commit()
