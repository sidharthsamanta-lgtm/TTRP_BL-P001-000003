# Supplier Receipt Reporting

A persistent TTRP Python project workspace for supplier receipt line analytics. This repository implements the monthly supplier/product receipt reporting backlog on top of cleaned `supplier_receipt_lines.csv` data (accepted upstream lines are assumed, not provided in this package).

Read the existing permanent [TTRP Resident Guide](TTRP_GUIDE.md) in your template-based repository before submitting a backlog.

## Project overview

This project produces descriptive receipt-volume reporting. It does not estimate spending, supplier reliability, lead times, or other delivery performance measures.

## Current backlog

- **Backlog code:** `BL-P001-000002`
- **Title:** Summarise Monthly Supplier Receipt Activity per Product
- **Implemented behaviour:** report monthly receipt frequency and total quantity grouped by supplier, product and calendar receipt month, with a requested reporting date range and a JSON reconciliation report.
- **Prerequisite:** DAB00 — the accepted cleaned receipt-lines output is treated as the baseline. It was not included with this example package.

## Requirements and configuration

Python 3.10+ with pandas and pytest. Input CSV must contain `Supplier_ID`, `Product_ID`, `Receipt_ID`, `Receipt_Date` and `Quantity`. Dates must be readable by pandas; quantities must be numeric. No credentials or environment variables are needed.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python src/supplier_receipt_summary.py \
  --input supplier_receipt_lines.csv \
  --start-date 2026-01-01 \
  --end-date 2026-03-31 \
  --output outputs/monthly_supplier_receipts.csv \
  --report outputs/validation_report.json
```

A small synthetic fixture is included for smoke testing:

```bash
python src/supplier_receipt_summary.py \
  --input tests/fixtures/receipt_lines_sample.csv \
  --start-date 2026-01-01 --end-date 2026-03-01
```

The reporting window is intended to include the start and end dates.

## Output interpretation

The summary CSV has one row per `(Supplier_ID, Product_ID, Receipt_Month)`:

- `Receipt_Month`: receipt calendar month as `YYYY-MM`.
- `Receipt_Frequency`: number of distinct receipt IDs observed at the reporting grain.
- `Total_Quantity`: total receipt-line quantity for the given supplier/product/month. Never compare quantities for different products as if they had the same unit.

The JSON validation report includes the requested range, input and included row counts, metric definitions, a per-product source/summary quantity comparison, and a reconciliation flag.

## Verify

```bash
python -m pytest -q
```

The fixture verifies representative monthly groups, per-product quantity separation, and CLI file creation. No actual resident data or live supplier data was executed for this package.

## Repository structure

- `src/` — implementation, extended rather than replaced across backlogs.
- `tests/` — synthetic checks and fixtures.
- `docs/reflections/` — backlog-specific reflections.
- `docs/DECISIONS.md` — lasting engineering decisions.
- `evidence/` — relevant verification outputs.
- `TTRP_GUIDE.md` — permanent resident instructions from the template.

## Source limitations

The input is assumed to have already passed upstream cleaning. This report has no master-data validation of supplier identity, product units, receipt corrections or duplicate source records. It reports descriptive volumes only. Time series are shown for months with source activity; zero-activity months are not expanded in this backlog.

## Backlog handoffs

- [BL-P001-000002 reflection](docs/reflections/BL-P001-000002.md)

## Known limitations

Only CSV input is supported. Source correctness and unit consistency depend on the accepted upstream data. This task does not generate forecasts, charts or dashboards.
