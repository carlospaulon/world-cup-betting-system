from app.models.user import User
from app.models.bet import Bet
from app.models.enum.bet_enum import BetResult
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository, ModelType

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    def create(self, session: Session, user_data: ModelType):
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data
    
    def get_by_email(self, session: Session, email: str) -> User | None:
        query = select(self.model).where(self.model.email == email)
        result = session.execute(query)

        return result.scalars().first()

    def get_by_cpf(self, session: Session, cpf: str) -> User | None:
        query = select(self.model).where(self.model.cpf == cpf)
        result = session.execute(query)

        return result.scalars().first()

    def get_all(self, session: Session) -> list[User]:
        query = select(self.model)
        result = session.execute(query)

        return result.scalars().all()
    
    def get_points(self, session: Session, cpf: str) -> User | None:
        query = select(self.model.points).where(self.model.cpf == cpf)
        result = session.execute(query)

        return result.scalars().first()
    
    def update_points(self, session: Session, user_id, delta: int) -> User:
        query = update(self.model).where(self.model.id == user_id).values(points=self.model.points + delta) 
        result = session.execute(query)
        session.commit()

        return self.get_by_id(session, user_id)
    
    
    def deactivate(self, session: Session, user_id) -> User:
        query = update(self.model).where(self.model.id == user_id).values(is_active=False)
        session.execute(query)
        session.commit()

        return self.get_by_id(session, user_id)
    
    def get_ranking(self, session: Session) -> list:
        wins_count = func.count(Bet.id).label('bets_wins')

        query = (select(
                self.model.nickname, 
                self.model.points,
                wins_count
            )
            .join(Bet)
            .where(Bet.result == BetResult.WON)
            .group_by(
                self.model.id,
                self.model.nickname,
                self.model.points
            )
            .order_by(
                wins_count.desc(), 
                self.model.points.desc()
            )
        )

        result = session.execute(query)

        return result.all()


user_repository = UserRepository()