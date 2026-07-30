from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str = ''
    ALGORITHM: str = ''
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    API_KEY: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

@lru_cache
def get_settings():
    return Settings()