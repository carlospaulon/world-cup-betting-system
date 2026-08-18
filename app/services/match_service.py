from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.models.user import User
from app.models.match import Match
from app.repositories.match_repository import match_repository
from app.services.football_api_service import FootballService
from app.schemas.match import FootballApiResponse, MatchResponse, MatchApiData
from app.models.enum.match_enum import MatchResult, MatchStatus
from app.models.enum.bet_enum import BetPrediction
from app.core.exceptions import MatchNotFoundException, InvalidDateRangeException
from app.services.bet_service import BetService

class MatchService:
    def import_matches(self, session: Session):
        # controle
        ignored = 0
        imported = 0

        football_service = FootballService() # injeta footballService
        response = football_service.fetch_matches() # JSON
        matches = FootballApiResponse.model_validate(response).matches # Lista de matchApiData

        for match in matches:

            existing_match = match_repository.get_by_api_id(session, match.api_match_id)

            if existing_match:
                print("Partida existente no banco")
                ignored += 1
                continue

            mapped_match = football_service.map_to_match(match)
            match_repository.create(session, mapped_match)
            imported += 1    

        return {
            "matches_imported": imported,
            "matches_ignored": ignored
        }

    # Pega open, pega com filtro de time, status e stage
    def get_matches(
            self, 
            session: Session,
            team_name: Optional[str] = None,
            match_status: Optional[MatchStatus] = None,
            stage: Optional[str] = None,
            from_date: Optional[date] = None,
            to_date: Optional[date] = None
        ):

        bet_service = BetService()

        if from_date and to_date and from_date > to_date:
            raise InvalidDateRangeException()


        matches = match_repository.filter_matches(
            session=session,
            team_name=team_name,
            status=match_status,
            stage=stage,
            from_date=from_date,
            to_date=to_date
        )

        open_matches = []

        for match in matches:
            home_odds = bet_service.calculate_odds(session, match.id, BetPrediction.HOME_WIN)
            away_odds = bet_service.calculate_odds(session, match.id, BetPrediction.AWAY_WIN)

            response = MatchResponse.model_validate(match)
            response.home_score = None
            response.away_score = None
            response.match_result = None
            response.odds_home = home_odds
            response.odds_away = away_odds


            open_matches.append(response)

        if not open_matches:
            raise MatchNotFoundException()

        return open_matches


    # list de matchresponse?
    def get_team_history(self, session: Session, team_name: str) -> list[Match]:
        team_history = match_repository.get_by_team(session, team_name)

        if not team_history:
            raise MatchNotFoundException()

        return team_history
    
    def finish_match(self, session: Session, id: int):
        current_match = match_repository.get_by_id(session, id)
        
        if not current_match:
            raise MatchNotFoundException()
            
        # Realizar depois SoC - tirando a conversão daqui e levando para o FootballService

        football_service = FootballService() # injeta footballService
        response = football_service.fetch_match_by_id(current_match.api_match_id)
        
        # chaves vazia ou nulas não quebram o mapeamento .get()
        full_time = response.get('score', {}).get('fullTime') or {}
        score = response.get('score') or {}
        
        # Mudar tipo para none
        transformed = {
            "api_match_id": str(response.get("id")),
            'stage': response.get('stage'),
            'match_date': response.get('utcDate'),
            'status': response.get('status'),
            "home_team": (response.get("homeTeam") or {}).get('name'), 
            "away_team": (response.get("awayTeam") or {}).get('name'), 
            "home_score": full_time.get("home"), 
            "away_score": full_time.get('away'), 
            "match_result": score.get('winner')        
        }

        match = MatchApiData.model_validate(transformed)
        mapped_match = football_service.map_to_match(match)

        update_match = match_repository.update_result(
            session, 
            id, 
            mapped_match.home_score, 
            mapped_match.away_score, 
            mapped_match.match_result, 
            MatchStatus.FINISHED
        )

        bet_service = BetService()

        bet_service.settle_bets(session, update_match)
        
        return MatchResponse.model_validate(update_match)

    def update_status(self, session: Session, match_id: int):
        current_match = match_repository.get_by_id(session, match_id)
                
        if not current_match:
            raise MatchNotFoundException()

        update_match = match_repository.update_status(session, match_id)
        return MatchResponse.model_validate(update_match)