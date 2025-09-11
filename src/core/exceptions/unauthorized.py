from fastapi import Request, status
from fastapi.responses import JSONResponse

from .base import BaseExceptionCustom


class UnAuthorizedException(BaseExceptionCustom):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, message=message)


async def raise_unauthorized_exception(_: Request, exception: UnAuthorizedException):
    return JSONResponse(status_code=exception.status_code, content=exception.respuesta)
