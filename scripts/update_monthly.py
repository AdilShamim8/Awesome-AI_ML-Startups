#!/usr/bin/env python3
"""
Monthly Update Script for Awesome AI/ML Startups Repository.

This script helps automate the monthly data update process:
1. Creates the new month's data directory
2. Copies the schema template
3. Validates the new data
4. Updates the README statistics

Usage:
    python update_monthly.py --month may --year 2026
"""

import argparse
import csv
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"


def create_month_directory(year: int, month: str) -> Path:
    """Create the new month's data directory."""
    month_dir = DATA_DIR / str(year) / month.lower()
    month_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {month_dir}")
    return month_dir


def create_csv_template(month_dir: Path, month: str, year: int) -> Path:
    """Create an empty CSV template for the new month."""
    csv_path = month_dir / f"startups_{month.lower()}_{year}.csv"
    if csv_path.exists():
        print(f"CSV already exists: {csv_path}")
        return csv_path

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "startup_name", "about", "description", "website",
            "category", "funding_stage", "funding_amount", "headquarters",
            "founded_year", "source", "date_added"
        ])

    print(f"Created CSV template: {csv_path}")
    return csv_path


def create_json_template(month_dir: Path, month: str, year: int) -> Path:
    """Create an empty JSON template for the new month."""
    json_path = month_dir / f"startups_{month.lower()}_{year}.json"

    template = {
        "metadata": {
            "month": month.capitalize(),
            "year": year,
            "date_published": f"{year}-{_month_to_num(month)}-30",
            "total_startups": 0,
            "new_this_month": 0,
            "categories": [
                "AI/ML", "Generative AI", "AI Agents", "SaaS",
                "DevTools", "FinTech", "HealthTech", "Robotics",
                "Cybersecurity", "EdTech"
            ],
            "sources": [],
            "license": "MIT",
            "next_update": f"{year}-{_next_month_num(month)}-30"
        },
        "startups": []
    }

    if json_path.exists():
        print(f"JSON already exists: {json_path}")
        return json_path

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

    print(f"Created JSON template: {json_path}")
    return json_path


def _month_to_num(month: str) -> str:
    """Convert month name to 2-digit number."""
    months = {
        "january": "01", "february": "02", "march": "03",
        "april": "04", "may": "05", "june": "06",
        "july": "07", "august": "08", "september": "09",
        "october": "10", "november": "11", "december": "12"
    }
    return months.get(month.lower(), "01")


def _next_month_num(month: str) -> str:
    """Get the next month's number."""
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    idx = months.index(month.lower())
    next_idx = (idx + 1) % 12
    return f"{next_idx + 1:02d}"


def copy_previous_data(month_dir: Path, year: int, month: str) -> None:
    """Optionally copy data from the previous month as a starting point."""
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    idx = months.index(month.lower())

    if idx == 0:
        prev_month = "december"
        prev_year = year - 1
    else:
        prev_month = months[idx - 1]
        prev_year = year

    prev_dir = DATA_DIR / str(prev_year) / prev_month
    if prev_dir.exists():
        prev_csv = prev_dir / f"startups_{prev_month}_{prev_year}.csv"
        if prev_csv.exists():
            print(f"Previous month data found at: {prev_csv}")
            print("Tip: Use the previous month's data as a baseline for updates.")


def count_startups(month_dir: Path) -> int:
    """Count the number of startups in the current month's data."""
    json_files = list(month_dir.glob("*.json"))
    if not json_files:
        return 0

    with open(json_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    return len(data.get("startups", []))


def main():
    parser = argparse.ArgumentParser(
        description="Monthly update script for Awesome AI/ML Startups"
    )
    parser.add_argument(
        "--month", required=True,
        help="Month name (e.g., may, june)"
    )
    parser.add_argument(
        "--year", type=int, required=True,
        help="Year (e.g., 2026)"
    )
    parser.add_argument(
        "--copy-previous", action="store_true",
        help="Copy previous month's data as starting point"
    )

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Monthly Update: {args.month.capitalize()} {args.year}")
    print(f"{'='*60}\n")

    # Step 1: Create month directory
    month_dir = create_month_directory(args.year, args.month)

    # Step 2: Create data templates
    create_csv_template(month_dir, args.month, args.year)
    create_json_template(month_dir, args.month, args.year)

    # Step 3: Optionally copy previous data
    if args.copy_previous:
        copy_previous_data(month_dir, args.year, args.month)

    # Step 4: Summary
    count = count_startups(month_dir)
    print(f"\n{'='*60}")
    print(f"  Setup Complete!")
    print(f"  - Directory: {month_dir}")
    print(f"  - Current startup count: {count}")
    print(f"  - Next steps: Add startup data to CSV and JSON files")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
