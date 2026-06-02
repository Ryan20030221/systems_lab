from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from gpu_lab.paths import ensure_directory


def load_summary_rows(summary_csv_path: Path) -> list[dict[str, str]]:
    if not summary_csv_path.exists():
        raise FileNotFoundError(f"summary CSV does not exist:{summary_csv_path}")
    if not summary_csv_path.is_file():
        raise ValueError(f"summary CSV path is not a file: {summary_csv_path}")

    with open(summary_csv_path, newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError(f"summary CSV has no header rows:{summary_csv_path}")

        rows = list(reader)

    if not rows:
        raise ValueError(f"CSV has headers but no rows:{summary_csv_path}")

    return rows


def validate_required_columns(
    rows: list[dict[str, str]], required_columns: set[str]
) -> None:
    if not rows:
        raise ValueError("rows are empty")

    missing = required_columns - set(rows[0])
    if missing:
        raise ValueError(f"missing required metrics: {missing}")


def _extract_numeric_column(
    rows: list[dict[str, str]],
    column_name: str,
) -> list[float]:
    values = []
    for row in rows:
        raw_value = row[column_name]

        if raw_value == "":
            raise ValueError(f"empty value in column: {column_name}")
        try:
            values.append(float(raw_value))
        except ValueError as error:
            raise ValueError(
                f"non-numeric value in column {column_name}: {raw_value}"
            ) from error
    return values


def plot_metric(
    rows: list[dict[str, str]],
    output_path: Path,
    x_column: str,
    y_column: str,
    title: str,
    x_label: str,
    y_label: str,
) -> Path:
    validate_required_columns(rows, {x_column, y_column})

    ensure_directory(output_path.parent)

    xs = _extract_numeric_column(rows, x_column)
    ys = _extract_numeric_column(rows, y_column)

    fig, ax = plt.subplots()
    ax.plot(xs, ys, marker="o")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

    return output_path


def write_markdown_report(
    output_path: Path,
    source_csv_path: Path,
    chart_path: Path,
    title: str,
    limitations: list[str],
) -> Path:
    ensure_directory(output_path.parent)
    if not title.strip():
        raise ValueError("Report title cannot be empty.")
    if not limitations:
        raise ValueError("Limitations list cannot be empty.")

    cleaned_limitations = [
        limitation.strip() for limitation in limitations if limitation.strip()
    ]

    if not cleaned_limitations:
        raise ValueError("Limitations list cannot contain only empty text.")

    limitation_lines = "\n".join(f"- {limitation}" for limitation in limitations)

    report_text = f"""# {title}

## Source Data

- Source CSV: `{source_csv_path}`

## Generated Chart

- Chart path: `{chart_path}`

## Limitations

{limitation_lines}
"""
    output_path.write_text(report_text, encoding="utf-8")

    return output_path
