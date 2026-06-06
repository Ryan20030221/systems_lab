
from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosisResult:
    experiment_name: str
    label: str
    confidence: str
    evidence: list[str]
    competing_explanations: list[str]
    limitations: list[str]


REQUIRED_DIAGNOSIS_FIELDS = {
    "experiment_name",
    "sample_count",
    "avg_power",
    "avg_temp",
    "avg_utilization",
    "min_power",
    "max_power",
    "min_temp",
    "max_temp",
}

HIGH_AVG_TEMP_THRESHOLD = 80.0
HIGH_MAX_TEMP_THRESHOLD = 82.0
LOW_UTILIZATION_THRESHOLD = 60.0
HIGH_UTILIZATION_THRESHOLD = 95.0
MIN_SAMPLE_COUNT = 20
LARGE_POWER_RANGE_THRESHOLD = 50.0
LARGE_TEMP_RANGE_THRESHOLD = 15.0


def _check_required_fields(record: dict) -> None:
    missing_fields = REQUIRED_DIAGNOSIS_FIELDS - set(record.keys())
    if missing_fields:
        raise ValueError(f"fields are missing: {missing_fields}")


def _has_insufficient_samples(record: dict) -> bool:
    return record["sample_count"] < MIN_SAMPLE_COUNT


def _has_temperature_pressure(record: dict) -> bool:
    if record["avg_temp"] >= HIGH_AVG_TEMP_THRESHOLD:
        return True
    if record["max_temp"] >= HIGH_MAX_TEMP_THRESHOLD:
        return True
    return False


def _has_low_utilization(record: dict) -> bool:
    return record["avg_utilization"] < LOW_UTILIZATION_THRESHOLD


def _has_high_utilization(record: dict) -> bool:
    return record["avg_utilization"] >= HIGH_UTILIZATION_THRESHOLD


def _has_mixed_signals(record: dict) -> bool:
    power_range = record["max_power"] - record["min_power"]
    temp_range = record["max_temp"] - record["min_temp"]
    if power_range >= LARGE_POWER_RANGE_THRESHOLD:
        return True
    if temp_range >= LARGE_TEMP_RANGE_THRESHOLD:
        return True
    if _has_low_utilization(record) and _has_temperature_pressure(record):
        return True
    return False


def _build_insufficient_evidence_result(record: dict) -> DiagnosisResult:
    return DiagnosisResult(
        experiment_name=record["experiment_name"],
        label="insufficient_evidence",
        confidence="low",
        evidence=["sample count below minimum threshold"],
        competing_explanations=[],
        limitations=[],
    )


def _build_mixed_signals_result(record: dict) -> DiagnosisResult:
    return DiagnosisResult(
        experiment_name=record["experiment_name"],
        label="mixed_or_competing_signals",
        confidence="medium",
        evidence=["conflicting indicators across power, temperature, or utilization"],
        competing_explanations=[],
        limitations=[],
    )


def _build_temperature_pressure_result(record: dict) -> DiagnosisResult:
    return DiagnosisResult(
        experiment_name=record["experiment_name"],
        label="possible_temperature_pressure",
        confidence="medium",
        evidence=["avg_temp is above the temperature threshold"],
        competing_explanations=["bad cooling"],
        limitations=[],
    )


def _build_gpu_underutilized_result(record: dict) -> DiagnosisResult:
    return DiagnosisResult(
        experiment_name=record["experiment_name"],
        label="gpu_underutilized",
        confidence="medium",
        evidence=["avg_utilization is below the low-utilization threshold."],
        competing_explanations=[
            "CPU feeding limitation",
            "I/O wait",
            "small workload",
            "measurement window included idle time",
        ],
        limitations=[
            "GPU underutilization is a symptom, not a proven root cause.",
            "Summary does not include CPU, memory, I/O, or clock data.",
        ],
    )


def _build_gpu_busy_result(record: dict) -> DiagnosisResult:
    return DiagnosisResult(
        experiment_name=record["experiment_name"],
        label="gpu_busy",
        confidence="medium",
        evidence=["average utilization was above threshold"],
        competing_explanations=["possibly low frequency"],
        limitations=["high utilization doesn't mean throughput is at max capacity"],
    )


def _build_unknown_result(record: dict) -> DiagnosisResult:
    return DiagnosisResult(
        experiment_name=record["experiment_name"],
        label="unknown",
        confidence="low",
        evidence=["no bottleneck has been identified"],
        competing_explanations=[],
        limitations=[],
    )


def diagnose_experiment(record: dict) -> DiagnosisResult:
    _check_required_fields(record)
    if _has_insufficient_samples(record):
        return _build_insufficient_evidence_result(record)
    if _has_mixed_signals(record):
        return _build_mixed_signals_result(record)
    if _has_temperature_pressure(record):
        return _build_temperature_pressure_result(record)
    if _has_low_utilization(record):
        return _build_gpu_underutilized_result(record)
    if _has_high_utilization(record):
        return _build_gpu_busy_result(record)
    return _build_unknown_result(record)


def diagnose_experiments(records: list[dict]) -> list[DiagnosisResult]:
    return [diagnose_experiment(record) for record in records]
