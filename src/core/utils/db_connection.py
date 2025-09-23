from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

URL: str = (
    f"postgresql+asyncpg://{settings.BD_USERNAME}:"
    f"{settings.BD_PASSWORD}@"
    f"{settings.BD_HOST}:"
    f"{settings.BD_PORT}/"
    f"{settings.BD_NAME}"
)

async_engine: AsyncEngine = create_async_engine(URL, pool_pre_ping=True)
Async_session_local: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autoflush=False, bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


class Model(AsyncAttrs, DeclarativeBase): ...
