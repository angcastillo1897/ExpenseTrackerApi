from fastapi import Request, status
from fastapi.responses import JSONResponse

from .base import BaseExceptionCustom


class BadRequestException(BaseExceptionCustom):
    def __init__(self, message: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, message=message)


async def raise_bad_exception(_: Request, exception: BadRequestException):
    return JSONResponse(status_code=exception.status_code, content=exception.respuesta)
