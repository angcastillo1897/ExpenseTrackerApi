"""
this exceptions are used as response in FASTAPI
"""

from .bad_request import BadRequestException, raise_bad_exception
from .forbidden_exception import ForbiddenException, raise_forbidden_exception
from .general import GeneralException, raise_general_exception
from .not_found import NotFoundException, raise_not_found_exception
from .unauthorized import UnAuthorizedException, raise_unauthorized_exception
from .unprocessable_entity import (
    UnprocessableException,
    raise_unprocessable_entity_exception,
)

exception_handlers: dict = {
    GeneralException: raise_general_exception,
    UnprocessableException: raise_unprocessable_entity_exception,
    NotFoundException: raise_not_found_exception,
    BadRequestException: raise_bad_exception,
    UnAuthorizedException: raise_unauthorized_exception,
    ForbiddenException: raise_forbidden_exception,
}
