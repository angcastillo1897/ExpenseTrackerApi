from fastapi import Request, status
from fastapi.responses import JSONResponse

from .base import BaseExceptionCustom


class UnprocessableException(BaseExceptionCustom):
    def __init__(self, message: str, data: dict | list | None = None) -> None:
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY, message=message, data={"detail": data}
        )


async def raise_unprocessable_entity_exception(
    _: Request, exception: UnprocessableException
):
    return JSONResponse(status_code=exception.status_code, content=exception.respuesta)
