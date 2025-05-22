from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.reader import Reader
from app.schemas.reader import ReaderCreate, ReaderUpdate


def get_reader(db: Session, reader_id: int) -> Optional[Reader]:
    """
    Get a reader by ID.
    """
    return db.query(Reader).filter(Reader.id == reader_id).first()


def get_reader_by_email(db: Session, email: str) -> Optional[Reader]:
    """
    Get a reader by email.
    """
    return db.query(Reader).filter(Reader.email == email).first()


def get_readers(db: Session, skip: int = 0, limit: int = 100) -> List[Reader]:
    """
    Get a list of readers.
    """
    return db.query(Reader).offset(skip).limit(limit).all()  # type: ignore


def create_reader(db: Session, reader_in: ReaderCreate) -> Reader:
    """
    Create a new reader.
    """
    existing = get_reader_by_email(db, str(reader_in.email))
    if existing:
        raise ValueError(f"Reader with email {reader_in.email} already exists.")

    db_reader = Reader(
        name=reader_in.name,
        email=str(reader_in.email),
    )
    db.add(db_reader)
    db.flush()
    db.refresh(db_reader)
    return db_reader


def update_reader(db: Session, db_reader: Reader, reader_in: ReaderUpdate) -> Reader:
    """
    Update an existing reader.
    """
    data = reader_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_reader, field, value)
    db.flush()
    db.refresh(db_reader)
    return db_reader


def delete_reader(db: Session, reader_id: int) -> None:
    """
    Delete a reader by ID.
    """
    reader = get_reader(db, reader_id)
    if not reader:
        raise NoResultFound(f"Reader with ID={reader_id} not found.")
    db.delete(reader)
    db.flush()
