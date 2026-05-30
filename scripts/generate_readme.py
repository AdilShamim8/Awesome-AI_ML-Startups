#!/usr/bin/env python3
"""
README Statistics Generator for Awesome AI/ML Startups Repository.

This script reads the current month's JSON data and generates
updated statistics for the README.md file.

Usage:
    python generate_readme.py
    python generate_readme.py --year 2026 --month may
"""

import argparse
import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"


def get_latest_month_dir() -> tuple:
    """Find the latest month directory with data."""
    latest_year = 0
    latest_month = ""

    for year_dir in sorted(DATA_DIR.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        year = int(year_dir.name)
        if year < latest_year:
            continue

        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            json_files = list(month_dir.glob("*.json"))
            if json_files:
                latest_year = year
                latest_month = month_dir.name

    return latest_year, latest_month


def generate_stats(year: int, month: str) -> dict:
    """Generate statistics from the month's JSON data."""
    month_dir = DATA_DIR / str(year) / month.lower()
    json_files = list(month_dir.glob("*.json"))

    if not json_files:
        return {"error": f"No JSON data found in {month_dir}"}

    with open(json_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    startups = data.get("startups", [])
    metadata = data.get("metadata", {})

    # Category distribution
    categories = Counter(s.get("category", "Unknown") for s in startups)

    # Funding stage distribution
    stages = Counter(s.get("funding_stage", "Unknown") for s in startups)

    # Headquarters distribution
    hqs = Counter(s.get("headquarters", "Unknown") for s in startups)

    # Source distribution
    sources = Counter()
    for s in startups:
        for source in s.get("source", "").split(" / "):
            sources[source.strip()] += 1

    # Founded year distribution
    founded_years = Counter(s.get("founded_year", "Unknown") for s in startups)

    stats = {
        "month": month.capitalize(),
        "year": year,
        "total_startups": len(startups),
        "new_this_month": metadata.get("new_this_month", 0),
        "categories": dict(categories.most_common()),
        "funding_stages": dict(stages.most_common()),
        "headquarters": dict(hqs.most_common(10)),
        "sources": dict(sources.most_common(10)),
        "founded_years": dict(sorted(founded_years.items())),
    }

    return stats


def print_stats(stats: dict) -> None:
    """Print formatted statistics."""
    if "error" in stats:
        print(f"  ❌ {stats['error']}")
        return

    print(f"\n{'='*60}")
    print(f"  Statistics: {stats['month']} {stats['year']}")
    print(f"{'='*60}")

    print(f"\n  📊 Overview:")
    print(f"    Total Startups: {stats['total_startups']}")
    print(f"    New This Month: {stats['new_this_month']}")

    print(f"\n  🏷️ Categories:")
    for cat, count in stats['categories'].items():
        bar = "█" * count + "░" * (20 - min(count, 20))
        print(f"    {cat:25s} {bar} {count}")

    print(f"\n  💰 Funding Stages:")
    for stage, count in stats['funding_stages'].items():
        print(f"    {stage:15s} {count}")

    print(f"\n  🌍 Top Headquarters:")
    for hq, count in stats['headquarters'].items():
        print(f"    {hq:40s} {count}")

    print(f"\n  📰 Top Sources:")
    for source, count in stats['sources'].items():
        print(f"    {source:30s} {count}")

    print(f"\n  📅 Founded Years:")
    for year, count in stats['founded_years'].items():
        print(f"    {year:>6}  {count}")

    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate README statistics"
    )
    parser.add_argument(
        "--year", type=int,
        help="Year (e.g., 2026)"
    )
    parser.add_argument(
        "--month",
        help="Month (e.g., may)"
    )

    args = parser.parse_args()

    if args.year and args.month:
        year, month = args.year, args.month
    else:
        year, month = get_latest_month_dir()

    print(f"  Analyzing data for: {month.capitalize()} {year}")

    stats = generate_stats(year, month)
    print_stats(stats)

    # Save stats to JSON
    stats_path = DATA_DIR / str(year) / month.lower() / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"  Stats saved to: {stats_path}")


if __name__ == "__main__":
    main()
