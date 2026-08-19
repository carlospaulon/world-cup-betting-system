import uuid
from app.models.enum.bet_enum import BetPrediction
from app.models.enum.match_enum import MatchStatus
from pydantic import BaseModel, computed_field
from decimal import Decimal

# admin
class MatchStats(BaseModel):
    match_id: int
    home_team: str
    away_team: str
    status: MatchStatus
    total_bets: int

    bets_home_win: int
    bets_away_win: int 
    bets_draw: int

    odds_home: float
    odds_away: float
    odds_draw: float

# user
class UserStats(BaseModel):
    user_id: uuid.UUID
    nickname: str

    total_bets: int
    pending_bets: int
    won_bets: int
    lost_bets: int
    draw_bets: int

    @computed_field
    @property
    def win_rate(self) -> float: 
        if self.total_bets == 0:
            return 0.0

        return (self.won_bets / self.total_bets) * 100

    current_points: Decimal
    points_invested: Decimal
    favorite_prediction: BetPrediction | None
    favorite_team: str | None # mais apostou

# admin
class SystemStats(BaseModel):
    total_users: int
    active_users: int
    total_bets: int
    total_points_in_system: Decimal
    total_matches: int
    matches_open: int
    matches_finished: int

# publica
class TeamStats(BaseModel):
    team: str
    matches: int
    wins: int
    draws: int
    losses: int
    goals_scored: int
    goals_conceded: int

    @computed_field
    @property
    def goal_difference(self) -> int:
        return self.goals_scored - self.goals_conceded
    

    @computed_field
    @property
    def win_rate(self)-> float:
        if self.matches == 0:
            return 0.0

        return (self.wins / self.matches) * 100