import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.models.enum.bet_enum import BetPrediction, BetResult, BetStatus

class BetCreate(BaseModel):
    match_id: int
    prediction: BetPrediction
    points_bet: int = Field(ge=1) # maior-igual a 1

class BetResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    match_id: int
    prediction: BetPrediction
    points_bet: int
    odds: float
    result: Optional[BetResult] = None
    status: BetStatus
    created_at: datetime

class BetMultiply(BaseModel):
    factor: int = Field(ge=2, le=5) # Multiplicador

class BetWithMatchResponse(BetResponse):
    home_team: str
    away_team: str