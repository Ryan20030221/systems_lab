import json
from json import JSONDecodeError
from pathlib import Path

from gpu_lab.time_utils import utc_timestamp_for_filename

REQUIRED_DEFAULT_KEYS = {
    "min_utilization",
    "default_results_dir",
    "default_logs_dir",
}


def project_root():
    return Path(__file__).resolve().parents[1]


def project_path(*parts):
    return project_root().joinpath(*parts)


def ensure_directory(path):
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def load_defaults(config_path=None):
    if config_path is None:
        config_path = project_path("config", "defaults.json")
    else:
        config_path = Path(config_path)

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            defaults = json.load(file)

    except JSONDecodeError as error:
        raise ValueError(f"Invalid JSON config: {config_path}") from error

    missing_keys = REQUIRED_DEFAULT_KEYS - defaults.keys()

    if missing_keys:
        raise ValueError(f"Missing required config keys: {sorted(missing_keys)}")
    if not isinstance(defaults["min_utilization"], int):
        raise ValueError("min_utilization must be an integer")

    if not isinstance(defaults["default_results_dir"], str):
        raise ValueError("default_results_dir must be a string")

    if not isinstance(defaults["default_logs_dir"], str):
        raise ValueError("default_logs_dir must be a string")
    return defaults


def create_run_directory(experiment_name, base_dir=None):
    if experiment_name.strip() == "":
        raise ValueError("experiment_name cannot be empty")

    if base_dir is None:
        defaults = load_defaults()
        base_dir = project_path(defaults["default_results_dir"])

    else:
        base_dir = Path(base_dir)

    timestamp = utc_timestamp_for_filename()
    run_folder = base_dir / f"{timestamp}_{experiment_name}"

    run_folder.mkdir(parents=True, exist_ok=False)

    return run_folder
