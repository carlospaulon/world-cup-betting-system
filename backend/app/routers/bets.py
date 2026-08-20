import uuid
from fastapi import APIRouter, status, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.bet import BetResponse, BetCreate, BetWithMatchResponse, BetMultiply
from app.core.security import get_current_user
from app.models.user import User
from app.core.database import get_db
from app.services.bet_service import BetService
from app.schemas.bet import BetStatus
from app.repositories.bet_repository import bet_repository
from app.repositories.user_repository import UserRepository


router = APIRouter(
    tags=["bets"]
)

bet_service = BetService()

@router.post(
    "/bets",
    response_model=BetResponse,
    status_code=status.HTTP_201_CREATED
)
def create_bet(bet: BetCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Place a new bet on an available match.

    - **match_id**: ID of the target match (must be TIMED and available for betting)
    - **prediction**: Outcome prediction (HOME_WIN, AWAY_WIN, or DRAW)
    - **points_bet**: Amount of points wagered (must not exceed user available balance)

    Returns:
    - **BetResponse**: Placed bet details including dynamic odds calculated at creation time.
    """

    return bet_service.create_bet(db, current_user, bet)

@router.get(
    "/bets",
    response_model=list[BetWithMatchResponse],
    status_code=status.HTTP_200_OK
)
def get_bets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), bet_status: Optional[BetStatus] = Query(None, description="Bet Status")):
    """
    Retrieve all bets placed by the authenticated user.

    - **bet_status**: Optional filter query parameter (e.g., PENDING or SETTLED)

    Returns:
    - **list[BetWithMatchResponse]**: List of user bets augmented with home and away team names.
    """

    return bet_service.get_user_bets(db, current_user, bet_status)


@router.get(
    "/bets/{bet_id}",
    response_model=BetWithMatchResponse, # Tá retornando Bet
    status_code=status.HTTP_200_OK
)
def get_bet_by_id(bet_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve details of a specific bet by UUID.

    - **bet_id**: Unique UUID identifier of the bet

    Returns:
    - **BetWithMatchResponse**: Detailed bet information combined with match details.
    """

    return bet_service.get_bet_by_id(db, bet_id, current_user)

@router.patch(
    "/bets/{bet_id}/multiply",
    response_model=BetResponse,
)
def update_multiply_bet(bet_id: uuid.UUID, factor: BetMultiply , current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Multiply wagered points on an existing pending bet.

    - **bet_id**: Target bet UUID
    - **factor**: Multiplication integer factor (e.g., 2, 3)

    Returns:
    - **BetResponse**: Updated bet instance with new wagered points total.
    """

    return bet_service.multiply_bet(db, current_user, bet_id, factor.factor)
