from typing import List, Optional

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.security import get_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: EmailStr) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=str(user_in.email),
        password=get_password(user_in.password),
        is_active=user_in.is_active,
    )
    db.add(db_user)
    try:
        db.flush()
        return db_user
    except IntegrityError:
        db.rollback()
        raise


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    data = user_in.model_dump(exclude_unset=True)
    if "password" in data:
        db_user.password = get_password(data.pop("password"))
    if "email" in data:
        db_user.email = str(data["email"])
    if "is_active" in data:
        db_user.is_active = data["is_active"]

    try:
        db.flush()
        return db_user
    except IntegrityError:
        db.rollback()
        raise


def delete_user(db: Session, user_id: int) -> None:
    db_user = get_user(db, user_id)
    if not db_user:
        return
    db.delete(db_user)
    db.flush()
