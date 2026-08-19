import csv
import io
from sqlalchemy.orm import Session
from app.services.statistics_service import StatisticsService

statistics_service = StatisticsService()
class ExportService:
    def export_system_csv(self, session: Session):
        stats = statistics_service.get_system_stats(session)

        output = io.StringIO()

        writer = csv.DictWriter(
            output,
            fieldnames=[
                "total_users",
                "active_users",
                "total_bets",
                "total_points_in_system",
                "total_matches",
                "matches_open",
                "matches_finished",
            ],
        )

        writer.writeheader()
        writer.writerow(stats.model_dump())

        return output.getvalue()


    def export_user_csv(self, session: Session, cpf: str):
        stats = statistics_service.get_user_stats(session, cpf)

        output = io.StringIO()

        writer = csv.DictWriter(
            output,
            fieldnames=[
                "user_id",
                "nickname",
                "total_bets",
                "pending_bets",
                "won_bets",
                "lost_bets",
                "draw_bets",
                "current_points",
                "points_invested",
                "favorite_prediction",
                "favorite_team",
                "win_rate",
            ],
        )

        writer.writeheader()
        writer.writerow(stats.model_dump())

        return output.getvalue()

    def export_match_csv(self, session: Session, match_id: int):
        stats = statistics_service.get_match_stats(session, match_id)

        output = io.StringIO()
        
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "match_id",
                "home_team",
                "away_team",
                "status",
                "total_bets",
                "bets_home_win",
                "bets_away_win",
                "bets_draw",
                "odds_home",
                "odds_away",
                "odds_draw",
            ],
        )
        
        writer.writeheader()
        writer.writerow(stats.model_dump())

        return output.getvalue()

    def export_team_csv(self, session: Session, team: str):
            stats = statistics_service.get_team_stats(session, team)
    
            output = io.StringIO()
            
            writer = csv.DictWriter(
                output,
                fieldnames=[
                    'team',
                    'matches',
                    'wins',
                    'draws',
                    'losses',
                    'goals_scored',
                    'goals_conceded',
                    'goal_difference',
                    'win_rate',
                ],
            )
            
            writer.writeheader()
            writer.writerow(stats.model_dump())
    
            return output.getvalue()



