# Changelog

All notable changes to the Awesome AI/ML Startups repository are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Monthly Updates on the 30th](./README.md).

---

## [September 2026 — 2025 Dataset Extension] — 2026-09-09

Adds the missing piece of the original brief: full-year 2025 coverage, as an
event-level funding dataset with monthly snapshots.

### Added
- **`data/master/funding_rounds.json` + `.csv`** — 172 funding events from January 2025
  through September 2026 ($352.9B tracked capital), one row per round, each with source
  name, source URL(s), verification status, and an `in_registry` flag
- **`data/2025/<month>/`** — 12 monthly event snapshots (CSV + stats.json), 109 events
  in 2025 across 91 unique companies ($107.3B, 93 mega-rounds ≥$100M)
- **SOURCES.md 2025-extension section** — the four-step 2025 collection method
  (TechCrunch 2025 mega-round census + evidence-base mining + gap searches + merge)
- **Validator support** — `validate_data.py` now validates the rounds dataset
  (schema, dates, dedupe, URL coverage) and the event snapshots

### Method notes
- Backbone: TechCrunch's "55 US AI startups that raised $100M+ in 2025" (updated
  Jan 19, 2026), parsed into 64 structured events and transcribed as stated
- Registry-company 2025 events re-verified from the Sep 5–7, 2026 evidence base
  (152 blocks) and resolved to direct source URLs
- Reported-but-unconfirmed events (Perplexity Sep 2025, Poolside/Nvidia, Surge AI)
  are flagged `partial` with notes — never mixed silently with confirmed figures
- Dedupe rule: company + month + amount within 5% tolerance

---

## [September 2026 — Source Documentation & README Rewrite] — 2026-09-09

Closes the loop on provenance: the dataset already carried per-entry sources, but the
methodology itself was not documented anywhere. Also replaces the README, which read
like a template.

### Added
- **SOURCES.md** (repo root) — where the dataset comes from, the six-step collection
  method, the source inventory (91 distinct domains ranked), and a per-company source
  registry table listing every cited source name, URL, verification date, and status
- **docs/evidence_log.md** — 152 dated evidence blocks (search snippets with source
  domains and publication dates), one per company, captured during the Sep 5–7 window
- **docs/search_queries.md** — the full 197-query log (45 A / 45 A2 / 35 B / 20 C /
  28 FU / 24 D), so the collection method is reproducible

### Changed
- **README.md rewritten** in a plainer voice: fewer badges, no emoji headers, "what
  this is / what this is not" sections, a working pandas example, and a numbered PR
  checklist. Style matched to the maintainer's other repositories
- README statistics corrected against the master file: September snapshot is 103 rows
  (was listed as 102), 76 verified (was listed as 75), 53 new companies (was listed
  as 52)

---

## [September 2026 — Full Data Audit & Rebuild] — 2026-09-07

This was not a routine monthly append: it was an end-to-end audit and rebuild of the
dataset, pipeline, and repository. Full findings in
[docs/DATA_AUDIT_2026-09-07.md](./docs/DATA_AUDIT_2026-09-07.md).

### Added
- **Canonical master dataset** (`data/master/startups_master.json` + `.csv`) — one
  deduplicated row per company, schema v2.0, the single source of truth
- **52 new companies** fully researched and verified as of 2026-09-06/07, including
  OpenAI's $122B round, Anthropic's $65B round, ElevenLabs, Suno, Thinking Machines Lab,
  Safe Superintelligence, Together AI, Crusoe, Fireworks AI, Baseten, Helsing, Saronic,
  Castelion, Hadrian, Cyera, OpenEvidence, Ramp, Mercury, Plaid, Supabase, ClickHouse,
  Databricks, Groq, Lambda, Physical Intelligence, Apptronik, Generalist AI, Legora,
  Decagon, Harvey, Clay, Mercor, Surge AI, OpenRouter, Owner.com, Emerald AI,
  Instinct, Black Forest Labs, Lovable, and others
