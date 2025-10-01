import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from src.core.exceptions import UnAuthorizedException
from src.domain.auth import schemas as auth_schemas
from src.settings import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)


#! TODO : IMPROVE
def generate_password_reset_token() -> str:
    password_reset_token = generate_refresh_token()
    password_reset_token_hash = hash_token(password_reset_token)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.RESET_TOKEN_EXPIRE_MINUTES
    )
    return


def prepare_refresh_token_creation(
    user_id: int, device_info: str = None, ip_address: str = None
) -> auth_schemas.CreateRefreshToken:
    refresh_token = generate_refresh_token()
    refresh_token_hash = hash_token(refresh_token)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    refresh_token_data = auth_schemas.CreateRefreshToken(
        user_id=user_id,
        token_hash=refresh_token_hash,
        device_info=device_info,
        ip_address=ip_address,
        expires_at=expires_at,
    )

    return refresh_token_data


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise UnAuthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnAuthorizedException("Invalid token")
