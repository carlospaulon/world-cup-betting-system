import os
import joblib
import pandas as pd
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sklearn.linear_model import LogisticRegression

from app.models.match import Match
from app.models.enum.match_enum import MatchStatus, MatchResult
from app.repositories.match_repository import match_repository
from app.repositories.statistics_repository import statistics_repository
from app.schemas.prediction import MatchPredictionResponse
from app.core.exceptions import InsufficientMatchDataException, MatchNotFoundException

MODEL_PATH = "ml_models/match_predictor.pkl"

class MLService:

    def _extract_team_features(
        self,
        session: Session,
        team_name: str
    ):
        """
        Extract historical statistical metrics for a specific team to build model features.

        Args:
            session (Session): Current database session.
            team_name (str): Target team name.

        Raises:
            InsufficientMatchDataException: If the team has fewer than 3 completed matches.

        Returns:
            Dict[str, float]: Dictionary containing average goals, conceded goals, win, draw, and loss rates.
        """
        
        stats = statistics_repository.get_team_stats(
            session,
            team_name
        )

        if not stats or stats["matches"] < 3:
            raise InsufficientMatchDataException()

        matches = stats["matches"]

        return {
            "avg_goals": stats["goals_scored"] / matches,
            "avg_conceded": stats["goals_conceded"] / matches,
            "win_rate": stats["wins"] / matches,
            "draw_rate": stats["draws"] / matches,
            "loss_rate": stats["losses"] / matches
        }

    def train_model(self, session: Session) -> Dict[str, Any]:
        """
        Fetch all FINISHED matches, extract team features, and train a Logistic Regression model.

        Saves the trained model instance to disk at MODEL_PATH.

        Args:
            session (Session): Current database session.

        Raises:
            InsufficientMatchDataException: If fewer than 10 valid training samples exist in the database.

        Returns:
            Dict[str, Any]: Dictionary containing status and total samples trained.
        """

        finished_matches = match_repository.filter_matches(session=session, status=MatchStatus.FINISHED)
        
        X: List[Dict[str, float]] = []
        y: List[str] = []

        for m in finished_matches:
            if not m.home_score or not m.away_score or not m.match_result:
                continue

            try:
                home_feat = self._extract_team_features(session, m.home_team)
                away_feat = self._extract_team_features(session, m.away_team)
            except InsufficientMatchDataException:
                continue

            features = {
                "home_avg_goals": home_feat["avg_goals"],
                "home_avg_conceded": home_feat["avg_conceded"],
                "home_win_rate": home_feat["win_rate"],

                "away_avg_goals": away_feat["avg_goals"],
                "away_avg_conceded": away_feat["avg_conceded"],
                "away_win_rate": away_feat["win_rate"],
            }
            
            X.append(features)
            y.append(m.match_result.value)

        if len(X) < 10:
            raise InsufficientMatchDataException()

        df_X = pd.DataFrame(X)
        model = LogisticRegression(max_iter=1000)
        model.fit(df_X, y)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(model, MODEL_PATH)

        return {"status": "success", "samples_trained": len(X)}

    def predict_match(self, session: Session, match_id: int) -> MatchPredictionResponse:
        """
        Load the trained model, compute team feature vectors, and predict match probabilities.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.

        Raises:
            MatchNotFoundException: Target match ID does not exist.

        Returns:
            MatchPredictionResponse: Schema containing outcome probabilities and predicted winner.
        """

        match = match_repository.get_by_id(session, match_id)
        if not match:
            raise MatchNotFoundException()

        # Garante a existência do arquivo binário do modelo
        if not os.path.exists(MODEL_PATH):
            self.train_model(session)

        model: LogisticRegression = joblib.load(MODEL_PATH)

        # Extração de features dos times do confronto
        home_feat = self._extract_team_features(session, match.home_team)
        away_feat = self._extract_team_features(session, match.away_team)

        features = pd.DataFrame([{
            "home_avg_goals": home_feat["avg_goals"],
            "home_avg_conceded": home_feat["avg_conceded"],
            "home_win_rate": home_feat["win_rate"],
            "away_avg_goals": away_feat["avg_goals"],
            "away_avg_conceded": away_feat["avg_conceded"],
            "away_win_rate": away_feat["win_rate"],
        }])

        probabilities = model.predict_proba(features)[0]
        classes = list(model.classes_)  # Exemplo: ['HOME_TEAM', 'DRAW', 'AWAY_TEAM']

        probs_map = dict(zip(classes, probabilities))

        home_prob = round(probs_map.get(MatchResult.HOME_TEAM.value, 0.0), 2)
        draw_prob = round(probs_map.get(MatchResult.DRAW.value, 0.0), 2)
        away_prob = round(probs_map.get(MatchResult.AWAY_TEAM.value, 0.0), 2)

        # Determina a maior probabilidade
        max_pred = max(probs_map, key=probs_map.get)

        return MatchPredictionResponse(
            match_id=match.id,
            home_team=match.home_team,
            away_team=match.away_team,
            home_win_probability=home_prob,
            draw_probability=draw_prob,
            away_win_probability=away_prob,
            prediction=MatchResult(max_pred)
        )