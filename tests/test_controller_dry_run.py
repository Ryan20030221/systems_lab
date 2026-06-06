from __future__ import annotations

import subprocess
import sys

from gpu_lab.controller import ControllerDecision
from scripts.controller_dry_run import format_decision

VALID_SUMMARY_CSV = (
    "experiment_name,sample_count,avg_power,avg_temp,avg_utilization,"
    "min_power,max_power,min_temp,max_temp\n"
    "busy_run,30,150.0,70.0,96.0,130.0,160.0,65.0,75.0\n"
)


def test_format_decision_includes_required_dry_run_fields():
    decision = ControllerDecision(
        experiment_name="busy_run",
        decision_type="dry_run_recommendation",
        dry_run=True,
        recommendation="Review whether the workload is capacity-bound.",
        confidence="medium",
        reason="Diagnosis supports a dry-run recommendation.",
        evidence_references=["average utilization was above threshold"],
        limitation="High utilization does not prove root cause.",
        safety_note=(
            "Dry run only. No GPU settings, power limits, clocks, or scheduler "
            "behavior were changed."
        ),
        rollback_note="No rollback is required because no real action was performed.",
    )

    report = format_decision(decision)

    assert "Controller Dry-Run Decision" in report
    assert "Experiment: busy_run" in report
    assert "Decision type: dry_run_recommendation" in report
    assert "Dry run: True" in report
    assert "average utilization was above threshold" in report
    assert "No GPU settings" in report
    assert "No rollback is required" in report


def test_controller_dry_run_script_happy_path(tmp_path):
    summary_path = tmp_path / "experiment_summary.csv"
    summary_path.write_text(VALID_SUMMARY_CSV, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/controller_dry_run.py",
            "--input",
            str(summary_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "Controller Dry-Run Decision" in result.stdout
    assert "Experiment: busy_run" in result.stdout
    assert "Decision type: dry_run_recommendation" in result.stdout
    assert "Dry run: True" in result.stdout
    assert "Safety note: Dry run only." in result.stdout
    assert "No rollback is required" in result.stdout


def test_controller_dry_run_script_rejects_apply_flag(tmp_path):
    summary_path = tmp_path / "experiment_summary.csv"
    summary_path.write_text(VALID_SUMMARY_CSV, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/controller_dry_run.py",
            "--input",
            str(summary_path),
            "--apply",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "unrecognized arguments: --apply" in result.stderr
