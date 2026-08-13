import uuid
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_current_admin, get_current_user
from app.core.database import get_db
from app.services.statistics_service import StatisticsService

router = APIRouter(
    prefix="/statistics",
    tags=["statistics"]
)

statistics_service = StatisticsService()

@router.get(
    "/admin/matches/{match_id}",
    status_code=status.HTTP_200_OK
)
def get_matches_statistics(match_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return statistics_service.get_match_stats(db, match_id)

# vejo as stats do meu user
@router.get(
    "/users/me",
    status_code=status.HTTP_200_OK
)
def get_user_statistics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return statistics_service.get_user_stats(db, current_user.id)

@router.get(
    "/admin/system",
    status_code=status.HTTP_200_OK
)
def get_system_statistics(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return statistics_service.get_system_stats(db)

@router.get(
    "/team",
    status_code=status.HTTP_200_OK
)
def get_team_statistics(team: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return statistics_service.get_team_stats(db, team)
