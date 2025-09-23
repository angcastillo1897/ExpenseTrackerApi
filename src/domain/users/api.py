# Presentation layer (HTTP routes, request/response handling).
from fastapi import APIRouter, status

from src.core.dependencies.async_bd import AsyncSessionDepends

from . import schemas, service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.RegisterRequest, db: AsyncSessionDepends):
    return await service.register_user(db, user)
