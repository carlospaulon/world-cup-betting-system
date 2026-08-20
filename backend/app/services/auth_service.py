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
        """
        Verify user credentials against database records.

        Executes constant-time dummy password verification if user is not found
        to mitigate timing attacks.

        Args:
            session (Session): Database session connection.
            data (LoginRequest): User login payload containing email and password.

        Returns:
            User | False: User entity if authentication succeeds, False otherwise.
        """

        user =  user_repository.get_by_email(session, data.email)
            
        # User inexistente e senha não verificada
        if not user:
            verify_password(data.password.get_secret_value(), DUMMY_HASH)
            return False
        if not verify_password(data.password.get_secret_value(), user.password):
            return False
        
        return user
        
    def login(self, session: Session, data: LoginRequest) -> Token:
        """Authenticate a registered user

        Args:
            session (Session): current db connection
            data (LoginRequest): schema to request the login

        Raises:
            InvalidCredentialsException: Some information is wrong
            UserInactiveException: User is not active on the system

        Returns:
            Token: Generated JWT access token
        """
        user = self.authenticate_user(session, data)

        if not user:
            raise InvalidCredentialsException()
        
        if not user.is_active:
            raise UserInactiveException()
        
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return Token(access_token=access_token, token_type="bearer")