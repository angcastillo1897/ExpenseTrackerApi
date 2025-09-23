# Presentation layer (HTTP routes, request/response handling).
from fastapi import APIRouter, status

from src.core.dependencies.async_bd import AsyncSessionDepends

from . import schemas, service

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", response_model=schemas.RegisterResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user: schemas.RegisterRequest, db: AsyncSessionDepends):
    return await service.register_user(db, user)


@router.post("/login", response_model=schemas.LoginResponse)
async def login_user(login: schemas.LoginRequest, db: AsyncSessionDepends):
    return await service.login_user(db, login)


@router.get("/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: AsyncSessionDepends):
    return await service.get_user_by_id(db, user_id)
