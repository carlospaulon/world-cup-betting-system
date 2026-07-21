from enum import Enum

class MatchResult(str, Enum):
    HOME_TEAM = "HOME_TEAM"
    AWAY_TEAM = "AWAY_TEAM"
    DRAW = "DRAW"

class MatchStatus(str, Enum):
    TIMED = "TIMED"
    IN_PLAY = "IN_PLAY"
    FINISHED = "FINISHED"
    POSTPONED = "POSTPONED"