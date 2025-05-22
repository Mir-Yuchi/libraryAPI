from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.reader import (create_reader, delete_reader, get_reader,
                             get_readers, update_reader)
from app.db.session import get_db
from app.schemas.reader import ReaderCreate, ReaderOut, ReaderUpdate

router = APIRouter(prefix="/readers", tags=["readers"])


@router.post("/", response_model=ReaderOut, status_code=status.HTTP_201_CREATED)
def create_reader_endpoint(reader_in: ReaderCreate, db: Session = Depends(get_db)):
    """
    Create a new reader.
    """
    try:
        db_reader = create_reader(db, reader_in)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return db_reader


@router.get("/", response_model=List[ReaderOut])
def read_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of readers with pagination.
    """
    readers = get_readers(db, skip=skip, limit=limit)
    return readers


@router.get("/{reader_id}", response_model=ReaderOut)
def read_reader(reader_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single reader by ID.
    """
    reader = get_reader(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found",
        )
    return reader


@router.put("/{reader_id}", response_model=ReaderOut)
def update_reader_endpoint(
    reader_id: int, reader_in: ReaderUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing reader by ID.
    """
    db_reader = get_reader(db, reader_id)
    if not db_reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found",
        )
    updated = update_reader(db, db_reader, reader_in)
    return updated


@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader_endpoint(reader_id: int, db: Session = Depends(get_db)):
    """
    Delete a reader by ID.
    """
    reader = get_reader(db, reader_id)
    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reader not found",
        )
    delete_reader(db, reader_id)
