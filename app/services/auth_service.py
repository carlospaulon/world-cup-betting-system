from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, Token
from app.core.exceptions import InvalidCredentialsException, UserInactiveException
from app.repositories.user_repository import user_repository
from app.core.security import verify_password, create_access_token

#hardcoded...
DUMMY_HASH = "$2b$12$4Z70bklJ1yRvrP1GPCMdbOVmO7EtyzHGoAQZLdqkD2UuK10GbQsBC"

class AuthService:
    
    # aux method
    def authenticate_user(self, session: Session, data: LoginRequest):
        user =  user_repository.get_by_email(session, data.email)
            
        # User inexistente e senha não verificada
        if not user:
            verify_password(data.password.get_secret_value(), DUMMY_HASH)
            return False
        if not verify_password(data.password.get_secret_value(), user.password):
            return False
        
        return user
        
    def login(self, session: Session, data: LoginRequest) -> Token:
        user = self.authenticate_user(session, data)

        if not user:
            raise InvalidCredentialsException()
        
        if not user.is_active:
            raise UserInactiveException()
        
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return Token(access_token=access_token, token_type="bearer")