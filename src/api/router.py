from fastapi import FastAPI

from src.domain.auth.api import router as auth_router
from src.domain.users.api import router as users_router


def load_routes(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(users_router)
