import uuid
from .base import Base
from datetime import datetime
from sqlalchemy import Uuid, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .enum.bet_enum import BetPrediction, BetStatus, BetResult


class Bet(Base):
    __tablename__ = "bet"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    match_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("match.id", ondelete="CASCADE"))
    prediction: Mapped[BetPrediction] = mapped_column(Enum(BetPrediction), nullable=False)
    points_bet: Mapped[int] = mapped_column(nullable=False)
    odds: Mapped[float] = mapped_column(nullable=False)
    result: Mapped[BetResult] = mapped_column(Enum(BetResult), nullable=True)
    status: Mapped[BetStatus] = mapped_column(Enum(BetStatus), default=BetStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())