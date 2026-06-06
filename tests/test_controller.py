from __future__ import annotations

from gpu_lab.controller import ControllerDecision, make_controller_decision
from gpu_lab.diagnosis import DiagnosisResult


def test_low_confidence_returns_no_action():
    diagnosis = DiagnosisResult(
        experiment_name="short_run",
        label="insufficient_evidence",
        confidence="low",
        evidence=["sample count below minimum threshold"],
        competing_explanations=[],
        limitations=[],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.decision_type == "no_action"
    assert decision.dry_run is True
    assert decision.recommendation == "No action recommended."
    assert decision.confidence == "low"
    assert decision.reason == "diagnosis confidence is low"


def test_unknown_diagnosis_returns_no_action():
    diagnosis = DiagnosisResult(
        experiment_name="unknown_run",
        label="unknown",
        confidence="low",
        evidence=["no bottleneck has been identified"],
        competing_explanations=[],
        limitations=[],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.decision_type == "no_action"
    assert decision.dry_run is True
    assert decision.recommendation == "No action recommended."


def test_mixed_or_competing_signals_returns_no_action_even_with_medium_confidence():
    diagnosis = DiagnosisResult(
        experiment_name="mixed_run",
        label="mixed_or_competing_signals",
        confidence="medium",
        evidence=["conflicting indicators across power, temperature, or utilization"],
        competing_explanations=[],
        limitations=[],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.decision_type == "no_action"
    assert decision.dry_run is True
    assert "competing signals" in decision.reason


def test_unsupported_label_returns_no_action():
    diagnosis = DiagnosisResult(
        experiment_name="unsupported_run",
        label="new_future_label",
        confidence="medium",
        evidence=["future evidence format"],
        competing_explanations=[],
        limitations=[],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.decision_type == "no_action"
    assert decision.dry_run is True
    assert decision.reason == "diagnosis label is not supported by the controller"


def test_supported_temperature_pressure_returns_dry_run_recommendation():
    diagnosis = DiagnosisResult(
        experiment_name="hot_run",
        label="possible_temperature_pressure",
        confidence="medium",
        evidence=["avg_temp is above the temperature threshold"],
        competing_explanations=["bad cooling"],
        limitations=[],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.decision_type == "dry_run_recommendation"
    assert decision.dry_run is True
    assert "Review cooling" in decision.recommendation
    assert decision.confidence == "medium"
    assert "dry-run recommendation" in decision.reason
    assert "bad cooling" in decision.limitation


def test_supported_gpu_underutilized_returns_dry_run_recommendation():
    diagnosis = DiagnosisResult(
        experiment_name="underutilized_run",
        label="gpu_underutilized",
        confidence="medium",
        evidence=["avg_utilization is below the low-utilization threshold."],
        competing_explanations=["CPU feeding limitation"],
        limitations=["GPU underutilization is a symptom, not a proven root cause."],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.decision_type == "dry_run_recommendation"
    assert decision.dry_run is True
    assert "Investigate host feeding" in decision.recommendation
    assert "CPU feeding limitation" in decision.limitation
    assert "not a proven root cause" in decision.limitation


def test_supported_gpu_busy_returns_dry_run_recommendation():
    diagnosis = DiagnosisResult(
        experiment_name="busy_run",
        label="gpu_busy",
        confidence="medium",
        evidence=["average utilization was above threshold"],
        competing_explanations=["possibly low frequency"],
        limitations=["high utilization doesn't mean throughput is at max capacity"],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.decision_type == "dry_run_recommendation"
    assert decision.dry_run is True
    assert "capacity-bound" in decision.recommendation
    assert "possibly low frequency" in decision.limitation


def test_decision_includes_required_audit_fields():
    diagnosis = DiagnosisResult(
        experiment_name="audit_run",
        label="gpu_busy",
        confidence="medium",
        evidence=["average utilization was above threshold"],
        competing_explanations=["possibly low frequency"],
        limitations=["high utilization doesn't mean throughput is at max capacity"],
    )

    decision = make_controller_decision(diagnosis)

    assert isinstance(decision, ControllerDecision)
    assert decision.experiment_name == "audit_run"
    assert decision.evidence_references == ["average utilization was above threshold"]
    assert decision.reason
    assert decision.limitation
    assert decision.safety_note
    assert decision.rollback_note


def test_safety_note_proves_no_real_actuation():
    diagnosis = DiagnosisResult(
        experiment_name="safe_run",
        label="gpu_busy",
        confidence="medium",
        evidence=["average utilization was above threshold"],
        competing_explanations=[],
        limitations=[],
    )

    decision = make_controller_decision(diagnosis)

    assert "Dry run only" in decision.safety_note
    assert "No GPU settings" in decision.safety_note
    assert "power limits" in decision.safety_note
    assert "clocks" in decision.safety_note
    assert "scheduler behavior" in decision.safety_note


def test_rollback_note_says_no_rollback_required_because_no_action_happened():
    diagnosis = DiagnosisResult(
        experiment_name="rollback_run",
        label="gpu_busy",
        confidence="medium",
        evidence=["average utilization was above threshold"],
        competing_explanations=[],
        limitations=[],
    )

    decision = make_controller_decision(diagnosis)

    assert decision.rollback_note == (
        "No rollback is required because no real action was performed."
    )


def test_decision_is_always_dry_run_for_no_action_and_recommendation():
    no_action_diagnosis = DiagnosisResult(
        experiment_name="unknown_run",
        label="unknown",
        confidence="low",
        evidence=["no bottleneck has been identified"],
        competing_explanations=[],
        limitations=[],
    )
    recommendation_diagnosis = DiagnosisResult(
        experiment_name="busy_run",
        label="gpu_busy",
        confidence="medium",
        evidence=["average utilization was above threshold"],
        competing_explanations=[],
        limitations=[],
    )

    assert make_controller_decision(no_action_diagnosis).dry_run is True
    assert make_controller_decision(recommendation_diagnosis).dry_run is True
