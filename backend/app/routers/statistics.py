from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_current_admin, get_current_user
from app.core.database import get_db
from app.services.statistics_service import StatisticsService
from app.schemas.statistics import TeamStats, SystemStats, MatchStats, UserStats

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"]
)

statistics_service = StatisticsService()

# vejo as stats do meu user
@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK,
    response_model=UserStats
)
def get_user_statistics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return statistics_service.get_user_stats(db, current_user.cpf)

@router.get(
    "/team",
    status_code=status.HTTP_200_OK,
    response_model=TeamStats
)
def get_team_statistics(team: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return statistics_service.get_team_stats(db, team)

@router.get(
    "/admin/system",
    status_code=status.HTTP_200_OK,
    response_model=SystemStats
)
def get_system_statistics(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return statistics_service.get_system_stats(db)

@router.get(
    "/admin/matches/{match_id}",
    status_code=status.HTTP_200_OK,
    response_model=MatchStats
)
def get_matches_statistics(match_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return statistics_service.get_match_stats(db, match_id)

@router.get(
    "/admin/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserStats
)
def get_user_statistics_admin(cpf: str, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return statistics_service.get_user_stats(db, cpf)