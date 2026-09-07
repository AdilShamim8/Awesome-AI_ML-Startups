#!/usr/bin/env python3
"""Data Validation Script (v2) for Awesome AI/ML Startups.

v2 changes vs v1:
- Fixes the false "Duplicate IDs" bug (v1 compared per-file unique IDs against a
  cumulative counter shared across all files).
- Validates the canonical master dataset (schema v2) with controlled vocabularies.
- Validates monthly snapshots in two modes: legacy (Jan 2026 - Aug 2026, warnings
  only) and strict (schema v2 snapshots generated from master).
- Cross-checks: CSV/JSON parity, snapshot-vs-master consistency, stats.json sums.

Usage:
    python scripts/validate_data.py                     # validate everything
    python scripts/validate_data.py --master            # master only
    python scripts/validate_data.py --year 2026 --month september
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
MASTER_PATH = DATA_DIR / "master" / "startups_master.json"

# ---- controlled vocabularies (schema v2) ------------------------------------
VALID_CATEGORIES = {
    "AI/ML", "Generative AI", "AI Agents", "SaaS", "DevTools",
    "FinTech", "HealthTech", "Robotics", "Cybersecurity", "EdTech",
}
VALID_STAGES = {
    "Pre-Seed", "Seed", "Series A", "Series B", "Series C", "Series D",
    "Series E", "Series F", "Series G", "Series H", "Series I", "Series J",
    "Series K", "Late Stage", "IPO", "Bootstrapped", "Series Unknown",
}
VALID_STATUS = {"active", "acquired", "pending_acquisition", "majority_acquired", "public"}
VALID_VERIFICATION = {"verified", "partial", "unverified"}
VALID_REGIONS = {"North America", "Europe", "Middle East", "Asia-Pacific", "Africa", "Latin America", "Other"}

V2_REQUIRED_FIELDS = [
    "id", "slug", "startup_name", "about", "description", "website",
    "category", "subcategory", "funding_stage", "funding_amount",
    "funding_amount_usd", "valuation_display", "valuation_usd",
    "total_raised_display", "last_round_date", "investors",
    "headquarters", "city", "country", "region", "founded_year",
    "status", "status_note", "source", "source_urls", "date_added",
    "last_updated", "last_verified", "verification_status", "tags", "notes",
]

# fields that legitimately hold null/empty values
NULLABLE_FIELDS = {
    "funding_amount_usd", "valuation_display", "valuation_usd",
    "total_raised_display", "last_round_date", "status_note", "notes",
}

LEGACY_REQUIRED_FIELDS = [
    "id", "startup_name", "about", "description", "website",
    "category", "funding_stage", "funding_amount", "headquarters",
    "founded_year", "source", "date_added",
]

# snapshots from September 2026 onward are generated from master (strict mode)
STRICT_SNAPSHOT_MONTHS = {"september", "october", "november", "december"}

URL_PATTERN = re.compile(r"^https?://[^\s<>\"']+\.[^\s<>\"']+$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.startups_validated = 0
        self.files_validated = 0

    def error(self, file, subject, message):
        self.errors.append(f"[{file}] {subject}: {message}")

    def warn(self, file, subject, message):
        self.warnings.append(f"[{file}] {subject}: {message}")

    @property
    def ok(self):
        return not self.errors

    def report(self):
        print(f"\n{'=' * 60}")
        print("  Validation Report (v2)")
        print(f"{'=' * 60}")
        print(f"  Files validated: {self.files_validated}")
        print(f"  Startups validated: {self.startups_validated}")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        if self.errors:
            print("\n  ERRORS:")
            for e in self.errors[:60]:
                print(f"    - {e}")
            if len(self.errors) > 60:
                print(f"    ... and {len(self.errors) - 60} more")
        if self.warnings:
            print("\n  WARNINGS:")
            for w in self.warnings[:30]:
                print(f"    - {w}")
            if len(self.warnings) > 30:
                print(f"    ... and {len(self.warnings) - 30} more")
        if self.ok and not self.warnings:
            print("\n  All data is valid!")
        elif self.ok:
            print("\n  PASS (with warnings)")
        print(f"{'=' * 60}\n")
        return self.ok


def _check_url(value, file, subject, result, level="error"):
    if value and not URL_PATTERN.match(value):
        (result.error if level == "error" else result.warn)(file, subject, f"Invalid URL format: '{value}'")


def _check_date(value, file, subject, result, level="error"):
    if value and not DATE_PATTERN.match(str(value)):
        (result.error if level == "error" else result.warn)(file, subject, f"Invalid date format: '{value}'")


def validate_v2_record(rec, file, result, seen_ids, seen_slugs):
    sid = str(rec.get("id") or rec.get("slug") or "UNKNOWN")
    result.startups_validated += 1
    rid = str(rec.get("id", ""))
    slug = str(rec.get("slug", ""))

    for field in V2_REQUIRED_FIELDS:
        if field not in rec:
            result.error(file, sid, f"Missing required field: {field}")

    if rid in seen_ids:
        result.error(file, sid, f"Duplicate id: {rid}")
    seen_ids.add(rid)
    if slug and slug in seen_slugs:
        result.error(file, sid, f"Duplicate slug: {slug}")
    seen_slugs.add(slug)

    if rec.get("category") not in VALID_CATEGORIES:
        result.error(file, sid, f"Invalid category: '{rec.get('category')}'")
    if rec.get("funding_stage") not in VALID_STAGES:
        result.error(file, sid, f"Invalid funding_stage: '{rec.get('funding_stage')}'")
    if rec.get("status") not in VALID_STATUS:
        result.error(file, sid, f"Invalid status: '{rec.get('status')}'")
    if rec.get("verification_status") not in VALID_VERIFICATION:
        result.error(file, sid, f"Invalid verification_status: '{rec.get('verification_status')}'")
    if rec.get("region") not in VALID_REGIONS:
        result.warn(file, sid, f"Unexpected region: '{rec.get('region')}'")

    _check_url(rec.get("website"), file, sid, result)
    _check_date(rec.get("date_added"), file, sid, result)
    _check_date(rec.get("last_updated"), file, sid, result)
    _check_date(rec.get("last_verified"), file, sid, result)
    _check_date(rec.get("last_round_date"), file, sid, result, level="warn")

    fy = rec.get("founded_year")
    if not (isinstance(fy, int) and 1990 <= fy <= 2026):
        result.warn(file, sid, f"Unusual founded_year: {fy}")

    for i, url in enumerate(rec.get("source_urls") or []):
        _check_url(url, file, f"{sid}#src{i}", result, level="warn")

    # numeric consistency
    fau = rec.get("funding_amount_usd")
    if fau is not None and not isinstance(fau, (int, float)):
        result.error(file, sid, "funding_amount_usd must be numeric or null")
    vu = rec.get("valuation_usd")
    if vu is not None and not isinstance(vu, (int, float)):
        result.error(file, sid, "valuation_usd must be numeric or null")


def validate_master(result):
    result.files_validated += 1
    if not MASTER_PATH.exists():
        result.error(str(MASTER_PATH), "MASTER", "Master dataset not found")
        return None
    with open(MASTER_PATH, encoding="utf-8") as f:
        master = json.load(f)

    meta = master.get("metadata") or {}
    if meta.get("schema_version") != "2.0":
        result.error(str(MASTER_PATH), "METADATA", "schema_version must be 2.0")
    if meta.get("total_startups") != len(master.get("startups", [])):
        result.error(str(MASTER_PATH), "METADATA", "metadata.total_startups mismatch")

    seen_ids, seen_slugs = set(), set()
    for rec in master.get("startups", []):
        validate_v2_record(rec, str(MASTER_PATH), result, seen_ids, seen_slugs)
    return master


def _snapshot_mode(month_dir: Path) -> str:
    """strict for snapshots generated from master; legacy otherwise."""
    month = month_dir.name.lower()
    year = int(month_dir.parent.name)
    if year > 2026 or (year == 2026 and month in STRICT_SNAPSHOT_MONTHS):
        return "strict"
    return "legacy"


def validate_month_dir(month_dir: Path, result, master=None):
    mode = _snapshot_mode(month_dir)
    rel = str(month_dir.relative_to(REPO_ROOT))

    csv_rows = []
    json_data = None

    for csv_file in sorted(month_dir.glob("*.csv")):
        result.files_validated += 1
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            if mode == "strict":
                missing = set(V2_REQUIRED_FIELDS) - set(headers)
                if missing:
                    result.error(str(csv_file), "HEADER", f"Missing v2 headers: {sorted(missing)}")
            else:
                missing = set(LEGACY_REQUIRED_FIELDS) - set(headers)
                if missing:
                    result.warn(str(csv_file), "HEADER", f"Legacy file missing headers: {sorted(missing)}")
            local_ids = set()
            rows = 0
            for row in reader:
                rows += 1
                csv_rows.append(row)
                rid = row.get("id", "")
                if rid in local_ids:
                    (result.error if mode == "strict" else result.warn)(
                        str(csv_file), rid, "Duplicate id within file")
                local_ids.add(rid)
                for field in (V2_REQUIRED_FIELDS if mode == "strict" else LEGACY_REQUIRED_FIELDS):
                    if field in NULLABLE_FIELDS:
                        if field not in headers:
                            (result.error if mode == "strict" else result.warn)(
                                str(csv_file), rid, f"Missing nullable column: {field}")
                        continue
                    if not (row.get(field) or "").strip():
                        (result.error if mode == "strict" else result.warn)(
                            str(csv_file), rid, f"Missing field: {field}")
                if mode == "strict":
                    if row.get("category") not in VALID_CATEGORIES:
                        result.error(str(csv_file), rid, f"Invalid category: '{row.get('category')}'")
                    if row.get("funding_stage") not in VALID_STAGES:
                        result.error(str(csv_file), rid, f"Invalid funding_stage: '{row.get('funding_stage')}'")
                    if row.get("verification_status") not in VALID_VERIFICATION:
                        result.error(str(csv_file), rid, f"Invalid verification_status: '{row.get('verification_status')}'")
                    if row.get("status") not in VALID_STATUS:
                        result.error(str(csv_file), rid, f"Invalid status: '{row.get('status')}'")
                    _check_url(row.get("website"), str(csv_file), rid, result)
                    for d in ("date_added", "last_updated", "last_verified"):
                        _check_date(row.get(d), str(csv_file), rid, result)
                else:
                    if row.get("category") and row["category"] not in VALID_CATEGORIES:
                        result.warn(str(csv_file), rid, f"Legacy category: '{row['category']}'")
                    if row.get("funding_stage") and row["funding_stage"] not in VALID_STAGES:
                        result.warn(str(csv_file), rid, f"Legacy funding_stage: '{row['funding_stage']}'")
                    _check_url(row.get("website"), str(csv_file), rid, result, level="warn")
                    _check_date(row.get("date_added"), str(csv_file), rid, result, level="warn")
            result.startups_validated += rows

    for json_file in sorted(month_dir.glob("startups_*.json")):
        result.files_validated += 1
        try:
            with open(json_file, encoding="utf-8") as f:
                json_data = json.load(f)
        except json.JSONDecodeError as e:
            result.error(str(json_file), "JSON", f"Invalid JSON: {e}")
            continue

        startups = json_data.get("startups", [])
        meta = json_data.get("metadata") or {}
        if meta.get("total_startups") not in (None, len(startups)):
            result.error(str(json_file), "METADATA", "metadata.total_startups mismatch")
        seen_ids, seen_slugs = set(), set()
        for s in startups:
            if mode == "strict":
                # validate_v2_record handles id/slug dedup + startup count
                validate_v2_record(s, str(json_file), result, seen_ids, seen_slugs)
            else:
                result.startups_validated += 1
                sid = str(s.get("id", "UNKNOWN"))
                if sid in seen_ids:
                    result.warn(str(json_file), sid, "Legacy file: duplicate id")
                seen_ids.add(sid)
                for field in LEGACY_REQUIRED_FIELDS:
                    if field not in s or not str(s.get(field) or "").strip():
                        result.warn(str(json_file), sid, f"Legacy file missing field: {field}")

    # CSV/JSON parity
    if csv_rows and json_data is not None:
        csv_names = [r.get("startup_name") for r in csv_rows]
        json_names = [s.get("startup_name") for s in json_data.get("startups", [])]
        if sorted(csv_names) != sorted(json_names):
            (result.error if mode == "strict" else result.warn)(
                rel, "PARITY", "CSV and JSON startup lists differ")

    # strict snapshot must be a subset of master
    if mode == "strict" and master is not None and json_data is not None:
        master_slugs = {s["slug"] for s in master["startups"]}
        snap = json_data.get("startups", [])
        missing = [s.get("slug") for s in snap if s.get("slug") not in master_slugs]
        if missing:
            result.error(rel, "MASTER-SYNC", f"Snapshot entries not in master: {missing[:10]}")
        if len(snap) != len(master["startups"]):
            result.warn(rel, "MASTER-SYNC",
                        f"Snapshot has {len(snap)} entries vs master {len(master['startups'])}")

    # stats.json consistency
    stats_file = month_dir / "stats.json"
    if stats_file.exists():
        result.files_validated += 1
        with open(stats_file, encoding="utf-8") as f:
            stats = json.load(f)
        total = stats.get("total_startups")
        if total is not None and json_data is not None and total != len(json_data.get("startups", [])):
            result.error(str(stats_file), "STATS", f"total_startups={total} != JSON count")
        cat_sum = sum(stats.get("categories", {}).values())
        stage_sum = sum(stats.get("funding_stages", {}).values())
        if total is not None:
            if cat_sum and cat_sum != total:
                result.error(str(stats_file), "STATS", f"Category sum {cat_sum} != total {total}")
            if stage_sum and stage_sum != total:
                result.error(str(stats_file), "STATS", f"Stage sum {stage_sum} != total {total}")
        # duplicate keys cannot occur in json.loads (last wins) — detect via raw text
        raw = stats_file.read_text()
        for key in sorted(set(re.findall(r'"(Series [A-K])":', raw))):
            if raw.count(f'"{key}"') > 1:
                (result.error if mode == "strict" else result.error)(
                    str(stats_file), "STATS", f"Duplicate key in stats.json: {key}")


def validate_all(result, master=None, only=None):
    for year_dir in sorted(DATA_DIR.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            if only and (year_dir.name, month_dir.name) != only:
                continue
            print(f"  Validating: {month_dir.relative_to(REPO_ROOT)} ({_snapshot_mode(month_dir)})")
            validate_month_dir(month_dir, result, master)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", action="store_true", help="validate master dataset only")
    ap.add_argument("--year", type=int)
    ap.add_argument("--month")
    args = ap.parse_args()

    print(f"\n{'=' * 60}")
    print("  Data Validation (v2) - Awesome AI/ML Startups")
    print(f"{'=' * 60}\n")

    result = ValidationResult()
    master = None
    if not (args.year and args.month):
        print("  Validating: data/master/startups_master.json")
        master = validate_master(result)

    if args.master:
        ok = result.report()
        sys.exit(0 if ok else 1)

    only = (str(args.year), args.month.lower()) if (args.year and args.month) else None
    validate_all(result, master, only)

    ok = result.report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
