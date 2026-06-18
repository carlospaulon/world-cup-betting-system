from fastapi import FastAPI, Depends
from .core.config import Settings, get_settings
from .core.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()


@app.get('/info')
def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        'app.name': settings.APP_NAME
    }

@app.get('/health')
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}