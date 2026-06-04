from __future__ import annotations

import os
import subprocess
import sys


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    return subprocess.run(
        [sys.executable, "scripts/run_configured_analysis.py", *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_run_configured_analysis_uses_default_config() -> None:
    result = run_script()

    assert result.returncode == 0
    assert "config file: config/defaults.json" in result.stdout
    assert "min utilization: 50.0" in result.stdout


def test_run_configured_analysis_cli_override_wins() -> None:
    result = run_script("--min-util", "80")

    assert result.returncode == 0
    assert "min utilization: 80.0" in result.stdout


def test_run_configured_analysis_rejects_invalid_override() -> None:
    result = run_script("--min-util", "150")

    assert result.returncode != 0
    assert "min_utilization must be between 0 and 100 inclusive" in result.stderr