from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gpu_lab.controller import ControllerDecision

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate dry-run controller decisions from experiment summaries."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to experiment_summary.csv.",
    )
    return parser


def run_controller(input_path: Path) -> list[ControllerDecision]:
    from gpu_lab.controller import make_controller_decision
    from gpu_lab.diagnosis import diagnose_experiments
    from gpu_lab.experiment_summary import load_experiment_summaries

    summaries = load_experiment_summaries(input_path)
    diagnoses = diagnose_experiments(summaries)
    return [make_controller_decision(diagnosis) for diagnosis in diagnoses]


def format_decision(decision: ControllerDecision) -> str:
    evidence_lines = "\n".join(
        f"  - {evidence_reference}"
        for evidence_reference in decision.evidence_references
    )

    if not evidence_lines:
        evidence_lines = "  - No evidence references provided."

    return (
        "Controller Dry-Run Decision\n"
        f"Experiment: {decision.experiment_name}\n"
        f"Decision type: {decision.decision_type}\n"
        f"Dry run: {decision.dry_run}\n"
        f"Recommendation: {decision.recommendation}\n"
        f"Confidence: {decision.confidence}\n"
        f"Reason: {decision.reason}\n"
        "Evidence references:\n"
        f"{evidence_lines}\n"
        f"Limitation: {decision.limitation}\n"
        f"Safety note: {decision.safety_note}\n"
        f"Rollback note: {decision.rollback_note}"
    )


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    decisions = run_controller(args.input)

    for index, decision in enumerate(decisions):
        if index > 0:
            print()
        print(format_decision(decision))


if __name__ == "__main__":
    main()
