import uuid
from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from app.core.security import get_current_admin
from app.models.user import User
from app.core.database import get_db
from app.services.export_service import ExportService

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

@router.get(
    "/admin/system/csv",
    status_code=status.HTTP_200_OK
)
def export_system_stats_csv(
    current_admin: User = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    export_service = ExportService()
    csv_data = export_service.export_system_csv(db)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=system_stats.csv"
        }
    )


@router.get(
    "/admin/user/csv",
    status_code=status.HTTP_200_OK
)
def export_user_stats_csv(
    user_id: uuid.UUID,
    current_admin: User = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    export_service = ExportService()
    csv_data = export_service.export_user_csv(db, user_id)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=user_stats.csv"
        }
    )

@router.get(
    "/admin/match/csv",
    status_code=status.HTTP_200_OK
)
def export_match_stats_csv(
    match_id: int,
    current_admin: User = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    export_service = ExportService()
    csv_data = export_service.export_match_csv(db, match_id)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=match_stats.csv"
        }
    )

@router.get(
    "/admin/team/csv",
    status_code=status.HTTP_200_OK
)
def export_team_stats_csv(
    team: str,
    current_admin: User = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    export_service = ExportService()
    csv_data = export_service.export_team_csv(db, team)

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=team_stats.csv"
        }
    )