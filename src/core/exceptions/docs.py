"""
this module contain data type to openApi schemas in exceptions
"""

from pydantic import BaseModel


class ExceptionBase(BaseModel):
    message: str


class NotFoundException(ExceptionBase): ...


class BadRequestException(ExceptionBase): ...


class UnAuthorizedException(ExceptionBase): ...


class ForbiddenException(ExceptionBase): ...


class UnprocessableException(ExceptionBase): ...


class GeneralException(ExceptionBase): ...
