from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class Reader(Base):
    __tablename__ = "readers"
    __table_args__ = (UniqueConstraint("email", name="uq_readers_email"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)

    borrowed_records = relationship(
        "BorrowedBook", back_populates="reader", cascade="all, delete-orphan"
    )
