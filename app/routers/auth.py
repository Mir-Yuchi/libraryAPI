from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.auth.security import verify_password
from app.core.config import settings
from app.crud.user import create_user, get_user_by_email
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    :param user_in: UserCreate schema with email, password, is_active flag
    :param db: Database session
    :return: The created UserOut schema
    :raises HTTPException: 409 if email already exists
    """
    if get_user_by_email(db, str(user_in.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = create_user(db, user_in)
    return UserOut.model_validate(user)


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    """
    Authenticate user and return JWT access token.

    Uses OAuth2 form with 'username' as email and 'password'.
    :param form_data: OAuth2PasswordRequestForm containing username and password
    :param db: Database session
    :return: Token schema with access_token and token_type
    :raises HTTPException: 401 if credentials are invalid
    """
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
