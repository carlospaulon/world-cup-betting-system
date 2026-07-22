class AppException(Exception):
    def __init__(self, message: str, status_code: int, headers: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers

class UnderageUserException(AppException):
    def __init__(self, message: str = "User must be at least 18 years old", status_code: int = 400):
        super().__init__(message, status_code)

class UserAlreadyExistsException(AppException):
    def __init__(self, message: str = 'User already exists', status_code: int = 409):
        super().__init__(message, status_code)

class InvalidCredentialsException(AppException):
    def __init__(self, message: str = 'Invalid email or password', status_code: int = 401, headers: dict = {}):
        super().__init__(message, status_code, headers)

class UserNotFoundException(AppException):
    def __init__(self, message: str = 'User was not found', status_code: int = 404):
        super().__init__(message, status_code)

class UserInactiveException(AppException):
    def __init__(self, message: str = 'User is inactive', status_code: int = 403):
        super().__init__(message, status_code)

class WeakPasswordException(AppException):
    def __init__(self, message: str = 'Password does not meet security requirements', status_code: int = 422):
        super().__init__(message, status_code)

class ServiceUnavailableException(AppException):
    def __init__(self, message: str = 'Service Unavailable', status_code: int = 503):
        super().__init__(message, status_code)

class MatchNotFoundException(AppException):
    def __init__(self, message: str = 'Match was not found', status_code: int = 404):
        super().__init__(message, status_code)

class MatchNotOpenException(AppException):
    def __init__(self, message: str = 'Match is not open for betting', status_code: int = 409):
        super().__init__(message, status_code)

class InsufficientPointsException(AppException):
    def __init__(self, message: str = 'Insufficient points for this bet', status_code: int = 409):
        super().__init__(message, status_code)

