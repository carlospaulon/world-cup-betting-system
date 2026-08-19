from sqlalchemy.orm import Session
from app.repositories.match_repository import match_repository
from app.repositories.statistics_repository import statistics_repository
from app.services.bet_service import BetService
from app.core.exceptions import MatchNotFoundException, UserNotFoundException, TeamNotFoundException
from app.schemas.statistics import MatchStats, UserStats, SystemStats, TeamStats
from app.models.enum.bet_enum import BetPrediction

bet_service = BetService()

class StatisticsService:
    def get_match_stats(self, session: Session, match_id: int):

        # row mapping dict - imutavel
        stats = statistics_repository.get_match_stats(session, match_id)

        if not stats:
            raise MatchNotFoundException()

        # transforma em mutavel
        stats_data = dict(stats)

        home_odds = bet_service.calculate_odds(session, match_id, BetPrediction.HOME_WIN)
        away_odds = bet_service.calculate_odds(session, match_id, BetPrediction.AWAY_WIN)

        stats_data["odds_home"] = home_odds
        stats_data["odds_away"] = away_odds
        stats_data["odds_draw"] = 1.0

        match_stats = MatchStats.model_validate(stats_data)

        return match_stats

    def get_user_stats(self, session: Session, cpf: str):
        stats = statistics_repository.get_user_stats(session, cpf)

        if not stats:
            raise UserNotFoundException()

        user_stats = UserStats.model_validate(stats)

        return user_stats

    def get_system_stats(self, session: Session):
        stats = statistics_repository.get_system_stats(session)

        system_stats = SystemStats.model_validate(stats)

        return system_stats

    def get_team_stats(self, session: Session, team: str):
        team_history = match_repository.get_by_team(session, team)

        if not team_history:
            raise TeamNotFoundException()

        stats = statistics_repository.get_team_stats(session, team)

        stats_data = dict(stats)

        stats_data['team'] = team

        team_stats = TeamStats.model_validate(stats_data)

        return team_stats