from __future__ import annotations

from dataclasses import dataclass

from gpu_lab.diagnosis import DiagnosisResult

NO_ACTION_LABELS = {
    "insufficient_evidence",
    "mixed_or_competing_signals",
    "unknown",
}

SUPPORTED_RECOMMENDATION_LABELS = {
    "possible_temperature_pressure",
    "gpu_underutilized",
    "gpu_busy",
}


@dataclass(frozen=True)
class ControllerDecision:
    experiment_name: str
    decision_type: str
    dry_run: bool
    recommendation: str
    confidence: str
    reason: str
    evidence_references: list[str]
    limitation: str
    safety_note: str
    rollback_note: str


def make_controller_decision(diagnosis: DiagnosisResult) -> ControllerDecision:
    label = diagnosis.label

    if diagnosis.confidence == "low":
        return _build_no_action_decision(
            diagnosis=diagnosis,
            reason="diagnosis confidence is low",
        )

    if label in NO_ACTION_LABELS:
        return _build_no_action_decision(
            diagnosis=diagnosis,
            reason="diagnosis is unknown, insufficient, or has competing signals",
        )

    if label not in SUPPORTED_RECOMMENDATION_LABELS:
        return _build_no_action_decision(
            diagnosis=diagnosis,
            reason="diagnosis label is not supported by the controller",
        )

    if diagnosis.confidence in {"medium", "high"}:
        return _build_recommendation_decision(diagnosis=diagnosis)

    return _build_no_action_decision(
        diagnosis=diagnosis,
        reason="diagnosis confidence is not supported by the controller",
    )


def _build_no_action_decision(
    diagnosis: DiagnosisResult,
    reason: str,
) -> ControllerDecision:
    return ControllerDecision(
        experiment_name=diagnosis.experiment_name,
        decision_type="no_action",
        dry_run=True,
        recommendation="No action recommended.",
        confidence=diagnosis.confidence,
        reason=reason,
        evidence_references=list(diagnosis.evidence),
        limitation=_build_limitation(diagnosis),
        safety_note=_build_safety_note(),
        rollback_note=_build_rollback_note(),
    )


def _build_recommendation_decision(
    diagnosis: DiagnosisResult,
) -> ControllerDecision:
    return ControllerDecision(
        experiment_name=diagnosis.experiment_name,
        decision_type="dry_run_recommendation",
        dry_run=True,
        recommendation=_recommendation_for_label(diagnosis.label),
        confidence=diagnosis.confidence,
        reason=(
            f"Diagnosis label {diagnosis.label!r} has enough confidence for a "
            "dry-run recommendation, but not for real actuation."
        ),
        evidence_references=list(diagnosis.evidence),
        limitation=_build_limitation(diagnosis),
        safety_note=_build_safety_note(),
        rollback_note=_build_rollback_note(),
    )


def _recommendation_for_label(label: str) -> str:
    if label == "possible_temperature_pressure":
        return (
            "Review cooling, temperature pressure, and workload thermals before "
            "considering any control change."
        )

    if label == "gpu_underutilized":
        return (
            "Investigate host feeding, I/O wait, workload size, and "
            "measurement-window effects before considering placement changes."
        )

    if label == "gpu_busy":
        return (
            "Review whether the workload is capacity-bound before considering "
            "scheduling or placement changes."
        )

    return "No action recommended."


def _build_limitation(diagnosis: DiagnosisResult) -> str:
    limitation_parts = list(diagnosis.limitations)

    if diagnosis.competing_explanations:
        competing = ", ".join(diagnosis.competing_explanations)
        limitation_parts.append(f"Competing explanations remain possible: {competing}.")

    if not limitation_parts:
        return (
            "Decision is based only on available diagnosis evidence and is not "
            "proof of root cause."
        )

    return " ".join(limitation_parts)


def _build_safety_note() -> str:
    return (
        "Dry run only. No GPU settings, power limits, clocks, or scheduler "
        "behavior were changed."
    )


def _build_rollback_note() -> str:
    return "No rollback is required because no real action was performed."
