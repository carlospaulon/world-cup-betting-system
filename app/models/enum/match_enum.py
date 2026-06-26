from enum import Enum

class MatchResult(str, Enum):
    HOME_TEAM = "home_team"
    AWAY_TEAM = "away_team"
    DRAW = "draw"

class MatchStatus(str, Enum):
    TIMED = "timed"
    IN_PLAY = "in_play"
    FINISHED = "finished"
    POSTPONED = "postponed"