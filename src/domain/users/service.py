# Business logic (rules, validations, orchestration).
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException

from . import repository, types


async def get_user_profile(db: AsyncSession, user_id: int):
    db_user = await repository.get_user_by_id(db, user_id)
    if not db_user:
        raise NotFoundException("No user found")
    return types.UserSerializer.model_validate(db_user)
