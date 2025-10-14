# Business logic (rules, validations, orchestration).

from datetime import datetime, timezone

from fastapi import BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import BadRequestException, UnAuthorizedException
from src.core.utils.constants import MAX_TOKENS_PER_USER
from src.core.utils.hashing import get_password_hash, verify_password
from src.core.utils.mailer import send_email
from src.core.utils.token import (
    create_access_token,
    generate_password_reset_token,
    prepare_refresh_token_creation,
)
from src.core.utils.user_extra_info import get_user_ip
from src.domain.auth import repository as auth_repository
from src.domain.users import repository as user_repository

from . import types


async def auth_register(
    db: AsyncSession,
    user_request: types.RegisterRequest,
    background_tasks: BackgroundTasks,
    http_request: Request,
):
    db_user = await user_repository.get_user_by_email(db, email=user_request.email)
    if db_user:
        raise BadRequestException("Email already registered")
    hashed_password = get_password_hash(user_request.password)
    db_user = await user_repository.create_user(db, user_request, hashed_password)
    user = types.UserSerializer.model_validate(db_user)

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

    return types.RegisterResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token_data.token_hash,
    )


async def auth_login(
    db: AsyncSession, user_login: types.LoginRequest, http_request: Request
):
    db_user = await user_repository.get_user_by_email(db, email=user_login.email)
    if not db_user or not verify_password(user_login.password, db_user.hashed_password):
        raise BadRequestException("Invalid email or password")
    user = types.UserSerializer.model_validate(db_user)
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

    return types.LoginResponse(
        user=user,
        access_token=access_token,
        refresh_token=refresh_token_data.token_hash,
    )


async def refresh_access_token(
    db: AsyncSession, refresh_request: types.RefreshRequest, http_request: Request
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

    return types.TokensBase(
        access_token=access_token, refresh_token=new_refresh_token_data.token_hash
    )


async def auth_logout(db: AsyncSession, request: types.LogoutRequest):
    db_token = await auth_repository.get_refresh_token_from_db(
        db, request.refresh_token
    )
    if db_token:
        await auth_repository.invalidate_token(db, db_token.id)

    return {"message": "Logged out successfully"}


async def auth_forgot_password(
    db: AsyncSession,
    request: types.ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
):
    db_user = await user_repository.get_user_by_email(db, email=request.email)
    if not db_user or not db_user.is_active:
        # For security, do not reveal if email is registered
        return {"message": "If the email is registered, a reset link has been sent."}

    password_reset_token_data = generate_password_reset_token(user_id=db_user.id)
    await auth_repository.create_reset_password_token(db, password_reset_token_data)

    # ? send email with reset link
    reset_link = f"https://your-frontend-app.com/reset-password?token={password_reset_token_data.token_hash}"
    user = types.UserSerializer.model_validate(db_user)
    # Send welcome email as brackground task
    # ? in future, consider using a task queue like Celery with redis for better scalability
    # background_tasks.add_task(
    #     send_email,
    #     to_email=user.email,
    #     subject="Reset password for Expense Tracker App",
    #     template_name="reset_password.html",
    #     username=user.first_name,
    #     reset_link=reset_link,
    # )

    return {
        "message": "If the email is registered, a reset link has been sent.",
        "reset_link": reset_link,
        "user": user,
    }


async def auth_validate_reset_password_token(db: AsyncSession, token: str):
    """if response is 200, show reset password form with time remaining to reset password"""
    user_reset_token_db = await user_repository.get_user_by_reset_password_token(
        db, token
    )
    print(user_reset_token_db)

    if user_reset_token_db:
        # Calculate remaining time
        expires_at = user_reset_token_db["expires_at"]
        now = datetime.now(timezone.utc)

        time_remaining = expires_at - now

        if time_remaining.total_seconds() <= 0:
            return {"message": "Token has expired."}

        # Round UP minutes
        minutes_remaining = int((time_remaining.total_seconds() + 59) // 60)
        return {
            "message": "Token is valid.",
            "expires_in_minutes": minutes_remaining,
        }

    else:
        raise BadRequestException(
            "Invalid or expired reset token. Please request a new password reset."
        )


async def auth_reset_password(db: AsyncSession, request: types.ResetPasswordRequest):
    user_reset_token_db = await user_repository.get_user_by_reset_password_token(
        db, request.token
    )

    if not user_reset_token_db:
        raise BadRequestException(
            "Invalid or expired reset token. Please request a new password reset."
        )

    if len(request.new_password) < 8:
        raise BadRequestException("Password must be at least 8 characters long")

    # Update user's password
    hashed_password = get_password_hash(request.new_password)
    await user_repository.update_user_password(
        db, user_id=user_reset_token_db["user_id"], new_hashed_password=hashed_password
    )

    # Invalidate the used reset token
    await auth_repository.invalidate_reset_password_token(db, request.token)

    # invalidate all existing refresh tokens for the user (force logout from all devices)
    await auth_repository.invalidate_all_user_refresh_tokens(
        db, user_reset_token_db["user_id"]
    )

    return {"message": "Password has been reset successfully."}
