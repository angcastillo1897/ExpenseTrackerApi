from fastapi import Request, status
from fastapi.responses import JSONResponse

from .base import BaseExceptionCustom


class ForbiddenException(BaseExceptionCustom):
    def __init__(
        self, message: str = "Usted no tiene privilegios para esta acción"
    ) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, message=message)


async def raise_forbidden_exception(_: Request, exception: ForbiddenException):
    return JSONResponse(status_code=exception.status_code, content=exception.respuesta)
