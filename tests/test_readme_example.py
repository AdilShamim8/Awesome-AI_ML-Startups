#!/usr/bin/env python3
"""Integration test: the README's 'Using the data' example must actually work.

The README promises that pandas users can sort, filter, and slice the master
CSV. If a schema change ever breaks that promise, this test fails before the
change ships.

Run with:  python -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:  # pragma: no cover - CI installs nothing extra; pandas is present
    HAS_PANDAS = False


@unittest.skipUnless(HAS_PANDAS, "pandas not installed")
class TestReadmeUsageExample(unittest.TestCase):
    CSV = REPO_ROOT / "data" / "master" / "startups_master.csv"

    def setUp(self):
        self.df = pd.read_csv(self.CSV)

    def test_loads_with_expected_shape(self):
        self.assertGreater(len(self.df), 100)
        for col in ("startup_name", "funding_stage", "funding_amount_usd",
                    "valuation_usd", "region", "verification_status"):
            self.assertIn(col, self.df.columns)

    def test_biggest_rounds_sort_works(self):
        top = self.df.nlargest(10, "funding_amount_usd")[
            ["startup_name", "funding_stage", "funding_amount_usd", "valuation_usd"]]
        self.assertEqual(len(top), 10)
        self.assertGreater(top["funding_amount_usd"].iloc[0], 1e11)  # OpenAI $122B

    def test_europe_filter_works(self):
        eu = self.df[self.df.region == "Europe"].sort_values(
            "funding_amount_usd", ascending=False)
        self.assertGreater(len(eu), 10)
        for region in eu["region"]:
            self.assertEqual(region, "Europe")

    def test_verified_only_filter_works(self):
        safe = self.df[self.df.verification_status == "verified"]
        self.assertGreater(len(safe), 50)

    def test_new_region_asia_pacific_present(self):
        apac = self.df[self.df.region == "Asia-Pacific"]
        self.assertEqual(len(apac), 7)


if __name__ == "__main__":
    unittest.main()
