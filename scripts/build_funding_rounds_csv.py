#!/usr/bin/env python3
"""Regenerate data/master/funding_rounds.csv from funding_rounds.json.

The JSON file is the canonical event-level dataset; the CSV is the mirror.
This script also derives a clean `source_domain` column from the first
source URL (the September 2026 build left partially-populated values such
as ' + elevenlabs.io', which this replaces with proper domains).

    python scripts/build_funding_rounds_csv.py            # rewrite the CSV
    python scripts/build_funding_rounds_csv.py --check    # exit 1 if out of sync
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).parent.parent
ROUNDS_JSON = REPO_ROOT / "data" / "master" / "funding_rounds.json"
ROUNDS_CSV = REPO_ROOT / "data" / "master" / "funding_rounds.csv"

FIELDS = [
    "event_id", "startup_name", "round_date", "month", "amount_display",
    "amount_usd_m", "stage", "valuation_display", "valuation_usd_m",
    "investors", "about", "country", "source", "source_domain",
    "source_urls", "verification_status", "last_verified", "in_registry",
    "notes",
]


def derive_domain(source_urls) -> str:
    """Registrable-ish domain of the first URL, with www. stripped."""
    if not source_urls:
        return ""
    first = str(source_urls).split("|")[0].strip()
    if not first:
        return ""
    try:
        host = urlparse(first).netloc or ""
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def record_to_row(rec: dict) -> dict:
    row = {k: rec.get(k) for k in FIELDS if k != "source_domain"}
    row["source_domain"] = derive_domain(rec.get("source_urls"))
    for k, v in row.items():
        if v is None:
            row[k] = ""
        elif isinstance(v, bool):
            row[k] = "True" if v else "False"
    return row


def build_rows():
    with open(ROUNDS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    rounds = data.get("rounds") or []
    if not rounds:
        raise SystemExit("funding_rounds.json contains no events; refusing to write empty CSV")
    return [record_to_row(r) for r in rounds]


def write_csv(rows):
    with open(ROUNDS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def csv_is_current(rows) -> bool:
    if not ROUNDS_CSV.exists():
        return False
    try:
        with open(ROUNDS_CSV, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing = list(reader)
            header = reader.fieldnames or []
    except (OSError, csv.Error):
        return False
    if header != FIELDS or len(existing) != len(rows):
        return False
    for old, new in zip(existing, rows):
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
            print(f"OK: {ROUNDS_CSV.name} is in sync with the JSON ({len(rows)} events)")
            return
        print(f"OUT OF SYNC: {ROUNDS_CSV.name} does not match {ROUNDS_JSON.name}")
        print("Run: python scripts/build_funding_rounds_csv.py")
        sys.exit(1)

    write_csv(rows)
    print(f"Wrote {len(rows)} events to {ROUNDS_CSV.relative_to(REPO_ROOT)}")
    print(f"Columns: {len(FIELDS)} (source_domain derived from source_urls)")


if __name__ == "__main__":
    main()
