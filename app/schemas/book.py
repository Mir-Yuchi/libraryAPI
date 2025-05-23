from __future__ import annotations

from pydantic import BaseModel, conint


class BookBase(BaseModel):
    """
    Base model for Book.
    """

    title: str
    author: str
    year: int | None = None
    isbn: str | None = None
    description: str | None = None


class BookCreate(BookBase):
    """
    Book creation model.
    """

    copies_available: conint(ge=0) = 1
    description: str | None = None


class BookUpdate(BaseModel):
    """
    Book update model.
    This model is used for updating book information.
    """

    title: str | None = None
    author: str | None = None
    year: int | None = None
    isbn: str | None = None
    copies_available: int | None = None
    description: str | None = None


class BookOut(BookBase):
    """
    Book output model.
    This model is used for returning book information.
    """

    id: int
    copies_available: int
    description: str | None = None

    class Config:
        from_attributes = True
