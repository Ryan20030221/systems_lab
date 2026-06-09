from __future__ import annotations

import json

from scripts.validate_config_professional import main

VALID = {
    "min_utilization": 50.0,
    "default_results_dir": "results",
    "default_logs_dir": "logs",
}


def _write(tmp_path, data):
    path = tmp_path / "config.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_valid_config_exits_zero(tmp_path, capsys):
    path = _write(tmp_path, VALID)
    assert main(["--config", str(path)]) == 0
    assert "valid" in capsys.readouterr().out


def test_override_is_applied(tmp_path, capsys):
    path = _write(tmp_path, VALID)
    assert main(["--config", str(path), "--min-utilization", "80"]) == 0
    assert "80" in capsys.readouterr().out  # the new value shows in the resolved output


def test_missing_file_exits_one(tmp_path):
    assert main(["--config", str(tmp_path / "nope.json")]) == 1


def test_out_of_range_override_exits_one(tmp_path):
    path = _write(tmp_path, VALID)
    assert main(["--config", str(path), "--min-utilization", "150"]) == 1
