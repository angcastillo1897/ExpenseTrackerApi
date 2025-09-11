from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils.db_connection import Async_session_local


async def get_async_session():
    async with Async_session_local() as s:
        yield s


AsyncSessionDepends = Annotated[AsyncSession, Depends(get_async_session)]
