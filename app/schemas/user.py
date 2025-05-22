from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base model for user.
    """

    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    """
    User creation model.
    """

    password: str


class UserUpdate(BaseModel):
    """
    User update model.
    This model is used for updating user information.
    """

    email: EmailStr | None = None
    is_active: bool | None = None
    password: str | None = None


class UserOut(UserBase):
    """
    User output model.
    This model is used for returning user information.
    """

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
