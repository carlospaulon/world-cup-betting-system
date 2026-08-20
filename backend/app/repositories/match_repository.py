from typing import Optional
from datetime import datetime, time, timedelta
from app.repositories.base_repository import BaseRepository
from app.models.match import Match
from app.models.enum.match_enum import MatchStatus, MatchResult
from sqlalchemy import select, or_, update
from sqlalchemy.orm import Session

class MatchRepository(BaseRepository[Match]):
    def __init__(self):
        super().__init__(Match)

    def create(self, session: Session, match: Match) -> Match:
        """
        Persist a new Match entity.

        Args:
            session (Session): Current database session.
            match (Match): Match instance to be added.

        Returns:
            Match: Saved and refreshed Match model.
        """

        session.add(match)
        session.commit()
        session.refresh(match)
        return match
    
    def get_by_api_id(self, session: Session, api_match_id: str) -> Match | None:
        """
        Retrieve a match matching the external provider API ID.

        Args:
            session (Session): Current database session.
            api_match_id (str): Unique external provider ID.

        Returns:
            Match | None: Match entity if found, None otherwise.
        """

        query = select(self.model).where(self.model.api_match_id == api_match_id)
        result = session.execute(query)

        return result.scalars().first()
    
    def get_all_open(self, session: Session) -> list[Match]:
        """
        Retrieve all matches currently scheduled with status TIMED.

        Args:
            session (Session): Current database session.

        Returns:
            list[Match]: List of TIMED matches.
        """

        query = select(self.model).where(self.model.status == MatchStatus.TIMED)
        result = session.execute(query)

        return result.scalars().all()

    def filter_matches(
        self, 
        session: Session,
        competition: Optional[str] = None,
        team_name: Optional[str] = None,
        status: Optional[MatchStatus] = None,
        is_bet_available: Optional[bool] = None,
        stage: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
        ):
        """
        Filter matches with composite dynamic criteria.

        Args:
            session (Session): Current database session.
            competition (Optional[str]): Target competition code.
            team_name (Optional[str]): Partial string filter for team names.
            status (Optional[MatchStatus]): Status filter.
            is_bet_available (Optional[bool]): Availability filter.
            stage (Optional[str]): Competition stage filter.
            from_date (Optional[datetime]): Start date boundary.
            to_date (Optional[datetime]): End date boundary.

        Returns:
            list[Match]: Matching list of Match records.
        """
        query = select(self.model)
        filters = []

        if competition is not None:
            filters.append(self.model.competition == competition.upper())

        if team_name is not None:
            filters.append(or_(
                self.model.home_team.ilike(f'%{team_name}%'),
                self.model.away_team.ilike(f'%{team_name}%')
                ))

        if status is not None and self.model.is_bet_available:
            filters.append(self.model.status == status)

        if stage is not None:
            filters.append(self.model.stage == stage.upper())

        if from_date is not None:
            filters.append(self.model.match_date >= datetime.combine(from_date, time.min)) # transformo em datetime min

        if to_date is not None:
            next_day = to_date + timedelta(days=1) # pego exatamente na data do to_date passado

            filters.append(self.model.match_date < datetime.combine(next_day, time.min))

        if is_bet_available is not None:
            filters.append(
                self.model.is_bet_available == is_bet_available
            )

        if filters:
            query = query.where(*filters)

        result = session.execute(query)

        return result.scalars().all()
    
    def get_by_team(self, session: Session, team_name: str) -> list[Match]:
        """
        Retrieve past finished matches for a specific team.

        Args:
            session (Session): Current database session.
            team_name (str): Target team name.

        Returns:
            list[Match]: Historical finished matches involving the team.
        """

        query = select(self.model).where(
            or_(
            self.model.home_team.ilike(f'%{team_name}%'),
            self.model.away_team.ilike(f'%{team_name}%')
            ),
            self.model.status == MatchStatus.FINISHED
        )

        result = session.execute(query)

        return result.scalars().all()
    
    def update_result(
            self, 
            session: Session, 
            match_id: int, 
            home_score: int, 
            away_score: int, 
            match_result: MatchResult, 
            status: MatchStatus) -> Match | None:

        """
        Update match scores, final result outcome, and set status to FINISHED.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.
            home_score (int): Home team final score.
            away_score (int): Away team final score.
            match_result (MatchResult): Winner result outcome.
            status (MatchStatus): New match status (FINISHED).

        Returns:
            Match | None: Updated Match model instance.
        """
        
        query = update(self.model).where(self.model.id == match_id).values(
            home_score=home_score,
            away_score=away_score,
            match_result=match_result,
            status=status
        )
        
        session.execute(query)
        session.commit()

        return self.get_by_id(session, match_id)

    def update_status(self, session: Session, match_id: int):
        """
        Update match status back to TIMED.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.

        Returns:
            Match | None: Updated Match model instance.
        """

        query = update(self.model).where(self.model.id == match_id).values(
            status = MatchStatus.TIMED
        )

        session.execute(query)
        session.commit()
        return self.get_by_id(session, match_id)

    def update_bet_availability(self, session: Session, match_id: int):
        """
        Set match betting availability flag to True.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.

        Returns:
            Match | None: Updated Match model instance.
        """

        query = update(self.model).where(self.model.id == match_id).values(
            is_bet_available = True
        )

        session.execute(query)
        session.commit()
        return self.get_by_id(session, match_id)

match_repository = MatchRepository()