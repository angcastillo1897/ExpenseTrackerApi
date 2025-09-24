#! TODO
# POST /auth/register - User registration
# POST /auth/login - User authentication
# POST /auth/refresh - Token refresh
# POST /auth/logout - Single session logout
# POST /auth/forgot-password - Password reset request
# POST /auth/reset-password - Complete password reset
from fastapi import APIRouter, status

from src.core.dependencies.async_bd import AsyncSessionDepends

from . import schemas, service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=schemas.RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def auth_register(user: schemas.RegisterRequest, db: AsyncSessionDepends):
    return await service.auth_register(db, user)


@router.post("/login", response_model=schemas.LoginResponse)
async def login_user(user_credentials: schemas.LoginRequest, db: AsyncSessionDepends):
    return await service.login_user(db, user_credentials)


@router.post("/refresh", response_model=schemas.RefreshResponse)
async def refresh_token(refresh: schemas.RefreshRequest):
    return await service.refresh_access_token(refresh)
