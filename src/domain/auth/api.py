#! TODO
# POST /auth/register - User registration
# POST /auth/login - User authentication
# POST /auth/refresh - Token refresh
# POST /auth/logout - Single session logout
# POST /auth/forgot-password - Password reset request
# POST /auth/reset-password - Complete password reset
from fastapi import APIRouter, BackgroundTasks, status

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
):
    return await service.auth_register(db, user, background_tasks)


@router.post("/login", response_model=schemas.LoginResponse)
async def auth_login(user_credentials: schemas.LoginRequest, db: AsyncSessionDepends):
    return await service.auth_login(db, user_credentials)


@router.post("/refresh", response_model=schemas.RefreshResponse)
async def auth_refresh_token(refresh: schemas.RefreshRequest):
    return await service.refresh_access_token(refresh)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def auth_logout():
    #!!! Optionally: invalidate the refresh token in your DB/session store
    # For stateless JWT, just respond OK and let client delete tokens
    return {"message": "Logged out successfully"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def auth_forgot_password(
    request: schemas.ForgotPasswordRequest, db: AsyncSessionDepends
):
    return await service.forgot_password(db, request)
