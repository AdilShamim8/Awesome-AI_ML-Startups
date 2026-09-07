#!/usr/bin/env python3
"""README Statistics Generator for Awesome AI/ML Startups Repository (v2).

Reads the canonical master dataset by default (or a specific month's snapshot)
and prints/saves statistics used in the README.

Usage:
    python scripts/generate_readme.py                    # master dataset stats
    python scripts/generate_readme.py --year 2026 --month september
"""

import argparse
import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
MASTER_PATH = DATA_DIR / "master" / "startups_master.json"


def generate_stats(source: dict, label: str) -> dict:
    startups = source.get("startups", [])
    categories = Counter(s.get("category", "Unknown") for s in startups)
    stages = Counter(s.get("funding_stage", "Unknown") for s in startups)
    regions = Counter(s.get("region", "Unknown") for s in startups)
    countries = Counter(s.get("country", "Unknown") for s in startups)
    sources = Counter()
    for s in startups:
        for src in (s.get("source") or "").split(","):
            if src.strip():
                sources[src.strip()] += 1
    verification = Counter(s.get("verification_status", "Unknown") for s in startups)
    statuses = Counter(s.get("status", "active") for s in startups)
    founded = Counter(s.get("founded_year") for s in startups)

    return {
        "label": label,
        "total_startups": len(startups),
        "categories": dict(categories.most_common()),
        "funding_stages": dict(stages.most_common()),
        "regions": dict(regions.most_common()),
        "countries": dict(countries.most_common()),
        "sources": dict(sources.most_common(12)),
        "verification_status": dict(verification.most_common()),
        "status": dict(statuses.most_common()),
        "founded_years": dict(sorted((k, v) for k, v in founded.items() if k)),
    }


def print_stats(stats: dict) -> None:
    print(f"\n{'=' * 60}")
    print(f"  Statistics: {stats['label']}")
    print(f"{'=' * 60}")
    print(f"\n  Total Startups: {stats['total_startups']}")
    print(f"\n  Categories:")
    for cat, count in stats["categories"].items():
        bar = "█" * min(count, 25) + "░" * max(25 - min(count, 25), 0)
        print(f"    {cat:15s} {bar} {count}")
    print(f"\n  Funding Stages:")
    for stage, count in stats["funding_stages"].items():
        print(f"    {stage:15s} {count}")
    print(f"\n  Regions: {stats['regions']}")
    print(f"\n  Verification: {stats['verification_status']}")
    print(f"\n  Status: {stats['status']}")
    print(f"{'=' * 60}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int)
    ap.add_argument("--month")
    args = ap.parse_args()

    if args.year and args.month:
        path = DATA_DIR / str(args.year) / args.month.lower() / f"startups_{args.month.lower()}_{args.year}.json"
        label = f"{args.month.capitalize()} {args.year}"
        with open(path, encoding="utf-8") as f:
            source = json.load(f)
    else:
        path = MASTER_PATH
        label = "Master dataset"
        with open(path, encoding="utf-8") as f:
            source = json.load(f)

    print(f"  Analyzing: {path.relative_to(REPO_ROOT)}")
    stats = generate_stats(source, label)
    print_stats(stats)

    if args.year and args.month:
        out_path = path.parent / "stats.json"
        out_path.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  Stats saved to: {out_path}")


if __name__ == "__main__":
    main()
