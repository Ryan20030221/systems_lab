from csv import DictReader
from pathlib import Path

EXPERIMENT_SUMMARY_SCHEMA = {
    "experiment_name": str,
    "sample_count": int,
    "avg_power": float,
    "avg_temp": float,
    "avg_utilization": float,
    "min_power": float,
    "max_power": float,
    "min_temp": float,
    "max_temp": float,
}

REQUIRED_COLUMNS = set(EXPERIMENT_SUMMARY_SCHEMA.keys())


def _validate_required_columns(fieldnames: list[str]) -> None:
    missing_columns = REQUIRED_COLUMNS - set(fieldnames)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")


def _convert_float_value(value: str, column_name: str, row_number: int) -> float:
    try:
        return float(value)
    except ValueError as error:
        raise ValueError(
            f"Row {row_number}, column '{column_name}': "
            f"expected a float, got {value!r}"
        ) from error


def _convert_int_value(value: str, column_name: str, row_number: int) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise ValueError(
            f"Row {row_number}, column '{column_name}': "
            f"expected an int, got {value!r}"
        ) from error


def _convert_row(
    row: dict[str, str],
    row_number: int,
) -> dict[str, str | float | int]:
    return {
        "experiment_name": row["experiment_name"],
        "sample_count": _convert_int_value(
            row["sample_count"], "sample_count", row_number
        ),
        "avg_power": _convert_float_value(
            row["avg_power"], "avg_power", row_number
        ),
        "avg_temp": _convert_float_value(
            row["avg_temp"], "avg_temp", row_number
        ),
        "avg_utilization": _convert_float_value(
            row["avg_utilization"], "avg_utilization", row_number
        ),
        "min_power": _convert_float_value(
            row["min_power"], "min_power", row_number
        ),
        "max_power": _convert_float_value(
            row["max_power"], "max_power", row_number
        ),
        "min_temp": _convert_float_value(
            row["min_temp"], "min_temp", row_number
        ),
        "max_temp": _convert_float_value(
            row["max_temp"], "max_temp", row_number
        ),
    }


def load_experiment_summaries(
    path: Path | str,
) -> list[dict[str, str | int | float]]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"given path does not exist: {path}")

    if not path.is_file():
        raise ValueError(f"given path is not a file: {path}")

    validated_summary: list[dict[str, str | int | float]] = []

    with path.open(encoding="utf-8", newline="") as file:
        reader = DictReader(file)
        headers = reader.fieldnames

        if headers is None:
            raise ValueError(f"given CSV file has no header row: {path}")

        _validate_required_columns(headers)

        for row_number, row in enumerate(reader, start=2):
            validated_summary.append(_convert_row(row, row_number))

    if not validated_summary:
        raise ValueError(f"given CSV file has no data rows: {path}")

    return validated_summary