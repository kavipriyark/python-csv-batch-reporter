"""Command-line entry point: python -m csv_batch_reporter <csv files...>"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .reporter import build_summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate one or more sales CSV files into a summary report."
    )
    parser.add_argument("csv_files", nargs="+", type=Path, help="CSV files to process")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Write report to a file instead of stdout"
    )
    args = parser.parse_args(argv)

    missing = [p for p in args.csv_files if not p.exists()]
    if missing:
        print(f"Error: file(s) not found: {', '.join(str(p) for p in missing)}", file=sys.stderr)
        return 1

    summary = build_summary(args.csv_files)
    report_text = summary.as_text()

    if args.output:
        args.output.write_text(report_text + "\n", encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
