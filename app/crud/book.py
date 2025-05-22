from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Optional[Book]:
    """
    Retrieve a single book by its ID.
    """
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    """
    Retrieve multiple books with pagination.
    """
    return db.query(Book).offset(skip).limit(limit).all()  # type: ignore


def create_book(db: Session, book_in: BookCreate) -> Book:
    """
    Create a new book record.
    """
    db_book = Book(
        title=book_in.title,
        author=book_in.author,
        year=book_in.year,
        isbn=book_in.isbn,
        copies_available=book_in.copies_available,
    )
    db.add(db_book)
    db.flush()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, db_book: Book, book_in: BookUpdate) -> Book:
    """
    Update an existing book.
    """
    data = book_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_book, field, value)
    db.flush()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> None:
    """
    Delete a book by its ID.
    """
    book = get_book(db, book_id)
    if not book:
        raise NoResultFound(f"Book with id={book_id} not found")
    db.delete(book)
    db.flush()
