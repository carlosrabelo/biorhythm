"""Tests for the biorhythm CLI entry point."""

import sys

import pytest

from biorhythm.cli import main


def _run_main(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
) -> tuple[int | None, str, str]:
    """Invoke main() with argv and capture exit code plus stdout/stderr."""
    monkeypatch.setattr(sys, "argv", ["biorhythm", *argv])
    exit_code: int | None = None

    def fake_exit(code: int = 0) -> None:
        nonlocal exit_code
        exit_code = code
        raise SystemExit(code)

    monkeypatch.setattr(sys, "exit", fake_exit)

    from io import StringIO

    out = StringIO()
    err = StringIO()
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setattr(sys, "stderr", err)

    try:
        main()
    except SystemExit:
        pass

    return exit_code, out.getvalue(), err.getvalue()


class TestCli:
    """Tests for CLI argument handling and output."""

    def test_valid_date_prints_three_lines(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A valid birth date with --as-of prints three biorhythm lines."""
        code, out, err = _run_main(
            monkeypatch,
            ["2000-01-01", "--as-of", "2000-01-01"],
        )
        assert code is None
        assert err == ""
        assert "Physical biorhythm" in out
        assert "Emotional biorhythm" in out
        assert "Intellectual biorhythm" in out
        assert "0.00" in out

    def test_missing_birth_date_exits(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Omitting the birth date makes argparse exit with code 2."""
        monkeypatch.setattr(sys, "argv", ["biorhythm"])
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "birth_date" in captured.err or "required" in captured.err.lower()

    def test_invalid_date_exits_one(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """An unparseable birth date exits with code 1 and an error message."""
        code, out, err = _run_main(monkeypatch, ["not-a-date"])
        assert code == 1
        assert out == ""
        assert "Error:" in err
        assert "not-a-date" in err

    def test_future_date_exits_one(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A future birth date exits with code 1."""
        code, out, err = _run_main(
            monkeypatch,
            ["2099-01-01", "--as-of", "2000-01-01"],
        )
        assert code == 1
        assert out == ""
        assert "future" in err

    def test_invalid_as_of_exits_one(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """An invalid --as-of value exits with code 1."""
        code, out, err = _run_main(
            monkeypatch,
            ["2000-01-01", "--as-of", "bad"],
        )
        assert code == 1
        assert out == ""
        assert "Error:" in err
