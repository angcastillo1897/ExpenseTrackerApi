# Business logic (rules, validations, orchestration).

from fastapi import BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import BadRequestException, UnAuthorizedException
from src.core.utils.constants import MAX_TOKENS_PER_USER
from src.core.utils.hashing import get_password_hash, verify_password
from src.core.utils.mailer import send_email
from src.core.utils.token import (
    create_access_token,
    prepare_refresh_token_creation,
)
from src.core.utils.user_extra_info import get_user_ip
from src.domain.auth import repository as auth_repository
from src.domain.users import repository as user_repository

from . import schemas


async def auth_register(
    db: AsyncSession,
    user_request: schemas.RegisterRequest,
    background_tasks: BackgroundTasks,
    http_request: Request,
):
    db_user = await user_repository.get_user_by_email(db, email=user_request.email)
    if db_user:
        raise BadRequestException("Email already registered")
    hashed_password = get_password_hash(user_request.password)
    db_user = await user_repository.create_user(db, user_request, hashed_password)
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
        user_id=db_user.id, device_info=user_request.device_info, ip_address=ip_address
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

    ip_address = get_user_ip(http_request)
    refresh_token_data = prepare_refresh_token_creation(
        user_id=db_user.id, device_info=user_login.device_info, ip_address=ip_address
    )

    # * current device has a valid active refresh token , session .  update token
    current_device_refresh_token = (
        await auth_repository.current_device_active_refresh_token(
            db, user.id, user_login.device_info
        )
    )

    if current_device_refresh_token:
        # update old refresh token values - TOKEN ROTATION
        await auth_repository.update_refresh_token(
            db,
            old_refresh_token_id=current_device_refresh_token.id,
            new_refresh_token_data=refresh_token_data,
        )
    else:
        # create new refresh token
        await auth_repository.create_refresh_token(db, refresh_token_data)

    # Clean up old expired tokens (lazy cleanup)
    await auth_repository.delete_user_expired_tokens(db, user.id)

    return schemas.LoginResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token_data.token_hash,
    )


async def refresh_access_token(
    db: AsyncSession, refresh_request: schemas.RefreshRequest, http_request: Request
):
    token_hash = refresh_request.refresh_token
    # Get and validate refresh token from DB
    db_token = await auth_repository.get_refresh_token_from_db(db, token_hash)
    if not db_token or not db_token.is_active:
        print(db_token)
        raise UnAuthorizedException("Invalid or expired refresh token")

    # Get user
    db_user = await user_repository.get_user_by_id(db, db_token.user_id)
    if not db_user or not db_user.is_active:
        raise UnAuthorizedException("User not found or inactive")

    # * generate new tokens
    access_token = create_access_token({"sub": str(db_user.id)})
    # create new refresh token
    ip_address = get_user_ip(http_request)

    new_refresh_token_data = prepare_refresh_token_creation(
        user_id=db_user.id,
        device_info=refresh_request.device_info,
        ip_address=ip_address,
    )

    # update old refresh token values - TOKEN ROTATION , set newtokenhash to old token hash
    await auth_repository.update_refresh_token(
        db,
        old_refresh_token_id=db_token.id,
        new_refresh_token_data=new_refresh_token_data,
    )

    return schemas.TokensBase(
        access_token=access_token, refresh_token=new_refresh_token_data.token_hash
    )


async def auth_logout(db: AsyncSession, request: schemas.LogoutRequest):
    db_token = await auth_repository.get_refresh_token_from_db(
        db, request.refresh_token
    )
    if db_token:
        await auth_repository.invalidate_token(db, db_token.id)

    return {"message": "Logged out successfully"}


async def auth_forgot_password(
    db: AsyncSession, request: schemas.ForgotPasswordRequest
):
    db_user = await user_repository.get_user_by_email(db, email=request.email)
    if not db_user or not db_user.is_active:
        # For security, do not reveal if email is registered
        return {"message": "If the email is registered, a reset link has been sent."}

    #!!! TODO:  Here you would generate a password reset token and send an email
    password_reset_token = generate_refresh_token()
    password_reset_token_hash = hash_token(password_reset_token)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.RESET_TOKEN_EXPIRE_MINUTES
    )
    # For simplicity, we'll skip email sending and just return a message

    return {"message": "If the email is registered, a reset link has been sent."}
