from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.crud.borrowedBook import (borrow_book, get_active_borrows_by_reader,
                                   return_book)
from app.db.session import get_db
from app.schemas.borrow import BorrowCreate, BorrowOut, ReturnCreate

router = APIRouter(prefix="/borrow", tags=["borrow"])


@router.post("/", response_model=BorrowOut, status_code=status.HTTP_201_CREATED)
def borrow_book_endpoint(borrow_in: BorrowCreate, db: Session = Depends(get_db)):
    """
    Borrow a book for a reader, enforcing business rules.
    """
    try:
        borrow = borrow_book(db, borrow_in)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return borrow


@router.post("/return", response_model=BorrowOut)
def return_book_endpoint(
    return_in: ReturnCreate, db: Session = Depends(get_db)
) -> BorrowOut:
    """
    Return a borrowed book and restore availability.
    """
    try:
        borrow = return_book(db, return_in)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return borrow


@router.get("/reader/{reader_id}", response_model=List[BorrowOut])
def read_active_borrows(
    reader_id: int, db: Session = Depends(get_db)
) -> List[BorrowOut]:
    """
    List all active borrows for a given reader.
    """
    borrows = get_active_borrows_by_reader(db, reader_id)
    return borrows
