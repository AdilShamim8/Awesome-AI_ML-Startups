# Data Audit & Rebuild Report — September 7, 2026

**Scope:** Full audit and rebuild of the Awesome AI/ML Startups dataset, pipeline, and repository.
**Data cutoff:** September 6–7, 2026. **Method:** Understand → Audit → Research → Rebuild → Integrate → Validate.
**Research base:** ~200 targeted web searches against company announcements, Reuters, Bloomberg, CNBC, TechCrunch, The Information, Newcomer, WSJ, Forbes, Crunchbase, Tracxn, and Y Combinator.

---

## 1. Executive Summary

The repository began as a set of monthly snapshots (Jan–May 2026) where each month re-listed many of the same companies with re-typed descriptions. That produced **no canonical dataset**, redundant work, and silent drift between months. This rebuild introduces a **master dataset as the single source of truth** (103 deduplicated companies, schema v2.0), regenerates snapshots and category pages from it, replaces the broken validator, captures every major funding/valuation/M&A event through September 7, 2026, and adds the missing repository infrastructure (CI, workflows, banner, FUNDING.yml).

**Result:** 103 companies — 76 verified, 26 partial, 1 unverified — every row carrying source URLs, verification dates, numeric funding/valuation fields, and status flags. Historical months are preserved untouched as an archive.

---

## 2. Pre-Rebuild Findings (what was wrong)

