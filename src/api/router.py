from fastapi import FastAPI

from src.domain.auth.api import router as auth_router
from src.domain.categories.api import router as categories_router
from src.domain.users.api import router as users_router
from src.domain.accounts.api import router as accounts_router
from src.domain.transactions.api import router as transactions_router




def load_routes(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(categories_router)
    app.include_router(accounts_router)
    app.include_router(transactions_router)

