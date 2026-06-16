from fastapi import FastAPI, Depends
from .core.config import Settings, get_settings

app = FastAPI()


@app.get('/info')
def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        'app.name': settings.APP_NAME
    }