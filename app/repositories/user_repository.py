from app.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository, ModelType

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    # Crio um schema para userInDb? Retorna um User!
    def create(self, session: Session, user_data: ModelType):
        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data
    
    def get_by_email(self, session: Session, email: str) -> User | None:
        # Usando query e execute, mas posso usar o scalar direto com o select
        query = select(self.model).where(self.model.email == email)
        result = session.execute(query)

        return result.scalars().first()

    def get_by_cpf(self, session: Session, cpf: str) -> User | None:
        ...

    def get_all(self, session: Session) -> list[User]:
        ...
    
    def update_points(self, user_id, delta: int) -> User:
        ...

    def deactivate(self, session: Session, user_id) -> User:
        ...
    
    def get_ranking(self, session: Session) -> list:
        ...
    
    


user_repository = UserRepository()