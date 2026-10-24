# Awesome AI/ML Startups

![GitHub stars](https://img.shields.io/github/stars/AdilShamim8/Awesome-AI_ML-Startups?style=social)
![GitHub forks](https://img.shields.io/github/forks/AdilShamim8/Awesome-AI_ML-Startups?style=social)
![License](https://img.shields.io/badge/license-MIT-blue)
![Last Updated](https://img.shields.io/badge/last%20updated-October%202026-brightgreen)
![Startups Tracked](https://img.shields.io/badge/startups%20tracked-118-orange)

> A monthly tracker of AI/ML startups. 118 companies across 11 countries plus an event-level funding history covering January 2025 through October 24, 2026, every number tied to a source you can open and check.

I started this repo in January 2026 as a simple list of AI companies I was watching. It grew into a full dataset: 118 companies across 10 categories, rebuilt in September 2026 with 197 targeted web searches, two-pass source verification, and an automated validation pipeline. A second layer added in September 2026 records **193 individual funding events across 2025 and 2026** — so you can see the market move month by month, not just where each company stands today. The **October 24, 2026 research window** added 15 companies (China's frontier labs among them), 21 funding events, and the pipeline hardening described below. Every entry carries the source name, the direct URLs, and the date the facts were last checked.

Star the repo if you want to follow the monthly updates. The next scheduled snapshot lands on **November 30, 2026** (the October 30 cycle continues; the current file is an October 24 pre-month-end research snapshot).

Last updated: October 24, 2026.

## Table of Contents

- [What this is](#what-this-is)
- [What this is not](#what-this-is-not)
- [The dataset](#the-dataset)
- [What changed in October 2026](#what-changed-in-october-2026)
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

- **118 companies**, deduplicated — one row per company, checked by `id` and `slug`
- **10 categories** — AI/ML, Generative AI, Robotics, DevTools, FinTech, AI Agents, HealthTech, Cybersecurity, SaaS, EdTech
- **11 countries** — the US core plus the UK, Germany, France, Sweden, Switzerland, Canada, and (new in October) China, Japan, India, and Singapore
- **Funding stage, amount raised, and valuation as three separate fields** — sortable in USD, not mushed together
- **Investors, HQ, founded year, region** for every company
- **M&A tracking** — 9 completed or pending deals flagged in the status fields (Google–Wiz, SpaceX–Anysphere, SpaceX–xAI, Capital One–Brex, Stripe–OpenRouter, CoreWeave–W&B, Workday–Sana, Meta–Scale, Stryker–CMR option)
- **Event-level funding history** — [`funding_rounds.csv`](data/master/funding_rounds.csv) records every verified round from Jan 2025 to Oct 24, 2026 (193 events, $369.4B confirmed capital), with monthly snapshots for all of 2025
- **Full provenance** — `source`, `source_urls`, `last_verified`, and an honest `verification_status` on every row and every event

A validation script runs in CI on every push (validation, CSV/JSON parity, unit tests). It checks the schema, controlled vocabularies, duplicates, event cutoffs, registry cross-references, and that the monthly snapshots actually match the master file.

## What this is not

- Not a Crunchbase clone. Database hits are used as cross-checks, never copied blindly — the record is company announcements and financial press.
- Not generated. No entry exists without a real, datable source. Nothing was written from memory.
- Not investment advice. It is a research dataset; figures are as-reported by the cited sources.
- Not finished. This is a living tracker. If a number looks wrong, open an issue with a source and I will fix it.

## The dataset

The canonical file is [`data/master/startups_master.json`](data/master/startups_master.json) (with a CSV mirror). Everything else — monthly snapshots, category pages, statistics — is generated from it. Edit the master, run the scripts, commit.

| Metric | Value |
|--------|-------|
| Companies tracked | 118 (15 added in the October window; 103 retained from September) |
| Funding events recorded | 193 — [funding_rounds.csv](data/master/funding_rounds.csv) |
| 2025 events / confirmed capital | 110 events · $104.3B verified · 165 mega-rounds (≥$100M) all-time |
| 2026 events / confirmed capital | 71 events · $262.7B verified |
| Verified against primary + financial press | 85 |
| Single-source / estimate (noted in `notes`) | 32 |
| Could not be confirmed | 1 |
| Categories | 10 |
| Countries | 11 (USA 94, UK 6, China 4, Germany 3, France 3, Sweden 3, Japan 1, India 1, Singapore 1, Canada 1, Switzerland 1) |
| Regions | North America 95 · Europe 16 · Asia-Pacific 7 |
| Distinct source domains cited | 103 |
| Founded | 2010 – 2026 |

## What changed in October 2026

The dataset was refreshed on **October 24, 2026** — a pre-month-end research snapshot, not the October 30 cycle. The full audit trail is in [docs/DATA_AUDIT_2026-10-24.md](docs/DATA_AUDIT_2026-10-24.md). Headlines:

### The dataset went global

China's frontier labs entered the registry for the first time: **DeepSeek** ($7.4B first external round at $50B+, with ~$15B more at ~$74B reportedly closing), **Moonshot AI** (~$2B at $20B), and the Hong Kong listings of **Z.ai** and **MiniMax**. **Sakana AI** (Japan), **Sarvam AI** (India), and **Manus AI** (Singapore) completed the Asia-Pacific expansion — the region went from zero to seven entries.

### Corrections to stale records

Five major records were corrected to closed rounds the September build had missed or under-recorded: **Mistral AI** (€3B Series D at €21B), **Cognition** ($2B at $48B), **Harvey** ($550M at $15.5B), **Crusoe** ($3.9B at $30.9B), and **Ramp** ($1.85B at $60B). The **xAI–SpaceX merger** (finalized May 6, 2026) and the **SpaceX–Anysphere** close (August 2026) moved both companies to `acquired`; ElevenLabs' $22B employee tender was recorded with the primary/secondary distinction preserved.

### Pipeline hardening

The README previously claimed CI existed — it didn't. Now it does: validation, CSV-parity checks, and 28 unit tests run on every push. The funding-events metadata gained an enforced `cutoff` field, coverage now matches the actual event range, and a name-variant cross-check caught three events that had silently drifted out of the registry flag.

## What changed in September 2026

The whole dataset was rebuilt and re-verified as of September 7, 2026. The full list of corrections is in the [audit report](docs/DATA_AUDIT_2026-09-07.md). Headlines:

### Largest latest rounds

| # | Company | Raised | Valuation | When |
|---|---------|--------|-----------|------|
| 1 | OpenAI | $122B | $852B | Mar 2026 |
| 2 | Anthropic | $65B | $965B | May 2026 |
| 3 | xAI | $20B (Series E) | ~$230B → $250B in SpaceX merger | Jan 2026 |
| 4 | Scale AI | $14.3B (Meta, 49%) | $29B | Jun 2025 |
| 5 | OpenRouter | $7.5B acquired by Stripe | — | Aug 2026 |
| 6 | DeepSeek | $7.4B+ (first external) | $50B+ | Jun 2026 |
| 7 | Crusoe | $3.9B (Series F) | $30.9B | Sep 2026 |
| 8 | Anduril | $5B (Series H) | $61B | May 2026 |
| 9 | Mistral AI | €3B (Series D) | €21B (~$24.4B) | Sep 2026 |
| 10 | Cognition | $2B (Series E) | $48B | Sep 2026 |

### M&A on record

| Company | Acquirer | Deal | Status |
|---------|----------|------|--------|
| Wiz | Google | $32B | Closed Mar 11, 2026 |
| Anysphere (Cursor) | SpaceX | $60B, stock | Closed Aug 2026 |
| xAI | SpaceX | all-stock; xAI at ~$250B in $1.25T entity | Finalized May 6, 2026 |
| OpenRouter | Stripe | $7.5B | Announced Aug 19, 2026 |
| Brex | Capital One | $5.15B | Announced Jan 23, 2026 |
| CMR Surgical | Stryker | ~$400M equity + exclusive option | Announced Oct 12, 2026 |
| Sana | Workday | $1.1B | Completed |
| Weights & Biases | CoreWeave | ~$1.7B | Closed May 2025 |
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

Full methodology, the per-company source registry, and the source inventory live in [SOURCES.md](SOURCES.md). The dated search evidence behind every company is preserved in [docs/evidence_log.md](docs/evidence_log.md) — 188 evidence blocks (152 from September, 36 from the October window) — and the exact 243 queries used (197 in September, 46 in October) are logged in [docs/search_queries.md](docs/search_queries.md). If you want to audit a number, start there.

## How it is collected

Six steps, run manually for the September rebuild, repeated for the October 2026 window, and repeated for every future release:

1. **Seed list** — companies already tracked in the master dataset plus targeted sweeps for the research gap (September 8 – October 24, 2026 events, global expansion candidates).
2. **Search** — 197 tiered queries in the September rebuild plus 46 in the October window (gap-window round lookups, new-company verification, regional sweeps for Asia-Pacific, and verification passes on existing records).
3. **Verify** — two independent source types preferred (company announcement + financial press). One source only → `partial` with a note naming the source tier. Nothing confirmed → `unverified`. Reported-but-unconfirmed rounds (e.g. DeepSeek's October ~$15B) are recorded as `partial` events with explicit notes, never mixed silently with closed rounds.
4. **Extract** — normalize raised vs valuation to separate numeric fields; keep original currency in the display fields; record acquirer and deal value for M&A; distinguish primary financing from debt, tenders, and acquisitions; month-precision dates are flagged and use the month-end convention.
5. **Link check** — websites tested for liveness (`python scripts/check_links.py`); bot-blocked sites (HTTP 403/429) are distinguished from genuinely dead URLs and are not counted as failures.
6. **Validate** — `python scripts/validate_data.py`, plus `python -m unittest discover -s tests`, both enforced in CI on every push.

No entry is added from memory. If I cannot find a datable source, the company does not go in — see the October audit's research-gaps section for candidates deliberately left out.

## Repository layout

```
awesome-ai-ml-startups/
├── README.md                        # you are here
├── SOURCES.md                       # where the data comes from, per-company source registry
├── CONTRIBUTING.md                  # how to add or fix entries
├── CHANGELOG.md                     # monthly changelog
├── docs/
│   ├── DATA_AUDIT_2026-10-24.md     # full audit trail of the October refresh
│   ├── DATA_AUDIT_2026-09-07.md     # full audit trail of the September rebuild
│   ├── evidence_log.md              # dated search evidence, per company
│   └── search_queries.md            # the exact queries used
├── data/
│   ├── master/                      # canonical dataset (edit here)
│   │   ├── startups_master.json
│   │   ├── startups_master.csv
│   │   ├── funding_rounds.json
│   │   ├── funding_rounds.csv
│   │   └── link_check_report.json
│   └── 2026/                        # monthly snapshots (generated)
│       ├── january/ … may/          # legacy months, preserved as published
│       ├── september/               # September 2026 rebuild (historical)
│       └── october/                 # Oct 24 pre-month-end research snapshot
├── categories/                      # 10 category pages (generated)
├── scripts/                         # pipeline: build, validate, check links
├── tests/                           # unit tests for the validator
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

The full event list for the year: [funding_rounds.csv](data/master/funding_rounds.csv). 110 events in the master log for 2025 across 92 unique companies ($104.3B verified). The monthly archive files below remain exactly as originally published (109 events; the master log gained Sakana AI's November 2025 round in the October refresh).

| Month | Events (archive) | Capital | CSV | Notes |
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
| October 2026 | 118 | [CSV](data/2026/october/startups_october_2026.csv) | [JSON](data/2026/october/startups_october_2026.json) | Oct 24 pre-month-end research snapshot; 15 new |
| September 2026 | 103 | [CSV](data/2026/september/startups_september_2026.csv) | [JSON](data/2026/september/startups_september_2026.json) | Full rebuild, schema v2, 53 new (historical) |
| May 2026 | 60 | [CSV](data/2026/may/startups_may_2026.csv) | [JSON](data/2026/may/startups_may_2026.json) | Legacy, as published |
| April 2026 | 25 | [CSV](data/2026/april/startups_april_2026.csv) | — | Legacy |
| March 2026 | 20 | [CSV](data/2026/march/startups_march_2026.csv) | — | Legacy |
| February 2026 | 15 | [CSV](data/2026/february/startups_february_2026.csv) | — | Legacy |
| January 2026 | 20 | [CSV](data/2026/january/startups_january_2026.csv) | — | Legacy |

Snapshots for Jan–May 2026 are kept exactly as originally published — they are historical records, warts included. From September 2026 onward, snapshots are generated from the master file; the September 2026 snapshot is likewise preserved as published (103 companies, as-of 2026-09-07) rather than silently rewritten. The October 24, 2026 file is a **pre-month-end research snapshot** — it records the state verified on that date and does not claim the October 30 reporting period completed. The 2025 monthly snapshots are **event-based**: they list the funding rounds announced that month, not the full company universe.

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
