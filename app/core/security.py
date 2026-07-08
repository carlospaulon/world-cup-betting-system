import re
import bcrypt
from typing import Annotated
from app.core.config import get_settings
from datetime import datetime, UTC, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#Declaro como classmethod?
@classmethod 
def validate_password_strength(cls, password: str) -> str:
        """Verifica se a senha atende aos requisitos de complexidade."""
        # Tamanho da senha verificada na entidade/schema?
        if not re.search(r"[A-Z]", password):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[a-z]", password):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r"\d", password):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("A senha deve conter pelo menos um caractere especial.")
        return password

#Bcrypt - hashed passwrod
def hash_password(plain_password) -> str:
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

#JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expire token",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Evoluir depois com DB = db: AsyncSession = Depends(get_db) e buscar o User pelo sub do payload — retornando o objeto completo ou 404.
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return username # Por enquanto até retornar o schema

# Criar get_current_admin