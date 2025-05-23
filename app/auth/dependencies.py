from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.crud.user import get_user
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Dependency to get the current authenticated user from the JWT token.

    :param token: The JWT token from the request
    :param db: DB session
    :return: Pydentic UserOut model of the authenticated user
    :raises HTTPException: 401 if the token is invalid, or user not found
    """

    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    user = get_user(db, user_id=user_id)
    if not user:
        raise credentials_exception

    return user
