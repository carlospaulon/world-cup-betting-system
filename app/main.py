from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from .core.config import Settings, get_settings
from .core.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from .core.exceptions import AppException

app = FastAPI()

# Separar a camada de exception handler em core e chamar no main o def handler.

@app.exception_handler(AppException)
def global_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
        }
    )


@app.get('/info')
def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        'app.name': settings.APP_NAME
    }

@app.get('/health')
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}