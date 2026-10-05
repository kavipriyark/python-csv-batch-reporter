from pathlib import Path

from csv_batch_reporter.reporter import build_summary


def test_build_summary_aggregates_across_files(tmp_path: Path) -> None:
    f1 = tmp_path / "a.csv"
    f1.write_text("category,amount\nGroceries,10.50\nElectronics,99.99\n")
    f2 = tmp_path / "b.csv"
    f2.write_text("category,amount\nGroceries,5.00\n")

    summary = build_summary([f1, f2])

    assert summary.total_rows == 3
    assert round(summary.total_amount, 2) == 115.49
    assert summary.by_category["Groceries"] == 15.50
    assert summary.by_category["Electronics"] == 99.99


def test_build_summary_skips_malformed_rows(tmp_path: Path) -> None:
    f = tmp_path / "bad.csv"
    f.write_text("category,amount\nGroceries,oops\nGroceries,10\n")

    summary = build_summary([f])

    assert summary.total_rows == 1
    assert summary.total_amount == 10


def test_missing_required_columns_raises(tmp_path: Path) -> None:
    f = tmp_path / "bad_schema.csv"
    f.write_text("name,value\nfoo,1\n")

    try:
        build_summary([f])
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_report_text_contains_totals() -> None:
    from csv_batch_reporter.reporter import ReportSummary

    summary = ReportSummary()
    summary.add_row("Groceries", 10.0)
    text = summary.as_text()

    assert "Total rows processed : 1" in text
    assert "Groceries" in text
