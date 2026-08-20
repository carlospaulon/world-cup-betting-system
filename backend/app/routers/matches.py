from fastapi import APIRouter, status, Depends, Query
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app.core.security import get_current_user, get_current_admin
from app.repositories.match_repository import match_repository
from app.services.match_service import MatchService
from app.schemas.match import MatchResponse
from app.models.enum.match_enum import MatchStatus
from app.schemas.bet import BetResponse
from app.core.database import get_db
from app.models.user import User
from app.models.match import Match
from app.repositories.bet_repository import bet_repository

router = APIRouter(
    tags=["matches"]
)

# retornando partidas em aberto (sem parametro) e partidas finalizadas (com parametro)
@router.get(
    "/matches",
    response_model=list[MatchResponse],
    status_code=status.HTTP_200_OK
)
def get_matches(
    db: Session = Depends(get_db), 
    competition: Optional[str] = Query('WC', description="Filter by competition"),
    team: Optional[str] = Query(None, description="Filter by home or away team"), 
    match_status: Optional[MatchStatus] = Query(None, description="Match Status "),
    is_bet_available: Optional[bool] = Query(None, description="Filter matches available for betting"),
    stage: Optional[str] = Query(None, description="Match Stage"),
    from_date: Optional[date] = Query(None, description="From Date (AAAA-MM-DD)"),
    to_date: Optional[date] = Query(None, description="To Date (AAAA-MM-DD)"),
    ):
    """
    Retrieve matches matching specified filter criteria.

    Calculates dynamic odds for open matches.

    - **competition**: Target competition code (default: WC)
    - **team**: Optional search string for team names
    - **match_status**: Status filter (TIMED, IN_PLAY, FINISHED, POSTPONED)
    - **is_bet_available**: Filter by betting availability flag
    - **stage**: Competition stage filter
    - **from_date / to_date**: Date range filter

    Returns:
    - **list[MatchResponse]**: List of matches with calculated odds.
    """

    match_service = MatchService()

    
    return match_service.get_matches(
        db,
        competition,
        team,
        match_status,
        is_bet_available,
        stage,
        from_date,
        to_date
    )

@router.get(
    "/matches/history/{team}",
    response_model=list[MatchResponse],
    status_code=status.HTTP_200_OK
)
def get_team_history(team: str, db: Session = Depends(get_db)):
    """
    Retrieve historical finished matches for a specific team.

    - **team**: Target team name

    Returns:
    - **list[MatchResponse]**: List of past finished matches involving the team.
    """

    match_service = MatchService()

    return match_service.get_team_history(db, team)

# matches available com filtros

# pega partida por id de Match
@router.get(
    "/matches/{match_id}",
    response_model=MatchResponse,
    status_code=status.HTTP_200_OK
)
def get_matches(match_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details of a single match by ID.

    - **match_id**: Target match integer ID

    Returns:
    - **MatchResponse**: Detailed match entity data.
    """

    
    return match_repository.get_by_id(db, match_id)

# importa partidas da api para o banco (apenas o admin faz)
# import sem parâmetro (WC), com pega outra competição para import
@router.post(
    "/matches/admin/import",
    status_code=status.HTTP_201_CREATED
)
def import_matches(competition: str = Query('WC'), current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Import competition matches from external Football API (Admin only).

    - **competition**: Code of the competition to import (default: WC)

    Returns:
    - **dict**: Summary containing count of imported and ignored existing matches.
    """

    match_service = MatchService()
    return match_service.import_matches(db, competition)

@router.get(
    "/matches/admin/{id}/bets",
    status_code=status.HTTP_200_OK,
    response_model=list[BetResponse]
)
def get_match_bets(id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Retrieve all bets placed on a specific match (Admin only).

    - **id**: Target match ID

    Returns:
    - **list[BetResponse]**: List of all user bets associated with the match.
    """
    
    return bet_repository.get_bets_for_match(db, id)

@router.patch(
    "/matches/admin/{id}/finish",
)
def finish_match(id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Fetch external match results, update match score, and settle pending bets (Admin only).

    - **id**: Target match ID

    Returns:
    - **MatchResponse**: Updated match instance marked as FINISHED.
    """

    match_service = MatchService()

    return match_service.finish_match(db, id)

@router.patch(
    "/matches/admin/{match_id}/status"
)
def update_status(match_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Reset match status back to TIMED (Admin only).

    - **match_id**: Target match ID

    Returns:
    - **MatchResponse**: Updated match instance.
    """

    match_service = MatchService()

    return match_service.update_status(db, match_id)


@router.patch(
    "/matches/admin/{match_id}/availability"
)
def update_bet_availability(match_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """
    Toggle betting availability for a TIMED match (Admin only).

    - **match_id**: Target match ID

    Returns:
    - **MatchResponse**: Updated match instance with enabled betting availability.
    """

    match_service = MatchService()

    return match_service.update_bet_availability(db, match_id)
