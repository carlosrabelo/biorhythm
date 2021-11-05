# Biorhythm

Biorhythm calculator that computes the physical, emotional, and intellectual cycles from a given birth date.

## Highlights

- Computes three biorhythm cycles: physical (23 days), emotional (28 days), and intellectual (33 days)
- Accepts dates in YYYY-MM-DD (ISO 8601) format
- Rejects invalid and future birth dates
- Returns values as percentages ranging from -100 to +100
- Optional `--as-of` reference date for deterministic calculations
- Make-driven setup with ruff, mypy, and pytest
- Installable entry point via `make install`

## Installation

### Build from Source

```bash
git clone https://github.com/carlosrabelo/biorhythm.git
cd biorhythm
make setup
```

Install to `~/.local/bin` (default), or system-wide to `/usr/local/bin` (sudo only for the copy):

```bash
make install
make install-system
make uninstall    # removes from both common locations
```

## Usage

```bash
.venv/bin/python -m biorhythm.cli 2000-01-01 --as-of 2000-01-12
# Physical biorhythm     : 13.62
# Emotional biorhythm    : 62.35
# Intellectual biorhythm : 86.60
```

Omit `--as-of` to use today as the reference date:

```bash
.venv/bin/python -m biorhythm.cli 2000-01-01
```

Or after `make install`:

```bash
biorhythm 2000-01-01
biorhythm 2000-01-01 --as-of 2020-06-15
```

## Project Layout

```
biorhythm/           # Source code package
    cli.py           # Entry point (CLI)
    processor.py     # Calculation logic
    errors.py        # Custom exceptions
tests/               # Test suite
.make/               # Automation scripts
pyproject.toml       # Metadata and dependencies
Makefile             # Orchestration
```

## Development

```bash
make setup           # Create .venv and install dependencies (first time only)
make test            # Run all tests
make quality         # Format, lint, and type-check
make install         # Install entry point to ~/.local/bin
make install-system  # Install entry point to /usr/local/bin
make uninstall       # Remove from both common locations
```

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
