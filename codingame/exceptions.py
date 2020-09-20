class CodinGameAPIError(Exception):
    """Base exception for the CodinGame API."""
    def __init__(self, message: str):
        self.message = message

class CodinGamerNotFound(CodinGameAPIError):
    """Raised when a CodinGamer isn't found."""
    pass

class ClashOfCodeNotFound(CodinGameAPIError):
    """Raised when a Clash of Code isn't found."""
    pass

class LoginRequired(CodinGameAPIError):
    """Raised when an action requires the client to log in."""
    def __init__(self, message: str = None):
        super().__init__(message or "You must be logged in to perform this action.")
