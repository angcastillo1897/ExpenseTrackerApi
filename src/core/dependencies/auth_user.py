from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.dependencies.async_bd import AsyncSessionDepends
from src.core.exceptions import ForbiddenException, UnAuthorizedException
from src.core.utils.token import verify_jwt_token
from src.domain.users import repository as user_repository
from src.domain.users.types import UserSerializer

# Security scheme to extract Bearer token
security = HTTPBearer()
SecurityDepends = Annotated[HTTPAuthorizationCredentials, Depends(security)]


async def get_current_user(
    credentials: SecurityDepends,
    db: AsyncSessionDepends,
):
    """
    Dependency to get current authenticated user from JWT token
    """

    try:
        token = credentials.credentials

        payload = verify_jwt_token(token)

        # Extract user_id from token payload
        user_id: int = int(payload.get("sub"))

        if user_id is None:
            raise UnAuthorizedException("Could not validate credentials")

        # Check token expiration (jwt.decode already does this, but explicit check)
        exp = payload.get("exp")

        if exp and datetime.now(timezone.utc).timestamp() > float(exp):
            raise UnAuthorizedException("Could not validate credentials")

    except jwt.PyJWTError as e:
        print("EXCEPTION", e)
        raise UnAuthorizedException("Could not validate credentials")

    db_user = await user_repository.get_user_by_id(db, user_id)
    if db_user is None:
        raise UnAuthorizedException("Could not validate credentials")

    if not db_user.is_active:
        raise ForbiddenException()

    return UserSerializer.model_validate(db_user)


AuthUserDepends = Annotated[UserSerializer, Depends(get_current_user)]
