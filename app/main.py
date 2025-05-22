from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.routers.book import router as book_router
from app.routers.borrow import router as borrow_router
from app.routers.reader import router as readers_router
from app.routers.user import router as user_router

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(user_router)
app.include_router(book_router)
app.include_router(readers_router)
app.include_router(borrow_router)


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
