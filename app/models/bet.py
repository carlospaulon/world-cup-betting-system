import uuid
from .base import Base
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Uuid, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .enum.bet_enum import BetPrediction, BetStatus, BetResult

if TYPE_CHECKING:
    from .user import User
    from .match import Match

class Bet(Base):
    __tablename__ = "bet"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    match_id: Mapped[int] = mapped_column(ForeignKey("match.id", ondelete="CASCADE"))
    prediction: Mapped[BetPrediction] = mapped_column(Enum(BetPrediction), nullable=False)
    points_bet: Mapped[int] = mapped_column(nullable=False)
    odds: Mapped[float] = mapped_column(nullable=False)
    result: Mapped[BetResult] = mapped_column(Enum(BetResult), nullable=True)
    status: Mapped[BetStatus] = mapped_column(Enum(BetStatus), default=BetStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # needed the relation, so use lazy to search bets on the other entitites
    user: Mapped["User"] = relationship(back_populates="bets", lazy="selectin")
    match: Mapped["Match"] = relationship(back_populates="bets", lazy="selectin")

    def __repr__(self):
        return f'Bet: {self.id}, status: {self.status}'