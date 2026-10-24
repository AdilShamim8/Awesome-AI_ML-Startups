## Type of Change

- [ ] New startup added
- [ ] Existing data updated (funding round, valuation, status, correction)
- [ ] Funding event added to `data/master/funding_rounds.json`
- [ ] Error fix
- [ ] New category/source suggestion
- [ ] Pipeline/tooling improvement

## Startup Details (if adding or updating)

- **Name:**
- **Website:**
- **Category:**
- **Source(s):** (company announcement or financial press preferred; include URL and publication date)

## Evidence Checklist

- [ ] Source URL is dated and checkable (press release / financial press beats aggregators)
- [ ] Round is **closed**, not talks-stage ("reported" / "in talks" items belong in `notes`)
- [ ] `funding_amount` is money raised — not a valuation, not an acquisition price, not debt
- [ ] `valuation_display` / `valuation_usd` carry the worth, with the date of the mark
- [ ] `last_verified` is set to the date you actually checked
- [ ] Conflicting source figures (if any) are preserved in `notes`, not silently resolved

## Pipeline Checklist

- [ ] `data/master/startups_master.json` edited (canonical)
- [ ] `python scripts/build_master_csv.py` run (CSV mirror regenerated)
- [ ] `python scripts/build_funding_rounds_csv.py` run (if events changed)
- [ ] Snapshot / category pages regenerated (`build_snapshots.py`, `build_categories.py`)
- [ ] `python scripts/validate_data.py` passes locally
- [ ] `python -m unittest discover -s tests` passes locally

## Additional Notes

(Any context about this contribution)
