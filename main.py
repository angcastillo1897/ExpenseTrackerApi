from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.settings import settings
from src.core.exceptions import exception_handlers
from src.routes import load_routes

app: FastAPI = FastAPI(
    title="EXPENSE TRACKER API",
    description="API for managing EXPENSE TRACKER APP",
    version="0.1.0",
    contact={"email": "angcastillo18@gmail.com", "name": "Angelo Castillo"},
    exception_handlers=exception_handlers,
    root_path=settings.ROOT_PATH,
)


@app.exception_handler(RequestValidationError)
def request_validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": str(exc), "data": exc.errors()},
    )


load_routes(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
