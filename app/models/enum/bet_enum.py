from enum import Enum

# (str) transform the value of the Enum in str
class BetPrediction(str, Enum):
    HOME_WIN = "HOME_WIN"
    AWAY_WIN = "AWAY_WIN"
    DRAW = "DRAW"

class BetResult(str, Enum):
    WON = "WON"
    LOST = "LOST"
    DRAW = "DRAW"

class BetStatus(str, Enum):
    PENDING = "PENDING"
    SETTLED = "SETTLED"
    CANCELLED = "CANCELLED"