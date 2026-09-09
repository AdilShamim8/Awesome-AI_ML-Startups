# Awesome AI/ML Startups

![GitHub stars](https://img.shields.io/github/stars/AdilShamim8/Awesome-AI_ML-Startups?style=social)
![GitHub forks](https://img.shields.io/github/forks/AdilShamim8/Awesome-AI_ML-Startups?style=social)
![License](https://img.shields.io/badge/license-MIT-blue)
![Last Updated](https://img.shields.io/badge/last%20updated-September%202026-brightgreen)
![Startups Tracked](https://img.shields.io/badge/startups%20tracked-103-orange)

> A monthly tracker of AI/ML startups. 103 companies plus an event-level funding history covering January 2025 through September 2026, every number tied to a source you can open and check.

I started this repo in January 2026 as a simple list of AI companies I was watching. It grew into a full dataset: 103 companies across 10 categories, rebuilt from scratch in September 2026 with 197 targeted web searches, two-pass source verification, and an automated validation pipeline. A second layer added in September 2026 records **172 individual funding events across 2025 and 2026** — so you can see the market move month by month, not just where each company stands today. Every entry carries the source name, the direct URLs, and the date the facts were last checked.

Star the repo if you want to follow the monthly updates. The next snapshot lands on **September 30, 2026**.

Last updated: September 9, 2026.

## Table of Contents

- [What this is](#what-this-is)
- [What this is not](#what-this-is-not)
- [The dataset](#the-dataset)
- [What changed in September 2026](#what-changed-in-september-2026)
- [Where the data comes from](#where-the-data-comes-from)
- [How it is collected](#how-it-is-collected)
- [Repository layout](#repository-layout)
- [Data schema](#data-schema)
- [Using the data](#using-the-data)
- [Monthly archive](#monthly-archive)
- [Contributing](#contributing)
- [License](#license)

## What this is

A monthly snapshot of the private AI/ML startup landscape, built around one canonical master dataset. You get:

- **103 companies**, deduplicated — one row per company, checked by `id` and `slug`
- **10 categories** — AI/ML, Generative AI, Robotics, DevTools, FinTech, AI Agents, HealthTech, Cybersecurity, SaaS, EdTech
- **Funding stage, amount raised, and valuation as three separate fields** — sortable in USD, not mushed together
- **Investors, HQ, founded year, region** for every company
- **M&A tracking** — 7 acquisitions flagged in the status fields (Google–Wiz, SpaceX–Anysphere, Capital One–Brex, Stripe–OpenRouter, CoreWeave–W&B, Workday–Sana, Meta–Scale)
- **Event-level funding history** — [`funding_rounds.csv`](data/master/funding_rounds.csv) records every verified round from Jan 2025 to Sep 2026 (172 events, $352.9B tracked capital), with monthly snapshots for all of 2025
- **Full provenance** — `source`, `source_urls`, `last_verified`, and an honest `verification_status` on every row and every event

A validation script runs in CI on every push. It checks the schema, controlled vocabularies, duplicates, CSV/JSON parity, and that the monthly snapshots actually match the master file.

## What this is not

- Not a Crunchbase clone. Database hits are used as cross-checks, never copied blindly — the record is company announcements and financial press.
- Not generated. No entry exists without a real, datable source. Nothing was written from memory.
- Not investment advice. It is a research dataset; figures are as-reported by the cited sources.
- Not finished. This is a living tracker. If a number looks wrong, open an issue with a source and I will fix it.

## The dataset

The canonical file is [`data/master/startups_master.json`](data/master/startups_master.json) (with a CSV mirror). Everything else — monthly snapshots, category pages, statistics — is generated from it. Edit the master, run the scripts, commit.

| Metric | Value |
|--------|-------|
| Companies tracked | 103 (53 added in the September rebuild) |
| Funding events recorded (2025 → Sep 2026) | 172 — [funding_rounds.csv](data/master/funding_rounds.csv) |
| 2025 events / capital | 109 events · $107.3B · 93 mega-rounds (≥$100M) |
| Verified against primary + financial press | 76 |
| Single-source / estimate (noted in `notes`) | 26 |
| Could not be confirmed | 1 |
| Categories | 10 |
| Distinct source domains cited | 91+ |
| Countries | 7 (USA 88, UK 5, Germany 3, Sweden 3, France 2, Canada 1, Switzerland 1) |
| Founded | 2010 – 2025 |

## What changed in September 2026

The whole dataset was rebuilt and re-verified as of September 7, 2026. The full list of corrections is in the [audit report](docs/DATA_AUDIT_2026-09-07.md). Headlines:

### Largest latest rounds

| # | Company | Raised | Valuation | When |
|---|---------|--------|-----------|------|
| 1 | OpenAI | $122B | $852B | Mar 2026 |
| 2 | Anthropic | $65B | $965B | May 2026 |
| 3 | xAI | $20B (Series E) | ~$230B | Jan 2026 |
| 4 | Scale AI | $14.3B (Meta, 49%) | $29B | Jun 2025 |
| 5 | OpenRouter | $7.5B acquired by Stripe | — | Aug 2026 |
| 6 | Crusoe | $3B+ | ~$30B | Sep 2026 |
| 7 | Anduril | $5B (Series H) | $61B | May 2026 |
| 8 | Mistral AI | €1.7B (Series C) | €11.7B | Sep 2025 |
| 9 | Fireworks AI | $1.5B (Series D) | $17.5B | Jul 2026 |
| 10 | Baseten | $1.5B (Series F) | $13B | Jun 2026 |

### M&A on record

| Company | Acquirer | Deal | Status |
|---------|----------|------|--------|
| Wiz | Google | $32B | Closed Mar 11, 2026 |
| Anysphere (Cursor) | SpaceX | $60B, stock | Announced Jun 16, 2026 |
| OpenRouter | Stripe | $7.5B | Announced Aug 19, 2026 |
| Brex | Capital One | $5.15B | Announced Jan 23, 2026 |
| Sana | Workday | $1.1B | Completed |
| Weights & Biases | CoreWeave | — | Closed May 2025 |
| Scale AI | Meta | 49% stake, $14.3B | Completed Jun 2025 |

An earlier version of this repo conflated "raised" with "valued at" — OpenAI's famous "$110B" was a valuation, not a round. The schema now separates `funding_amount` (raised) from `valuation_display` (worth), and every historical row was re-extracted with that rule.

## Where the data comes from

Five source groups, in priority order:

| Group | Examples | Role |
|-------|----------|------|
| Company announcements | Official blogs, press releases, investor pages | Primary record for rounds, valuations, M&A |
| Financial press | Reuters, Bloomberg, CNBC, WSJ, Financial Times | Independent confirmation |
| Tech press | TechCrunch, The Information, Newcomer | Funding details, early-stage coverage |
| Funding databases | Crunchbase, Tracxn, Sacra | Round histories, cross-checks only |
| Accelerator / rankings | Y Combinator directory, Forbes | Early-stage facts, founded year, HQ |

Full methodology, the per-company source registry, and the source inventory live in [SOURCES.md](SOURCES.md). The dated search evidence behind every company is preserved in [docs/evidence_log.md](docs/evidence_log.md), and the exact 197 queries used are logged in [docs/search_queries.md](docs/search_queries.md). If you want to audit a number, start there.

## How it is collected

Six steps, run manually for the September rebuild and repeated for every future release:

1. **Seed list** — companies already tracked in the monthly snapshots (61 unique names).
2. **Search** — 197 tiered queries against the live web (45 per-company round lookups, 45 second-pass investor/date checks, 35 category sweeps, 20 macro-context queries, 28 follow-ups, 24 late additions).
3. **Verify** — two independent source types preferred (company announcement + financial press). One source only → `partial` with a note. Nothing confirmed → `unverified`.
4. **Extract** — normalize raised vs valuation to separate numeric fields; keep original currency in the display fields; record acquirer and deal value for M&A.
5. **Link check** — all 103 websites tested for liveness; bot-blocked sites (HTTP 403/429) verified manually in a browser.
6. **Validate** — `python scripts/validate_data.py`, also enforced in CI on every push.

No entry is added from memory. If I cannot find a datable source, the company does not go in.

## Repository layout

```
awesome-ai-ml-startups/
├── README.md                        # you are here
├── SOURCES.md                       # where the data comes from, per-company source registry
├── CONTRIBUTING.md                  # how to add or fix entries
├── CHANGELOG.md                     # monthly changelog
├── docs/
│   ├── DATA_AUDIT_2026-09-07.md     # full audit trail of the September rebuild
│   ├── evidence_log.md              # dated search evidence, per company
│   └── search_queries.md            # the exact queries used
├── data/
│   ├── master/                      # canonical dataset (edit here)
│   │   ├── startups_master.json
│   │   ├── startups_master.csv
│   │   └── link_check_report.json
│   └── 2026/                        # monthly snapshots (generated)
│       ├── january/ … may/          # legacy months, preserved as published
│       └── september/               # latest
├── categories/                      # 10 category pages (generated)
├── scripts/                         # pipeline: build, validate, check links
└── .github/workflows/               # CI: validate on push + monthly update reminder
```

## Data schema

Version 2 keeps the original 12 fields for backward compatibility and adds traceability plus machine-readable money. Highlights:

| Field | What it holds |
|-------|---------------|
| `id` / `slug` | Stable unique keys (3-digit id, URL-safe slug) |
| `startup_name`, `about`, `description` | Identity and what the company does |
| `website` | Official URL, link-checked |
| `category` / `subcategory` | One of 10 controlled categories + fine-grained segment |
| `funding_stage` | Pre-Seed … Series K, Late Stage, IPO, Bootstrapped |
| `funding_amount` / `funding_amount_usd` | Latest round raised — display string + numeric USD |
| `valuation_display` / `valuation_usd` | Latest valuation — display string + numeric USD |
| `last_round_date` | Date of the latest round (YYYY-MM-DD) |
| `investors` | Key investors in the latest round |
| `headquarters` / `city` / `country` / `region` | Location, split and derived |
| `founded_year` | Year founded |
| `status` / `status_note` | active / acquired / pending_acquisition / majority_acquired / public + deal context |
| `source` / `source_urls` | Where the facts came from |
| `date_added` / `last_updated` / `last_verified` | Three distinct dates — first tracked, last changed, last checked against sources |
| `verification_status` | verified / partial / unverified |

## Using the data

CSV and JSON carry identical rows. Something like:

```python
import pandas as pd

df = pd.read_csv("data/master/startups_master.csv")

# Biggest latest rounds
df.nlargest(10, "funding_amount_usd")[["startup_name", "funding_stage", "funding_amount_usd", "valuation_usd"]]

# What is raising in Europe right now
eu = df[df.region == "Europe"].sort_values("funding_amount_usd", ascending=False)

# Only fully verified entries
safe = df[df.verification_status == "verified"]
```

If you use the dataset in a paper, dashboard, or post, a link back here is appreciated but not required.

## Monthly archive

### 2025 — funding events (one row per round announced that month)

The full event list for the year: [funding_rounds.csv](data/master/funding_rounds.csv). 109 events, $107.3B, 91 unique companies.

| Month | Events | Capital | CSV | Notes |
|-------|--------|---------|-----|-------|
| December 2025 | 9 | $1.5B | [CSV](data/2025/december/funding_events_december_2025.csv) | Mythic, Chai Discovery, Fal ×2… |
| November 2025 | 13 | $7.7B | [CSV](data/2025/november/funding_events_november_2025.csv) | Cursor $2.3B, Luma $900M, Ramp ×2 |
| October 2025 | 12 | $5.4B | [CSV](data/2025/october/funding_events_october_2025.csv) | Reflection AI $2B, Lila $350M |
| September 2025 | 20 | $20.2B | [CSV](data/2025/september/funding_events_september_2025.csv) | Anthropic $13B, Cerebras $1.1B, Mistral €1.7B |
| August 2025 | 5 | $1.2B | [CSV](data/2025/august/funding_events_august_2025.csv) | EliseAI $250M, Cohere $500M, Decart |
| July 2025 | 10 | $4.7B | [CSV](data/2025/july/funding_events_july_2025.csv) | Thinking Machines $2B seed, Ramp $500M |
| June 2025 | 10 | $16.9B | [CSV](data/2025/june/funding_events_june_2025.csv) | Scale AI–Meta $14.3B, Applied Intuition $600M |
| May 2025 | 4 | $0.3B | [CSV](data/2025/may/funding_events_may_2025.csv) | LMArena $100M seed, Snorkel $100M |
| April 2025 | 4 | $2.8B | [CSV](data/2025/april/funding_events_april_2025.csv) | Safe Superintelligence $2B @ $32B |
| March 2025 | 10 | $44.7B | [CSV](data/2025/march/funding_events_march_2025.csv) | OpenAI $40B @ $300B, Anthropic $3.5B |
| February 2025 | 8 | $1.6B | [CSV](data/2025/february/funding_events_february_2025.csv) | Lambda $480M, Together AI $305M, Harvey $300M |
| January 2025 | 4 | $0.5B | [CSV](data/2025/january/funding_events_january_2025.csv) | ElevenLabs $180M @ $3.3B |

### 2026 — company snapshots

| Month | Companies | CSV | JSON | Notes |
|-------|-----------|-----|------|-------|
| September 2026 | 103 | [CSV](data/2026/september/startups_september_2026.csv) | [JSON](data/2026/september/startups_september_2026.json) | Full rebuild, schema v2, 53 new |
| May 2026 | 60 | [CSV](data/2026/may/startups_may_2026.csv) | [JSON](data/2026/may/startups_may_2026.json) | Legacy, as published |
| April 2026 | 25 | [CSV](data/2026/april/startups_april_2026.csv) | — | Legacy |
| March 2026 | 20 | [CSV](data/2026/march/startups_march_2026.csv) | — | Legacy |
| February 2026 | 15 | [CSV](data/2026/february/startups_february_2026.csv) | — | Legacy |
| January 2026 | 20 | [CSV](data/2026/january/startups_january_2026.csv) | — | Legacy |

Snapshots for Jan–May 2026 are kept exactly as originally published — they are historical records, warts included. From September 2026 onward, snapshots are generated from the master file. The 2025 monthly snapshots are **event-based**: they list the funding rounds announced that month, not the full company universe.

## Contributing

Found a wrong number? A missing company? Open an issue or a PR with a source — a link to the company announcement or financial press coverage is all I need.

1. Fork the repo
2. Add or fix the row in `data/master/startups_master.json` (mirror it in the CSV)
3. Fill `source`, `source_urls`, `last_verified`, and an honest `verification_status`
4. Run `python scripts/validate_data.py`
5. Open the PR — CI validates automatically

PR checklist:

- [ ] One row per company (validator enforces `id` + `slug` uniqueness)
- [ ] Real, datable source with a working URL
- [ ] `funding_amount_usd` filled so the row sorts correctly
- [ ] Raised and valuation not swapped
- [ ] `last_verified` set to today

## License

MIT. See [LICENSE](LICENSE).

The data itself is collected from publicly available sources. Company names and trademarks belong to their owners.

## Connect With Me

<p align="center">
  <a href="https://www.adilshamim.me/">
    <img src="https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white" />
  </a>
  <a href="https://adilshamim8.medium.com/">
    <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" />
  </a>
  <a href="https://linkedin.com/in/adilshamim8">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://twitter.com/adil_shamim8">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" />
  </a>
  <a href="https://www.kaggle.com/adilshamim8">
    <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" />
  </a>
  <a href="https://leetcode.com/u/AdilShamim8">
    <img src="https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black" />
  </a>
</p>
