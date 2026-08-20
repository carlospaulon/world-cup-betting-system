import uuid
from fastapi import status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdatePassword
from app.models.user import User
from app.core.exceptions import UserAlreadyExistsException,UserNotFoundException, InvalidCredentialsException, UserAlreadyIsAdminException
from app.repositories.user_repository import user_repository
from app.core.security import hash_password, verify_password, validate_password_strength

class UserService:
    def register_user(self, session: Session, user_data: UserCreate) -> UserResponse:
        """
        Register a new user account with initial points balance.

        Validates uniqueness of email and CPF identifiers.

        Args:
            session (Session): Current database session.
            user_data (UserCreate): Registration input payload.

        Raises:
            UserAlreadyExistsException: If email or CPF is already registered.

        Returns:
            UserResponse: Validated schema of created user account.
        """

        existing_user = user_repository.get_by_email(session, user_data.email)

        if existing_user:
            raise UserAlreadyExistsException(
                message="Email já em uso",
                status_code=status.HTTP_409_CONFLICT
            )
        
        # Verificar cpf duplicado
        existing_cpf = user_repository.get_by_cpf(session, user_data.cpf)

        if existing_cpf:
            raise UserAlreadyExistsException(
                message="CPF já cadastrado",
                status_code=status.HTTP_409_CONFLICT
            )


        hashed_password = hash_password(user_data.password)

        user = User(
            nickname=user_data.nickname,
            email=user_data.email,
            cpf=user_data.cpf,
            date_of_birth=user_data.date_of_birth,
            password=hashed_password,
            points=100,
            is_active=True,
            is_admin=False
        )
        
        created_user = user_repository.create(session, user)
        return UserResponse.model_validate(created_user)

    def update_is_admin(self, session: Session, admin_user: User, user_id: uuid.UUID):
        """
        Promote a standard user to administrator status.

        Args:
            session (Session): Current database session.
            admin_user (User): Requesting administrator user entity.
            user_id (uuid.UUID): Target user UUID to promote.

        Raises:
            UserNotFoundException: Target user does not exist.
            UserAlreadyIsAdminException: User is already an administrator.
            InvalidCredentialsException: Requesting user lacks administrator privileges.

        Returns:
            User: Updated target user instance with administrator rights.
        """

        user = user_repository.get_by_id(session, user_id)

        if not user:
            raise UserNotFoundException()

        if user.is_admin:
            raise UserAlreadyIsAdminException()

        if not admin_user.is_admin:
            raise InvalidCredentialsException()

        user_repository.update_is_admin(session, user.id)

        return user

    
    def update_password(self, session: Session, user_id,  data: UserUpdatePassword):
        """
        Change an existing user's password following current password validation and strength rules.

        Args:
            session (Session): Current database session.
            user_id (uuid.UUID): Target user UUID.
            data (UserUpdatePassword): Current and new password payload.

        Raises:
            UserNotFoundException: Target user does not exist.
            InvalidCredentialsException: Provided current password is incorrect.

        Returns:
            User: Updated user model instance with refreshed hashed password.
        """

        user = user_repository.get_by_id(session, user_id)

        if not user:
            raise UserNotFoundException()
        
        is_match = verify_password(data.current_password, user.password)

        if not is_match:
            raise InvalidCredentialsException()

        strong_password = validate_password_strength(data.new_password)

        hashed_password = hash_password(strong_password)

        user.password = hashed_password
        session.commit()
        session.refresh(user)

        return user