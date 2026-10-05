# CSV Batch Reporter

A small, dependency-free Python CLI that aggregates one or more CSV files
into a readable summary report (total rows, total amount, per-category
breakdown). Modeled after the kind of "watch a folder, roll up the daily
feed, produce a report" automation scripts used to turn tedious manual
CSV reconciliation into a one-command job.

Built from scratch with dummy sample data for a portfolio — no proprietary
logic or data involved.

## Features

- Validates required columns before processing (fails loudly, not silently)
- Skips malformed individual rows instead of crashing an entire batch
- Aggregates across multiple files in one pass
- Clean `dataclass`-based summary object, easy to extend (e.g. JSON output)
- Fully unit tested with `pytest`

## Usage

```bash
uv venv
uv pip install -e ".[dev]"

# Run the CLI against the sample data
python -m csv_batch_reporter.cli sample_data/sales_jan.csv sample_data/sales_feb.csv

# Or write the report to a file
python -m csv_batch_reporter.cli sample_data/*.csv -o report.txt
```

## Sample output

```
SALES SUMMARY REPORT
========================================
Total rows processed : 8
Total amount         : $1,382.49

By category:
  Clothing        $178.75
  Electronics     $959.99
  Groceries       $243.75
```

## Running tests

```bash
uv pip install -e ".[dev]"
pytest -v
```

## Project layout

```
src/csv_batch_reporter/reporter.py   - aggregation logic (ReportSummary, build_summary)
src/csv_batch_reporter/cli.py        - argparse CLI entry point
tests/test_reporter.py               - unit tests
sample_data/                          - dummy input CSVs for a quick demo run
```
