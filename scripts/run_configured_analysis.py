from __future__ import annotations

import argparse
from pathlib import Path

from gpu_lab.config import MIN_UTILIZATION_KEY, load_config, resolve_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run GPU analysis with config defaults and CLI overrides."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/defaults.json"),
        help="Path to the JSON config file.",
    )
    parser.add_argument(
        "--min-util",
        type=float,
        default=None,
        help="Override the minimum utilization threshold.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    default_config = load_config(args.config)
    resolved_config = resolve_config(
        default_config,
        min_utilization=args.min_util,
    )

    print(f"config file: {args.config}")
    print(f"min utilization: {resolved_config[MIN_UTILIZATION_KEY]}")


if __name__ == "__main__":
    main()
