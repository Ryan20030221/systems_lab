import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path("scripts/analyze_gpu_log.py")


def test_analyze_gpu_log_writes_summary_for_valid_input(tmp_path):
    input_path = tmp_path / "gpu_log.csv"
    output_path = tmp_path / "summary.txt"

    input_path.write_text(
        "timestamp,power,temp,utilization\n"
        "12:00,140,68,95\n"
        "12:01,145,70,97\n"
        "12:02,50,45,5\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--min-util",
            "50",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert output_path.exists()

    summary_text = output_path.read_text(encoding="utf-8")
    assert "sample_count: 2" in summary_text
    assert "avg_power: 142.5" in summary_text
    assert "avg_utilization: 96.0" in summary_text


def test_analyze_gpu_log_fails_for_missing_input(tmp_path):
    output_path = tmp_path / "summary.txt"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--input",
            str(tmp_path / "missing.csv"),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "input file does not exist" in result.stdout
    assert not output_path.exists()


def test_analyze_gpu_log_rejects_invalid_min_util(tmp_path):
    input_path = tmp_path / "gpu_log.csv"
    output_path = tmp_path / "summary.txt"

    input_path.write_text(
        "timestamp,power,temp,utilization\n12:00,140,68,95\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--min-util",
            "101",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "minimum utilization is out of bounds" in result.stdout
    assert not output_path.exists()
