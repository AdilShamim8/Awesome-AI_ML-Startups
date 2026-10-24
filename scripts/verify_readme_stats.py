#!/usr/bin/env python3
"""Verify that headline numbers in README.md match the actual dataset.

The README's statistics table is hand-written, which let it drift in the
past. This script recomputes every headline figure from
data/master/startups_master.json and data/master/funding_rounds.json and
checks that the same numbers appear in the README. Run it in CI or before
any release:

    python scripts/verify_readme_stats.py            # check README.md
    python scripts/verify_readme_stats.py --report   # print computed stats

Exit codes: 0 = README matches the data; 1 = drift detected (fix the README
or the data, not this script).
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
README = REPO_ROOT / "README.md"
MASTER = REPO_ROOT / "data" / "master" / "startups_master.json"
ROUNDS = REPO_ROOT / "data" / "master" / "funding_rounds.json"


def compute_stats():
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    startups = master["startups"]
    fr = json.loads(ROUNDS.read_text(encoding="utf-8"))
    rounds = fr["rounds"]

    verified_rounds = [r for r in rounds if r.get("verification_status") == "verified"]
    verified_capital_m = sum(r.get("amount_usd_m") or 0 for r in verified_rounds)
    mega = [r for r in rounds if (r.get("amount_usd_m") or 0) >= 100]
    events_2025 = [r for r in rounds if str(r.get("month") or "").startswith("2025")]
    events_2026 = [r for r in rounds if str(r.get("month") or "").startswith("2026")]
    cap25_m = sum(r.get("amount_usd_m") or 0 for r in events_2025 if r.get("verification_status") == "verified")
    cap26_m = sum(r.get("amount_usd_m") or 0 for r in events_2026 if r.get("verification_status") == "verified")
    uniq_companies = {r["startup_name"] for r in rounds}

    domains = set()
    for s in startups:
        for u in (s.get("source_urls") or []):
            m = re.match(r"https?://(?:www\.)?([^/]+)", u)
            if m:
                domains.add(m.group(1))

    return {
        "total_companies": len(startups),
        "total_events": len(rounds),
        "verified_capital_b": round(verified_capital_m / 1000, 1),
        "mega_rounds": len(mega),
        "events_2025": len(events_2025),
        "cap25_b": round(cap25_m / 1000, 1),
        "events_2026": len(events_2026),
        "cap26_b": round(cap26_m / 1000, 1),
        "verified": sum(1 for s in startups if s["verification_status"] == "verified"),
        "partial": sum(1 for s in startups if s["verification_status"] == "partial"),
        "unverified": sum(1 for s in startups if s["verification_status"] == "unverified"),
        "countries": len({s["country"] for s in startups}),
        "categories": len({s["category"] for s in startups}),
        "source_domains": len(domains),
        "unique_event_companies": len(uniq_companies),
        "founded_min": min(s["founded_year"] for s in startups),
        "founded_max": max(s["founded_year"] for s in startups),
        "as_of": master["metadata"]["as_of"],
    }


CHECKS = [
    # (stat key, README regex, description)
    ("total_companies", r"startups%20tracked-(\d+)-orange", "badge: startups tracked"),
    ("total_companies", r"\| Companies tracked \| (\d+) ", "table: companies tracked"),
    ("total_events", r"\| Funding events recorded \| (\d+) ", "table: funding events"),
    ("events_2025", r"\| 2025 events / confirmed capital \| (\d+) events", "table: 2025 events"),
    ("events_2026", r"\| 2026 events / confirmed capital \| (\d+) events", "table: 2026 events"),
    ("verified", r"\| Verified against primary \+ financial press \| (\d+) ", "table: verified"),
    ("partial", r"\| Single-source / estimate \(noted in `notes`\) \| (\d+) ", "table: partial"),
    ("unverified", r"\| Could not be confirmed \| (\d+) ", "table: unverified"),
    ("countries", r"\| Countries \| (\d+) ", "table: countries"),
    ("categories", r"\| Categories \| (\d+) ", "table: categories"),
    ("source_domains", r"\| Distinct source domains cited \| (\d+) ", "table: source domains"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="print computed stats only")
    args = ap.parse_args()

    stats = compute_stats()
    if args.report:
        for k, v in stats.items():
            print(f"  {k:26s} {v}")
        return 0

    text = README.read_text(encoding="utf-8")
    drift = []
    for key, pattern, desc in CHECKS:
        m = re.search(pattern, text)
        if not m:
            drift.append(f"README missing/changed: {desc} (pattern not found)")
            continue
        readme_val = int(m.group(1))
        if readme_val != stats[key]:
            drift.append(f"{desc}: README says {readme_val}, data says {stats[key]}")

    # capital figures appear as $X.XB strings
    m = re.search(r"\((\d+) events, \$(\d+(?:\.\d+)?)B confirmed capital\)", text)
    if not m:
        drift.append("README missing/changed: verified capital")
    else:
        if int(m.group(1)) != stats["total_events"]:
            drift.append(f"event count inline: README says {m.group(1)}, data says {stats['total_events']}")
        if abs(float(m.group(2)) - stats["verified_capital_b"]) > 0.05:
            drift.append(f"verified capital: README says ${m.group(2)}B, data says ${stats['verified_capital_b']}B")

    year_rows = re.findall(r"\| (\d{4}) events / confirmed capital \| (\d+) events · \$(\d+(?:\.\d+)?)B verified", text)
    for year_s, ev_s, cap_s in year_rows:
        year = int(year_s)
        ev_key = f"events_{year}"
        cap_key = f"cap{str(year)[2:]}_b"
        if year in (2025, 2026) and ev_key in stats:
            if int(ev_s) != stats[ev_key]:
                drift.append(f"{year} events: README says {ev_s}, data says {stats[ev_key]}")
            if abs(float(cap_s) - stats[cap_key]) > 0.05:
                drift.append(f"{year} verified capital: README says ${cap_s}B, data says ${stats[cap_key]}B")

    if drift:
        print("README STAT DRIFT DETECTED:")
        for d in drift:
            print(f"  - {d}")
        print("\nRecompute from the data (scripts/verify_readme_stats.py --report) and update README.md.")
        return 1
    print(f"OK: README headline stats match the dataset "
          f"({stats['total_companies']} companies, {stats['total_events']} events, "
          f"${stats['verified_capital_b']}B verified capital, as_of {stats['as_of']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
