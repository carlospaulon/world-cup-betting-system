from pydantic import BaseModel, ConfigDict
from app.models.enum.match_enum import MatchResult

class MatchPredictionResponse(BaseModel):
    match_id: int
    home_team: str
    away_team: str
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    prediction: MatchResult 

    model_config = ConfigDict(from_attributes=True)