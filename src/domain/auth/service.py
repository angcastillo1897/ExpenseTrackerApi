# Business logic (rules, validations, orchestration).

from fastapi import BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import BadRequestException, UnAuthorizedException
from src.core.utils.constants import MAX_TOKENS_PER_USER
from src.core.utils.hashing import get_password_hash, verify_password
from src.core.utils.mailer import send_email
from src.core.utils.token import (
    create_access_token,
    hash_token,
    prepare_refresh_token_creation,
)
from src.core.utils.user_extra_info import get_user_ip
from src.domain.auth import repository as auth_repository
from src.domain.users import repository as user_repository

from . import schemas


async def auth_register(
    db: AsyncSession,
    user: schemas.RegisterRequest,
    background_tasks: BackgroundTasks,
    http_request: Request,
):
    db_user = await user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise BadRequestException("Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = await user_repository.create_user(db, user, hashed_password)
    user = schemas.UserSerializer.model_validate(db_user)

    # Send welcome email as brackground task
    # ? in future, consider using a task queue like Celery with redis for better scalability
    background_tasks.add_task(
        send_email,
        to_email=user.email,
        subject="Welcome to Expense Tracker 🎉",
        template_name="welcome_email.html",
        username=user.first_name,
        email=user.email,
    )

    access_token = create_access_token({"sub": str(db_user.id)})

    # * Handle refresh token creation with limit
    active_refresh_tokens_count = (
        await auth_repository.count_active_refresh_token_by_user(db, user_id=db_user.id)
    )

    if active_refresh_tokens_count >= MAX_TOKENS_PER_USER:
        # Delete the oldest token
        oldest_refresh_token = await auth_repository.get_oldest_refresh_token_by_user(
            db, user_id=db_user.id
        )
        if oldest_refresh_token:
            await auth_repository.delete_refresh_token(db, oldest_refresh_token)

    # create new refresh token
    ip_address = get_user_ip(http_request)

    refresh_token_data = prepare_refresh_token_creation(
        user_id=db_user.id, device_info=user.device_info, ip_address=ip_address
    )

    await auth_repository.create_refresh_token(db, refresh_token_data)

    return schemas.RegisterResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token_data.token_hash,
    )


async def auth_login(
    db: AsyncSession, user_login: schemas.LoginRequest, http_request: Request
):
    db_user = await user_repository.get_user_by_email(db, email=user_login.email)
    if not db_user or not verify_password(user_login.password, db_user.hashed_password):
        raise BadRequestException("Invalid email or password")
    user = schemas.UserSerializer.model_validate(db_user)
    access_token = create_access_token({"sub": str(user.id)})
    # refresh_token = create_refresh_token({"sub": str(user.id)})

    # create new refresh token
    ip_address = get_user_ip(http_request)

    refresh_token_data = prepare_refresh_token_creation(
        user_id=db_user.id, device_info=user_login.device_info, ip_address=ip_address
    )

    await auth_repository.create_refresh_token(db, refresh_token_data)

    # Clean up old expired tokens (lazy cleanup)
    await auth_repository.delete_user_expired_tokens(db, user.id)

    return schemas.LoginResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token_data.token_hash,
    )


async def refresh_access_token(
    db: AsyncSession, refresh_token: schemas.RefreshRequest, http_request: Request
):
    token_hash = hash_token(refresh_token)
    # Get and validate refresh token from DB
    db_token = await auth_repository.get_refresh_token_from_db(db, token_hash)
    if not db_token:
        raise UnAuthorizedException("Invalid or expired refresh token")

    # Get user
    user = await user_repository.get_user_by_id(db, db_token.user_id)
    if not user or not user.is_active:
        raise UnAuthorizedException("User not found or inactive")

    # payload = verify_token(refresh.refresh_token)
    # user_id: int = int(payload.get("sub"))
    # if not user_id:
    #     raise BadRequestException("Invalid refresh token")
    # access_token = create_access_token({"sub": str(user_id)})

    # * generate new tokens
    access_token = create_access_token({"sub": str(user.id)})
    #! NEED TO ADD MORE LOGIC

    return schemas.TokensBase(access_token=access_token, refresh_token=refresh_token)


async def forgot_password(db: AsyncSession, request: schemas.ForgotPasswordRequest):
    db_user = await user_repository.get_user_by_email(db, email=request.email)
    if not db_user or not db_user.is_active:
        # For security, do not reveal if email is registered
        return {"message": "If the email is registered, a reset link has been sent."}

    #!!! Here you would generate a password reset token and send an email
    # For simplicity, we'll skip email sending and just return a message

    return {"message": "If the email is registered, a reset link has been sent."}
