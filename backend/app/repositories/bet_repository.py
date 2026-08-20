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
        """
        Persist a new bet in the database.

        Args:
            session (Session): Current database session.
            bet (Bet): Bet entity instance to insert.

        Returns:
            Bet: Saved and refreshed Bet entity.
        """

        session.add(bet)
        session.commit()
        session.refresh(bet)
        return bet

    def get_by_user(self, session: Session, user_id: uuid.UUID) -> list[Bet]:
        """
        Retrieve all bets placed by a specific user.

        Args:
            session (Session): Current database session.
            user_id (uuid.UUID): Target user UUID.

        Returns:
            list[Bet]: List of user bets.
        """

        query = select(self.model).where(self.model.user_id == user_id)
        result = session.execute(query)

        return result.scalars().all()

    def filter_bets(self, session: Session, user_id: uuid.UUID, status: BetStatus):
        """
        Filter user bets by status.

        Args:
            session (Session): Current database session.
            user_id (uuid.UUID): Target user UUID.
            status (Optional[BetStatus]): Target status filter.

        Returns:
            list[Bet]: Matching list of bets.
        """

        query = select(self.model).where(self.model.user_id == user_id)

        if status is not None:
            query = query.where(status == self.model.status)

        result = session.execute(query)

        return result.scalars().all()


    def get_bets_for_match(self, session: Session, match_id: int) -> list[Bet]:
        """
        Fetch all bets associated with a given match.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.

        Returns:
            list[Bet]: List of bets placed on the match.
        """

        query = select(self.model).where(self.model.match_id == match_id)
        result = session.execute(query)
    
        return result.scalars().all()

    def get_pending_by_match(self, session: Session, match_id: int) -> list[Bet]:
        """
        Retrieve all PENDING bets for a specific match prior to settlement.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.

        Returns:
            list[Bet]: List of pending bets.
        """

        query = select(self.model).where(and_(
            self.model.match_id == match_id,
            self.model.status == BetStatus.PENDING
        ))
        result = session.execute(query)

        return result.scalars().all()

    def count_by_prediction(self, session: Session, match_id: int, prediction: BetPrediction) -> int:
        """
        Count total bets placed on a specific match prediction outcome.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.
            prediction (BetPrediction): Targeted outcome.

        Returns:
            int: Number of matching bets.
        """

        query = select(func.count(self.model.id)).where(and_(
            self.model.match_id == match_id,
            self.model.prediction == prediction
        ))
        result = session.execute(query)

        return result.scalar() or 0

    def update_result(
            self, 
            session: Session, 
            bet_id: uuid.UUID, 
            result: BetResult, 
            status: BetStatus
            ) -> Bet | None:
        """
        Update the settlement result and status of a bet.

        Args:
            session (Session): Current database session.
            bet_id (uuid.UUID): Target bet UUID.
            result (BetResult): Final bet outcome (WON, LOST, DRAW).
            status (BetStatus): Updated bet status (SETTLED).

        Returns:
            Bet | None: Updated Bet model instance.
        """
        
        
        query = update(self.model).where(self.model.id == bet_id).values(
            result=result,
            status=status
        )

        session.execute(query)
        session.commit()

        return self.get_by_id(session, bet_id)

    def update_bet_points(self, session: Session, bet_id: uuid.UUID, points_bet: int):
        """
        Update wagered points balance for a bet.

        Args:
            session (Session): Current database session.
            bet_id (uuid.UUID): Target bet UUID.
            points_bet (int): New total points wagered.

        Returns:
            Bet | None: Updated Bet model instance.
        """

        query = update(self.model).where(self.model.id == bet_id).values(
            points_bet=points_bet
        )

        session.execute(query)
        session.commit()

        return self.get_by_id(session, bet_id)

    def get_user_wins(self, session: Session, user_id: uuid.UUID) -> int:
        """
        Get the total count of won bets for a given user.

        Args:
            session (Session): Current database session.
            user_id (uuid.UUID): Target user UUID.

        Returns:
            int: Total won bets count.
        """

        query = select(func.count()).where(and_(
            self.model.user_id == user_id,
            self.model.result == BetResult.WON
        ))

        result = session.execute(query)

        return result.scalar()

bet_repository = BetRepository()