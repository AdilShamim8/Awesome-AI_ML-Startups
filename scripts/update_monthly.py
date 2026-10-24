#!/usr/bin/env python3
"""Monthly Update Script for Awesome AI/ML Startups Repository (v3).

Workflow since the October 2026 refresh:
1. Edit the canonical master datasets:
   - data/master/startups_master.json (companies) — then regenerate
     the CSV with scripts/build_master_csv.py
   - data/master/funding_rounds.json (events) — then regenerate the
     CSV with scripts/build_funding_rounds_csv.py
   Keep event round_dates <= metadata.cutoff (the validator enforces it).
2. Regenerate the month's snapshot from master:
       python scripts/build_snapshots.py --month october --year 2026
   (add --date YYYY-MM-DD for a pre-month-end research snapshot)
3. Regenerate category pages:
       python scripts/build_categories.py
4. Validate everything:
       python scripts/validate_data.py
       python -m unittest discover -s tests
       python scripts/build_master_csv.py --check
       python scripts/build_funding_rounds_csv.py --check
5. Optionally check links (bot-blocked 403/429 are not failures):
       python scripts/check_links.py
6. Update README.md stats, CHANGELOG.md, docs/evidence_log.md, and
   docs/search_queries.md with the research trail.

CI runs the validation, parity checks, and tests on every push, and a
scheduled workflow opens the monthly checklist issue on the 28th.

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
    print("   1. Update data/master/startups_master.json (+ regenerate startups_master.csv")
    print("      via scripts/build_master_csv.py) with new/changed companies")
    print("   2. Update data/master/funding_rounds.json with verified events (respect")
    print("      metadata.cutoff) and regenerate funding_rounds.csv via")
    print("      scripts/build_funding_rounds_csv.py")
    print(f"   3. python scripts/build_snapshots.py --month {month} --year {args.year}")
    print("      (add --date YYYY-MM-DD for a pre-month-end research snapshot)")
    print("   4. python scripts/build_categories.py")
    print("   5. python scripts/validate_data.py && python -m unittest discover -s tests")
    print("   6. python scripts/build_master_csv.py --check && \\")
    print("      python scripts/build_funding_rounds_csv.py --check")
    print("   7. python scripts/check_links.py (optional; 403/429 = bot-blocked, not dead)")
    print("   8. Update README.md highlights + CHANGELOG.md + docs/evidence_log.md")
    print("      + docs/search_queries.md with the research trail\n")


if __name__ == "__main__":
    main()
