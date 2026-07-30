from fastapi import APIRouter, status, Depends
from app.schemas.user import UserResponse, UserUpdatePassword
from sqlalchemy.orm import Session
from app.models import User
from app.core.security import get_current_user
from app.core.database import get_db
from app.repositories.user_repository import user_repository
from app.repositories.bet_repository import bet_repository
from app.services.user_service import UserService
from app.core.security import get_current_admin

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

@router.get(
    "/admin/users" # ajustar rota
)
def get_users_status(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return user_repository.get_users_actives(db)

@router.get(
    "/admin/users/all"
)
def get_all_users(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = user_repository.get_all(db)
    print(users)
    return users

@router.get(
    "/admin/users/{cpf}"
)
def get_users_by_cpf(cpf: str, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return user_repository.get_by_cpf(db, cpf) # tratar no service

