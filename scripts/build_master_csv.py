#!/usr/bin/env python3
"""Regenerate data/master/startups_master.csv from startups_master.json.

The JSON file is the canonical dataset; the CSV is a mirror for spreadsheet
users. This script keeps the two in lockstep so they never drift:

    python scripts/build_master_csv.py            # rewrite the CSV
    python scripts/build_master_csv.py --check    # exit 1 if out of sync

List-valued fields are serialized with the same conventions used by the
monthly snapshot generator (build_snapshots.py):
  investors   -> "; " joined
  tags        -> "; " joined
  source_urls -> " | " joined
Null values are written as empty cells.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MASTER_JSON = REPO_ROOT / "data" / "master" / "startups_master.json"
MASTER_CSV = REPO_ROOT / "data" / "master" / "startups_master.csv"

FIELDS = [
    "id", "slug", "startup_name", "about", "description", "website",
    "category", "subcategory", "funding_stage", "funding_amount",
    "funding_amount_usd", "valuation_display", "valuation_usd",
    "total_raised_display", "last_round_date", "investors",
    "headquarters", "city", "country", "region", "founded_year",
    "status", "status_note", "source", "source_urls", "date_added",
    "last_updated", "last_verified", "verification_status", "tags", "notes",
]


def record_to_row(rec: dict) -> dict:
    row = {}
    for field in FIELDS:
        val = rec.get(field)
        if field == "investors":
            val = "; ".join(val or [])
        elif field == "tags":
            val = "; ".join(val or [])
        elif field == "source_urls":
            val = " | ".join(val or [])
        elif val is None:
            val = ""
        row[field] = val
    return row


def build_rows():
    with open(MASTER_JSON, encoding="utf-8") as f:
        master = json.load(f)
    startups = master.get("startups", [])
    if not startups:
        raise SystemExit("master JSON contains no startups; refusing to write empty CSV")
    return [record_to_row(s) for s in startups]


def write_csv(rows):
    with open(MASTER_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def csv_is_current(rows) -> bool:
    """True if the on-disk CSV matches what we would generate."""
    if not MASTER_CSV.exists():
        return False
    try:
        with open(MASTER_CSV, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing = list(reader)
            header = reader.fieldnames or []
    except (OSError, csv.Error):
        return False
    if header != FIELDS:
        return False
    if len(existing) != len(rows):
        return False
    for old, new in zip(existing, rows):
        # CSV cells are always strings; coerce both sides before comparing
        if {k: (v or "") for k, v in old.items()} != {k: str(v) for k, v in new.items()}:
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify the CSV matches the JSON; exit 1 if not")
    args = ap.parse_args()

    rows = build_rows()

    if args.check:
        if csv_is_current(rows):
            print(f"OK: {MASTER_CSV.name} is in sync with the JSON ({len(rows)} rows)")
            return
        print(f"OUT OF SYNC: {MASTER_CSV.name} does not match {MASTER_JSON.name}")
        print("Run: python scripts/build_master_csv.py")
        sys.exit(1)

    write_csv(rows)
    print(f"Wrote {len(rows)} rows to {MASTER_CSV.relative_to(REPO_ROOT)}")
    print(f"Columns: {len(FIELDS)}")


if __name__ == "__main__":
    main()
