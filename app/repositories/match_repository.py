from app.repositories.base_repository import BaseRepository
from app.models.match import Match
from app.models.enum.match_enum import MatchStatus, MatchResult
from sqlalchemy import select, or_, update
from sqlalchemy.orm import Session

class MatchRepository(BaseRepository[Match]):
    def __init__(self):
        super().__init__(Match)

    def create(self, session: Session, match: Match) -> Match:
        session.add(match)
        session.commit()
        session.refresh(match)
        return match
    
    def get_by_api_id(self, session: Session, api_match_id: str) -> Match | None:
        query = select(self.model).where(self.model.api_match_id == api_match_id)
        result = session.execute(query)

        return result.scalars().first()
    
    def get_all_open(self, session: Session) -> list[Match]:
        query = select(self.model).where(self.model.status == MatchStatus.TIMED)
        result = session.execute(query)

        return result.scalars().all()
    
    def get_by_team(self, session: Session, team_name: str) -> list[Match]:
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
        
        query = update(self.model).where(self.model.id == match_id).values(
            home_score=home_score,
            away_score=away_score,
            match_result=match_result,
            status=status
        )
        
        session.execute(query)
        session.commit()

        return self.get_by_id(session, match_id)

match_repository = MatchRepository()