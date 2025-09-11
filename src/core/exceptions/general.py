from fastapi import Request, status
from fastapi.responses import JSONResponse

from .base import BaseExceptionCustom


class GeneralException(BaseExceptionCustom):
    def __init__(self, message: str) -> None:
        super().__init__(status.HTTP_409_CONFLICT, message=message)


async def raise_general_exception(_: Request, exception: GeneralException):
    return JSONResponse(status_code=exception.status_code, content=exception.respuesta)
