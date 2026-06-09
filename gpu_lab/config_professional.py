from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class LabConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_utilization: float = Field(default=50.0, ge=0.0, le=100.0)
    default_results_dir: str = Field(default="results")
    default_logs_dir: str = Field(default="logs")


def load_config(config_path: str | Path) -> dict:
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"config file path does not exist: {config_path}")
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    LabConfig(**data)
    return data


def validate_config(config: dict) -> None:
    LabConfig(**config)


def resolve_config(default_config: dict, override_config: dict) -> dict:
    merged = {**default_config, **override_config}
    LabConfig(**merged)
    return merged