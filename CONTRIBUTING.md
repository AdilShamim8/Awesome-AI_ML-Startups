# 🤝 Contributing to Awesome AI/ML Startups

First off, thank you for considering contributing to this project! 🎉 This repository thrives because of community contributions like yours.

## 🌟 Ways to Contribute

### 1. Add a New Startup

This is the most valuable contribution! If you know of an AI/ML or tech startup that should be listed:

1. **Fork** this repository
2. **Edit the canonical master dataset** — `data/master/startups_master.json` — adding one entry. One row per company: check the `slug` list first, duplicates fail CI
3. **Regenerate the CSV mirror** — `python scripts/build_master_csv.py` (never hand-edit the CSV; CI verifies it matches the JSON)
4. **Regenerate** the snapshot and category pages:
   ```bash
   python scripts/build_snapshots.py --month october --year 2026            # month-end snapshot
   python scripts/build_snapshots.py --month october --year 2026 --date 2026-10-24  # pre-month-end research snapshot
   python scripts/build_categories.py
   ```
5. **Validate** locally: `python scripts/validate_data.py` and `python -m unittest discover -s tests`
6. **Submit** a Pull Request with the title: `Add [Startup Name] - [Month Year]` — CI runs the validator, CSV parity checks, and tests automatically

> See `scripts/update_monthly.py` for the full monthly checklist.

### 2. Update Existing Data

If a startup has new funding, changed categories, or updated descriptions:

1. **Fork** this repository
2. **Update the entry in the master dataset** — refresh `funding_stage`, `funding_amount`, `valuation_*`, `last_round_date`, `last_updated`, and bump `last_verified` (with source URLs)
3. **Add the funding event** to `data/master/funding_rounds.json` if a round closed (one row per round; respect `metadata.cutoff` — events beyond it fail validation), then regenerate with `python scripts/build_funding_rounds_csv.py`
4. **Regenerate** the CSV mirror, snapshots, and category pages, then validate
5. **Submit** a Pull Request with the title: `Update [Startup Name] - [Field Changed]`

### 3. Fix Errors

Found a broken link, incorrect data, or typo? We appreciate fixes!

1. **Fork** this repository
2. **Fix the error in the master dataset** (not in generated files) and regenerate
3. **Submit** a Pull Request with the title: `Fix [Description]`

### 4. Suggest New Categories or Sources

