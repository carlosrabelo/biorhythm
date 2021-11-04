"""Tests for the biorhythm processor module.

Covers date parsing, day-counting, sine-wave calculation, and the high-level
compute() entry point. Each function is tested in isolation with edge cases
and parametrized inputs.
"""

from datetime import date, timedelta

import pytest

from biorhythm.errors import FutureBirthDateError, InvalidBirthDateError
from biorhythm.processor import (
    calculate_biorhythm,
    compute,
    days_since_birth,
    parse_date,
)


class TestCalculateBiorhythm:
    """Tests for the calculate_biorhythm() function."""

    def test_zero_days_all_zero(self) -> None:
        """At day zero all cycles start at the baseline (0)."""
        physical, emotional, intellectual = calculate_biorhythm(0)
        assert physical == pytest.approx(0.0, abs=0.01)
        assert emotional == pytest.approx(0.0, abs=0.01)
        assert intellectual == pytest.approx(0.0, abs=0.01)

    def test_physical_cycle_full_period(self) -> None:
        """After exactly 23 days the physical cycle returns to baseline."""
        physical, _, _ = calculate_biorhythm(23)
        assert physical == pytest.approx(0.0, abs=0.01)

    def test_emotional_cycle_full_period(self) -> None:
        """After exactly 28 days the emotional cycle returns to baseline."""
        _, emotional, _ = calculate_biorhythm(28)
        assert emotional == pytest.approx(0.0, abs=0.01)

    def test_intellectual_cycle_full_period(self) -> None:
        """After exactly 33 days the intellectual cycle returns to baseline."""
        _, _, intellectual = calculate_biorhythm(33)
        assert intellectual == pytest.approx(0.0, abs=0.01)

    def test_returns_three_values(self) -> None:
        """The function always returns exactly three float values."""
        result = calculate_biorhythm(100)
        assert len(result) == 3

    @pytest.mark.parametrize("days", [1, 10, 100, 365, 1000, 10000])
    def test_values_always_within_range(self, days: int) -> None:
        """All three biorhythm values must lie between -100 and +100."""
        physical, emotional, intellectual = calculate_biorhythm(days)
        for value in [physical, emotional, intellectual]:
            assert -100.0 <= value <= 100.0


class TestDaysSinceBirth:
    """Tests for the days_since_birth() function."""

    def test_today_returns_zero(self) -> None:
        """A birth date set to today yields zero days."""
        today = date.today()
        assert days_since_birth(today) == 0

    def test_yesterday_returns_one(self) -> None:
        """A birth date one day ago yields exactly one day."""
        yesterday = date.today() - timedelta(days=1)
        assert days_since_birth(yesterday) == 1

    def test_as_of_overrides_today(self) -> None:
        """An explicit as_of date controls the day count."""
        birth = date(2000, 1, 1)
        assert days_since_birth(birth, as_of=date(2000, 1, 11)) == 10

    def test_future_birth_raises(self) -> None:
        """A birth date after the reference date raises FutureBirthDateError."""
        with pytest.raises(FutureBirthDateError):
            days_since_birth(date(2099, 1, 1), as_of=date(2000, 1, 1))


class TestParseDate:
    """Tests for the parse_date() function."""

    def test_iso_format(self) -> None:
        """ISO 8601 format (YYYY-MM-DD) is accepted."""
        dt = parse_date("2000-01-01")
        assert dt == date(2000, 1, 1)

    def test_invalid_brazilian_format_raises(self) -> None:
        """Brazilian format (DD/MM/YYYY) is rejected."""
        with pytest.raises(InvalidBirthDateError):
            parse_date("01/01/2000")

    def test_iso_with_time_raises(self) -> None:
        """ISO format with time component is rejected."""
        with pytest.raises(InvalidBirthDateError):
            parse_date("2000-01-01 12:30:00")

    def test_invalid_string_raises(self) -> None:
        """A string that is not a date raises InvalidBirthDateError."""
        with pytest.raises(InvalidBirthDateError):
            parse_date("not-a-date")

    def test_impossible_calendar_date_raises(self) -> None:
        """Impossible calendar dates are rejected."""
        with pytest.raises(InvalidBirthDateError):
            parse_date("2000-02-30")


class TestCompute:
    """Tests for the high-level compute() function."""

    def test_returns_dict_with_expected_keys(self, sample_date: str) -> None:
        """The result dict contains physical, emotional, and intellectual keys."""
        result = compute(sample_date, as_of=date(2000, 1, 1))
        assert set(result) == {"physical", "emotional", "intellectual"}

    def test_values_are_floats(self, sample_date: str) -> None:
        """All values in the result dict are of type float."""
        result = compute(sample_date, as_of=date(2000, 1, 1))
        for value in result.values():
            assert isinstance(value, float)

    def test_as_of_is_deterministic(self, sample_date: str) -> None:
        """compute() with as_of returns stable values independent of today."""
        result = compute(sample_date, as_of=date(2000, 1, 1))
        assert result["physical"] == pytest.approx(0.0, abs=0.01)
        assert result["emotional"] == pytest.approx(0.0, abs=0.01)
        assert result["intellectual"] == pytest.approx(0.0, abs=0.01)

    def test_invalid_date_raises(self) -> None:
        """Passing an unparseable date string raises InvalidBirthDateError."""
        with pytest.raises(InvalidBirthDateError):
            compute("invalid")

    def test_future_date_raises(self) -> None:
        """A future birth date raises FutureBirthDateError."""
        with pytest.raises(FutureBirthDateError):
            compute("2099-01-01", as_of=date(2000, 1, 1))
