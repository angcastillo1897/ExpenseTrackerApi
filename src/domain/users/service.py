# Business logic (rules, validations, orchestration).

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import BadRequestException

from . import repository, schemas

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_user(db: AsyncSession, user: schemas.RegisterRequest):
    db_user = await repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise BadRequestException("Email already registered")
    hashed_password = bcrypt_context.hash(user.password)
    return await repository.create_user(db, user, hashed_password)
