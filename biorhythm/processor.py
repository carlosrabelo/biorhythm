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

PHYSICAL_CYCLE = 23
EMOTIONAL_CYCLE = 28
INTELLECTUAL_CYCLE = 33


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
