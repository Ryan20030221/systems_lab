import os
import subprocess
import sys
from pathlib import Path

import pytest

os.environ.setdefault("MPLBACKEND", "Agg")

from gpu_lab.reporting import (  # noqa: E402
    load_summary_rows,
    plot_metric,
    validate_required_columns,
    write_markdown_report,
)


def write_sample_summary_csv(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "power_limit,fps_per_watt,avg_power_w,avg_temp_c",
                "50,0.7488,89.48,65",
                "60,0.7485,104.21,66",
                "70,0.7187,118.27,67",
                "80,0.6393,140.77,68",
            ]
        ),
        encoding="utf-8",
    )


def test_load_summary_rows_reads_csv_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "experiment_summary.csv"
    write_sample_summary_csv(csv_path)

    rows = load_summary_rows(csv_path)

    assert len(rows) == 4
    assert rows[0]["power_limit"] == "50"
    assert rows[0]["fps_per_watt"] == "0.7488"


def test_load_summary_rows_rejects_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_summary_rows(missing_path)


def test_load_summary_rows_rejects_header_only_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "empty_summary.csv"
    csv_path.write_text("power_limit,fps_per_watt\n", encoding="utf-8")

    with pytest.raises(ValueError, match="headers but no rows"):
        load_summary_rows(csv_path)


def test_validate_required_columns_accepts_present_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "experiment_summary.csv"
    write_sample_summary_csv(csv_path)
    rows = load_summary_rows(csv_path)

    validate_required_columns(rows, {"power_limit", "fps_per_watt"})


def test_validate_required_columns_rejects_missing_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "experiment_summary.csv"
    write_sample_summary_csv(csv_path)
    rows = load_summary_rows(csv_path)

    with pytest.raises(ValueError, match="missing required metrics"):
        validate_required_columns(rows, {"power_limit", "missing_metric"})


def test_plot_metric_creates_png_chart(tmp_path: Path) -> None:
    csv_path = tmp_path / "experiment_summary.csv"
    chart_path = tmp_path / "charts" / "fps_per_watt.png"
    write_sample_summary_csv(csv_path)
    rows = load_summary_rows(csv_path)

    returned_path = plot_metric(
        rows=rows,
        output_path=chart_path,
        x_column="power_limit",
        y_column="fps_per_watt",
        title="FPS/W by power limit",
        x_label="Power limit (%)",
        y_label="FPS per watt",
    )

    assert returned_path == chart_path
    assert chart_path.exists()
    assert chart_path.stat().st_size > 0


def test_plot_metric_rejects_non_numeric_chart_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "bad_summary.csv"
    chart_path = tmp_path / "bad_chart.png"
    csv_path.write_text(
        "\n".join(
            [
                "power_limit,fps_per_watt",
                "50,0.7488",
                "60,not-a-number",
            ]
        ),
        encoding="utf-8",
    )
    rows = load_summary_rows(csv_path)

    with pytest.raises(ValueError, match="non-numeric value"):
        plot_metric(
            rows=rows,
            output_path=chart_path,
            x_column="power_limit",
            y_column="fps_per_watt",
            title="Bad chart",
            x_label="Power limit (%)",
            y_label="FPS per watt",
        )


def test_write_markdown_report_creates_report_file(tmp_path: Path) -> None:
    source_csv_path = tmp_path / "experiment_summary.csv"
    chart_path = tmp_path / "charts" / "fps_per_watt.png"
    report_path = tmp_path / "reports" / "fps_per_watt_report.md"
    write_sample_summary_csv(source_csv_path)
    chart_path.parent.mkdir(parents=True)
    chart_path.write_bytes(b"fake png content")

    returned_path = write_markdown_report(
        output_path=report_path,
        source_csv_path=source_csv_path,
        chart_path=chart_path,
        title="FPS/W by power limit",
        limitations=[
            "Single manual sample dataset.",
            "Does not prove stability across workloads.",
        ],
    )

    report_text = report_path.read_text(encoding="utf-8")

    assert returned_path == report_path
    assert report_path.exists()
    assert "# FPS/W by power limit" in report_text
    assert f"Source CSV: `{source_csv_path}`" in report_text
    assert f"Chart path: `{chart_path}`" in report_text
    assert "- Single manual sample dataset." in report_text
    assert "- Does not prove stability across workloads." in report_text


def test_write_markdown_report_rejects_empty_title(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="title"):
        write_markdown_report(
            output_path=tmp_path / "report.md",
            source_csv_path=tmp_path / "summary.csv",
            chart_path=tmp_path / "chart.png",
            title="   ",
            limitations=["Some limitation."],
        )


def test_write_markdown_report_rejects_empty_limitations(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Limitations"):
        write_markdown_report(
            output_path=tmp_path / "report.md",
            source_csv_path=tmp_path / "summary.csv",
            chart_path=tmp_path / "chart.png",
            title="Report",
            limitations=[],
        )


def test_generate_experiment_report_script_creates_chart_and_report(
    tmp_path: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = tmp_path / "experiment_summary.csv"
    chart_path = tmp_path / "fps_per_watt.png"
    report_path = tmp_path / "fps_per_watt_report.md"
    write_sample_summary_csv(csv_path)

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_experiment_report.py",
            "--input",
            str(csv_path),
            "--chart-output",
            str(chart_path),
            "--report-output",
            str(report_path),
            "--x-column",
            "power_limit",
            "--y-column",
            "fps_per_watt",
            "--x-label",
            "Power limit (%)",
            "--y-label",
            "FPS per watt",
            "--title",
            "FPS/W by power limit",
            "--limitation",
            "Single manual sample dataset.",
            "--limitation",
            "Does not prove stability across workloads.",
        ],
        cwd=repo_root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    assert chart_path.exists()
    assert chart_path.stat().st_size > 0
    assert report_path.exists()
    assert "Summary chart saved to:" in result.stdout
    assert "Markdown report saved to:" in result.stdout
