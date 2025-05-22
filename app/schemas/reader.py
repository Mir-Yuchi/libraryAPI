from __future__ import annotations

from pydantic import BaseModel, EmailStr


class ReaderBase(BaseModel):
    """
    Base model for a reader.
    """

    name: str
    email: EmailStr


class ReaderCreate(ReaderBase):
    """
    Model for creating a new reader.
    """

    name: str
    email: EmailStr


class ReaderUpdate(ReaderBase):
    """
    Model for updating an existing reader.
    """

    name: str | None = None
    email: EmailStr | None = None


class ReaderOut(ReaderBase):
    """
    Model for outputting reader information.
    """

    id: int

    class Config:
        from_attributes = True
