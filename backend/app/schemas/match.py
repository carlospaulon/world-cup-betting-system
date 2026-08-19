from typing import List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict
from app.models.enum.match_enum import MatchStatus, MatchResult

class MatchApiData(BaseModel):
    api_match_id: str
    competition: Optional[str] = None
    stage: Optional[str] = None
    match_date: Optional[datetime] = None
    status: Optional[MatchStatus] = None
    home_team: Optional[str] = None  # Permitir None para jogos futuros
    away_team: Optional[str] = None 
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_result: Optional[MatchResult] = None

class FootballApiResponse(BaseModel):
    matches: List[MatchApiData]

    @field_validator("matches", mode="before") 
    @classmethod
    def prepare_matches(cls, v: Any) -> Any:
        if not isinstance(v, list):
            return v
            
        transformed = []
        for match in v:
            # chaves vazia ou nulas não quebram o mapeamento .get()
            full_time = match.get('score', {}).get('fullTime') or {}
            score = match.get('score') or {}

            api_status = match.get('status')

            if api_status == "SCHEDULED":
                api_status = "TIMED"
            
            transformed.append({
                "api_match_id": str(match.get("id")),
                "competition": (match.get("competition") or {}).get('code'),
                'stage': match.get('stage'),
                'match_date': match.get('utcDate'),
                'status': api_status,
                "home_team": (match.get("homeTeam") or {}).get('name'), 
                "away_team": (match.get("awayTeam") or {}).get('name'), 
                "home_score": full_time.get("home"), 
                "away_score": full_time.get('away'), 
                "match_result": score.get('winner')        
            })
        return transformed
    
class MatchResponse(BaseModel):
    id: int
    api_match_id: str
    competition: Optional[str] = None
    stage: Optional[str] = None
    match_date: Optional[datetime] = None
    status: Optional[MatchStatus] = None # Enum
    is_bet_available: bool = False
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_result: Optional[MatchResult] = None # Enum
    odds_home: Optional[float] = None  # preenchido pelo service
    odds_away: Optional[float] = None # Atualizado irt
    odds_draw: float = 1.0

    model_config = ConfigDict(from_attributes=True)