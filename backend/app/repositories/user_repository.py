import uuid
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
        """
        Persist a new User entity in the database.

        Args:
            session (Session): Database session instance.
            user_data (User): Instantiated User model to be persisted.

        Returns:
            User: Freshly saved and refreshed User model instance.
        """

        session.add(user_data)
        session.commit()
        session.refresh(user_data)
        return user_data
    
    def get_by_email(self, session: Session, email: str) -> User | None:
        """
        Retrieve a single user matching the specified email address.

        Args:
            session (Session): Database session connection.
            email (str): Target email address.

        Returns:
            User | None: User model if found, None otherwise.
        """

        query = select(self.model).where(self.model.email == email)
        result = session.execute(query)

        return result.scalars().first()

    def get_by_cpf(self, session: Session, cpf: str) -> User | None:
        """
        Retrieve a single user matching the specified CPF identification.

        Args:
            session (Session): Database session connection.
            cpf (str): Target CPF string.

        Returns:
            User | None: User model if found, None otherwise.
        """

        query = select(self.model).where(self.model.cpf == cpf)
        result = session.execute(query)

        return result.scalars().first()

    def get_all(self, session: Session) -> list[User]:
        """
        Fetch all registered users from database.

        Args:
            session (Session): Database session connection.

        Returns:
            list[User]: List of all existing users.
        """

        query = select(self.model)
        result = session.execute(query)

        return result.scalars().all()

    def get_users_actives(self, session: Session) -> list[User]:
        """
        Retrieve all active user accounts.

        Args:
            session (Session): Database session connection.

        Returns:
            list[User]: List of active user records.
        """

        query = select(self.model).where(self.model.is_active == True)
        result = session.execute(query)

        return result.scalars().all()
    
    def get_points(self, session: Session, cpf: str) -> User | None:
        """
        Get the current total points of a user identified by CPF.

        Args:
            session (Session): Database session connection.
            cpf (str): Target user CPF.

        Returns:
            int | None: User total points balance or None if CPF is not found.
        """

        query = select(self.model.points).where(self.model.cpf == cpf)
        result = session.execute(query)

        return result.scalars().first()

    def update_is_admin(self, session: Session, user_id: uuid.UUID):
        """
        Grant administrator privileges to a specific user.

        Args:
            session (Session): Database session connection.
            user_id (uuid.UUID): Target user UUID.

        Returns:
            User | None: Updated User record.
        """

        query = update(self.model).where(self.model.id == user_id).values(is_admin=True)
        session.execute(query)
        session.commit()

        return self.get_by_id(session, user_id)

    
    def update_points(self, session: Session, user_id, delta: int) -> User:
        """
        Increment or decrement user points score.

        Args:
            session (Session): Database session connection.
            user_id (uuid.UUID): Target user UUID.
            delta (int): Amount of points to add or subtract.

        Returns:
            User | None: Updated User record.
        """

        query = update(self.model).where(self.model.id == user_id).values(points=self.model.points + delta) 
        session.execute(query)
        session.commit()

        return self.get_by_id(session, user_id)
    
    
    def deactivate(self, session: Session, user_id) -> User:
        """
        Soft-delete a user account by setting is_active to False.

        Args:
            session (Session): Database session connection.
            user_id (uuid.UUID): Target user UUID.

        Returns:
            User | None: Updated User record.
        """

        query = update(self.model).where(self.model.id == user_id).values(is_active=False)
        session.execute(query)
        session.commit()

        return self.get_by_id(session, user_id)
    
    def get_ranking(self, session: Session) -> list:
        """
        Get user leaderboard ranked by won bets and total points.

        Args:
            session (Session): Database session connection.

        Returns:
            list[dict]: Ordered ranking mapping nickname, total points, and won bets count.
        """

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

        return result.mappings().all()


user_repository = UserRepository()