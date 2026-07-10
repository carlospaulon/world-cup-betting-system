from fastapi import APIRouter, status, Depends
from app.schemas.user import UserResponse, UserCreate
from app.schemas.auth import Token, LoginRequest
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.services.user_service import UserService

# Autenticao

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
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user_service = AuthService()

    token = user_service.login(db, data)

    return token