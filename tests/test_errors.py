"""Tests for the custom exception types.

Verifies the exception hierarchy and the message/value formatting of
domain errors.
"""

from biorhythm.errors import (
    BiorhythmError,
    FutureBirthDateError,
    InvalidBirthDateError,
)


class TestBiorhythmError:
    """Tests for the base BiorhythmError class."""

    def test_is_exception(self) -> None:
        """BiorhythmError inherits from Exception."""
        assert issubclass(BiorhythmError, Exception)


class TestInvalidBirthDateError:
    """Tests for InvalidBirthDateError."""

    def test_message_contains_value(self) -> None:
        """The error message includes the raw input string."""
        err = InvalidBirthDateError("bad-date")
        assert "bad-date" in str(err)

    def test_value_attribute(self) -> None:
        """The value attribute stores the original input."""
        err = InvalidBirthDateError("bad-date")
        assert err.value == "bad-date"

    def test_inherits_biorhythm_error(self) -> None:
        """InvalidBirthDateError is a subclass of BiorhythmError."""
        assert issubclass(InvalidBirthDateError, BiorhythmError)


class TestFutureBirthDateError:
    """Tests for FutureBirthDateError."""

    def test_message_contains_value(self) -> None:
        """The error message includes the birth date string."""
        err = FutureBirthDateError("2099-01-01")
        assert "2099-01-01" in str(err)

    def test_inherits_biorhythm_error(self) -> None:
        """FutureBirthDateError is a subclass of BiorhythmError."""
        assert issubclass(FutureBirthDateError, BiorhythmError)
