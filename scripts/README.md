# Pipeline Scripts

The repository is built around one canonical dataset and a set of
deterministic generators. **Never hand-edit generated files** — edit the
canonical JSON, run the generator, commit both.

## Canonical files (edit these)

| File | Contents |
|------|----------|
| `data/master/startups_master.json` | The company registry (schema v2, 31 fields per company) |
| `data/master/funding_rounds.json`  | The event-level funding history (one row per round) |

## Generators (run after editing the canonical files)

| Script | What it does |
|--------|--------------|
| `build_master_csv.py` | Rewrites `startups_master.csv` from the JSON. `--check` exits 1 on drift. |
| `build_funding_rounds_csv.py` | Rewrites `funding_rounds.csv` from the JSON; derives a clean `source_domain` column. `--check` exits 1 on drift. |
| `build_snapshots.py` | Builds `data/<year>/<month>/` (CSV + JSON + stats.json) from the master. `--date YYYY-MM-DD` publishes a **pre-month-end research snapshot** (stamped in metadata + stats) instead of the regular month-end snapshot. |
| `build_categories.py` | Regenerates the ten `categories/*.md` pages from the master, with curated spotlights/trends from `CATEGORY_INSIGHTS`. |
| `generate_readme.py` | Prints dataset statistics for release notes. |
| `site/build_site_data.py` | Derives `site/site_data.json` (the explorer payload) from the canonical master + funding data. |
| `site/build_site.py` | Assembles the self-contained `index.html` at the repo root from `site/parts/` + the payload. |

## Verification

| Script | What it checks |
|--------|----------------|
| `validate_data.py` | Full validation: schema v2, controlled vocabularies, id/slug uniqueness, duplicate events, master/rounds CSV parity, coverage honesty, cutoff enforcement, registry name-variant + staleness cross-checks, category-page consistency, evidence-log coverage, snapshot-vs-master sync, stats sums. |
| `verify_readme_stats.py` | Recomputes every README headline figure from the canonical data and fails on drift. `--report` prints the computed stats. |
| `check_links.py` | Liveness check of all registry websites (and `--check-sources` for source URLs). HTTP 403/429 are classified **bot-blocked**, not dead, and do not fail the run. |
| `site/audit_site.py` | Recomputes the 59 headline figures shown in `index.html` and fails if the published page disagrees with the canonical data. Runs in CI on every push. |

## Tests

```bash
python -m unittest discover -s tests   # 39 tests; pytest-compatible
```

Covers the validator (vocabularies, required fields, duplicates, URL/date
formats, name normalization), the CSV generators (roundtrip fidelity,
serialization conventions, domain derivation), link classification, and
the snapshot date helpers — plus integration tests against the live
repository data.

## The monthly workflow

See `update_monthly.py --month <month> --year <year>` for the checklist,
`CONTRIBUTING.md` for the evidence standards, and
`.github/workflows/monthly-reminder.yml` for the scheduled reminder
(fires on the 28th, ahead of the 30th publication date).

## Conventions that keep the data honest

- Rounds must be **closed** — talks-stage items go in `notes`, not events
- `funding_amount` is money raised; valuations live in `valuation_*`
- Tenders and debt are secondary context, never `funding_amount`
- Month-precision dates use the month end and say so in `notes`
- Events beyond `metadata.cutoff` fail validation
- `last_verified` is the date a human actually checked the sources
