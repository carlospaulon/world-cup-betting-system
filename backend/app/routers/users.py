import uuid
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
    """
    Retrieve profile details of the currently authenticated user.

    Returns:
    - **UserResponse**: Profile details of the logged-in user.
    """

    return current_user

@router.patch(
    "/me/password",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
def update_password(password_update: UserUpdatePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Update password for the authenticated user account.

    - **current_password**: Current valid user password
    - **new_password**: New password meeting security criteria

    Returns:
    - **UserResponse**: Updated user account details.
    """

    user_service = UserService()
    return user_service.update_password(db, current_user.id, password_update)

@router.patch(
    "/me/deactivate"
)
def deactivate_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Deactivate (soft-delete) the authenticated user account.

    Returns:
    - **UserResponse**: Updated user instance marked with is_active = False.
    """

    return user_repository.deactivate(db, current_user.id)

@router.get(
    "/me/points"
)
def get_points(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Retrieve current total points balance for the authenticated user.

    Returns:
    - **int**: Numerical points balance.
    """

    return user_repository.get_points(db, current_user.cpf)

@router.get(
    "/me/points/ranking"
)
def get_ranking(db: Session = Depends(get_db)):
    """
    Fetch global leaderboard ranked by winning bets count and total points balance.

    Returns:
    - **list[dict]**: Ranked mapping containing nickname, points, and won bets count.
    """

    return user_repository.get_ranking(db)

@router.patch(
    "/admin/{user_id}/role",
)
def promote_to_admin(user_id: uuid.UUID, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Grant administrator privileges to a target user (Admin only).

    - **user_id**: Target user UUID

    Returns:
    - **UserResponse**: Updated user profile with administrator permissions.
    """

    user_service = UserService()
    return user_service.update_is_admin(db, current_admin, user_id)

@router.get(
    "/admin/users",
    response_model=list[UserResponse]
)
def get_users_status(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Retrieve list of all active user accounts (Admin only).

    Returns:
    - **list[UserResponse]**: List of active user records.
    """

    return user_repository.get_users_actives(db)

@router.get(
    "/admin/all", 
    response_model=list[UserResponse]
)
def get_all_users(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Retrieve all registered users in the system (Admin only).

    Returns:
    - **list[UserResponse]**: List of all registered users.
    """

    users = user_repository.get_all(db)
    print(users)
    return users

@router.get(
    "/admin/users/{cpf}",
    response_model=UserResponse
)
def get_users_by_cpf(cpf: str, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Lookup a user by Brazilian CPF identifier (Admin only).

    - **cpf**: Target user CPF string

    Returns:
    - **UserResponse**: Matching user account data.
    """

    return user_repository.get_by_cpf(db, cpf) # tratar no service
