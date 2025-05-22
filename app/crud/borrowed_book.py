from datetime import datetime, timezone

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.borrowed_book import BorrowedBook
from app.models.reader import Reader
from app.schemas.borrow import BorrowCreate, ReturnCreate


def get_borrow(db: Session, borrow_id: int):
    """
    Retrieve a borrow record by its ID.
    """
    return db.query(BorrowedBook).filter(BorrowedBook.id == borrow_id).first()


def get_active_borrows_by_reader(db: Session, reader_id: int):
    """
    Get all active borrow records for a reader.
    """
    return (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.reader_id == reader_id,
            BorrowedBook.return_date.is_(None),
        )
        .all()
    )


def borrow_book(db: Session, borrow_in: BorrowCreate):
    """
    Issue a book to a reader if business rules allow.

    Rules:
    1) copies_available > 0
    2) reader has fewer than 3 active borrows
    """
    book = db.query(Book).filter(Book.id == borrow_in.book_id).first()
    if not book:
        raise NoResultFound(f"Book id={borrow_in.book_id} not found")
    reader = db.query(Reader).filter(Reader.id == borrow_in.reader_id).first()
    if not reader:
        raise NoResultFound(f"Reader id={borrow_in.reader_id} not found")

    if book.copies_available < 1:
        raise ValueError("No copies available for this book")

    active = get_active_borrows_by_reader(db, borrow_in.reader_id)
    if len(active) >= 3:
        raise ValueError("Reader has reached the maximum of 3 borrowed books")

    book.copies_available -= 1
    borrow = BorrowedBook(
        book_id=borrow_in.book_id,
        reader_id=borrow_in.reader_id,
    )
    db.add(borrow)
    db.flush()
    db.commit()
    db.refresh(borrow)
    return borrow


def return_book(db: Session, return_in: ReturnCreate):
    """
    Return a borrowed book and update records.

    Rules:
    3) Cannot return if not borrowed or already returned
    """
    borrow = (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.book_id == return_in.book_id,
            BorrowedBook.reader_id == return_in.reader_id,
            BorrowedBook.return_date.is_(None),
        )
        .first()
    )
    if not borrow:
        raise NoResultFound(
            f"No active borrow found for book={return_in.book_id} and reader={return_in.reader_id}"
        )

    borrow.return_date = datetime.now(timezone.utc)
    book = db.query(Book).filter(Book.id == return_in.book_id).first()
    book.copies_available += 1

    db.flush()
    db.commit()
    db.refresh(borrow)
    return borrow
