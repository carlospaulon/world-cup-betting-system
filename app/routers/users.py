from fastapi import APIRouter, status, Depends
from app.schemas.user import UserResponse, UserUpdatePassword
from sqlalchemy.orm import Session
from app.models import User
from app.core.security import get_current_user
from app.core.database import get_db
from app.repositories.user_repository import user_repository
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def get_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch(
    "/me/password",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def update_password(password_update: UserUpdatePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_service = UserService()
    return user_service.update_password(db, current_user.id, password_update)

@router.patch(
    "/me/deactivate"
)
def deactivate_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_repository.deactivate(db, current_user.id)

@router.get(
    "/me/points"
)
def get_points(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_repository.get_points(db, current_user.cpf)

@router.get(
    "/me/points/ranking"
)
def get_ranking(db: Session = Depends(get_db)):
    return user_repository.get_ranking(db)
