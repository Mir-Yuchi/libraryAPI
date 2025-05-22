from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.user import (create_user, delete_user, get_user,
                           get_user_by_email, get_users, update_user)
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def api_create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    try:
        return create_user(db, user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )


@router.get("/{user_id}", response_model=UserOut)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.get("/", response_model=list[UserOut])
def api_list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List users with pagination.
    """
    return get_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserOut)
def api_update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user by ID.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    try:
        return update_user(db, db_user, user_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user by ID.
    """
    if not get_user(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    delete_user(db, user_id)
    return None