Open an [Issue](https://github.com/your-username/awesome-ai-ml-startups/issues) with:
- The proposed category name and description
- OR the new data source with URL and relevance

---

## 📋 Data Schema Requirements

When adding a startup, use this exact schema:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | 3-digit unique ID (e.g., "061") |
| `startup_name` | string | ✅ | Official company name |
| `about` | string | ✅ | Short tagline (1 line, under 100 chars) |
| `description` | string | ✅ | Detailed description (2-3 sentences) |
| `website` | URL | ✅ | Working direct link to the startup |
| `category` | string | ✅ | One of the defined categories |
| `funding_stage` | string | ✅ | Latest known funding stage |
| `funding_amount` | string | ✅ | Latest known funding amount |
| `headquarters` | string | ✅ | City, Country |
| `founded_year` | integer | ✅ | Year the company was founded |
| `source` | string | ✅ | Where you found the data |
| `date_added` | date | ✅ | YYYY-MM-DD format |

### Valid Categories

- `AI/ML` — Core AI & machine learning platforms
- `Generative AI` — LLMs, image gen, video gen, creative AI
- `AI Agents` — Autonomous AI agents & agentic systems
- `SaaS` — AI-powered SaaS products
- `DevTools` — Developer tools & infrastructure
- `FinTech` — AI-driven financial technology
- `HealthTech` — AI in healthcare & biotech
- `Robotics` — AI robotics & autonomous systems
- `Cybersecurity` — AI security & threat detection
- `EdTech` — AI in education & learning

### Valid Funding Stages

- `Pre-Seed`, `Seed`, `Series A` … `Series K`
- `Late Stage` — use for large rounds whose series label was not disclosed
- `IPO`, `Bootstrapped`, `Series Unknown`

---

## 🔍 Evidence and Verification Standards

Every number must trace to a dated, checkable source. The verification ladder:

| Status | Meaning | When to use |
|--------|---------|-------------|
| `verified` | Primary source (company announcement) or financial press (Reuters, Bloomberg, CNBC, WSJ, FT), ideally two independent types | Round terms, valuations, M&A |
| `partial` | Single source, an estimate, a Tier-3 aggregator, or unconfirmed reporting | Talks-stage rounds, single-source figures, public-record fields not directly re-verified |
| `unverified` | Existence confirmed, figures not | Rare; explain in `notes` |

**Rules that keep the dataset honest:**

- **Reported is not closed.** Rounds still being negotiated ("in talks", "reportedly") go in `notes`, never in the event log. A reported-in-progress round may be recorded as a `partial` event only with the caveat spelled out in its notes.
- **Raised is not worth.** `funding_amount` is money in the door; `valuation_display`/`valuation_usd` is the mark. Never swap them.
- **Primary is not secondary.** Employee tenders set valuation marks but stay out of `funding_amount`; debt financings are noted, not counted as rounds.
- **Month-precision dates** (when only the month is sourced) use the month-end date and say so in the event's `notes`.
- **`last_verified` is the actual date you checked** — never auto-substituted.
- **Conflicting sources are preserved.** If Reuters says $1.25T and CNBC says $1.4T, record both in `notes` — do not silently pick one.

---

## ✅ Contribution Checklist

Before submitting your Pull Request, verify:

- [ ] The startup has a **working website** (not a parked domain) — `python scripts/check_links.py` treats 403/429 as bot-blocked, not dead
- [ ] The startup is **real and operational** (not vaporware or stealth)
- [ ] The data includes a **dated, checkable source URL** — press release or financial press beats any aggregator
- [ ] The entry follows the **exact schema v2** format (all 31 fields)
- [ ] No **duplicate** entries exist — validator enforces unique `id` and `slug`
- [ ] **Both CSV mirrors are regenerated** (`build_master_csv.py`, `build_funding_rounds_csv.py`) — CI fails on drift
- [ ] Funding events respect **`metadata.cutoff`** and carry source URLs
- [ ] The relevant **category file** is regenerated (`build_categories.py`)
- [ ] `python scripts/validate_data.py` and `python -m unittest discover -s tests` both pass locally

---

## ❌ What NOT to Contribute

- ❌ **Stealth startups** without public information
- ❌ **Vaporware** — companies with no product or users
- ❌ **Affiliate links** or referral codes
- ❌ **Duplicate entries** — check existing data first
- ❌ **Inaccurate data** — verify before adding
- ❌ **Promotional content** — keep descriptions objective
- ❌ **Startups older than 10 years** without significant AI/ML pivot (we focus on newer companies or older ones with recent AI transformation)

---

## 🔄 Monthly Update Process

On the **30th of each month**, the maintainers will:

1. Review and merge all pending Pull Requests
2. Create the new month's data files
3. Update category files with new entries
4. Update the README with new statistics
5. Archive the previous month's data
6. Publish the monthly update

---

## 📝 Pull Request Template

```markdown
## Type of Change
- [ ] New startup added
- [ ] Existing data updated
- [ ] Error fix
- [ ] New category/source suggestion

## Startup Details (if adding)
- **Name:**
- **Website:**
- **Category:**
- **Source:**

## Checklist
- [ ] Working website verified
- [ ] Data source cited
- [ ] Schema format followed
- [ ] No duplicate entries
- [ ] CSV and JSON both updated
- [ ] Category file updated

## Additional Notes
(Any context about this contribution)
```

---

## 💬 Questions?

Open an [Issue](https://github.com/your-username/awesome-ai-ml-startups/issues) or start a [Discussion](https://github.com/your-username/awesome-ai-ml-startups/discussions) — we're happy to help!

Thank you for contributing! 🚀
