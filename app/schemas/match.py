from typing import List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict

class MatchApiData(BaseModel):
    api_match_id: str
    stage: Optional[str] = None
    match_date: Optional[datetime] = None
    status: Optional[str] = None
    home_team: Optional[str] = None  # Permitir None para jogos futuros
    away_team: Optional[str] = None 
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_result: Optional[str] = None

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
            
            transformed.append({
                "api_match_id": str(match.get("id")),
                'stage': match.get('stage') or {},
                'match_date': match.get('utcDate') or {},
                'status': match.get('status') or {},
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
    stage: Optional[str] = None
    match_date: Optional[datetime] = None
    status: Optional[str] = None # Enum
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_result: Optional[str] = None # Enum
    odds_home: Optional[float] = None  # preenchido pelo service
    odds_away: Optional[float] = None
    odds_draw: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)