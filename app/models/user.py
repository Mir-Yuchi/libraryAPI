from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, String,
                        UniqueConstraint, func)

from app.db.base import Base


class User(Base):
    """User model for authentication and authorization."""

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
