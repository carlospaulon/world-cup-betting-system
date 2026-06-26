from enum import Enum

# (str) transform the value of the Enum in str
class BetPrediction(str, Enum):
    HOME_WIN = "home_win"
    AWAY_WIN = "away_win"
    DRAW = "draw"

class BetResult(str, Enum):
    WON = "won"
    LOST = "lost"
    DRAW = "draw"

class BetStatus(str, Enum):
    PENDING = "pending"
    SETTLED = "settled"
    CANCELLED = "cancelled"