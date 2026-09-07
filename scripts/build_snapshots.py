#!/usr/bin/env python3
"""Generate a monthly snapshot (CSV + JSON + stats.json) from the master dataset.

Usage:
    python scripts/build_snapshots.py --month september --year 2026
    python scripts/build_snapshots.py --latest

The snapshot includes ALL master entries (the tracker tracks a cumulative
universe), sorted by id. stats.json mirrors data distributions for the README.
"""
import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).parent.parent
DATA_DIR = REPO / "data"
MASTER_PATH = DATA_DIR / "master" / "startups_master.json"

MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]


def month_end(year: int, month_idx: int) -> str:
    import calendar
    last = calendar.monthrange(year, month_idx)[1]
    return f"{year}-{month_idx:02d}-{last:02d}"


def load_master():
    with open(MASTER_PATH, encoding="utf-8") as f:
        return json.load(f)


def write_snapshot(year: int, month: str):
    master = load_master()
    startups = master["startups"]
    month_idx = MONTHS.index(month) + 1

    # snapshot metadata
    prev_year, prev_month = (year - 1, 12) if month_idx == 1 else (year, month_idx - 1)
    new_this_month = sum(
        1 for s in startups
        if (s.get("date_added") or "")[:7] == f"{year}-{month_idx:02d}"
    )

    payload = {
        "metadata": {
            "month": month.capitalize(),
            "year": year,
            "date_published": month_end(year, month_idx),
            "total_startups": len(startups),
            "new_this_month": new_this_month,
            "categories": sorted({s["category"] for s in startups}),
            "sources": sorted({
                src.strip()
                for s in startups
                for src in (s.get("source") or "").split(",")
            }),
            "schema_version": "2.0",
            "derived_from": "data/master/startups_master.json",
            "as_of": master["metadata"]["as_of"],
            "license": "MIT",
            "next_update": f"{prev_year}-{prev_month:02d}-30" if False else _next_update(year, month_idx),
        },
        "startups": startups,
    }

    month_dir = DATA_DIR / str(year) / month
    month_dir.mkdir(parents=True, exist_ok=True)

    json_path = month_dir / f"startups_{month}_{year}.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    csv_path = month_dir / f"startups_{month}_{year}.csv"
    fields = list(startups[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for s in startups:
            row = dict(s)
            row["investors"] = "; ".join(s.get("investors") or [])
            row["tags"] = "; ".join(s.get("tags") or [])
            row["source_urls"] = " | ".join(s.get("source_urls") or [])
            w.writerow(row)

    stats = build_stats(master, month, year, new_this_month)
    stats_path = month_dir / "stats.json"
    stats_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Snapshot written: {json_path}")
    print(f"Snapshot written: {csv_path}")
    print(f"Stats written:    {stats_path}")
    print(f"Total: {len(startups)} | New this month: {new_this_month}")


def _next_update(year: int, month_idx: int) -> str:
    ny, nm = (year + 1, 1) if month_idx == 12 else (year, month_idx + 1)
    return f"{ny}-{nm:02d}-30"


def build_stats(master, month: str, year: int, new_this_month: int) -> dict:
    startups = master["startups"]
    categories = Counter(s["category"] for s in startups)
    stages = Counter(s["funding_stage"] for s in startups)
    regions = Counter(s["region"] for s in startups)
    countries = Counter(s["country"] for s in startups)
    hqs = Counter(s["headquarters"] for s in startups)
    verif = Counter(s["verification_status"] for s in startups)
    statuses = Counter(s["status"] for s in startups)

    def parse_amount(v):
        if not v:
            return 0
        return v if isinstance(v, (int, float)) else 0

    top_rounds = sorted(
        (s for s in startups if s.get("funding_amount_usd")),
        key=lambda s: s["funding_amount_usd"], reverse=True,
    )[:10]
    top_valuations = sorted(
        (s for s in startups if s.get("valuation_usd")),
        key=lambda s: s["valuation_usd"], reverse=True,
    )[:10]

    return {
        "month": month.capitalize(),
        "year": year,
        "as_of": master["metadata"]["as_of"],
        "total_startups": len(startups),
        "new_this_month": new_this_month,
        "categories": dict(categories.most_common()),
        "funding_stages": dict(stages.most_common()),
        "regions": dict(regions.most_common()),
        "countries": dict(countries.most_common()),
        "headquarters_top": dict(hqs.most_common(10)),
        "verification_status": dict(verif.most_common()),
        "status": dict(statuses.most_common()),
        "top_rounds_latest": [
            {"startup": s["startup_name"], "amount": s["funding_amount"],
             "usd": s["funding_amount_usd"], "date": s.get("last_round_date")}
            for s in top_rounds
        ],
        "top_valuations": [
            {"startup": s["startup_name"], "valuation": s["valuation_display"],
             "usd": s["valuation_usd"]}
            for s in top_valuations
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month")
    ap.add_argument("--year", type=int)
    ap.add_argument("--latest", action="store_true", help="build snapshot for current month")
    args = ap.parse_args()

    if args.latest or not (args.month and args.year):
        today = date.today()
        args.year, args.month = today.year, MONTHS[today.month - 1]

    write_snapshot(args.year, args.month)


if __name__ == "__main__":
    main()