| # | Severity | Finding | Remediation |
|---|----------|---------|-------------|
| 1 | Critical | No canonical dataset; ~85% of rows re-listed across months with drifting descriptions | Master dataset + generated snapshots |
| 2 | Critical | Validator bug: cumulative counter across files produced 4 phantom "Duplicate IDs" errors | Validator rewritten (v2), per-file counters |
| 3 | Critical | Data 3+ months stale (no Jun–Aug releases despite "updated on the 30th" promise) | September snapshot generated from master |
| 4 | High | `funding_amount` conflated raised rounds with valuations (OpenAI "$110B", Stripe "$8.5B valuation", Figure "$1.5B+") | Separate `funding_amount_usd` / `valuation_usd` fields |
| 5 | High | Duplicate company: Anysphere (#020) and "Cursor by Anysphere" (#051) | Merged; full round history + SpaceX acquisition status |
| 6 | High | README promised files that didn't exist: monthly-update.yml, FUNDING.yml, banner.png, Jan–Apr JSONs | Infra added; archive links corrected |
| 7 | High | stats.json invalid: duplicate `Series E` key; stage sums 57 ≠ 60 | Regenerated derived artifact; validator now checks sums |
| 8 | High | Stale/wrong stages: Perplexity "Series B $1.5B" (~$22.6B by Jan 2026); Anthropic "$30B Series D" ($65B at $965B by May 2026) | Every entry re-verified against 2026 sources |
| 9 | Medium | Naming drift ("xC" for xAI in February); inconsistent HQ formats; non-startup publics (Duolingo, Lemonade) without policy | Normalized; publics kept with `status: public` |
| 10 | Medium | Category inconsistencies ("Robotics / Defense", "Robotics / AI") | Folded into Robotics + subcategory/tags |
| 11 | Medium | Broken markdown links (Mistral, Maven); dead websites (mavenpayments.io, blossom.team) | Pages generated from data; websites link-checked |
| 12 | Medium | Unverifiable entries (Eos AI, EV Structure, Flex, Wise AI, Romantic AI, NoimosAI) | Removed with documented rationale |
| 13 | Low | No traceability: no source URLs, no verification dates, no investor data | Full provenance fields in schema v2 |

---

## 3. Research Highlights (data as of Sep 6–7, 2026)

**Mega-rounds verified:**
- OpenAI — **$122B committed at $852B post** (Mar 31, 2026, company announcement)
- Anthropic — **$65B at $965B post** (May 29, 2026, Reuters) — now the most valuable private company
- xAI — **$20B Series E at ~$230B** (Jan 6, 2026, upsized from $15B target)
- Anduril — **$5B Series H at $61B** (May 13, 2026); ~$100B round reportedly in talks (Reuters, Jul 24, 2026)
- Helsing — **$1.8B Series E at $18B** (Jul 13, 2026) — Europe's largest defense round
- Crusoe — **$3B+ at ~$30B** (Sep 3, 2026, Bloomberg)

**Corporate events captured (status flags):**
- Google completed its **$32B acquisition of Wiz** (Mar 11, 2026)
- SpaceX agreed to acquire **Anysphere/Cursor for $60B** in stock (Jun 16, 2026)
- Capital One announced **Brex at $5.15B** (Jan 23, 2026)
- Stripe agreed to acquire **OpenRouter for $7.5B** (Aug 19, 2026); itself valued at **$159B** via Feb 2026 tender
- Weights & Biases → CoreWeave (~$1.7B, May 2025); Sana → Workday (~$1.1B, completed)
- Scale AI — Meta purchased 49% at a $29B valuation (Jun 2025)

**Macro context (cited in README):** Global VC $510B in H1 2026 (record; > all of 2025). OpenAI + Anthropic = ~$217B (43%) of H1 funding. AI ≈ 80% of Q1 2026 global VC per Crunchbase.

---

## 4. Rebuild Decisions

1. **Master + snapshots architecture.** `data/master/startups_master.json` is the source of truth; monthly snapshots, category pages, and statistics are generated. Contributors edit only the master.
2. **Schema v2.0, backward compatible.** All 12 original fields retained; 19 fields added. Round amounts and valuations are separate numeric fields so data is finally sortable and comparable.
3. **Flag, don't delete.** Weak/uncertain entries either received honest `verification_status: partial/unverified` with notes, or were removed with documented rationale (7 removals). Public companies (Duolingo, Lemonade, Aurora) kept as reference rows with `status: public`.
4. **Legacy months immutable.** Jan–May 2026 snapshots preserved exactly as published (only the derived May stats.json was regenerated). Validator runs in "legacy" mode for them (warnings, not errors).
5. **Stable IDs.** Companies are ordered by category then name; IDs are stable across future snapshots.

---

## 5. Data Quality Summary

| Metric | Value |
|--------|-------|
| Companies in master | 103 |
| Verification: verified / partial / unverified | 76 / 26 / 1 |
| New companies added in this rebuild | 53 |
| Legacy entries preserved | 50 |
| Categories | 10 (normalized) |
| Countries | USA, UK, Germany, France, Sweden, Switzerland, Canada |
| M&A / status events captured | 7 |
| Websites reachable (automated check) | 90/103; 12 returning 403/429 are bot-blocked but live (verified manually); 1 links to YC page pending a company site |

### Entry-selection criteria

- Funding-verified AI/ML/tech companies, ranked by market significance and data reliability
- Strong bias toward companies with a priced 2025–2026 round or major corporate event
- YC/early-stage entries kept only where the company/round is independently corroborated

### Removal log (7)

| Company | Reason |
|---------|--------|
| APILayer | Acquired by IAC (2021); no longer an independent startup |
| Eos AI | No credible source found; likely conflated entry |
| EV Structure | No credible source found |
| Flex | No credible source found |
| Wise AI | No credible source found; name collision with public company Wise plc |
| Romantic AI | No credible funding source found |
| NoimosAI | No credible source found |

---

## 6. Pipeline & Validation

**Scripts (all runnable, CI-integrated):**
- `scripts/build_snapshots.py` — master → monthly CSV/JSON/stats (idempotent)
- `scripts/build_categories.py` — master → 10 category pages with curated insights
- `scripts/validate_data.py` (v2) — 0 errors across all files:
  schema v2 compliance, controlled vocabularies, URL/date formats, duplicate detection (id + slug), CSV↔JSON parity, snapshot↔master sync, stats sums
- `scripts/check_links.py` — concurrent liveness checks, machine-readable report
- `scripts/generate_readme.py` — statistics generator (master or month mode)
- `scripts/update_monthly.py` — monthly update checklist

**CI:** `.github/workflows/validate.yml` runs the validator + link checks on every push; `.github/workflows/monthly-update.yml` schedules the monthly reminder (the 30th), as the README has promised since launch.

---

## 7. Limitations & Next Steps

- Private-market valuations (tenders, secondaries) fluctuate; `valuation_display` includes the as-of date, and `notes` records conflicts (e.g., Lambda's $2.5B–$6.9B spread).
- Several rounds were in active talks as of Sep 7, 2026 (Thinking Machines at ~$40B, Mercor at ~$20B, Harvey at ~$15.5B, Anduril at ~$100B, Mistral at ~€20B, Physical Intelligence at ~$11B) — recorded in `notes`, not as closed rounds.
- Bot-blocked websites (403/429) require periodic manual review; the link report is machine-readable for that purpose.
- Recommended cadence: refresh `last_verified` monthly during snapshot generation; re-run research sweeps quarterly.
