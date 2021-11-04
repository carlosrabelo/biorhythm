"""Command-line interface for the biorhythm calculator."""

import argparse
import sys

from .errors import FutureBirthDateError, InvalidBirthDateError
from .processor import compute, parse_date


def main() -> None:
    """Parse args, compute biorhythms, and print formatted results."""
    parser = argparse.ArgumentParser(
        description="Biorhythm calculator - compute physical, emotional, "
        "and intellectual cycles from a birth date",
    )
    parser.add_argument(
        "birth_date",
        help="Birth date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--as-of",
        default=None,
        metavar="YYYY-MM-DD",
        help="Reference date for the calculation (default: today)",
    )
    args = parser.parse_args()

    try:
        as_of = parse_date(args.as_of) if args.as_of else None
        result = compute(args.birth_date, as_of=as_of)
    except (InvalidBirthDateError, FutureBirthDateError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Physical biorhythm     : {result['physical']:.2f}")
    print(f"Emotional biorhythm    : {result['emotional']:.2f}")
    print(f"Intellectual biorhythm : {result['intellectual']:.2f}")


if __name__ == "__main__":
    main()
