from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    reader_id = Column(
        Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False
    )
    borrow_date = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    return_date = Column(TIMESTAMP(timezone=True), nullable=True)

    book = relationship("Book", back_populates="borrowed_books")
    reader = relationship("Reader", back_populates="borrowed_records")
