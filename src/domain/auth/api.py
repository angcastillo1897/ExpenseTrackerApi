#! TODO
# POST /auth/register - User registration *
# POST /auth/login - User authentication  *
# POST /auth/refresh - Token refresh      *
# POST /auth/logout - Single session logout *
# POST /auth/forgot-password - Password reset request *
# POST /auth/reset-password - Complete password reset
# POST /auth/validate-reset-token/{token} - Validate password reset token
from fastapi import APIRouter, BackgroundTasks, Request, status

from src.core.dependencies.async_bd import AsyncSessionDepends

from . import schemas, service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=schemas.RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def auth_register(
    user: schemas.RegisterRequest,
    db: AsyncSessionDepends,
    background_tasks: BackgroundTasks,
    http_request: Request,
):
    return await service.auth_register(db, user, background_tasks, http_request)


@router.post("/login", response_model=schemas.LoginResponse)
async def auth_login(
    user_credentials: schemas.LoginRequest,
    db: AsyncSessionDepends,
    http_request: Request,
):
    return await service.auth_login(db, user_credentials, http_request)


@router.post("/refresh", response_model=schemas.TokensBase)
async def auth_refresh_token(
    refresh: schemas.RefreshRequest, db: AsyncSessionDepends, http_request: Request
):
    return await service.refresh_access_token(db, refresh, http_request)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def auth_logout(request: schemas.LogoutRequest, db: AsyncSessionDepends):
    return await service.auth_logout(db, request)


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def auth_forgot_password(
    request: schemas.ForgotPasswordRequest,
    db: AsyncSessionDepends,
    background_tasks: BackgroundTasks,
):
    return await service.auth_forgot_password(db, request, background_tasks)


@router.post("/validate-reset-password-token", status_code=status.HTTP_200_OK)
async def auth_validate_reset_password_token(
    token: str,
    db: AsyncSessionDepends,
):
    return await service.auth_validate_reset_password_token(db, token)
