#!/usr/bin/env python3
"""Monthly Update Script for Awesome AI/ML Startups Repository (v2).

Workflow since the September 2026 rebuild:
1. Edit the canonical master dataset: data/master/startups_master.json
   (and mirror rows to startups_master.csv) — one row per company.
2. Regenerate the month's snapshot from master:
       python scripts/build_snapshots.py --month october --year 2026
3. Regenerate category pages:
       python scripts/build_categories.py
4. Validate everything:
       python scripts/validate_data.py
       python scripts/check_links.py

Usage:
    python update_monthly.py --month october --year 2026   # show the checklist
"""

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"

MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]


def main():
    parser = argparse.ArgumentParser(description="Monthly update checklist")
    parser.add_argument("--month", required=True, help="Month name (e.g., october)")
    parser.add_argument("--year", type=int, required=True, help="Year (e.g., 2026)")
    parser.add_argument("--copy-previous", action="store_true",
                        help="Deprecated: snapshots are generated from master; kept for compatibility")
    args = parser.parse_args()

    month = args.month.lower()
    if month not in MONTHS:
        raise SystemExit(f"Unknown month: {args.month}")

    print(f"\n{'=' * 60}")
    print(f"  Monthly Update: {month.capitalize()} {args.year}")
    print(f"{'=' * 60}\n")

    master = DATA_DIR / "master" / "startups_master.json"
    print(f"  Master dataset: {master.relative_to(REPO_ROOT)}"
          f" {'(found)' if master.exists() else '(MISSING!)'}\n")

    print("  Checklist:")
    print("   1. Update data/master/startups_master.json (+ .csv) with new/changed companies")
    print(f"   2. python scripts/build_snapshots.py --month {month} --year {args.year}")
    print("   3. python scripts/build_categories.py")
    print("   4. python scripts/validate_data.py")
    print("   5. python scripts/check_links.py")
    print("   6. Update README.md highlights + CHANGELOG.md\n")


if __name__ == "__main__":
    main()
