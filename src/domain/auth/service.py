# Business logic (rules, validations, orchestration).
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import BadRequestException
from src.core.utils.hashing import bcrypt_context
from src.core.utils.token import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from src.domain.users import repository as user_repository

from . import schemas


async def auth_register(db: AsyncSession, user: schemas.RegisterRequest):
    db_user = await user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise BadRequestException("Email already registered")
    hashed_password = bcrypt_context.hash(user.password)
    db_user = await user_repository.create_user(db, user, hashed_password)
    user = schemas.UserSerializer.model_validate(db_user)
    access_token = create_access_token({"sub": str(db_user.id)})
    refresh_token = create_refresh_token({"sub": str(db_user.id)})
    return schemas.RegisterResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def auth_login(db: AsyncSession, user_login: schemas.LoginRequest):
    db_user = await user_repository.get_user_by_email(db, email=user_login.email)
    if not db_user or not bcrypt_context.verify(
        user_login.password, db_user.hashed_password
    ):
        raise BadRequestException("Invalid email or password")
    user = schemas.UserSerializer.model_validate(db_user)
    access_token = create_access_token({"sub": str(db_user.id)})
    refresh_token = create_refresh_token({"sub": str(db_user.id)})
    return schemas.LoginResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def refresh_access_token(refresh: schemas.RefreshRequest):
    payload = verify_token(refresh.refresh_token)
    user_id: int = int(payload.get("sub"))
    if not user_id:
        raise BadRequestException("Invalid refresh token")
    access_token = create_access_token({"sub": str(user_id)})
    return schemas.RefreshResponse(access_token=access_token)


async def forgot_password(db: AsyncSession, request: schemas.ForgotPasswordRequest):
    db_user = await user_repository.get_user_by_email(db, email=request.email)
    if not db_user or not db_user.is_active:
        # For security, do not reveal if email is registered
        return {"message": "If the email is registered, a reset link has been sent."}

    #!!! Here you would generate a password reset token and send an email
    # For simplicity, we'll skip email sending and just return a message

    return {"message": "If the email is registered, a reset link has been sent."}
