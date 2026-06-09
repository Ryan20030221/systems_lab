from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from gpu_lab.config_professional import load_config, resolve_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Load, validate, and optionally override the GPU lab config "
        "using the professional (Pydantic) config implementation.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/defaults.json"),
        help="Path to the JSON config file (default: config/defaults.json).",
    )
    parser.add_argument(
        "--min-utilization",
        type=float,
        default=None,
        help="Optional override for min_utilization (0-100).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        loaded = load_config(args.config)
    except FileNotFoundError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as error:
        print(f"error: {args.config} is not valid JSON: {error}", file=sys.stderr)
        return 1
    except ValidationError as error:
        print(f"invalid config in {args.config}:\n{error}", file=sys.stderr)
        return 1

    print(f"loaded config from {args.config}: {loaded}")

    if args.min_utilization is None:
        print("no override provided; config is valid.")
        return 0

    try:
        resolved = resolve_config(loaded, {"min_utilization": args.min_utilization})
    except ValidationError as error:
        print(f"invalid override:\n{error}", file=sys.stderr)
        return 1

    print(
        f"override applied: min_utilization "
        f"{loaded.get('min_utilization', '(default)')} -> {resolved['min_utilization']}"
    )
    print(f"resolved config: {resolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
