import uuid
from pydantic import BaseModel

class MatchStats(BaseModel):
    match_id: int
    home_team: str
    away_team: str
    total_bets: int

    bets_home_win: int
    bets_away_win: int
    bets_draw: int

    odds_home: float
    odds_away: float
    odds_draw: float

class UserStats(BaseModel):
    user_id: uuid.UUID
    nickname: str
    total_bets: int
    won_bets: int
    lost_bets: int
    draw_bets: int
    win_rate: float
    current_points: int
    points_invested: int
    favorite_prediction: str
    favorite_team: str

class SystemStats(BaseModel):
    total_users: int
    active_users: int
    total_bets: int
    total_points_in_system: int
    total_matches: int
    matches_open: int
    matches_finished: int

class TeamStats(BaseModel):
    team: str
    matches: int
    wins: int
    draws: int
    losses: int
    goals_scored: int
    goals_conceded: int
    goal_difference: int
    win_rate: float