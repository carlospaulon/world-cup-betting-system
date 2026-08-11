import csv
import io
import uuid
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


    def export_user_csv(self, session: Session, user_id: uuid.UUID):
        stats = statistics_service.get_user_stats(session, user_id)

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



