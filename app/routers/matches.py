from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user, get_current_admin
from app.repositories.match_repository import match_repository
from app.services.match_service import MatchService
from app.schemas.match import MatchResponse
from app.core.database import get_db
from app.models.user import User
from app.models.match import Match

router = APIRouter(
    tags=["matches"]
)

# retornando partidas em aberto (sem parametro) e partidas finalizadas (com parametro)
@router.get(
    "/matches",
    response_model=list[MatchResponse],
    status_code=status.HTTP_200_OK
)
def get_matches(db: Session = Depends(get_db), team: str | None = None):
    match_service = MatchService()

    if team:
        return match_service.get_team_history(db, team)
    
    return match_service.get_open_matches(db)

# pega partida por id de Match
@router.get(
    "/matches/{match_id}",
    response_model=MatchResponse,
    status_code=status.HTTP_200_OK
)
def get_matches(match_id: int, db: Session = Depends(get_db)):
    
    return match_repository.get_by_id(db, match_id)

@router.get(
        "/admin/matches/{id}/bets",
        status_code=status.HTTP_200_OK
)
def get_match_bets(id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    # TODO: Implementar busca de apostas por partida
    pass

# importa partidas da api para o banco (apenas o admin faz)
@router.post(
    "/admin/matches/import",
    status_code=status.HTTP_201_CREATED
)
def import_matches(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    match_service = MatchService()
    return match_service.import_matches(db)


@router.patch(
    "/admin/matches/{id}/finish",
)
def finish_match(id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    match_service = MatchService()


    return match_service.finish_match(db, id)

@router.patch(
    "/admin/matches/{match_id}/status"
)
def update_status(match_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    match_service = MatchService()

    return match_service.update_status(db, match_id)
