import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Tiny CLU input demo")
    parser.add_argument("--input", required=True, help="Path to an input file")

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"error: input file does not exist: {input_path}")
        return 1

    print(f"input file: {input_path}")
    print(f"file size: {input_path.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
