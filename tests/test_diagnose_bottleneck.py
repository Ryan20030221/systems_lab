from __future__ import annotations

from pathlib import Path

from gpu_lab.diagnosis import DiagnosisResult
from scripts.diagnose_bottleneck import (
    build_parser,
    format_diagnosis_report,
    main,
    write_diagnosis_report,
)


def make_diagnosis() -> DiagnosisResult:
    return DiagnosisResult(
        experiment_name="low_util_run",
        label="gpu_underutilized",
        confidence="medium",
        evidence=[
            "avg_utilization is 42.0, below the low-utilization threshold of 60.0.",
        ],
        competing_explanations=[
            "CPU feeding limitation",
            "I/O wait",
        ],
        limitations=[
            "GPU underutilization is a symptom, not a proven root cause.",
        ],
    )


def test_build_parser_accepts_required_paths():
    parser = build_parser()

    args = parser.parse_args(
        [
            "--input",
            "results/experiment_summary.csv",
            "--report-output",
            "results/bottleneck_diagnosis.md",
        ]
    )

    assert args.input == Path("results/experiment_summary.csv")
    assert args.report_output == Path("results/bottleneck_diagnosis.md")


def test_format_diagnosis_report_includes_required_sections():
    report = format_diagnosis_report([make_diagnosis()])

    assert "# GPU Bottleneck Diagnosis Report" in report
    assert "low_util_run" in report
    assert "gpu_underutilized" in report
    assert "medium" in report
    assert "### Evidence" in report
    assert "### Competing explanations" in report
    assert "### Limitations" in report
    assert "not guaranteed root causes" in report


def test_format_diagnosis_report_handles_empty_diagnoses():
    report = format_diagnosis_report([])

    assert "# GPU Bottleneck Diagnosis Report" in report
    assert "## No diagnoses produced" in report
    assert "No experiment records were available to diagnose." in report


def test_write_diagnosis_report_creates_parent_directory(tmp_path):
    output_path = tmp_path / "nested" / "diagnosis" / "report.md"

    write_diagnosis_report(output_path, [make_diagnosis()])

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "low_util_run" in content
    assert "gpu_underutilized" in content


def test_main_loads_diagnoses_and_writes_report(tmp_path, monkeypatch):
    input_path = tmp_path / "experiment_summary.csv"
    output_path = tmp_path / "reports" / "diagnosis.md"

    input_path.write_text("fake csv content", encoding="utf-8")

    loaded_records = [
        {
            "experiment_name": "low_util_run",
            "sample_count": 100,
            "avg_power": 120.0,
            "avg_temp": 65.0,
            "avg_utilization": 42.0,
            "min_power": 100.0,
            "max_power": 135.0,
            "min_temp": 60.0,
            "max_temp": 70.0,
        }
    ]

    def fake_load_experiment_summaries(path: Path) -> list[dict]:
        assert path == input_path
        return loaded_records

    def fake_diagnose_experiments(records: list[dict]) -> list[DiagnosisResult]:
        assert records == loaded_records
        return [make_diagnosis()]

    monkeypatch.setattr(
        "scripts.diagnose_bottleneck.load_experiment_summaries",
        fake_load_experiment_summaries,
    )
    monkeypatch.setattr(
        "scripts.diagnose_bottleneck.diagnose_experiments",
        fake_diagnose_experiments,
    )
    monkeypatch.setattr(
        "sys.argv",
        [
            "diagnose_bottleneck.py",
            "--input",
            str(input_path),
            "--report-output",
            str(output_path),
        ],
    )

    main()

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "low_util_run" in content
    assert "gpu_underutilized" in content