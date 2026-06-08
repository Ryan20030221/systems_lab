import json
from pathlib import Path

import pytest

from gpu_lab.paths import (
    create_run_directory,
    ensure_directory,
    load_defaults,
    project_path,
    project_root,
)


def test_project_root_returns_existing_project_directory():
    root = project_root()

    assert isinstance(root, Path)
    assert root.exists()
    assert (root / "gpu_lab").exists()


def test_project_path_builds_path_from_project_root():
    path = project_path("config", "defaults.json")

    assert isinstance(path, Path)
    assert path.parts[-2:] == ("config", "defaults.json")


def test_ensure_directory_creates_directory(tmp_path):
    target = tmp_path / "new_results_folder"

    result = ensure_directory(target)

    assert isinstance(result, Path)
    assert result.exists()
    assert result.is_dir()


def test_load_defaults_loads_valid_config(tmp_path):
    config_path = tmp_path / "defaults.json"
    config_path.write_text(
        json.dumps(
            {
                "min_utilization": 50,
                "default_results_dir": "results",
                "default_logs_dir": "logs",
            }
        ),
        encoding="utf-8",
    )

    defaults = load_defaults(config_path)

    assert defaults["min_utilization"] == 50
    assert defaults["default_results_dir"] == "results"
    assert defaults["default_logs_dir"] == "logs"


def test_load_defaults_rejects_missing_required_key(tmp_path):
    config_path = tmp_path / "defaults.json"
    config_path.write_text(
        json.dumps(
            {
                "min_utilization": 50,
                "default_results_dir": "results",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_defaults(config_path)


def test_load_defaults_rejects_invalid_json(tmp_path):
    config_path = tmp_path / "defaults.json"
    config_path.write_text("{bad json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON config"):
        load_defaults(config_path)


def test_create_run_directory_creates_timestamped_folder(tmp_path):
    folder = create_run_directory("simple_test", tmp_path)

    assert isinstance(folder, Path)
    assert folder.exists()
    assert folder.is_dir()
    assert folder.parent == tmp_path
    assert "simple_test" in folder.name


def test_create_run_directory_rejects_empty_experiment_name(tmp_path):
    with pytest.raises(ValueError):
        create_run_directory("", tmp_path)


def test_load_defaults_rejects_invalid_value_types(tmp_path):
    config_path = tmp_path / "defaults.json"
    config_path.write_text(
        json.dumps(
            {
                "min_utilization": "high",
                "default_results_dir": 123,
                "default_logs_dir": None,
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_defaults(config_path)
