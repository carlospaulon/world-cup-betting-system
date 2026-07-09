from fastapi import status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginRequest, Token
from app.models.user import User
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException, UserInactiveException
from app.repositories.user_repository import user_repository
from app.core.security import hash_password, verify_password, create_access_token

DUMMY_HASH = "$2b$12$4Z70bklJ1yRvrP1GPCMdbOVmO7EtyzHGoAQZLdqkD2UuK10GbQsBC"


# Talvez dividir em 2 camadas user (register e change password) e auth (login)
class AuthService:
    
    def register_user(self, session: Session, user_data: UserCreate) -> UserResponse:
        existing_user = user_repository.get_by_email(session, user_data.email)

        if existing_user:
            raise UserAlreadyExistsException(
                message="Email já em uso",
                status_code=status.HTTP_409_CONFLICT
            )

        # Verificar cpf duplicado

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
    
    # aux method
    def authenticate_user(self, data: LoginRequest):
        user =  user_repository.get_by_email(data.email)
            
        # User inexistente e senha não verificada
        if not user:
            verify_password(data.password.get_secret_value(), DUMMY_HASH)
            return False
        if not verify_password(data.password.get_secret_value(), user.password):
            return False
        
        return user
        
    def login(self, data: LoginRequest) -> Token:
        user = self.authenticate_user(data)

        if not user:
            raise InvalidCredentialsException()
        
        if not user.is_active:
            raise UserInactiveException()
        
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return Token(access_token=access_token, token_type="bearer")