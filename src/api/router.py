from fastapi import FastAPI
from src.domain.users.api import router as users_router

def load_routes(app: FastAPI) -> None:
    app.include_router(users_router)
