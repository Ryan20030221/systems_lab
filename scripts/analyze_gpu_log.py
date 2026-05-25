import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def build_parser():
    parser = argparse.ArgumentParser(description="Analyze a GPU log CSV")
    parser.add_argument("--input", required=True, help="Path to input GPU log CSV")
    parser.add_argument("--output", required=True, help="Path to output summary report")
    parser.add_argument(
        "--min-util",
        type=int,
        default=50,
        help="Minimum utilization for active samples",
    )
    return parser


def write_summary(output_path, summary):
    with open(output_path, "w", encoding="utf-8") as file:
        for key, value in summary.items():
            file.write(f"{key}: {value}\n")


def main(argv=None):
    from gpu_lab.filters import filter_active_samples
    from gpu_lab.parser import load_lines, parse_gpu_rows
    from gpu_lab.summary import calculate_summary
    from gpu_lab.validation import validate_sample

    parser = build_parser()
    args = parser.parse_args(argv)

    min_util = args.min_util
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"error: input file does not exist: {input_path}")
        return 1

    if not input_path.is_file():
        print(f"error: input path is not a file: {input_path}")
        return 1

    if not 0 <= min_util <= 100:
        print(f"error: minimum utilization is out of bounds: {min_util}")
        return 1

    if not output_path.parent.exists():
        print(f"error: output directory does not exist: {output_path.parent}")
        return 1

    lines = load_lines(input_path)
    samples = parse_gpu_rows(lines)

    valid_samples = []
    for sample in samples:
        if validate_sample(sample):
            valid_samples.append(sample)

    active_samples = filter_active_samples(valid_samples, min_util)
    summary = calculate_summary(active_samples)

    write_summary(output_path, summary)

    print(f"Analyzed input: {input_path}")
    print(f"Parsed samples: {len(samples)}")
    print(f"Valid samples: {len(valid_samples)}")
    print(f"Active samples: {len(active_samples)}")
    print(f"Wrote summary: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
