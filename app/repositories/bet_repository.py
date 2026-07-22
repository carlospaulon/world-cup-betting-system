import uuid
from app.repositories.base_repository import BaseRepository
from sqlalchemy import select, update, func, and_
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
        query = select(self.model).where(self.model.user_id == user_id)
        result = session.execute(query)

        return result.scalars().all()

    def get_pending_by_match(self, session: Session, match_id: int) -> list[Bet]:
        query = select(self.model).where(and_(
            self.model.match_id == match_id,
            self.model.status == BetStatus.PENDING
        ))
        result = session.execute(query)

        return result.scalars().all()

    def count_by_prediction(self, session: Session, match_id: int, prediction: BetPrediction) -> int:
        query = select(func.count()).where(and_(
            self.model.match_id == match_id,
            self.model.prediction == prediction
        ))
        result = session.execute(query)

        return result.scalar()

    def update_result(
            self, 
            session: Session, 
            bet_id: uuid.UUID, 
            result: BetResult, 
            status: BetStatus
            ) -> Bet | None:
        
        query = update(self.model).where(self.model.id == bet_id).values(
            result=result,
            status=status
        )

        session.execute(query)
        session.commit()

        return self.get_by_id(session, bet_id)

    def get_user_wins(self, session: Session, user_id: uuid.UUID) -> int:
        query = select(func.count()).where(and_(
            self.model.user_id == user_id,
            self.model.result == BetResult.WON
        ))

        result = session.execute(query)

        return result.scalar()

bet_repository = BetRepository()