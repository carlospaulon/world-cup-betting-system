import httpx
from app.models.match import Match
from app.schemas.match import MatchApiData
from app.core.config import get_settings


settings = get_settings()
API_KEY = settings.API_KEY
headers = {'X-Auth-Token': API_KEY}

class FootballService:

    def fetch_matches(self, competition='WC', season=2026):
        # season? tratar erros - usar try
        with httpx.Client() as client:
            response = client.get(
                f'https://api.football-data.org/v4/competitions/{competition}/matches', 
                headers=headers)
            
            return response.json()
    
    def fetch_match_by_id(self, match_id: int):
        with httpx.Client() as client:
            response = client.get(
                f'https://api.football-data.org/v4/matches/{match_id}', 
                headers=headers)
            
            return response.json()
        
    def map_to_match(self, data: MatchApiData):

        match = Match(
            api_match_id = data.api_match_id,
            home_team = data.home_team,
            away_team = data.away_team,
            match_date = data.match_date,
            status = data.status,
            stage = data.stage,
            home_score = data.home_score,
            away_score = data.away_score,
            match_result = data.match_result
        )
        return match