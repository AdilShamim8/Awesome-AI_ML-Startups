#!/usr/bin/env python3
"""Unit tests for the validation logic in scripts/validate_data.py.

Run with:  python -m unittest discover -s tests -v
   or:      python -m pytest tests/test_validate.py -v

The tests cover the pure validation functions (no repository files needed):
controlled vocabularies, required fields, duplicate detection, URL/date
formats, numeric checks, and the name-variant normalization used by the
registry cross-checks. An integration test at the end runs the real
validator entry points against the live repository data.
"""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_data as vd  # noqa: E402


def make_result():
    return vd.ValidationResult()


def valid_record(**overrides):
    """A schema-v2 record that passes all checks."""
    base = {
        "id": "999",
        "slug": "test-co",
        "startup_name": "Test Co",
        "about": "Does testing",
        "description": "Test Co does testing at scale.",
        "website": "https://example.com",
        "category": "AI/ML",
        "subcategory": "Testing",
        "funding_stage": "Series A",
        "funding_amount": "$10M",
        "funding_amount_usd": 10000000,
        "valuation_display": "$50M (2026)",
        "valuation_usd": 50000000,
        "total_raised_display": "$10M",
        "last_round_date": "2026-01-15",
        "investors": ["Test VC"],
        "headquarters": "Testville, USA",
        "city": "Testville",
        "country": "USA",
        "region": "North America",
        "founded_year": 2020,
        "status": "active",
        "status_note": None,
        "source": "Test Source",
        "source_urls": ["https://example.com/press"],
        "date_added": "2026-01-01",
        "last_updated": "2026-01-01",
        "last_verified": "2026-01-01",
        "verification_status": "verified",
        "tags": ["test"],
        "notes": None,
    }
    base.update(overrides)
    return base


class TestNameNormalization(unittest.TestCase):
    def test_strips_ai_suffix(self):
        self.assertEqual(vd._normalize_name("Perplexity AI"), vd._normalize_name("Perplexity"))
        self.assertEqual(vd._normalize_name("Cognition AI"), vd._normalize_name("Cognition"))

    def test_strips_legal_suffixes(self):
        self.assertEqual(vd._normalize_name("Acme Inc"), "acme")
        self.assertEqual(vd._normalize_name("Acme LLC"), "acme")

    def test_does_not_conflate_agi(self):
        # 'Maven AGI' and 'Maven' are different companies; must NOT match
        self.assertNotEqual(vd._normalize_name("Maven AGI"), vd._normalize_name("Maven"))

    def test_case_and_whitespace(self):
        self.assertEqual(vd._normalize_name("  OpenAI "), "openai")

    def test_empty(self):
        self.assertEqual(vd._normalize_name(""), "")


class TestRecordValidation(unittest.TestCase):
    def test_valid_record_passes(self):
        result = make_result()
        vd.validate_v2_record(valid_record(), "test.json", result, set(), set())
        self.assertEqual(result.errors, [])

    def test_missing_required_field_is_error(self):
        rec = valid_record()
        del rec["website"]
        result = make_result()
        vd.validate_v2_record(rec, "test.json", result, set(), set())
        self.assertTrue(any("Missing required field: website" in e for e in result.errors))

    def test_invalid_category_is_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(category="Quantum"), "t", result, set(), set())
        self.assertTrue(any("Invalid category" in e for e in result.errors))

    def test_invalid_stage_is_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(funding_stage="Mega Round"), "t", result, set(), set())
        self.assertTrue(any("Invalid funding_stage" in e for e in result.errors))

    def test_invalid_status_is_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(status="zombie"), "t", result, set(), set())
        self.assertTrue(any("Invalid status" in e for e in result.errors))

    def test_invalid_verification_is_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(verification_status="guessed"), "t", result, set(), set())
        self.assertTrue(any("Invalid verification_status" in e for e in result.errors))

    def test_duplicate_id_is_error(self):
        result = make_result()
        seen_ids, seen_slugs = set(), set()
        vd.validate_v2_record(valid_record(), "t", result, seen_ids, seen_slugs)
        vd.validate_v2_record(valid_record(slug="other-co"), "t", result, seen_ids, seen_slugs)
        self.assertTrue(any("Duplicate id" in e for e in result.errors))

    def test_duplicate_slug_is_error(self):
        result = make_result()
        seen_ids, seen_slugs = set(), set()
        vd.validate_v2_record(valid_record(), "t", result, seen_ids, seen_slugs)
        vd.validate_v2_record(valid_record(id="998"), "t", result, seen_ids, seen_slugs)
        self.assertTrue(any("Duplicate slug" in e for e in result.errors))

    def test_bad_url_is_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(website="not-a-url"), "t", result, set(), set())
        self.assertTrue(any("Invalid URL format" in e for e in result.errors))

    def test_bad_date_is_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(date_added="2026/01/01"), "t", result, set(), set())
        self.assertTrue(any("Invalid date format" in e for e in result.errors))

    def test_non_numeric_funding_is_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(funding_amount_usd="lots"), "t", result, set(), set())
        self.assertTrue(any("funding_amount_usd must be numeric" in e for e in result.errors))

    def test_outlier_founded_year_is_warning_not_error(self):
        result = make_result()
        vd.validate_v2_record(valid_record(founded_year=1800), "t", result, set(), set())
        self.assertEqual(result.errors, [])
        self.assertTrue(any("Unusual founded_year" in w for w in result.warnings))


class TestUrlAndDateHelpers(unittest.TestCase):
    def test_check_url_accepts_valid(self):
        result = make_result()
        vd._check_url("https://example.com/path?x=1", "f", "s", result)
        self.assertEqual(result.errors, [])

    def test_check_url_rejects_garbage(self):
        result = make_result()
        vd._check_url("htp:/bad url", "f", "s", result)
        self.assertEqual(len(result.errors), 1)

    def test_check_date_accepts_iso(self):
        result = make_result()
        vd._check_date("2026-10-24", "f", "s", result)
        self.assertEqual(result.errors, [])

    def test_check_date_rejects_slashes(self):
        result = make_result()
        vd._check_date("10/24/2026", "f", "s", result)
        self.assertEqual(len(result.errors), 1)

    def test_check_date_ignores_none(self):
        result = make_result()
        vd._check_date(None, "f", "s", result)
        self.assertEqual(result.errors, [])


class TestValidationResultContract(unittest.TestCase):
    def test_ok_property(self):
        result = make_result()
        self.assertTrue(result.ok)
        result.error("f", "s", "boom")
        self.assertFalse(result.ok)

    def test_report_returns_ok(self):
        result = make_result()
        self.assertTrue(result.report())
        result.error("f", "s", "boom")
        self.assertFalse(result.report())


class TestLiveRepositoryIntegration(unittest.TestCase):
    """The shipped repository data must pass validation with zero errors."""

    def test_master_validates(self):
        result = make_result()
        master = vd.validate_master(result)
        self.assertIsNotNone(master)
        self.assertEqual(result.errors, [])

    def test_rounds_validate(self):
        result = make_result()
        master = vd.validate_master(make_result())
        vd.validate_rounds(result, master)
        self.assertEqual(result.errors, [])

    def test_master_csv_in_sync(self):
        result = make_result()
        vd.validate_master_csv_parity(result)
        self.assertEqual(result.errors, [])

    def test_rounds_csv_in_sync(self):
        result = make_result()
        vd.validate_rounds_csv_parity(result)
        self.assertEqual(result.errors, [])


if __name__ == "__main__":
    unittest.main()
