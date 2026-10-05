"""Core aggregation logic for the CSV batch reporter."""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_COLUMNS = {"category", "amount"}


@dataclass
class ReportSummary:
    """Aggregated totals produced from one or more CSV files."""

    total_rows: int = 0
    total_amount: float = 0.0
    by_category: dict[str, float] = field(default_factory=dict)

    def add_row(self, category: str, amount: float) -> None:
        self.total_rows += 1
        self.total_amount += amount
        self.by_category[category] = self.by_category.get(category, 0.0) + amount

    def as_text(self) -> str:
        lines = [
            "SALES SUMMARY REPORT",
            "=" * 40,
            f"Total rows processed : {self.total_rows}",
            f"Total amount         : ${self.total_amount:,.2f}",
            "",
            "By category:",
        ]
        for category, amount in sorted(self.by_category.items()):
            lines.append(f"  {category:<15} ${amount:,.2f}")
        return "\n".join(lines)


def load_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file and validate it has the required columns."""
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            raise ValueError(f"{path} is missing required columns: {REQUIRED_COLUMNS}")
        return list(reader)


def build_summary(csv_paths: list[Path]) -> ReportSummary:
    """Aggregate rows across one or more CSV files into a single summary.

    Malformed rows (non-numeric amounts) are skipped rather than aborting
    the whole batch -- one bad row in a daily feed shouldn't nuke the report.
    """
    summary = ReportSummary()
    for path in csv_paths:
        for row in load_csv(path):
            try:
                amount = float(row["amount"])
            except ValueError:
                continue
            category = row["category"].strip() or "UNCATEGORIZED"
            summary.add_row(category, amount)
    return summary
