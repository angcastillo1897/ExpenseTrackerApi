# Business logic (rules, validations, orchestration).

from sqlalchemy.orm import Session
from . import repository, schemas
from passlib.context import CryptContext
from src.core.exceptions import BadRequestException


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(db: Session, user: schemas.UserCreate):
    # Check if email exists
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise BadRequestException("Email already registered")

    # Hash password
    hashed_password = bcrypt_context.hash(user.password)

    # Create user
    return repository.create_user(db, user, hashed_password)