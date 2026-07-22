import uuid
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from app.models.bet import Bet
from app.models.enum.bet_enum import BetPrediction, BetStatus, BetResult

class BetRepository(BaseRepository[Bet]):
    def __init__(self):
        super().__init__(Bet)

    def create(self, session: Session, bet: Bet) -> Bet:
        session.add(bet)
        session.commit()
        session.refresh(bet)
        return bet

    def get_by_user(self, session: Session, user_id: uuid.UUID) -> list[Bet]:
        ...

    def get_pending_by_match(self, session: Session, match_id: int) -> list[Bet]:
        ...

    def count_by_prediction(self, session: Session, match_id: int, prediction: BetPrediction) -> int:
        ...

    def update_result(self, session: Session, bet_id: uuid.UUID, result: BetResult, status: BetStatus) -> Bet:
        ...

    def get_user_wins(self, session: Session, user_id: uuid.UUID) -> int:
        ...