__all__ = (
    "CodinGameAPIError",
    "LoginError",
    "EmailRequired",
    "MalformedEmail",
    "PasswordRequired",
    "EmailNotLinked",
    "IncorrectPassword",
    "LoginRequired",
    "NotFound",
    "CodinGamerNotFound",
    "ClashOfCodeNotFound",
    "ChallengeNotFound",
    "PuzzleNotFound",
)


class CodinGameAPIError(Exception):
    """Base exception for the CodinGame API."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class LoginError(CodinGameAPIError):
    """Raised when the login data is incorrect."""

    @classmethod
    def from_id(cls, id: int, message: str):  # pragma: no cover
        # unused since the login method changed
        errors = {
            332: EmailRequired,
            334: MalformedEmail,
            336: PasswordRequired,
            393: EmailNotLinked,
            396: IncorrectPassword,
            701: WrongCaptchaAnswer,
        }
        return errors.get(id, cls)(message)


class EmailRequired(LoginError):
    """Raised when the email given at login is empty."""


class MalformedEmail(LoginError):
    """Raised when the email given at login isn't well formed."""


class PasswordRequired(LoginError):
    """Raised when the password given at login is empty."""


class EmailNotLinked(LoginError):
    """Raised when the email given at login isn't linked to a CodinGamer
    account."""


class IncorrectPassword(LoginError):
    """Raised when the password given at login is incorrect."""


class WrongCaptchaAnswer(LoginError):
    """Raised when the captcha in the email/password login is incorrect.

    See :ref:`login` to fix this"""


class LoginRequired(LoginError):
    """Raised when an action requires the client to log in."""

    def __init__(self, message: str = None):
        super().__init__(
            message or "You must be logged in to perform this action."
        )


class NotFound(CodinGameAPIError):
    """Raised when something isn't found."""

    @classmethod
    def from_type(cls, type: str, message: str):
        errors = {
            "codingamer": CodinGamerNotFound,
            "clash_of_code": ClashOfCodeNotFound,
            "challenge": ChallengeNotFound,
            "puzzle": PuzzleNotFound,
        }
        return errors.get(type, cls)(message)


class CodinGamerNotFound(NotFound):
    """Raised when a CodinGamer isn't found."""


class ChallengeNotFound(NotFound):
    """Raised when a Challenge isn't found."""


class PuzzleNotFound(NotFound):
    """Raised when a Puzzle isn't found."""


class ClashOfCodeError(CodinGameAPIError):
    """Raised when there is an error with a Clash of Code."""

    @classmethod
    def from_id(cls, id: int, message: str):
        errors = {
            502: ClashOfCodeNotFound,
            504: ClashOfCodeStarted,
            505: ClashOfCodeFinished,
            506: ClashOfCodeFull,
        }
        return errors.get(id, cls)(message)


class ClashOfCodeNotFound(NotFound, ClashOfCodeError):
    """Raised when a Clash of Code isn't found."""


class ClashOfCodeStarted(ClashOfCodeError):
    """Raised when trying to join an already started Clash of Code."""


class ClashOfCodeFinished(ClashOfCodeError):
    """Raised when trying to join an already finished Clash of Code."""


class ClashOfCodeFull(ClashOfCodeError):
    """Raised when trying to join a Clash of Code that reached the maximum
    number of players."""
