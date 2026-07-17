from sqlalchemy.orm import Session
from app.models.match import Match
from app.repositories.match_repository import match_repository
from app.services.football_api_service import FootballService
from app.schemas.match import FootballApiResponse, MatchResponse, MatchApiData
from app.models.enum.match_enum import MatchResult, MatchStatus
from app.core.exceptions import MatchNotFoundException

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
    
    def get_open_matches(self, session: Session):
        open_matches = match_repository.get_all_open(session)
        return open_matches
        # Calcular odds?

    # list de matchresponse?
    def get_team_history(self, session: Session, team_name: str) -> list[Match]:
        team_history = match_repository.get_by_team(session, team_name)

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
            'stage': response.get('stage') or {},
            'match_date': response.get('utcDate') or {},
            'status': response.get('status') or {},
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
            mapped_match.status
        )

        # Chamar o settle bets - Depois

        return MatchResponse.model_validate(update_match)