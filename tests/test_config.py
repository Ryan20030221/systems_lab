from __future__ import annotations

import pytest

from gpu_lab.config import load_config, resolve_config, validate_config


def test_load_config_returns_validated_config(tmp_path) -> None:
    config_path = tmp_path / "defaults.json"
    config_path.write_text(
        '{"min_utilization": 50}',
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config == {"min_utilization": 50.0}


def test_load_config_missing_file_raises_file_not_found(tmp_path) -> None:
    missing_config_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_config(missing_config_path)


def test_validate_config_rejects_missing_min_utilization() -> None:
    with pytest.raises(ValueError):
        validate_config({})


def test_validate_config_rejects_invalid_min_utilization_value() -> None:
    with pytest.raises(ValueError):
        validate_config({"min_utilization": 150})


def test_validate_config_rejects_non_numeric_min_utilization() -> None:
    with pytest.raises(ValueError):
        validate_config({"min_utilization": "high"})


def test_validate_config_rejects_boolean_min_utilization() -> None:
    with pytest.raises(ValueError):
        validate_config({"min_utilization": True})


def test_resolve_config_keeps_default_when_no_override() -> None:
    config = resolve_config({"min_utilization": 50.0})

    assert config == {"min_utilization": 50.0}


def test_resolve_config_cli_override_wins() -> None:
    config = resolve_config(
        {"min_utilization": 50.0},
        min_utilization=80,
    )

    assert config == {"min_utilization": 80.0}


def test_resolve_config_rejects_invalid_cli_override() -> None:
    with pytest.raises(ValueError):
        resolve_config(
            {"min_utilization": 50.0},
            min_utilization=150,
        )
