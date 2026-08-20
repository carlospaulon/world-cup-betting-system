import uuid
from fastapi import HTTPException
from typing import Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.match import Match
from app.models.bet import Bet
from app.models.enum.bet_enum import BetPrediction, BetStatus, BetResult
from app.schemas.bet import BetCreate, BetWithMatchResponse, BetResponse
from app.repositories.bet_repository import bet_repository
from app.repositories.match_repository import match_repository
from app.core.exceptions import MatchNotFoundException, MatchNotOpenException, InsufficientPointsException, BetNotFoundException, BetAlreadySettledException, BetNotAvailableException
from app.models.enum.match_enum import MatchStatus, MatchResult
from app.repositories.user_repository import user_repository

class BetService:
    def get_user_bets(self, session: Session, user: User, bet_status: Optional[BetStatus]):
        """
        Fetch user bets decorated with team names for display.

        Args:
            session (Session): Current database session.
            user (User): Authenticated user instance.
            bet_status (Optional[BetStatus]): Filter criteria for bet status.

        Returns:
            list[BetWithMatchResponse]: Enriched list of bet objects.
        """

        if bet_status is None:
            bets = bet_repository.get_by_user(session, user.id)
        else:
            bets = bet_repository.filter_bets(session, user.id, bet_status)

        result = []

        for bet in bets:
            match = match_repository.get_by_id(session, bet.match_id)

            # valida e atribui os campo com o parametro
            response = BetWithMatchResponse(
                id=bet.id,
                user_id=bet.user_id,
                match_id=bet.match_id,
                prediction=bet.prediction,
                points_bet=bet.points_bet,
                odds=bet.odds,
                result=bet.result,
                status=bet.status,
                created_at=bet.created_at,
                home_team=match.home_team,
                away_team=match.away_team
            )

            result.append(response)

        return result

    def get_bet_by_id(self, session: Session, bet_id: uuid.UUID, user: User) -> BetWithMatchResponse:
        """
        Retrieve a specific bet enforcing ownership verification.

        Args:
            session (Session): Current database session.
            bet_id (uuid.UUID): Target bet UUID.
            user (User): Requesting user.

        Raises:
            BetNotFoundException: If no bet matches the given UUID.
            HTTPException (403): If the bet does not belong to the user.

        Returns:
            BetWithMatchResponse: Detailed bet schema.
        """

        bet = bet_repository.get_by_id(session, bet_id)

        if not bet:
            raise BetNotFoundException()

        # Validar se bet pertence a user

        if bet.user_id != user.id:
            raise HTTPException(status_code=403, detail="Bet doesnt belong to the user")

        match = match_repository.get_by_id(session, bet.match_id)

        response = BetWithMatchResponse(
            id=bet.id,
            user_id=bet.user_id,
            match_id=bet.match_id,
            prediction=bet.prediction,
            points_bet=bet.points_bet,
            odds=bet.odds,
            result=bet.result,
            status=bet.status,
            created_at=bet.created_at,
            home_team=match.home_team,
            away_team=match.away_team
        )

        return response



    # calcula no momento da criação da Bet
    def calculate_odds(self, session: Session, match_id: int, prediction: BetPrediction) -> Decimal:
        """
        Calculate dynamic odds based on overall market prediction ratio.

        Args:
            session (Session): Current database session.
            match_id (int): Target match ID.
            prediction (BetPrediction): Chosen prediction outcome.

        Returns:
            Decimal: Calculated numerical multiplier odds.
        """

        home_count = bet_repository.count_by_prediction(session, match_id, BetPrediction.HOME_WIN)
        away_count = bet_repository.count_by_prediction(session, match_id, BetPrediction.AWAY_WIN)

        if prediction == BetPrediction.HOME_WIN:
            return round(1 + (away_count / home_count if home_count > 0 else 0), 2)
        elif prediction == BetPrediction.AWAY_WIN:
            return round(1 + (home_count / away_count if away_count > 0 else 0), 2)
        else:  # DRAW
            return 1.0

        
    def create_bet(self, session: Session, user: User, data: BetCreate) -> Bet:
        """
        Process and validate new bet creation.

        Deducts points from the user balance immediately upon placement.

        Args:
            session (Session): Current database session.
            user (User): Authenticated user placing the bet.
            data (BetCreate): Bet request payload.

        Raises:
            MatchNotFoundException: Target match ID does not exist.
            MatchNotOpenException: Match status is not TIMED.
            BetNotAvailableException: Match is not marked available by admin.
            InsufficientPointsException: User does not have enough points.

        Returns:
            BetResponse: Validated created bet model instance.
        """

        match = match_repository.get_by_id(session, data.match_id)

        if not match:
            raise MatchNotFoundException()

        if not match.status == MatchStatus.TIMED:
            raise MatchNotOpenException()

        if not match.is_bet_available:
            raise BetNotAvailableException()

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

        return BetResponse.model_validate(bet_repository.create(session, bet))
        

    def multiply_bet(self, session: Session, user: User, bet_id: uuid.UUID, factor: int):
        """
        Multiply the wagered points on a pending bet and deduct additional points.

        Args:
            session (Session): Current database session.
            user (User): Authenticated user.
            bet_id (uuid.UUID): Target bet UUID.
            factor (int): Wager multiplier factor.

        Raises:
            BetNotFoundException: Bet UUID not found.
            HTTPException (403): Bet belongs to another user.
            BetAlreadySettledException: Bet status is not PENDING.
            InsufficientPointsException: User balance cannot cover additional wager cost.

        Returns:
            Bet: Updated Bet model instance.
        """

        current_bet = bet_repository.get_by_id(session, bet_id)

        if not current_bet:
            raise BetNotFoundException()

        if current_bet.user_id != user.id:
            raise HTTPException(status_code=403, detail="Bet doesnt belong to the user")

        if current_bet.status != BetStatus.PENDING:
            raise BetAlreadySettledException()

        additional_cost = current_bet.points_bet * (factor - 1)

        if user.points < additional_cost:
            raise InsufficientPointsException()

        # user desconto pontos
        user_repository.update_points(session, user.id, -additional_cost)

        # bet atualiza pontos apostados
        new_points = current_bet.points_bet * factor
        # model validate?
        return bet_repository.update_bet_points(session, bet_id, new_points)

    def settle_bets(self, session: Session, match: Match):
        """
        Settle all pending bets for a finished match and credit earnings to winners.

        Deactivates user accounts if total points drop to zero or below.

        Args:
            session (Session): Current database session.
            match (Match): Finalized match instance containing final result.

        Returns:
            list[Bet]: List of settled bet records.
        """

        bets = bet_repository.get_pending_by_match(session, match.id)

        for bet in bets:
            user = user_repository.get_by_id(session, bet.user_id)

            if bet.prediction == match.match_result:
                bet.result = BetResult.WON
                poinst_earned = round(bet.points_bet * Decimal(str(bet.odds)), 2)
                user_repository.update_points(session, user.id, poinst_earned)

            elif bet.prediction == MatchResult.DRAW:
                bet.result = BetResult.DRAW
                user_repository.update_points(session, user.id, bet.points_bet)

            else:
                bet.result = BetResult.LOST

            bet.status = BetStatus.SETTLED
            bet_repository.update_result(session, bet.id, bet.result, bet.status)

            if user.points <= 0:
                user_repository.deactivate(session, user.id)

        return bets
