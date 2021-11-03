"""Tests for the biorhythm processor module.

Covers date parsing and sine-wave calculation. Each function is tested
in isolation with edge cases and parametrized inputs.
"""

from datetime import date

import pytest

from biorhythm.errors import InvalidBirthDateError
from biorhythm.processor import calculate_biorhythm, parse_date


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
