from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, session: Session, id) -> ModelType | None:
        """
        Retrieve a single entity instance by primary key ID.

        Args:
            session (Session): Current database session.
            id (Any): Primary key identifier value.

        Returns:
            ModelType | None: Model instance if found, None otherwise.
        """

        return session.get(self.model, id)
    
    def delete(self, session: Session, id) -> bool:
        """
        Delete a single entity instance from the database by ID.

        Args:
            session (Session): Current database session.
            id (Any): Primary key identifier of the target record to delete.

        Returns:
            bool: True if record was found and deleted, False otherwise.
        """

        user = session.get(self.model, id)
        if not user:
            return False
        session.delete(user)
        session.commit()
        return True
