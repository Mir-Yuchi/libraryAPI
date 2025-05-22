from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, conint


class BorrowBase(BaseModel):
    """
    Base model for book borrowing/return operations.
    """

    book_id: conint(gt=0)
    reader_id: conint(gt=0)


class BorrowCreate(BorrowBase):
    """
    Model for borrowing a book.
    """

    # Inherits book_id and reader_id validation from BorrowBase
    pass


class ReturnCreate(BorrowBase):
    """
    Model for returning a borrowed book.
    """

    # Inherits book_id and reader_id validation from BorrowBase
    pass


class BorrowOut(BorrowBase):
    """
    Output model for a borrowed book record.
    """

    id: int
    borrow_date: datetime
    return_date: datetime | None

    class Config:
        from_attributes = True
