#!/usr/bin/env python3
"""Tests for the CSV sync generators and the link checker's classifier.

Run with:  python -m unittest discover -s tests -v
"""
import csv
import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_master_csv as bmc  # noqa: E402
import build_funding_rounds_csv as bfrc  # noqa: E402
import check_links as cl  # noqa: E402


class TestMasterCsvRoundtrip(unittest.TestCase):
    """Regenerating the CSV must reproduce the shipped file exactly."""

    def test_roundtrip_byte_identical(self):
        rows = bmc.build_rows()
        generated = bmc.MASTER_CSV.read_text(encoding="utf-8")
        # write to the same format in memory and compare values row by row
        with open(bmc.MASTER_CSV, encoding="utf-8") as f:
            existing = list(csv.DictReader(f))
        self.assertEqual(len(existing), len(rows))
        for old, new in zip(existing, rows):
            self.assertEqual({k: (v or "") for k, v in old.items()},
                             {k: str(v) for k, v in new.items()})

    def test_record_to_row_serialization(self):
        row = bmc.record_to_row({
            "id": "001", "slug": "x", "startup_name": "X", "about": "a",
            "description": "d", "website": "https://x.example",
            "category": "AI/ML", "subcategory": "s", "funding_stage": "Seed",
            "funding_amount": "$1M", "funding_amount_usd": 1000000,
            "valuation_display": None, "valuation_usd": None,
            "total_raised_display": None, "last_round_date": None,
            "investors": ["A", "B"], "headquarters": "h", "city": "c",
            "country": "USA", "region": "North America", "founded_year": 2020,
            "status": "active", "status_note": None, "source": "s",
            "source_urls": ["https://a.example", "https://b.example"],
            "date_added": "2026-01-01", "last_updated": "2026-01-01",
            "last_verified": "2026-01-01", "verification_status": "verified",
            "tags": ["t1", "t2"], "notes": None,
        })
        self.assertEqual(row["investors"], "A; B")
        self.assertEqual(row["tags"], "t1; t2")
        self.assertEqual(row["source_urls"], "https://a.example | https://b.example")
        self.assertEqual(row["valuation_display"], "")
        self.assertEqual(row["notes"], "")

    def test_csv_is_current_true_for_shipped_file(self):
        self.assertTrue(bmc.csv_is_current(bmc.build_rows()))


class TestFundingRoundsCsv(unittest.TestCase):
    def test_csv_is_current_true_for_shipped_file(self):
        self.assertTrue(bfrc.csv_is_current(bfrc.build_rows()))

    def test_derive_domain(self):
        self.assertEqual(bfrc.derive_domain("https://www.crusoe.ai/blog"), "crusoe.ai")
        self.assertEqual(bfrc.derive_domain("https://techcrunch.com/2026/x"), "techcrunch.com")
        self.assertEqual(bfrc.derive_domain("https://investor.capitalone.com"), "investor.capitalone.com")
        self.assertEqual(bfrc.derive_domain(""), "")
        self.assertEqual(bfrc.derive_domain(None), "")
        self.assertEqual(bfrc.derive_domain("https://a.example | https://b.example"), "a.example")

    def test_record_to_row_bool_and_none(self):
        row = bfrc.record_to_row({"event_id": "e1", "in_registry": True,
                                  "amount_usd_m": None, "notes": None,
                                  "source_urls": "https://x.example"})
        self.assertEqual(row["in_registry"], "True")
        self.assertEqual(row["amount_usd_m"], "")
        self.assertEqual(row["notes"], "")
        self.assertEqual(row["source_domain"], "x.example")


class TestLinkClassification(unittest.TestCase):
    def test_reachable(self):
        self.assertEqual(cl.classify(200), "reachable")
        self.assertEqual(cl.classify(301), "reachable")

    def test_bot_blocked(self):
        self.assertEqual(cl.classify(403), "bot_blocked")
        self.assertEqual(cl.classify(429), "bot_blocked")

    def test_failing(self):
        self.assertEqual(cl.classify(404), "failing")
        self.assertEqual(cl.classify(500), "failing")
        self.assertEqual(cl.classify("ERR:URLError"), "failing")
        self.assertEqual(cl.classify("ERR:TimeoutError"), "failing")


class TestSnapshotBuilderHelpers(unittest.TestCase):
    """The snapshot builder's month-end math and next-update logic."""

    def test_month_end(self):
        import build_snapshots as bs
        self.assertEqual(bs.month_end(2026, 10), "2026-10-31")
        self.assertEqual(bs.month_end(2026, 2), "2026-02-28")

    def test_next_update(self):
        import build_snapshots as bs
        self.assertEqual(bs._next_update(2026, 10), "2026-11-30")
        self.assertEqual(bs._next_update(2026, 12), "2027-01-30")


if __name__ == "__main__":
    unittest.main()
