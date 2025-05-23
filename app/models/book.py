from sqlalchemy import (CheckConstraint, Column, Integer, String, Text,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        UniqueConstraint("title", name="uq_books_title"),
        CheckConstraint("copies_available >= 0", name="ck_books_copies_nonnegative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    isbn = Column(String, nullable=True, unique=True, index=True)
    copies_available = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=True)

    borrowed_books = relationship(
        "BorrowedBook", back_populates="book", cascade="all, delete-orphan"
    )
