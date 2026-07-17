from app.repositories.base_repository import BaseRepository
from app.models.match import Match
from app.models.enum.match_enum import MatchStatus
from sqlalchemy import select
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