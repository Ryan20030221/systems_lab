from __future__ import annotations

import json
from pathlib import Path

Config = dict[str, float]
MIN_UTILIZATION_KEY = "min_utilization"

def validate_config(config: object) -> Config:
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    if MIN_UTILIZATION_KEY not in config:
        raise ValueError("missing required config key: min_utilization")
    value = config[MIN_UTILIZATION_KEY]
    if not isinstance(value , float | int) or isinstance(value, bool):
        raise ValueError("min_utilization must be float or int")
    if not 0<= value <= 100:
        raise ValueError("min_utilization must be between 0 and 100 inclusive")
    return {MIN_UTILIZATION_KEY: float(value)}




def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise FileNotFoundError(f"config file path does not exist: {config_path}")
    with open(config_path, "r",encoding="utf-8") as file:
        raw_config = json.load(file)
    
    validated_config = validate_config(raw_config)

    return validated_config

def resolve_config(
    default_config: Config,
    *,
    min_utilization: float | None = None,
) -> Config:
    resolved_config = dict(default_config)

    if min_utilization is not None:
        resolved_config[MIN_UTILIZATION_KEY] = min_utilization

    return validate_config(resolved_config)
    

    

