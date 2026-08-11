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