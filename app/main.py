from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/health/db")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for the database.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
