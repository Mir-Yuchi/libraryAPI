from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    """
    JWT access token response model.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Data stored in JWT payload.
    """

    sub: str
    exp: datetime

    class Config:
        from_attributes = True
