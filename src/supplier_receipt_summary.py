"""Produce monthly supplier/product receipt summaries from cleaned receipt lines.

The input is the accepted supplier_receipt_lines.csv file from the preceding backlog.
The analysis reports quantities and receipt frequencies at supplier/product/month grain.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"Supplier_ID", "Product_ID", "Receipt_ID", "Receipt_Date", "Quantity"}
OUTPUT_COLUMNS = ["Supplier_ID", "Product_ID", "Receipt_Month", "Receipt_Frequency", "Total_Quantity"]


def load_receipts(input_path: str | Path) -> pd.DataFrame:
    """Read a cleaned receipt-lines CSV and verify its essential fields."""
    frame = pd.read_csv(
        input_path,
        dtype={"Supplier_ID": "string", "Product_ID": "string", "Receipt_ID": "string"},
    )
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError("Required receipt columns missing: " + ", ".join(missing))
    if frame.empty:
        return frame

    frame["Receipt_Date"] = pd.to_datetime(frame["Receipt_Date"], errors="coerce")
    if frame["Receipt_Date"].isna().any():
        raise ValueError("Receipt_Date contains missing or invalid dates")

    frame["Quantity"] = pd.to_numeric(frame["Quantity"], errors="coerce")
    if frame["Quantity"].isna().any():
        raise ValueError("Quantity contains missing or non-numeric values")
    if frame[["Supplier_ID", "Product_ID", "Receipt_ID"]].isna().any().any():
        raise ValueError("Required identifiers cannot be null")
    return frame


def summarise_receipts(
    receipts: pd.DataFrame,
    start_date: str,
    end_date: str,
) -> tuple[pd.DataFrame, dict]:
    """Summarise receipt lines and construct a product reconciliation report."""
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    if end < start:
        raise ValueError("End date cannot precede start date")

    if receipts.empty:
        empty = pd.DataFrame(columns=OUTPUT_COLUMNS)
        return empty, {
            "reporting_range": {"start": start_date, "end": end_date},
            "source_rows": 0,
            "included_rows": 0,
            "metric_definitions": {
                "Receipt_Frequency": "Number of distinct receipts per supplier, product and month",
                "Total_Quantity": "Sum of receipt-line Quantity per supplier, product and month",
            },
            "per_product_reconciliation": [],
            "reconciled": True,
        }

    # Include only receipt activity in the reporting window.
    included = receipts.loc[
        (receipts["Receipt_Date"] >= start)
        & (receipts["Receipt_Date"] < end)
    ].copy()
    included["Receipt_Month"] = included["Receipt_Date"].dt.strftime("%Y-%m")

    if included.empty:
        summary = pd.DataFrame(columns=OUTPUT_COLUMNS)
    else:
        summary = (
            included.groupby(
                ["Supplier_ID", "Product_ID", "Receipt_Month"], dropna=False, as_index=False
            )
            .agg(
                Receipt_Frequency=("Receipt_ID", "count"),
                Total_Quantity=("Quantity", "sum"),
            )
            .sort_values(["Supplier_ID", "Product_ID", "Receipt_Month"])
            .reset_index(drop=True)
        )

    source_by_product = included.groupby("Product_ID")["Quantity"].sum()
    summary_by_product = (
        summary.groupby("Product_ID")["Total_Quantity"].sum()
        if not summary.empty
        else pd.Series(dtype="float64")
    )
    reconciliations = []
    for product in sorted(set(source_by_product.index) | set(summary_by_product.index)):
        source_total = float(source_by_product.get(product, 0))
        summary_total = float(summary_by_product.get(product, 0))
        matched = abs(source_total - summary_total) < 1e-8
        reconciliations.append({
            "Product_ID": str(product),
            "Source_Quantity": source_total,
            "Summary_Quantity": summary_total,
            "Matches": matched,
        })

    report = {
        "reporting_range": {"start": start_date, "end": end_date},
        "source_rows": int(len(receipts)),
        "included_rows": int(len(included)),
        "metric_definitions": {
            "Receipt_Frequency": "Number of distinct receipts per supplier, product and month",
            "Total_Quantity": "Sum of receipt-line Quantity per supplier, product and month",
        },
        "per_product_reconciliation": reconciliations,
        "reconciled": all(item["Matches"] for item in reconciliations),
    }
    return summary[OUTPUT_COLUMNS], report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarise monthly supplier receipt activity")
    parser.add_argument("--input", required=True, help="Cleaned supplier_receipt_lines.csv")
    parser.add_argument("--start-date", required=True, help="Start (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="End (YYYY-MM-DD)")
    parser.add_argument("--output", default="outputs/monthly_supplier_receipts.csv")
    parser.add_argument("--report", default="outputs/validation_report.json")
    args = parser.parse_args(argv)

    receipts = load_receipts(args.input)
    summary, report = summarise_receipts(receipts, args.start_date, args.end_date)
    output_path = Path(args.output)
    report_path = Path(args.report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Summary: {output_path} ({len(summary)} rows)")
    print(f"Validation report: {report_path} (reconciled={report['reconciled']})")
    return 0 if report["reconciled"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
