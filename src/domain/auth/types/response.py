from src.domain.users.types import UserSerializer

from .schema import TokensBase


class LoginResponse(TokensBase):
    user: UserSerializer


class RegisterResponse(TokensBase):
    user: UserSerializer
