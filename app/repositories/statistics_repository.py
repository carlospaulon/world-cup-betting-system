from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from app.models.match import Match
from app.models.bet import Bet
from app.schemas.bet import BetPrediction
from sqlalchemy import select, func

class StatisticsRepository():

    def get_match_stats(self, session: Session, match_id: int):
        # pega infos padrão da partida (infos iniciais pego no service para montar), conta as bets e prediction + odds
        query = (select(
            Match.id.label("match_id"),
            Match.home_team,
            Match.away_team,
            func.count(Bet.id).label("total_bets"),
            func.count(Bet.id)
                .filter(Bet.prediction == BetPrediction.HOME_WIN)
                .label("bets_home_win"),
            func.count(Bet.id)
                .filter(Bet.prediction == BetPrediction.AWAY_WIN)
                .label("bets_away_win"),
            func.count(Bet.id)
                .filter(Bet.prediction == BetPrediction.DRAW)
                .label("bets_draw"),
            # para pegar odds no service uso o calculate
            )
        .join(Bet, Bet.match_id == Match.id, isouter=True) # mostra partidas com contagem em 0
        .where(Match.id == match_id)
        .group_by(
            Match.id,
            Match.home_team,
            Match.away_team
            )
        )

        result = session.execute(query)
        return result.mappings().first() # retorna um dict

statistics_repository = StatisticsRepository()