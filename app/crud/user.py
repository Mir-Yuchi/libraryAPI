from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.auth.security import get_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> User | None:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users."""
    return db.query(User).offset(skip).limit(limit).all()  # type: ignore


def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user."""
    hashed_pw = get_password(user_in.password)
    db_user = User(
        email=str(user_in.email),
        password=hashed_pw,
        is_active=user_in.is_active,
    )
    db.add(db_user)
    db.flush()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    """Update user information."""
    if user_in.email is not None:
        db_user.email = user_in.email
    if user_in.is_active is not None:
        db_user.is_active = user_in.is_active
    if user_in.password:
        db_user.hashed_password = get_password(user_in.password)
    db.flush()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    """Delete user by ID."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise NoResultFound(f"User with id={user_id} not found")
    db.delete(db_user)
    db.flush()