- **Schema v2.0**: slug, funding_amount_usd (numeric), valuation fields (separate from
  raised amounts!), last_round_date, investors, city/country/region, status +
  status_note (M&A/IPO), source_urls, last_verified, verification_status, tags, notes
- **scripts/build_snapshots.py** — generate monthly snapshots from master
- **scripts/build_categories.py** — regenerate all 10 category pages from master
- **scripts/check_links.py** — automated website liveness checks
- **CI workflow** (`.github/workflows/validate.yml`) — validates data on every push
- **Monthly reminder workflow** (`.github/workflows/monthly-update.yml`), as promised
  by the README since launch
- **FUNDING.yml** and **assets/banner.svg** (README previously referenced missing files)
- **docs/DATA_AUDIT_2026-09-07.md** — complete audit trail

### Fixed
- **Validator bug**: `validate_data.py` v1 falsely reported "Duplicate IDs" in four
  monthly CSVs (cumulative counter shared across files). Rewritten as v2 with
  per-file counters, schema v2 checks, legacy/strict snapshot modes, CSV↔JSON parity,
  snapshot↔master sync, and stats consistency checks
- **May 2026 stats.json**: duplicate `Series E` JSON key and stage counts summing to
  57 ≠ 60 — regenerated as a derived artifact
- **Anysphere / "Cursor by Anysphere"** listed twice with the same $400M round — merged
  into one entry with full round history
- **"xC" naming drift** (February CSV) — xAI is correctly named in the master dataset
- **Broken markdown links** (Mistral, Maven) in category pages — all pages now generated
  from data; all websites link-checked (bot-blocked 403/429s reviewed manually)
- **Dead links in README** (Jan–Apr JSON files never existed; monthly-update.yml,
  FUNDING.yml, banner.png referenced but missing) — archives table corrected, missing
  infrastructure added

### Changed
- **Corrections to pre-existing entries** (major): Anthropic → $65B at $965B post
  (was "$30B Series D"); Perplexity → Series E at ~$22.6B (was "Series B $1.5B");
  Anduril → Series H $5B at $61B (was "Series F"); Skild AI → Series C $1.4B at $14B
  (was "Series A $300M"); Replit → Series D $400M at $9B (was "Series B $97M");
  Vercel → Series F $300M at $9.3B (was "Series E $250M"); Glean → Series F $150M at
  $7.2B (was "Series D $200M"); Abridge → Series E $300M at $5.3B (was "Series C
  $250M"); DeepJudge → $41.2M Series A (was $20M); Omnea → Series B $50M (was Series
  A $25M); Doppel → Series C $70M (was Series A $35M); Listen Labs → Series B $69M
  (was Series A $15M); LMArena → $150M at $1.7B (was $100M); Runway → Series E $315M
  at $5.3B (was Series D $141M); Figure AI → Series C $1B+ at $39B (was "Series B
  $1.5B+"); Scale AI → Meta 49% at $29B; K Health → corrected to Series F $50M (was
  "Series E $132M"); Harmonic → corrected company identity & $120M Series C; Blossom →
  corrected to $2M seed (was "Series A $22M"); Maven → $9.5M seed (was $4M)
- **Status changes captured**: Wiz → acquired by Google ($32B, completed Mar 11 2026);
  Weights & Biases → acquired by CoreWeave (May 2025); Brex → being acquired by Capital
  One ($5.15B); Sana → acquired by Workday (~$1.1B); Anysphere → pending SpaceX
  acquisition ($60B); OpenRouter → pending Stripe acquisition ($7.5B); Scale AI →
  majority-acquired by Meta (49%)
- **Category normalization**: "Robotics / Defense" and "Robotics / AI" folded into
  Robotics with subcategory/tags; legacy snapshots preserved as-is (warnings in v2
  validator)
- **7 weak entries removed** (documented with reasons in the audit): APILayer (acquired
  by IAC, 2021), Eos AI, EV Structure, Flex, Wise AI, Romantic AI, NoimosAI (all
  unverifiable via credible sources)
- **README rewritten** for schema v2, master-based architecture, corrected badges and
  archive links; CONTRIBUTING updated for the master-dataset workflow

