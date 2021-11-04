"""Shared pytest fixtures for the biorhythm test suite."""

import pytest


@pytest.fixture
def sample_date() -> str:
    """A fixed ISO-format date string used across tests."""
    return "2000-01-01"
