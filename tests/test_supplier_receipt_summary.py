"""Basic regression checks for supplier receipt reporting."""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "receipt_lines_sample.csv"
sys.path.insert(0, str(ROOT / "src"))
from supplier_receipt_summary import load_receipts, summarise_receipts  # noqa: E402


def test_groups_by_supplier_product_and_month():
    receipts = load_receipts(FIXTURE)
    summary, report = summarise_receipts(receipts, "2026-01-01", "2026-03-01")
    assert len(summary) == 4
    assert report["reconciled"] is True
    row = summary.loc[(summary.Supplier_ID == "S101") & (summary.Product_ID == "P100") & (summary.Receipt_Month == "2026-01")].iloc[0]
    assert row.Total_Quantity == 20
    assert row.Receipt_Frequency == 2


def test_keeps_products_separate():
    summary, _ = summarise_receipts(load_receipts(FIXTURE), "2026-01-01", "2026-03-01")
    totals = summary.groupby("Product_ID")["Total_Quantity"].sum().to_dict()
    assert totals == {"P100": 34, "P200": 6}


def test_cli_emits_csv_and_json(tmp_path):
    out = tmp_path / "summary.csv"
    report = tmp_path / "report.json"
    run = subprocess.run([
        sys.executable, str(ROOT / "src" / "supplier_receipt_summary.py"),
        "--input", str(FIXTURE), "--start-date", "2026-01-01", "--end-date", "2026-03-01",
        "--output", str(out), "--report", str(report),
    ], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
    assert list(pd.read_csv(out).columns) == ["Supplier_ID", "Product_ID", "Receipt_Month", "Receipt_Frequency", "Total_Quantity"]
    assert json.loads(report.read_text())["reconciled"] is True
