from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.book import (create_book, delete_book, get_book, get_books,
                           update_book)
from app.db.session import get_db
from app.schemas.book import BookCreate, BookOut, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book_endpoint(book_in: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book.
    """
    db_book = create_book(db, book_in)
    return db_book


@router.get("/", response_model=List[BookOut])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of books with pagination.
    """
    books = get_books(db, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single book by ID.
    """
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.put("/{book_id}", response_model=BookOut)
def update_book_endpoint(
    book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing book by ID.
    """
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    updated = update_book(db, book, book_in)
    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a book by ID.
    """
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    delete_book(db, book_id)
