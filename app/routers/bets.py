import uuid
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.schemas.bet import BetResponse, BetCreate, BetWithMatchResponse, BetMultiply
from app.core.security import get_current_user
from app.models.user import User
from app.core.database import get_db
from app.services.bet_service import BetService
from app.repositories.bet_repository import bet_repository


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
    return bet_service.create_bet(db, current_user, bet)

@router.get(
    "/bets",
    response_model=list[BetWithMatchResponse],
    status_code=status.HTTP_200_OK
)
def get_bets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return bet_service.get_user_bets(db, current_user)

@router.get(
    "/bets/{bet_id}",
    response_model=BetWithMatchResponse, # Tá retornando Bet
    status_code=status.HTTP_200_OK
)
def get_bet_by_id(bet_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return bet_service.get_bet_by_id(db, bet_id, current_user)

@router.patch(
    "/bets/{bet_id}/multiply",
    response_model=BetResponse,
)
def update_multiply_bet(bet_id: uuid.UUID, factor: BetMultiply , current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return bet_service.multiply_bet(db, current_user, bet_id, factor.factor)