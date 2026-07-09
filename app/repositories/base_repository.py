from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    # Definir type para uuid?
    # Create responsabilidade de cada entidade
    def get_by_id(self, session: Session, id) -> ModelType | None:
        return session.get(self.model, id)
    
    def delete(self, session: Session, id) -> bool:
        user = session.get(self.model, id)
        if not user:
            return False
        session.delete(user)
        session.commit()
        return True
