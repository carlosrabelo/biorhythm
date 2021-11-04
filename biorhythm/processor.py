"""Core biorhythm calculation logic.

This module contains the mathematical functions that compute biorhythm values
from a given number of days lived. The biorhythm theory posits three cycles:

- Physical cycle:   23 days  -  stamina, strength, coordination
- Emotional cycle:  28 days  -  mood, sensitivity, creativity
- Intellectual cycle: 33 days  -  alertness, analytical ability, memory

Each cycle is modelled as a sine wave oscillating between -100 and +100,
where zero represents the baseline, positive values indicate a high phase,
and negative values indicate a low phase.
"""

import math
from datetime import date, datetime
from typing import TypedDict

from .errors import FutureBirthDateError, InvalidBirthDateError

PHYSICAL_CYCLE = 23
EMOTIONAL_CYCLE = 28
INTELLECTUAL_CYCLE = 33


class BiorhythmResult(TypedDict):
    """Biorhythm values as percentages in the -100..+100 range."""

    physical: float
    emotional: float
    intellectual: float


def days_since_birth(birth_date: date, as_of: date | None = None) -> int:
    """Calculate the number of days between the birth date and a reference day.

    Args:
        birth_date: The person's date of birth.
        as_of: Reference date for the calculation. Defaults to today.

    Returns:
        The whole number of days elapsed since the birth date.

    Raises:
        FutureBirthDateError: If birth_date is after the reference date.
    """
    reference = as_of if as_of is not None else date.today()
    days = (reference - birth_date).days
    if days < 0:
        raise FutureBirthDateError(birth_date.isoformat())
    return days


def calculate_biorhythm(days: int) -> tuple[float, float, float]:
    """Compute the three biorhythm values for a given number of days lived.

    Each cycle is expressed as a sine wave normalized to a -100..+100 scale.
    A value of  0 means the cycle is at its baseline (crossing point).
    A value of +100 means the cycle is at its peak.
    A value of -100 means the cycle is at its trough.

    Args:
        days: Total number of days the person has lived.

    Returns:
        A 3-tuple of (physical, emotional, intellectual) as percentages.
    """
    physical = math.sin(2 * math.pi * days / PHYSICAL_CYCLE) * 100
    emotional = math.sin(2 * math.pi * days / EMOTIONAL_CYCLE) * 100
    intellectual = math.sin(2 * math.pi * days / INTELLECTUAL_CYCLE) * 100
    return physical, emotional, intellectual


def parse_date(date_str: str) -> date:
    """Parse a date string in ISO 8601 format (YYYY-MM-DD).

    This function enforces a strict single-format policy to avoid ambiguity.
    For example, "01/02/2000" could be January 2nd (US) or February 1st (BR),
    so only the unambiguous ISO format is accepted.

    Args:
        date_str: The date string to parse, must be in YYYY-MM-DD format.

    Returns:
        A date object corresponding to the parsed value.

    Raises:
        InvalidBirthDateError: If the string does not match YYYY-MM-DD.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise InvalidBirthDateError(date_str) from e


def compute(
    birth_date_str: str,
    as_of: date | None = None,
) -> BiorhythmResult:
    """High-level entry point: parse a birth date and compute biorhythms.

    This is the main function that the CLI delegates to. It combines date
    parsing, day-count calculation, and the biorhythm formula into a single
    call that returns a ready-to-display dictionary.

    Args:
        birth_date_str: A date string in YYYY-MM-DD format.
        as_of: Optional reference date. Defaults to today.

    Returns:
        A dictionary with keys 'physical', 'emotional', and 'intellectual',
        each mapping to a float between -100 and +100.

    Raises:
        InvalidBirthDateError: If birth_date_str cannot be parsed.
        FutureBirthDateError: If the birth date is after the reference date.
    """
    birth_date = parse_date(birth_date_str)
    days = days_since_birth(birth_date, as_of=as_of)
    physical, emotional, intellectual = calculate_biorhythm(days)
    return {
        "physical": physical,
        "emotional": emotional,
        "intellectual": intellectual,
    }
