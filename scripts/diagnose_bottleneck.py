from __future__ import annotations

import argparse
from pathlib import Path

from gpu_lab.diagnosis import DiagnosisResult, diagnose_experiments
from gpu_lab.experiment_summary import load_experiment_summaries
from gpu_lab.paths import ensure_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Diagnose GPU bottleneck symptoms from experiment summary evidence."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to experiment_summary.csv.",
    )
    parser.add_argument(
        "--report-output",
        required=True,
        type=Path,
        help="Path where the Markdown diagnosis report should be written.",
    )
    return parser


def format_diagnosis_report(diagnoses: list[DiagnosisResult]) -> str:
    lines: list[str] = [
        "# GPU Bottleneck Diagnosis Report",
        "",
        (
            "> **Note:** Labels are evidence-based symptoms derived from summary "
            "statistics, not guaranteed root causes. Treat each diagnosis as a "
            "starting point for deeper investigation."
        ),
        "",
    ]

    if not diagnoses:
        lines.extend(
            [
                "## No diagnoses produced",
                "",
                "No experiment records were available to diagnose.",
                "",
            ]
        )
        return "\n".join(lines)

    for diagnosis in diagnoses:
        lines.extend(
            [
                f"## {diagnosis.experiment_name}",
                "",
                f"**Label:** `{diagnosis.label}`",
                f"**Confidence:** `{diagnosis.confidence}`",
                "",
                "### Evidence",
                "",
            ]
        )

        for item in diagnosis.evidence:
            lines.append(f"- {item}")

        lines.extend(["", "### Competing explanations", ""])

        if diagnosis.competing_explanations:
            for item in diagnosis.competing_explanations:
                lines.append(f"- {item}")
        else:
            lines.append("- None listed.")

        lines.extend(["", "### Limitations", ""])

        if diagnosis.limitations:
            for item in diagnosis.limitations:
                lines.append(f"- {item}")
        else:
            lines.append("- None listed.")

        lines.append("")

    return "\n".join(lines)


def write_diagnosis_report(path: Path, diagnoses: list[DiagnosisResult]) -> None:
    ensure_directory(path.parent)
    path.write_text(format_diagnosis_report(diagnoses), encoding="utf-8")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    records = load_experiment_summaries(args.input)
    diagnoses = diagnose_experiments(records)
    write_diagnosis_report(args.report_output, diagnoses)

    print(f"Wrote diagnosis report: {args.report_output}")


if __name__ == "__main__":
    main()
