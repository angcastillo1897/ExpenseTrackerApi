# Business logic (rules, validations, orchestration).
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import BadRequestException, NotFoundException
from src.core.utils.auth import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from src.core.utils.hashing import bcrypt_context

from . import repository, schemas


async def register_user(db: AsyncSession, user: schemas.RegisterRequest):
    db_user = await repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise BadRequestException("Email already registered")
    hashed_password = bcrypt_context.hash(user.password)
    db_user = await repository.create_user(db, user, hashed_password)
    user_read = schemas.UserRead.model_validate(db_user)
    access_token = create_access_token({"uid": str(db_user.id)})
    refresh_token = create_refresh_token({"uid": str(db_user.id)})
    return schemas.RegisterResponse(
        user=user_read,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def get_user_by_id(db: AsyncSession, user_id: int):
    db_user = await repository.get_user_by_id(db, user_id)
    if not db_user:
        raise NotFoundException("No user found")
    return schemas.UserResponse.model_validate(db_user)


async def login_user(db: AsyncSession, user_login: schemas.LoginRequest):
    db_user = await repository.get_user_by_email(db, email=user_login.email)
    if not db_user or not bcrypt_context.verify(
        user_login.password, db_user.hashed_password
    ):
        raise BadRequestException("Invalid email or password")
    user = schemas.UserResponse.model_validate(db_user)
    access_token = create_access_token({"uid": str(db_user.id)})
    refresh_token = create_refresh_token({"uid": str(db_user.id)})
    return schemas.LoginResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def refresh_access_token(refresh: schemas.RefreshRequest):
    payload = verify_token(refresh.refresh_token)
    user_id = payload.get("uid")
    if not user_id:
        raise BadRequestException("Invalid refresh token")
    access_token = create_access_token({"uid": str(user_id)})
    return schemas.RefreshResponse(access_token=access_token)
