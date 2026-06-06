from __future__ import annotations

import pytest

from gpu_lab.diagnosis import (
    HIGH_AVG_TEMP_THRESHOLD,
    HIGH_MAX_TEMP_THRESHOLD,
    HIGH_UTILIZATION_THRESHOLD,
    LARGE_POWER_RANGE_THRESHOLD,
    LARGE_TEMP_RANGE_THRESHOLD,
    LOW_UTILIZATION_THRESHOLD,
    MIN_SAMPLE_COUNT,
    DiagnosisResult,
    diagnose_experiment,
    diagnose_experiments,
)

BASE_RECORD: dict = {
    "experiment_name": "test_exp",
    "sample_count": 30,
    "avg_power": 150.0,
    "avg_temp": 70.0,
    "avg_utilization": 75.0,
    "min_power": 130.0,
    "max_power": 160.0,
    "min_temp": 65.0,
    "max_temp": 75.0,
}


# --- Block 1: Field validation ---


def test_missing_required_fields_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        diagnose_experiment({"experiment_name": "x"})
    msg = str(exc_info.value)
    assert "avg_power" in msg
    assert "sample_count" in msg


# --- Block 2: One happy path per label ---


def test_insufficient_evidence_when_sample_count_below_minimum():
    record = {**BASE_RECORD, "sample_count": MIN_SAMPLE_COUNT - 1}
    result = diagnose_experiment(record)
    assert result.label == "insufficient_evidence"
    assert result.confidence == "low"


def test_mixed_signals_when_power_range_large():
    record = {
        **BASE_RECORD,
        "max_power": BASE_RECORD["min_power"] + LARGE_POWER_RANGE_THRESHOLD,
    }
    result = diagnose_experiment(record)
    assert result.label == "mixed_or_competing_signals"


def test_temperature_pressure_when_avg_temp_at_threshold():
    record = {**BASE_RECORD, "avg_temp": HIGH_AVG_TEMP_THRESHOLD}
    result = diagnose_experiment(record)
    assert result.label == "possible_temperature_pressure"
    assert result.confidence == "medium"


def test_gpu_underutilized_when_utilization_below_threshold():
    record = {**BASE_RECORD, "avg_utilization": LOW_UTILIZATION_THRESHOLD - 1}
    result = diagnose_experiment(record)
    assert result.label == "gpu_underutilized"
    assert result.confidence == "medium"


def test_gpu_busy_when_utilization_at_high_threshold():
    record = {**BASE_RECORD, "avg_utilization": HIGH_UTILIZATION_THRESHOLD}
    result = diagnose_experiment(record)
    assert result.label == "gpu_busy"
    assert result.confidence == "medium"


def test_unknown_when_no_rule_matches():
    result = diagnose_experiment(BASE_RECORD)
    assert result.label == "unknown"
    assert result.confidence == "low"


# --- Block 3: Boundary conditions ---


def test_sufficient_samples_at_exact_minimum():
    record = {**BASE_RECORD, "sample_count": MIN_SAMPLE_COUNT}
    result = diagnose_experiment(record)
    assert result.label != "insufficient_evidence"


def test_mixed_signals_when_temperature_range_large():
    record = {
        **BASE_RECORD,
        "max_temp": BASE_RECORD["min_temp"] + LARGE_TEMP_RANGE_THRESHOLD,
    }
    result = diagnose_experiment(record)
    assert result.label == "mixed_or_competing_signals"


def test_mixed_signals_when_low_util_and_high_temp():
    record = {
        **BASE_RECORD,
        "avg_utilization": LOW_UTILIZATION_THRESHOLD - 1,
        "avg_temp": HIGH_AVG_TEMP_THRESHOLD,
    }
    result = diagnose_experiment(record)
    assert result.label == "mixed_or_competing_signals"


def test_temperature_pressure_when_max_temp_at_threshold():
    # min_temp raised to keep temp range below LARGE_TEMP_RANGE_THRESHOLD
    record = {
        **BASE_RECORD,
        "max_temp": HIGH_MAX_TEMP_THRESHOLD,
        "min_temp": HIGH_MAX_TEMP_THRESHOLD - (LARGE_TEMP_RANGE_THRESHOLD - 1),
    }
    result = diagnose_experiment(record)
    assert result.label == "possible_temperature_pressure"


# --- Block 4: Priority ordering ---


def test_insufficient_samples_overrides_temperature_pressure():
    record = {
        **BASE_RECORD,
        "sample_count": MIN_SAMPLE_COUNT - 1,
        "avg_temp": HIGH_AVG_TEMP_THRESHOLD,
    }
    result = diagnose_experiment(record)
    assert result.label == "insufficient_evidence"


def test_mixed_signals_overrides_temperature_pressure():
    record = {
        **BASE_RECORD,
        "avg_temp": HIGH_AVG_TEMP_THRESHOLD,
        "max_power": BASE_RECORD["min_power"] + LARGE_POWER_RANGE_THRESHOLD,
    }
    result = diagnose_experiment(record)
    assert result.label == "mixed_or_competing_signals"


# --- Block 5: Result structure and batch ---


def test_result_experiment_name_matches_input():
    record = {**BASE_RECORD, "experiment_name": "my_run"}
    result = diagnose_experiment(record)
    assert result.experiment_name == "my_run"


def test_diagnose_experiments_returns_one_result_per_record():
    records = [BASE_RECORD, BASE_RECORD, BASE_RECORD]
    results = diagnose_experiments(records)
    assert len(results) == 3
    assert all(isinstance(r, DiagnosisResult) for r in results)


def test_diagnose_experiments_empty_list_returns_empty_list():
    assert diagnose_experiments([]) == []
