import uuid
from .base import Base
from sqlalchemy import Uuid, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .enum.match_enum import MatchResult, MatchStatus

class Match(Base):
    __tablename__ = "match"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    api_match_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    home_team: Mapped[str] = mapped_column(String(100))
    away_team: Mapped[str] = mapped_column(String(100))
    match_date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus), default=MatchStatus.TIMED)
    stage: Mapped[str] = mapped_column(String(50))
    home_score: Mapped[int] = mapped_column(nullable=True)
    away_score: Mapped[int] = mapped_column(nullable=True)
    match_result: Mapped[MatchResult] = mapped_column(Enum(MatchResult), nullable=True)


