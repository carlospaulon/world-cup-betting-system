class AppException(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class UnderageUserException(AppException):
    def __init__(self, message: str = "User must be at least 18 years old", status_code: int = 400):
        super().__init__(message, status_code)

class UserAlreadyExistsException(AppException):
    def __init__(self, message: str = 'User already exists', status_code: int = 409):
        super().__init__(message, status_code)

class InvalidCredentialsException(AppException):
    def __init__(self, message: str = 'Invalid email or password', status_code: int = 401):
        super().__init__(message, status_code)

class UserNotFoundException(AppException):
    def __init__(self, message: str = 'User was not found', status_code: int = 404):
        super().__init__(message, status_code)

class UserInactiveException(AppException):
    def __init__(self, message: str = 'User is inactive', status_code: int = 403):
        super().__init__(message, status_code)

class WeakPasswordException(AppException):
    def __init__(self, message: str = 'Password does not meet security requirements', status_code: int = 422):
        super().__init__(message, status_code)

