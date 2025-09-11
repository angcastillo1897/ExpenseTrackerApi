from fastapi import Request, status
from fastapi.responses import JSONResponse

from .base import BaseExceptionCustom


class NotFoundException(BaseExceptionCustom):
    def __init__(self, message: str) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, message=message)


async def raise_not_found_exception(_: Request, exception: NotFoundException):
    return JSONResponse(status_code=exception.status_code, content=exception.respuesta)
