from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(
    data: Dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token with an expiration time.

    :param data: A dict of data to include in the token payload
    :param expires_delta: A timedelta for token expiration; if provided, it overrides the default
                          expiration time from settings.access_token_expire_minutes.
    :return: Encoded JWT as a string.
    """
    to_encode = data.copy()
    expire_time = (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    expire = datetime.now(timezone.utc) + expire_time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT access token.

    :param token: The JWT token to decode
    :return: The decoded payload as a dict
    :raises JWTError: If the token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        raise e
