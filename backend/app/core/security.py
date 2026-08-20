import re
import uuid
import bcrypt
from typing import Annotated
from app.core.config import get_settings
from datetime import datetime, UTC, timedelta
from fastapi import HTTPException, status, Depends
from app.models.user import User
from sqlalchemy.orm import Session
from app.repositories.user_repository import user_repository
from app.core.database import get_db
from fastapi.security import OAuth2PasswordBearer
from app.core.exceptions import WeakPasswordException, InvalidCredentialsException, UserInactiveException
from jose import jwt, JWTError

settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def validate_password_strength(password: str) -> str:
        # Tamanho da senha verificada na entidade/schema
        if not re.search(r"[A-Z]", password):
            raise WeakPasswordException("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[a-z]", password):
            raise WeakPasswordException("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r"\d", password):
            raise WeakPasswordException("A senha deve conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise WeakPasswordException("A senha deve conter pelo menos um caractere especial.")
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
        raise InvalidCredentialsException(
            message="Invalid or expire token",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    payload = decode_token(token)
    user_id: str = payload.get("sub")

    user = user_repository.get_by_id(db, uuid.UUID(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    if not user.is_active:
        raise UserInactiveException()
    
    return user # Por enquanto até retornar o schema



def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin access required"
        )
    
    return current_user
