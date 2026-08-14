import uuid
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from app.models.match import Match
from app.models.user import User
from app.models.bet import Bet
from app.schemas.match import MatchStatus
from app.schemas.bet import BetPrediction, BetResult, BetStatus
from sqlalchemy import select, func, case, or_, and_

class StatisticsRepository():

    def get_match_stats(self, session: Session, match_id: int):
        # pega infos padrão da partida (infos iniciais pego no service para montar), conta as bets e prediction + odds
        query = (select(
            Match.id.label("match_id"),
            Match.home_team,
            Match.away_team,
            Match.status,
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

    # checar performance!
    def get_user_stats(self, session: Session, user_id: uuid):
        # stats geral
        query_general = (select(
            User.id.label("user_id"),
            User.nickname,
            User.points.label("current_points"),
            func.count(Bet.id)
                .label("total_bets"),
            func.count(Bet.id)
                .filter(Bet.status == BetStatus.PENDING)
                .label("pending_bets"),
            func.count(Bet.id)
                .filter(Bet.result == BetResult.WON)
                .label("won_bets"),
            func.count(Bet.id)
                .filter(Bet.result == BetResult.LOST)
                .label("lost_bets"),
            func.count(Bet.id)
                .filter(Bet.result == BetResult.DRAW)
                .label("draw_bets"),
            func.coalesce(func.sum(Bet.points_bet), 0) # permite valor 0
                .label("points_invested"),
            )
            .join(Bet, Bet.user_id == User.id, isouter=True)
            .where(User.id == user_id)
            .group_by(
                User.id,
                User.nickname,
                User.points
            )
        )

        # predict favorita
        query_favorite_prediction = (select(
            Bet.prediction,
            func.count(Bet.id).label("total")
        )
        .where(Bet.user_id == user_id)
        .group_by(Bet.prediction)
        .order_by(func.count(Bet.id).desc())
        .limit(1)
    )
        
        # time favorito
        # when then
        team = case(
            (Bet.prediction == BetPrediction.HOME_WIN, Match.home_team),
            (Bet.prediction == BetPrediction.AWAY_WIN, Match.away_team),
            else_=None
        )

        query_favorite_team = (
            select(
                team.label("favorite_team"),
                func.count(Bet.id)
            )
            .join(Match, Match.id == Bet.match_id)
            .where(Bet.user_id == user_id)
            .where(Bet.prediction != BetPrediction.DRAW)
            .group_by(team)
            .order_by(func.count(Bet.id).desc())
            .limit(1)
        )

        # executo as 3 queries
        general_stats = session.execute(query_general).mappings().first()
        favorite_prediction = session.execute(query_favorite_prediction).scalar()
        favorite_team = session.execute(query_favorite_team).scalar()

        # monto o retorno como dicionário
        data = dict(general_stats)
        data["favorite_prediction"] = favorite_prediction
        data["favorite_team"] = favorite_team

        return data

    def get_system_stats(self, session: Session):
        # cada campo com count ou sum como subquery
        total_users = select(func.count(User.id)).scalar_subquery()
        active_users = (select(func.count(User.id))
            .where(User.is_active.is_(True))
            .scalar_subquery())
        total_bets = select(func.count(Bet.id)).scalar_subquery()
        total_points = select(func.coalesce(func.sum(User.points), 0)).scalar_subquery()
        total_matches = select(func.count(Match.id)).scalar_subquery()
        matches_open = select(func.count(Match.id)).where(Match.status == MatchStatus.TIMED).scalar_subquery()
        matches_finished = select(func.count(Match.id)).where(Match.status == MatchStatus.FINISHED).scalar_subquery()

        # monto a minha query principal
        query = select(
            total_users.label("total_users"),
            active_users.label("active_users"),
            total_bets.label("total_bets"),
            total_points.label("total_points_in_system"),
            total_matches.label("total_matches"),
            matches_open.label("matches_open"),
            matches_finished.label("matches_finished"),
        )

        result = session.execute(query)
        return result.mappings().first()

    def get_team_stats(self, session: Session, team_name: str):

        team_filter = or_(
            Match.home_team.ilike(f'%{team_name}%'),
            Match.away_team.ilike(f'%{team_name}%')
        )
            

        goals_scored = case(
            (Match.home_team.ilike(team_name), Match.home_score),
            (Match.away_team.ilike(team_name), Match.away_score),
            else_=0
        )

        goals_conceded = case(
            (Match.home_team.ilike(team_name), Match.away_score),
            (Match.away_team.ilike(team_name), Match.home_score),
            else_=0
        )

        wins = case(
            (
                and_(
                    Match.home_team.ilike(team_name),
                    Match.home_score > Match.away_score
                ), 1),
            (
                and_(
                Match.away_team.ilike(team_name),
                Match.away_score > Match.home_score
            ), 1),
            else_=0
        )

        draws = case(
            (
                and_(
                    team_filter,
                    Match.home_score == Match.away_score
                ),
                1
            ),
            else_=0
        )

        losses = case(
            (
                and_(
                    Match.home_team.ilike(team_name),
                    Match.home_score < Match.away_score
                ), 1),
            (
                and_(
                Match.away_team.ilike(team_name),
                Match.away_score < Match.home_score
            ), 1),
            else_=0
        )

        query = (
            select(
                func.count(Match.id).label('matches'),
                func.coalesce(func.sum(wins), 0).label('wins'),
                func.coalesce(func.sum(draws), 0).label('draws'),
                func.coalesce(func.sum(losses), 0).label('losses'),
                func.coalesce(func.sum(goals_scored), 0).label('goals_scored'),
                func.coalesce(func.sum(goals_conceded), 0).label('goals_conceded'),
            ).where(
                team_filter,
                Match.status == MatchStatus.FINISHED
            )
        )

        result = session.execute(query)

        return result.mappings().first()


statistics_repository = StatisticsRepository()