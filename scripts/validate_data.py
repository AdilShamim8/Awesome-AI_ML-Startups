#!/usr/bin/env python3
"""
Data Validation Script for Awesome AI/ML Startups Repository.

This script validates all data files in the repository:
1. Checks CSV and JSON schema compliance
2. Verifies required fields are present
3. Checks for duplicate entries
4. Validates website URL format
5. Verifies category names
6. Reports statistics and issues

Usage:
    python validate_data.py
    python validate_data.py --year 2026 --month may
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"

VALID_CATEGORIES = {
    "AI/ML", "Generative AI", "AI Agents", "SaaS", "DevTools",
    "FinTech", "HealthTech", "Robotics", "Robotics / Defense",
    "Robotics / AI", "Cybersecurity", "EdTech"
}

VALID_FUNDING_STAGES = {
    "Pre-Seed", "Seed", "Series A", "Series B", "Series C",
    "Series D", "Series E", "Series F", "Late Stage", "IPO"
}

REQUIRED_FIELDS = [
    "id", "startup_name", "about", "description", "website",
    "category", "funding_stage", "funding_amount", "headquarters",
    "founded_year", "source", "date_added"
]

URL_PATTERN = re.compile(r"^https?://[^\s<>\"']+\.[^\s<>\"']+$")


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.startups_validated = 0
        self.files_validated = 0

    def add_error(self, file: str, startup_id: str, message: str):
        self.errors.append(f"[{file}] Startup #{startup_id}: {message}")

    def add_warning(self, file: str, startup_id: str, message: str):
        self.warnings.append(f"[{file}] Startup #{startup_id}: {message}")

    def report(self):
        print(f"\n{'='*60}")
        print(f"  Validation Report")
        print(f"{'='*60}")
        print(f"  Files validated: {self.files_validated}")
        print(f"  Startups validated: {self.startups_validated}")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")

        if self.errors:
            print(f"\n  ❌ ERRORS:")
            for error in self.errors:
                print(f"    - {error}")

        if self.warnings:
            print(f"\n  ⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"    - {warning}")

        if not self.errors and not self.warnings:
            print(f"\n  ✅ All data is valid!")

        print(f"{'='*60}\n")
        return len(self.errors) == 0


def validate_csv(csv_path: Path, result: ValidationResult) -> None:
    """Validate a CSV data file."""
    result.files_validated += 1

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Check headers
        headers = reader.fieldnames
        if not headers:
            result.add_error(str(csv_path), "HEADER", "Missing CSV headers")
            return

        missing_headers = set(REQUIRED_FIELDS) - set(headers)
        if missing_headers:
            result.add_error(
                str(csv_path), "HEADER",
                f"Missing required headers: {missing_headers}"
            )

        ids_seen = set()

        for row in reader:
            result.startups_validated += 1
            startup_id = row.get("id", "UNKNOWN")
            ids_seen.add(startup_id)

            # Check required fields
            for field in REQUIRED_FIELDS:
                if not row.get(field, "").strip():
                    result.add_error(
                        str(csv_path), startup_id,
                        f"Missing required field: {field}"
                    )

            # Validate category
            category = row.get("category", "").strip()
            if category and category not in VALID_CATEGORIES:
                result.add_warning(
                    str(csv_path), startup_id,
                    f"Unusual category: '{category}' (not in standard list)"
                )

            # Validate funding stage
            stage = row.get("funding_stage", "").strip()
            if stage and stage not in VALID_FUNDING_STAGES:
                result.add_warning(
                    str(csv_path), startup_id,
                    f"Unusual funding stage: '{stage}'"
                )

            # Validate URL
            website = row.get("website", "").strip()
            if website and not URL_PATTERN.match(website):
                result.add_error(
                    str(csv_path), startup_id,
                    f"Invalid URL format: '{website}'"
                )

            # Validate date format
            date_added = row.get("date_added", "").strip()
            if date_added and not re.match(r"^\d{4}-\d{2}-\d{2}$", date_added):
                result.add_error(
                    str(csv_path), startup_id,
                    f"Invalid date format: '{date_added}' (expected YYYY-MM-DD)"
                )

        # Check for duplicate IDs
        if len(ids_seen) != result.startups_validated:
            result.add_error(
                str(csv_path), "GLOBAL",
                "Duplicate IDs detected in CSV file"
            )


def validate_json(json_path: Path, result: ValidationResult) -> None:
    """Validate a JSON data file."""
    result.files_validated += 1

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check metadata
    metadata = data.get("metadata", {})
    if not metadata:
        result.add_error(str(json_path), "METADATA", "Missing metadata section")

    startups = data.get("startups", [])
    ids_seen = set()

    for startup in startups:
        result.startups_validated += 1
        startup_id = startup.get("id", "UNKNOWN")
        ids_seen.add(startup_id)

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in startup or not str(startup[field]).strip():
                result.add_error(
                    str(json_path), startup_id,
                    f"Missing required field: {field}"
                )

        # Validate category
        category = startup.get("category", "").strip()
        if category and category not in VALID_CATEGORIES:
            result.add_warning(
                str(json_path), startup_id,
                f"Unusual category: '{category}'"
            )

        # Validate funding stage
        stage = startup.get("funding_stage", "").strip()
        if stage and stage not in VALID_FUNDING_STAGES:
            result.add_warning(
                str(json_path), startup_id,
                f"Unusual funding stage: '{stage}'"
            )

        # Validate URL
        website = startup.get("website", "").strip()
        if website and not URL_PATTERN.match(website):
            result.add_error(
                str(json_path), startup_id,
                f"Invalid URL format: '{website}'"
            )

    # Check for duplicate IDs
    if len(ids_seen) != len(startups):
        result.add_error(
            str(json_path), "GLOBAL",
            "Duplicate IDs detected in JSON file"
        )


def validate_all(result: ValidationResult) -> None:
    """Validate all data files in the repository."""
    for year_dir in sorted(DATA_DIR.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue

        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue

            # Validate CSV files
            for csv_file in month_dir.glob("*.csv"):
                print(f"  Validating: {csv_file.relative_to(REPO_ROOT)}")
                validate_csv(csv_file, result)

            # Validate JSON files (skip stats.json and other non-startup files)
            for json_file in month_dir.glob("startups_*.json"):
                print(f"  Validating: {json_file.relative_to(REPO_ROOT)}")
                validate_json(json_file, result)


def validate_specific(year: int, month: str, result: ValidationResult) -> None:
    """Validate a specific month's data."""
    month_dir = DATA_DIR / str(year) / month.lower()
    if not month_dir.exists():
        print(f"  ❌ Directory not found: {month_dir}")
        return

    for csv_file in month_dir.glob("*.csv"):
        print(f"  Validating: {csv_file.relative_to(REPO_ROOT)}")
        validate_csv(csv_file, result)

    for json_file in month_dir.glob("startups_*.json"):
        print(f"  Validating: {json_file.relative_to(REPO_ROOT)}")
        validate_json(json_file, result)


def main():
    parser = argparse.ArgumentParser(
        description="Validate startup data files"
    )
    parser.add_argument(
        "--year", type=int,
        help="Specific year to validate (e.g., 2026)"
    )
    parser.add_argument(
        "--month",
        help="Specific month to validate (e.g., may)"
    )

    args = parser.parse_args()
    result = ValidationResult()

    print(f"\n{'='*60}")
    print(f"  Data Validation - Awesome AI/ML Startups")
    print(f"{'='*60}\n")

    if args.year and args.month:
        validate_specific(args.year, args.month, result)
    else:
        validate_all(result)

    is_valid = result.report()
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
