# 🚀 Awesome AI/ML & Tech Startups — Monthly Tracker

[![Validate Data](https://github.com/AdilShamim8/awesome-ai-ml-startups/actions/workflows/validate.yml/badge.svg)](https://github.com/AdilShamim8/awesome-ai-ml-startups/actions/workflows/validate.yml)
[![Last Updated](https://img.shields.io/badge/Updated-September%207%2C%202026-blue)](./data/master/)
[![Startups Count](https://img.shields.io/badge/Startups-103-brightgreen)](./data/master/startups_master.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Data Format](https://img.shields.io/badge/Data-CSV%20%7C%20JSON-orange)](./data/master/)
[![Schema](https://img.shields.io/badge/Schema-v2.0-informational)](#-data-schema)

> **A comprehensive, community-driven monthly tracker of AI/ML and tech software startups.** Every company entry is deduplicated against a canonical master dataset, refreshed from primary sources, and validated automatically. Current release rebuilt and verified as of **September 7, 2026**.

---

## 📋 Table of Contents

- [🔥 What Is This?](#-what-is-this)
- [📊 Current Release — September 2026 Highlights](#-current-release--september-2026-highlights)
- [🗂️ Repository Structure](#️-repository-structure)
- [🏷️ Categories Covered](#️-categories-covered)
- [📈 Data Schema (v2)](#-data-schema-v2)
- [✅ Data Quality & Verification](#-data-quality--verification)
- [📂 Monthly Archives](#-monthly-archives)
- [🔍 Data Sources](#-data-sources)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🔥 What Is This?

This repository is an open-source directory for tracking AI/ML and tech startups worldwide on a monthly basis. As of the **September 2026 rebuild**, the dataset is organized around a **canonical master file** — one deduplicated row per company — from which all monthly snapshots, category pages, and statistics are generated.

Each startup entry covers:

- **Startup Name** — official company name
- **About / Description** — what the company does, current as of the last verification date
- **Website** — direct URL (automatically link-checked)
- **Category / Subcategory** — one of 10 controlled categories plus a fine-grained subcategory
- **Funding Stage / Amount / Valuation** — latest known round and valuation, kept as separate, machine-readable fields
- **Headquarters** — city and country, plus derived region
- **Investors** — key investors in the latest round
- **Source & Source URLs** — where every fact came from
- **Verification dates** — when the entry was added, last updated, and last verified

### Why This Matters

The AI/ML startup landscape moves at breakneck speed. Global venture funding hit a record **$510B in H1 2026** (Crunchbase) — more than all of 2025 — and AI companies captured the large majority of it. Three private companies (OpenAI, Anthropic, xAI) alone absorbed ~$217B in H1 2026. Keeping on top of this ecosystem requires systematic tracking, deduplication, and verification — exactly what this repo provides.

Whether you're a founder scoping competitors, an investor mapping the market, a job seeker targeting high-growth companies, or a researcher studying the AI economy — this repo is your monthly pulse check.

---

## 📊 Current Release — September 2026 Highlights

| Metric | Value |
|--------|-------|
| **Total Startups Tracked** | 103 |
| **New in September Rebuild** | 52 |
| **Entries Verified Against Primary Sources** | 75 |
| **Categories Covered** | 10 |
| **M&A Events Captured** | 7 (Wiz→Google, Brex→Capital One, Cursor→SpaceX, W&B→CoreWeave, Sana→Workday, Scale→Meta (49%), OpenRouter→Stripe) |
| **Public-Company References** | 3 (Duolingo, Lemonade, Aurora Innovation) |

### 🔥 Top 10 Companies by Latest Round

| # | Startup | Latest Round | Valuation | Category |
|---|---------|--------------|-----------|----------|
| 1 | OpenAI | $122B (Mar 2026) | $852B | Generative AI |
| 2 | Anthropic | $65B (May 2026) | $965B | Generative AI |
| 3 | xAI | $20B Series E (Jan 2026) | ~$230B | Generative AI |
| 4 | Scale AI | $14.3B — Meta, 49% (Jun 2025) | $29B | AI/ML |
| 5 | OpenRouter | $7.5B acquisition by Stripe (Aug 2026) | $7.5B | DevTools |
| 6 | Crusoe | $3B+ (Sep 2026) | ~$30B | AI/ML |
| 7 | Anduril | $5B Series H (May 2026) | $61B | Robotics |
| 8 | Mistral AI | €1.7B Series C (Sep 2025) | €11.7B | Generative AI |
| 9 | Fireworks AI | $1.5B Series D (Jul 2026) | $17.5B | AI/ML |
| 10 | Baseten | $1.5B Series F (Jun 2026) | $13B | AI/ML |

### 📌 Notable Corporate Events (captured in this release)

- **Google completed its $32B acquisition of Wiz** (Mar 11, 2026) — the largest cybersecurity exit ever
- **SpaceX agreed to acquire Anysphere (Cursor) for $60B in stock** (announced Jun 16, 2026)
- **Capital One announced the $5.15B acquisition of Brex** (Jan 23, 2026)
- **Stripe agreed to acquire OpenRouter for $7.5B** (Aug 19, 2026) and held a $159B tender
- **Anduril** is reportedly raising at ~$100B, weeks after its $61B Series H

---

## 🗂️ Repository Structure

```
awesome-ai-ml-startups/
├── 📄 README.md                          # You are here
├── 📄 CONTRIBUTING.md                    # How to contribute
├── 📄 LICENSE                            # MIT License
├── 📄 CODE_OF_CONDUCT.md                 # Community guidelines
├── 📄 CHANGELOG.md                       # Monthly changelog
├── 📄 docs/
│   └── DATA_AUDIT_2026-09-07.md          # Full audit & rebuild report
│
├── 📁 data/                              # 📊 All startup datasets
│   ├── 📁 master/                        # ⭐ CANONICAL SOURCE OF TRUTH
│   │   ├── startups_master.json          # One deduplicated row per company
│   │   ├── startups_master.csv           # Flat CSV mirror
│   │   └── link_check_report.json        # Latest automated link check
│   └── 📁 2026/                          # Monthly snapshots
│       ├── 📁 january/ … 📁 may/         # Legacy snapshots (as originally published)
│       └── 📁 september/                 # ⭐ LATEST — generated from master
│           ├── startups_september_2026.csv
│           ├── startups_september_2026.json
│           └── stats.json
│
├── 📁 categories/                        # 🏷️ Category breakdowns (generated)
│   ├── ai-ml.md … edtech.md              # 10 category pages
│
├── 📁 scripts/                           # 🔧 Automation pipeline
│   ├── build_snapshots.py                # master → monthly CSV/JSON + stats
│   ├── build_categories.py               # master → category markdown pages
│   ├── validate_data.py (v2)             # schema + cross-file validation
│   ├── check_links.py                    # automated website liveness checks
│   ├── generate_readme.py                # statistics generator
│   └── update_monthly.py                 # monthly update checklist
│
├── 📁 .github/
│   ├── 📁 workflows/
│   │   ├── validate.yml                  # CI: validates data on every push
│   │   └── monthly-update.yml            # Scheduled monthly update reminder
│   └── FUNDING.yml                       # Sponsor info
│
└── 📁 assets/
    └── banner.svg                        # Repo banner
```

**Data flow:** `data/master/startups_master.json` → `build_snapshots.py` → `data/YYYY/month/` → `validate_data.py` → README/stats. Edit **only** the master file; snapshots are generated.

---

## 🏷️ Categories Covered

| Category | Description | Count (Sep 2026) |
|----------|-------------|-------------------|
| 🤖 **AI/ML** | Core AI platforms, infrastructure, data engines | 20 |
| ✨ **Generative AI** | LLMs, image/video/music gen, creative AI | 15 |
| 🦾 **Robotics** | AI robotics, defense & autonomous systems | 17 |
| 🛠️ **DevTools** | Developer tools, AI coding, app builders | 12 |
| 💰 **FinTech** | AI-driven financial technology | 9 |
| 🕵️ **AI Agents** | Autonomous agents & agentic systems | 8 |
| 🏥 **HealthTech** | AI in healthcare & biotech | 7 |
| 🔒 **Cybersecurity** | AI security & threat detection | 6 |
| 💻 **SaaS** | AI-powered SaaS products | 5 |
| 📚 **EdTech** | AI in education & learning | 4 |

---

## 📈 Data Schema (v2)

The canonical schema (v2.0) extends the original 12 fields with machine-readable funding data and full traceability. The original field names are preserved for backward compatibility.

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Stable unique identifier (3-digit) |
| `slug` | string | URL-safe unique key (dedupe key) |
| `startup_name` | string | Official company name |
| `about` | string | Short tagline (1 line) |
| `description` | string | Detailed, current description |
| `website` | URL | Official website (link-checked) |
| `category` | enum | One of the 10 controlled categories |
| `subcategory` | string | Fine-grained segment |
| `funding_stage` | enum | Pre-Seed … Series K, Late Stage, IPO, Bootstrapped |
| `funding_amount` | string | Latest primary round, display format |
| `funding_amount_usd` | number? | Latest round in USD (sortable/comparable) |
| `valuation_display` | string? | Latest valuation with date |
| `valuation_usd` | number? | Latest valuation in USD |
| `total_raised_display` | string? | Cumulative raised, display format |
| `last_round_date` | date? | Date of latest round (YYYY-MM-DD) |
| `investors` | string[] | Key investors, latest round |
| `headquarters` | string | "City, Country" |
| `city` / `country` | string | Split-out location fields |
| `region` | enum | North America / Europe / Middle East / Asia-Pacific / Other |
| `founded_year` | int | Year founded |
| `status` | enum | active / acquired / pending_acquisition / majority_acquired / public |
| `status_note` | string? | M&A / IPO context |
| `source` | string | Primary source labels |
| `source_urls` | URL[] | Where facts were verified |
| `date_added` | date | When the company first entered the tracker |
| `last_updated` | date | When any field last changed |
| `last_verified` | date | When facts were last checked against sources |
| `verification_status` | enum | verified / partial / unverified |
| `tags` | string[] | Free-form topic tags |
| `notes` | string? | Caveats, estimates, corrections |

> **Design note:** `funding_amount` (round raised) and `valuation` are now **separate fields**. Earlier releases conflated them (e.g., OpenAI's "$110B" was actually a valuation figure); the v2 rebuild separates raised capital ($122B round) from worth ($852B valuation).

---

## ✅ Data Quality & Verification

Every entry carries a `verification_status`:

| Status | Meaning | Count (Sep 2026) |
|--------|---------|-------------------|
| ✅ `verified` | Confirmed against company announcements and/or financial press (Reuters, Bloomberg, TechCrunch, CNBC, WSJ, Forbes) | 75 |
| 🟡 `partial` | Single-source or estimate; caveat recorded in `notes` | 26 |
| ⚠️ `unverified` | Existence confirmed; figures could not be verified | 1 |

**Automated quality gates** (run in CI on every push):

1. `validate_data.py` — schema compliance, controlled vocabularies, URL/date formats, duplicate detection (by id *and* slug), CSV/JSON parity, snapshot-vs-master sync, statistics consistency
2. `check_links.py` — liveness checks on all 103 websites (bot-blocked sites returning 403/429 are reviewed manually)

The full September 2026 audit — including every correction made to pre-existing data — is documented in [docs/DATA_AUDIT_2026-09-07.md](./docs/DATA_AUDIT_2026-09-07.md).

---

## 📂 Monthly Archives

| Month | Startups | CSV | JSON | Notes |
|-------|----------|-----|------|-------|
| **September 2026** ⭐ | 102 | [CSV](./data/2026/september/startups_september_2026.csv) | [JSON](./data/2026/september/startups_september_2026.json) | Full audit rebuild; schema v2; 52 new companies |
| May 2026 | 60 | [CSV](./data/2026/may/startups_may_2026.csv) | [JSON](./data/2026/may/startups_may_2026.json) | Legacy snapshot (as published) |
| April 2026 | 25 | [CSV](./data/2026/april/startups_april_2026.csv) | — | Legacy snapshot (CSV only) |
| March 2026 | 20 | [CSV](./data/2026/march/startups_march_2026.csv) | — | Legacy snapshot (CSV only) |
| February 2026 | 15 | [CSV](./data/2026/february/startups_february_2026.csv) | — | Legacy snapshot (CSV only) |
| January 2026 | 20 | [CSV](./data/2026/january/startups_january_2026.csv) | — | Legacy snapshot (CSV only) |

> **📅 Update schedule:** published on the **30th of every month**. Snapshots are generated from the master dataset; legacy months (Jan–May 2026) are preserved exactly as originally published for historical traceability.

---

## 🔍 Data Sources

The September 2026 rebuild was verified against primary and financial press sources:

| Source | Type | Used for |
|--------|------|----------|
| 🏢 **Company announcements** | Primary | Funding rounds, valuations, M&A |
| 📰 **Reuters / Bloomberg / CNBC** | Financial press | Round terms, market context |
| 📰 **TechCrunch / The Information / Newcomer** | Tech press | Funding details, product news |
| 📊 **Crunchbase / Tracxn** | Funding databases | Round histories, cross-checks |
| 🏆 **Forbes / WSJ** | Business press | Rankings, investigative figures |
| 🟠 **Y Combinator** | Accelerator | Early-stage company details |
| 📈 **Company IR pages** | Primary | Public-company references (Duolingo, Lemonade, Aurora) |

Each entry stores its `source` labels and direct `source_urls` in the dataset itself.

---

## 🤝 Contributing

We welcome contributions! The workflow since v2:

1. **Fork** this repository
2. **Edit the master dataset** (`data/master/startups_master.json` + mirror the row in `startups_master.csv`) — one row per company, no duplicates (the validator enforces slug/id uniqueness)
3. **Regenerate** snapshots and category pages via the scripts (see `scripts/update_monthly.py` checklist)
4. **Submit** a Pull Request — CI will validate the data automatically

### Contribution Rules

- ✅ Only add **real, verified** startups with working website links
- ✅ Include the **data source** and fill `source_urls` where possible
- ✅ Use the **v2 schema** (see [Data Schema](#-data-schema-v2))
- ✅ One row per company — check the `slug` list before adding
- ✅ Set an honest `verification_status`
- ❌ No vaporware or stealth startups without public information
- ❌ No affiliate links or referral codes

👉 See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](./LICENSE) for details.

All startup data is collected from publicly available sources. Company names, logos, and trademarks belong to their respective owners.

---

<div align="center">

**Built with ❤️ by the community, for the community**

**📅 Next Update: September 30, 2026**

[⬆ Back to Top](#-awesome-aiml--tech-startups--monthly-tracker)

</div>
