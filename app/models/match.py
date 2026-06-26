from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy import Integer, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .enum.match_enum import MatchResult, MatchStatus

if TYPE_CHECKING:
    from .bet import Bet

class Match(Base):
    __tablename__ = "match"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    api_match_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    home_team: Mapped[str] = mapped_column(String(100))
    away_team: Mapped[str] = mapped_column(String(100))
    match_date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus), default=MatchStatus.TIMED)
    stage: Mapped[str] = mapped_column(String(50))
    home_score: Mapped[int] = mapped_column(nullable=True)
    away_score: Mapped[int] = mapped_column(nullable=True)
    match_result: Mapped[MatchResult] = mapped_column(Enum(MatchResult), nullable=True)

    # relationship
    bets: Mapped[list["Bet"]] = relationship(
        back_populates="match",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Match: {self.id}, status: {self.status}"
