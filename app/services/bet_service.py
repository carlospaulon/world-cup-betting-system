import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.bet import Bet
from app.models.enum.bet_enum import BetPrediction, BetStatus
from app.schemas.bet import BetCreate
from app.repositories.bet_repository import bet_repository
from app.repositories.match_repository import match_repository
from app.core.exceptions import MatchNotFoundException, MatchNotOpenException, InsufficientPointsException, BetNotFoundException, BetAlreadySettledException
from app.models.enum.match_enum import MatchStatus
from app.repositories.user_repository import user_repository

class BetService:
    # calcula no momento da criação da Bet
    def calculate_odds(self, session: Session, match_id: int, prediction: BetPrediction) -> float:
        home_count = bet_repository.count_by_prediction(session, match_id, BetPrediction.HOME_WIN)
        away_count = bet_repository.count_by_prediction(session, match_id, BetPrediction.AWAY_WIN)

        if prediction == BetPrediction.HOME_WIN:
            my_count = home_count
            opponent_count = away_count

        if prediction == BetPrediction.AWAY_WIN:
            my_count = away_count
            opponent_count = home_count

        if prediction == BetPrediction.DRAW:
            return 1.0

        if my_count == 0 and opponent_count == 0:
            return 1.0

        if opponent_count == 0:
            return 1.0

        if my_count == 0:
            return 1.0

        return 1 + (opponent_count / my_count)

        
    def create_bet(self, session: Session, user: User, data: BetCreate) -> Bet:
        match = match_repository.get_by_id(session, data.match_id)

        if not match:
            raise MatchNotFoundException()

        if not match.status == MatchStatus.TIMED:
            raise MatchNotOpenException()

        if data.points_bet > user.points:
            raise InsufficientPointsException()

        bet_odds = self.calculate_odds(session, data.match_id, data.prediction)
        user_repository.update_points(session, user.id, -data.points_bet)

        bet = Bet(
            user_id = user.id,
            match_id = data.match_id,
            prediction = data.prediction,
            points_bet = data.points_bet,
            odds = bet_odds,
            result = None,
            status = BetStatus.PENDING
        )

        return bet_repository.create(session, bet)
        

    def multiply_bet(self, session: Session, user: User, bet_id: uuid.UUID, factor: int):
        current_bet = bet_repository.get_by_id(session, bet_id)

        if not current_bet:
            raise BetNotFoundException()

        if not current_bet.user_id == user.id:
            raise HTTPException(status_code=403, detail="Bet doesnt belong to the user")

        if not current_bet.status == BetStatus.PENDING:
            raise BetAlreadySettledException()

        additional_cost = current_bet.points_bet * (factor - 1)

        if not user.points >= additional_cost:
            raise InsufficientPointsException()

        # user desconto pontos
        user_repository.update_points(session, user.id, -additional_cost)

        # bet atualiza pontos apostados
        return bet_repository.update_bet_points(session, bet_id, current_bet.points_bet * factor)

        


        