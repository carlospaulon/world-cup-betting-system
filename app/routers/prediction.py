from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.prediction import MatchPredictionResponse
from app.services.ml_service import MLService

router = APIRouter(
    prefix="/predictions",
    tags=["ML Predictions"],
)

@router.get(
    "/matches/{match_id}",
    response_model=MatchPredictionResponse,
    status_code=status.HTTP_200_OK
)
def get_match_prediction(match_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ml_service = MLService()
    return ml_service.predict_match(db, match_id)

@router.post(
    "/admin/ml/retrain",
    status_code=status.HTTP_200_OK
)
def retrain_ml_model(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Endpoint para forçar o retreinamento do modelo quando novos jogos forem importados/finalizados."""
    ml_service = MLService()
    return ml_service.train_model(db)