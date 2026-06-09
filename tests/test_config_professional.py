from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from gpu_lab.config_professional import load_config, resolve_config, validate_config

# A config containing exactly the keys the model knows about.
# (With extra="forbid", an unknown key in here would itself raise — see the typo test.)
VALID = {
    "min_utilization": 50.0,
    "default_results_dir": "results",
    "default_logs_dir": "logs",
}


def test_valid_config_passes():
    # Happy path: a well-formed config validates without raising.
    validate_config(VALID)


def test_load_config_returns_the_data(tmp_path):
    # load_config reads JSON off disk and hands back the same dict.
    path = tmp_path / "config.json"
    path.write_text(json.dumps(VALID), encoding="utf-8")
    assert load_config(path) == VALID


def test_missing_file_raises(tmp_path):
    # A path that doesn't exist fails loudly instead of silently.
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.json")


def test_value_out_of_range_raises():
    # min_utilization is bounded 0–100; 150 must be rejected.
    with pytest.raises(ValidationError):
        validate_config({**VALID, "min_utilization": 150.0})


def test_wrong_type_raises():
    # A non-numeric string where a float is expected must be rejected.
    with pytest.raises(ValidationError):
        validate_config({**VALID, "min_utilization": "not a number"})


def test_misspelled_key_raises():
    # This is what extra="forbid" buys you: a typo is caught, not ignored.
    with pytest.raises(ValidationError):
        validate_config({**VALID, "min_utilizaton": 50.0})


def test_resolve_override_wins():
    # Override keys beat defaults, and the merged result is validated before return.
    merged = resolve_config(VALID, {"min_utilization": 80.0})
    assert merged["min_utilization"] == 80.0