### Removed
- Nothing historical deleted: Jan–May 2026 legacy snapshots preserved untouched for
  traceability; weak entries removed only from the canonical dataset (rationale
  documented in the audit report)

### Highlights
- Global venture funding hit a record **$510B in H1 2026** (Crunchbase), exceeding all
  of 2025; OpenAI and Anthropic alone absorbed ~$217B (43%)
- **Anthropic ($965B)** overtook **OpenAI ($852B)** as the most valuable private company
  after its May 2026 round; IPO chatter points to late 2026
- **M&A wave**: Google-Wiz ($32B, closed), SpaceX-Cursor ($60B, pending), Capital
  One-Brex ($5.15B), Stripe-OpenRouter ($7.5B) — the largest AI consolidation quarter
  on record
- **Defense autonomy boom**: Anduril, Helsing, Shield AI, Saronic, Castelion and Hadrian
  collectively raised $10B+ in 2026
- **Inference infrastructure became the volume business**: Fireworks ($1B ARR), Baseten,
  Together AI, Crusoe, Groq and Lambda all raised mega-rounds

---

## [May 2026] — 2026-05-30

### Added
- **25 new startups** added to the May 2026 dataset
- 60 total startups tracked across 10 categories
- New YC W26 batch startups: Beacon Health, Eos AI, Maven, Seeing Systems, Avoca, Rork, Momentic, Minitap, Coconote, SorceJobs
- New Exploding Topics entries: Romantic AI, Wise AI, Ev Structure, Flex, Atmos Financial, Apilayer
- New category file: `categories/ai-agents.md` for autonomous AI agent startups
- GitHub Actions workflow for automated monthly update reminders
- Python scripts for data validation and monthly updates

### Updated
- Anduril Industries funding updated to $5B (Series F) after record-breaking defense tech round
- OpenAI valuation updated to $852B with $25B annualized revenue
- Adaptive Security valuation updated to ~$9B
- 7AI named to Fast Company's Most Innovative Companies 2026 (#6 in Security)
- Abridge funding updated to $250M Series C
- Viz.ai funding updated to $100M Series D
- K Health funding updated to $132M Series E

### Highlights
- AI startups raised $255.5B globally in Q1 2026, surpassing 2025 full-year total
- YC W26 batch includes 199 companies with 3 AGI labs
- Forbes AI 50 list released for 2026
- Agentic AI emerges as the defining trend of 2026
- Humanoid robotics sector projected to draw $20B+ in funding through 2026

---

## [April 2026] — 2026-04-30

### Added
- **5 new startups** added to the April 2026 dataset
- 25 total startups tracked
- StackOne added from Forbes AI 50 list
- Adaptive Security updated to Series B after $81M raise

### Updated
- Anduril Industries funding updated to $3B+
- Multiple funding stage updates based on Q1 2026 data

---

## [March 2026] — 2026-03-30

### Added
- **20 startups** tracked in the March 2026 dataset
- LMArena added after $100M Series A
- Sana Labs added to EdTech category
- Forbes AI 50 2026 companies incorporated

### Updated
- Anduril Industries updated to Series F
- Abridge updated to Series C, $250M

---

## [February 2026] — 2026-02-28

### Added
- **15 startups** tracked in the February 2026 dataset
- xAI added after landmark $20B Series E
- Cognition (Devin) added to AI Agents category
- Sierra AI added to AI Agents category
- Poolside added to Generative AI category
- 7AI, Doppel, Adaptive Security added to Cybersecurity category

### Highlights
- xAI's $20B Series E marks one of the largest private funding rounds ever
- AI Agents emerge as a distinct startup category

---

## [January 2026] — 2026-01-30

### Added
- **20 startups** in the inaugural January 2026 dataset
- Core dataset schema established (CSV + JSON)
- Category files created for 8 categories
- Repository structure established
- README.md, CONTRIBUTING.md, LICENSE, CODE_OF_CONDUCT.md created

### Highlights
- Repository launched! 🎉
- Initial dataset covers foundation model labs, AI infrastructure, and key vertical startups
