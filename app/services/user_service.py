from fastapi import status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdatePassword
from app.models.user import User
from app.core.exceptions import UserAlreadyExistsException
from app.repositories.user_repository import user_repository
from app.core.security import hash_password

class UserService:
    def register_user(self, session: Session, user_data: UserCreate) -> UserResponse:
        existing_user = user_repository.get_by_email(session, user_data.email)

        if existing_user:
            raise UserAlreadyExistsException(
                message="Email já em uso",
                status_code=status.HTTP_409_CONFLICT
            )
        
        

        # Verificar cpf duplicado
        duplicated_cpf = session.query(
            session.query(User).filter_by(cpf=user_data.cpf).exists()
        ).scalar()

        if duplicated_cpf:
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
    
    def update_password(self, session: Session, data: UserUpdatePassword):
        ...