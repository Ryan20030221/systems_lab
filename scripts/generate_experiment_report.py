import argparse
from pathlib import Path

from gpu_lab.reporting import load_summary_rows, plot_metric, write_markdown_report

DEFAULT_INPUT = Path("results/experiment_summary.csv")
DEFAULT_OUTPUT = Path("results/charts/experiment_efficieny.png")
DEFAULT_MARKDOWN_OUTPUT = Path("results/expirement_reports/markdown_report.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a reusable experiement chart from a summary CSV."
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to the experiment summary CSV.",
    )

    parser.add_argument(
        "--chart-output",
        type=Path,
        required=True,
        help="Path where the PNG chart should be written.",
    )

    parser.add_argument(
        "--report-output",
        type=Path,
        required=True,
        help="Path where the Markdown report should be written.",
    )

    parser.add_argument(
        "--x-column",
        required=True,
        help="CSV column to use for the x-axis.",
    )

    parser.add_argument(
        "--y-column",
        required=True,
        help="CSV column to use for the y-axis.",
    )

    parser.add_argument(
        "--x-label",
        required=True,
        help="Human-readable x-axis label, including units when applicable.",
    )

    parser.add_argument(
        "--y-label",
        required=True,
        help="Human-readable y-axis label, including units when applicable.",
    )

    parser.add_argument(
        "--title",
        required=True,
        help="Title for both the chart and Markdown report.",
    )

    parser.add_argument(
        "--limitation",
        action="append",
        required=True,
        help="Report limitation. Repeat this argument for multiple limitations.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = load_summary_rows(args.input)

    chart_path = plot_metric(
        rows=rows,
        output_path=args.chart_output,
        x_column=args.x_column,
        y_column=args.y_column,
        title=args.title,
        x_label=args.x_label,
        y_label=args.y_label,
    )

    report_path = write_markdown_report(
        output_path=args.report_output,
        source_csv_path=args.input,
        chart_path=chart_path,
        title=args.title,
        limitations=args.limitation,
    )

    print(f"Summary chart saved to: {chart_path}")
    print(f"Markdown report saved to: {report_path}")


if __name__ == "__main__":
    main()
