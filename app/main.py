from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.routers.auth import router as auth_router
from app.routers.book import router as books_router
from app.routers.borrow import router as borrow_router
from app.routers.reader import router as readers_router
from app.routers.user import router as user_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(auth_router)

protected_deps = [Depends(get_current_user)]
app.include_router(user_router, dependencies=protected_deps)
app.include_router(books_router, dependencies=protected_deps)
app.include_router(readers_router, dependencies=protected_deps)
app.include_router(borrow_router, dependencies=protected_deps)


@app.get("/health/db")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok"}
