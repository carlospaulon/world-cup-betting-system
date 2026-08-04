from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from .core.config import Settings, get_settings
from .core.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from .core.exceptions import AppException
from app.routers import auth, users, matches, bets

app = FastAPI(
    title="World Cup Betting System",
    description="Worldcup Betting System using FastAPI, PostgreSQL, and Docker",
    version="1.0.0",
    contact={
        "name": "Carlos Paulon",
        "url": "https://www.linkedin.com/in/carlospaulon/",
        "email": "paulonluis222@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


@app.exception_handler(AppException)
def global_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        headers=getattr(exc, 'headers', None),
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
        }
    )

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(matches.router)
app.include_router(bets.router)


@app.get('/info')
def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        'app.name': settings.APP_NAME
    }

@app.get('/health')
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}