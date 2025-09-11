# Presentation layer (HTTP routes, request/response handling).
from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from src.core.dependencies.async_bd import AsyncSessionDepends 
from . import service,schemas


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db : AsyncSessionDepends):
    return service.register_user(db, user)