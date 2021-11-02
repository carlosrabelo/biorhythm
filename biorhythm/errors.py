"""Custom exception types for the biorhythm calculator.

Provides a hierarchy of domain-specific exceptions that allow callers to
handle validation and processing errors distinctly, rather than relying on
built-in exception types.
"""


class BiorhythmError(Exception):
    """Base exception for all biorhythm-related errors.

    All custom exceptions in this package inherit from this class, making it
    easy to catch any biorhythm error with a single except clause.
    """


class InvalidBirthDateError(BiorhythmError):
    """Raised when the birth date string is not a valid YYYY-MM-DD date.

    Attributes:
        value: The raw input string that failed to parse.
    """

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"invalid birth date: {value}")


class FutureBirthDateError(BiorhythmError):
    """Raised when the birth date is after the reference date.

    Attributes:
        value: The birth date string that was rejected.
    """

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f"birth date is in the future: {value}")
