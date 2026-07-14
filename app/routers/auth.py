from fastapi import APIRouter, status, Depends
from app.schemas.user import UserResponse, UserCreate
from app.schemas.auth import Token, LoginRequest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from pydantic import SecretStr
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService()
    return user_service.register_user(db, user_in)

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    data = LoginRequest(
        email=form_data.username,
        password=SecretStr(form_data.password)
    )
    
    auth_service = AuthService()

    token = auth_service.login(db, data)

    return token