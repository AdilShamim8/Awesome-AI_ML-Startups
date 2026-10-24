# Data Audit & Refresh Report — October 24, 2026

**Scope:** Full-dataset refresh of the Awesome AI/ML Startups repository: research gap coverage (2026-09-08 → 2026-10-24), verification of prior records, global expansion, pipeline hardening, and the October 24 pre-month-end snapshot.
**Data cutoff:** October 24, 2026 (hard cutoff, enforced by `funding_rounds.json` `metadata.cutoff` and the validator).
**Method:** Baseline audit → gap research → verified updates → new-company intake → pipeline & validation hardening → regeneration → documentation. 46 targeted web queries plus direct fetches of official announcements (Stryker, Walden Robotics, Sarvam, Cognition, Etched, Groq, Suno, Crusoe, ElevenLabs, xAI, Mistral, TypeSafe, Atoms, Sakana).

---

## 1. Executive Summary

The September 7, 2026 rebuild left a seven-week research gap (zero funding events after September 3) and a US-heavy registry: 88 of 103 companies were American, and no Chinese, Japanese, Indian, or Singaporean company was tracked despite those countries' central role in the 2026 AI market. This refresh closes both gaps while treating every existing record as a claim to re-verify.

**Result:** 118 companies (103 retained, 15 added) across 11 countries and 3 regions — 85 verified, 32 partial, 1 unverified — and 193 funding events (172 retained/corrected, 21 added) with $369.4B in verified capital. Five stale major records were corrected to closed rounds, two acquisitions were marked complete (xAI–SpaceX, Anysphere–SpaceX), one new acquisition option was recorded (CMR–Stryker), and one secondary-market valuation mark (ElevenLabs' $22B tender) was recorded with the primary/secondary distinction preserved. The pipeline gained CSV sync generators, five validator checks, 28 unit tests, and the CI workflows the README had claimed but never had.

**Snapshot discipline:** the October file is a pre-month-end research snapshot (`date_published: 2026-10-24`, `snapshot_type: pre-month-end research snapshot`). The October 30 reporting period is not claimed as completed, and the September snapshot is preserved untouched as a historical record.

---

## 2. Pre-Refresh Findings (defects discovered in the baseline audit)

| # | Severity | Finding | Remediation |
|---|----------|---------|-------------|
| 1 | Critical | README claimed "a validation script runs in CI on every push" but `.github/workflows/` did not exist | validate.yml + monthly-reminder.yml added; CI runs validation, CSV parity, and tests |
| 2 | Critical | Zero funding events captured between 2026-09-03 and 2026-10-24 despite at least 15 verifiable rounds in the window | 21 events added (round-173..193) |
| 3 | High | Geographic concentration: 88/103 companies US; no Asia-Pacific presence at all | 7 Asia-Pacific entries added (DeepSeek, Moonshot, Z.ai, MiniMax, Sakana, Sarvam, Manus) |
| 4 | High | `funding_rounds.json` metadata.coverage said "2025-01 through 2026-09" while the file contained 10 pre-2025 events (2022–2024) | Coverage corrected to the actual range with a documented focus window; validator now enforces coverage honesty |
| 5 | High | Registry name-variant bug: events for "Perplexity" (round-058, round-075) and "Cognition AI" (round-073) carried `in_registry=false` although both companies are in the registry — the September build matched names exactly and missed the " AI" suffix | Flags corrected; validator now normalizes name variants (and deliberately does not conflate "Maven AGI" with "Maven") |
| 6 | Medium | Master CSV and funding-rounds CSV had no regeneration path — hand-maintained mirrors certain to drift | `build_master_csv.py` and `build_funding_rounds_csv.py` with `--check` mode; parity enforced in validation and CI |
| 7 | Medium | `funding_rounds.csv` `source_domain` column broken: only 50/172 rows populated, several with split artifacts like `' + elevenlabs.io'` | Domain derived from source_urls for 168/172 rows (4 events have no URL) |
| 8 | Medium | Physical Intelligence event (round-112) dated 2025-11-25 vs the canonical master date 2025-11-20 (company announcement) | Event aligned to canonical; discrepancy documented in the event notes |
| 9 | Medium | Crusoe Series F recorded as "$3B+ at ~$30B" dated Sep 3; the official announcement (Sep 17) states $3.9B at $30.9B post-money | Record and event corrected from the primary source |
| 10 | Medium | xAI recorded as `active` with the SpaceX merger as an "unconfirmed secondary-market report"; the merger was announced Feb 2, finalized May 6, and SpaceX IPO'd Jun 12, 2026 | Status corrected to `acquired` with full deal context |
| 11 | Low | `build_snapshots.py` could only publish month-end snapshots, forcing a mid-month build to mislabel itself | `--date` flag added; pre-month-end type stamped in metadata and stats |
| 12 | Low | `build_categories.py` hardcoded "last updated September 7, 2026" | Derives the date from `master.metadata.as_of` |
| 13 | Low | No tests existed anywhere in the repository | 28 unit tests + integration tests added (stdlib unittest; pytest-compatible) |
| 14 | Low | OpenRouter's recorded source URL (`stripe-acquires-openrouter`) did not match Stripe's published newsroom slug | Corrected to `stripe-agrees-to-acquire-openrouter` |

---

## 3. Research Highlights (data as of 2026-10-24)

**Rounds closed in the gap window and verified:**
- Ramp — **$1.85B primary at $60B** led by Dragoneer (Oct 15, 2026; PRNewswire + Reuters; ARR $2B+)
- Mistral AI — **€3B Series D at €21B (~$24.4B)** led by Samsung with EQT and PSG co-leading (Sep 8, 2026) — the largest European tech equity round ever
- Cognition — **$2B Series E at $48B** led by a16z and Accel (Sep 8, 2026); run-rate revenue $492M → ~$900M in four months
- Harvey — **$550M at $15.5B** co-led by Diffusion and Lightspeed (Sep 9, 2026)
- Crusoe — **$3.9B Series F at $30.9B post-money** (Sep 17, 2026; official newsroom + Reuters); $140B+ TCV, 6GW+ contracted capacity
- Etched — **$700M at $21B led by Jane Street** (Sep 2026) after $300M at $10.3B (Jul 2026); $40–50B offers reported Oct 5 (talks-stage)
- TypeSafe AI — **$870M Series A at $7.5B** led by a16z (Oct 9, 2026) for the Jev decision model
- Walden Robotics — **$300M seed at $1.1B** co-led by Toyota and Deviation Capital (Jul 15, 2026)
- Atoms — **$1.7B led by a16z** (Jul 22, 2026); Travis Kalanick's industrial-automation holding company
- Moonshot AI — **~$2B at $20B** led by Meituan's Long-Z (May 7, 2026)
- DeepSeek — **$7.4B+ first external round at $50B+** (WSJ, Jun 16, 2026)
- Sarvam AI — **$234M first close of $300M Series B at $1.5B** (Jun 15, 2026; HCLTech $150M lead strategic)
- Sakana AI — **$135M Series B at $2.65B** (Nov 17, 2025) plus Google/Salesforce strategic follow-ons
- Manus AI — **$500M+ at $4B** led by Boyu and IDG (Oct 8, 2026) after Beijing unwound Meta's $2B acquisition
- MiniMax — **HK$4.8B (~$620M) IPO** on HKEX (Jan 9, 2026); ~$13.7B first-day close

**Corporate events captured (status flags):**
- **xAI → SpaceX**: all-stock merger announced Feb 2, 2026, finalized May 6, 2026 — xAI valued at ~$250B within the ~$1.25T combined entity; SpaceX IPO'd on Nasdaq Jun 12, 2026 ($75B raised, the largest IPO on record). Status: `acquired`.
- **Anysphere (Cursor) → SpaceX**: $60B all-stock deal announced Jun 16, 2026, closed ~Aug 14, 2026 after regulatory finalization. Status: `acquired`.
- **CMR Surgical ← Stryker**: ~$400M strategic equity investment with an exclusive option to acquire 100% and an exclusive U.S. commercial agency for Versius (Oct 12, 2026). Status: `pending_acquisition`.
- **ElevenLabs**: $300M employee tender at a $22B mark (Sep 30, 2026) — recorded as a secondary transaction; the latest primary round remains the $500M Series D at $11B (Feb 2026).
- **Anthropic**: IPO prospectus filed (seen by Reuters, Sep 28); marketing expected the week of Nov 9, 2026; Q3 revenue $16.8B (+45% QoQ). Remains private.
- **OpenAI**: in talks for $30B+ at $1.25–1.4T with conflicting figures across Reuters (Sep 29), The Guardian (Oct 9), and CNBC (Oct 24). An aggregator claim of a closed $20B round on Oct 1 (aifunding.me) contradicts the talks-stage reporting and is **not recorded** — the conflict is preserved in the OpenAI notes.

**Talks-stage developments recorded in notes only (no events):** OpenAI $30B+ round; Applied Intuition $30B+ offers (The Information, Oct 13); Anduril ~$100B talks (Reuters via TechCrunch, Jul 24); Perplexity Nvidia-led $30B+ talks; Etched $40–50B offers (Oct 5).

**Macro context (cited):** Q3 2026 saw a record count of billion-dollar rounds; AI-driven startups raised $102B, 64% of global VC, in the quarter (Crunchbase, Oct 5, 2026).

---

## 4. Intake Decisions (new companies)

### Entry-selection criteria applied
Same bar as September: a real company with a dated, checkable source for its funding facts; two independent sources preferred for `verified`; single-source or estimate-backed entries enter as `partial` with the limitation named in notes; nothing enters on memory alone.

### Added (15)

| Company | Category | Country | Why it qualifies |
|---------|----------|---------|------------------|
| DeepSeek | Generative AI | China | $7.4B first external round at $50B+ (WSJ) — China's flagship open-weight lab |
| Moonshot AI | Generative AI | China | ~$2B at $20B (TechCrunch); Kimi models, $200M+ ARR |
| Zhipu AI (Z.ai) | Generative AI | China | HKEX listing Jan 2026; ~$29B market cap (Oct 22) — partial (IPO raise not captured) |
| MiniMax | Generative AI | China | HK$4.8B IPO (Reuters) — partial (HQ/founding from public records) |
| Sakana AI | AI/ML | Japan | $135M Series B at $2.65B; official corporate page; Google strategic investment |
| Sarvam AI | AI/ML | India | $234M Series B at $1.5B (official announcement + Bloomberg) |
| Manus AI | AI Agents | Singapore | $500M+ at $4B (Reuters/CNBC/TechCrunch) — partial (HQ from public records) |
| Etched | AI/ML | USA | $700M at $21B led by Jane Street; official site fetched |
| TypeSafe AI | AI/ML | USA | $870M Series A at $7.5B (TechCrunch); Jev model |
| Walden Robotics | Robotics | USA | $300M seed at $1.1B; official launch announcement |
| Atoms | Robotics | USA | $1.7B a16z-led round (TechCrunch) |
| CMR Surgical | Robotics | UK | ~$400M Stryker investment + acquisition option (official Stryker release) |
| Pigment | SaaS | France | $250M at $2.3B — partial (single Tier-3 aggregator source) |
| EliseAI | SaaS | USA | $350M — partial (single Tier-3 roundup source; Aug 2025 round already in events) |
| Norm Ai | AI Agents | USA | $120M Series C at $1.2B — partial (single Tier-2 source, PYMNTS) |

### Deliberately not added (research gaps — documented for the next window)

| Candidate | Reason |
|-----------|--------|
| Fluidstack | $18B valuation verified (Forbes, Sep 3) but headquarters and the exact structure/dates of the $750M at $7B round could not be verified from accessible sources in this window |
| Flapping Airplanes | $1B Series A at $6B fully sourced (TechCrunch/Bloomberg, Oct 21) but no official website could be verified — a required schema field |
| Atlas Atomics | $400M Series A at $1.9B verified (Bloomberg/Axios, Oct 9) but headquarters not captured and the AI-data-center positioning could not be confirmed from primary text |
| ASI | $325M Series C at $3.0B per a single aggregator listing; company identity too thin to record responsibly |
| Armadin | $255.5M Series B per two Tier-3 aggregators; headquarters and product detail unverified |
| doxx.net / Halluminate / Reco | Single thin mentions in one roundup; below the intake bar |

---

## 5. Data Quality Summary

| Metric | September 7 | October 24 | Δ |
|--------|-------------|------------|---|
| Companies | 103 | 118 | +15 |
| Countries | 7 | 11 | +4 (China, Japan, India, Singapore) |
| Asia-Pacific entries | 0 | 7 | +7 |
| Funding events | 172 | 193 | +21 |
| Verified capital (events) | ~$352.9B tracked | $369.4B verified (+$15.6B reported, flagged partial) | — |
| Verified companies | 76 | 85 | +9 |
| Partial companies | 26 | 32 | +6 (single-source intake, honestly labeled) |
| Unverified | 1 | 1 | — |
| Distinct source domains | 91 | 103 | +12 |
| Mega-rounds (≥$100M) | — | 165 | — |
| Evidence blocks | 152 | 188 | +36 |
| Unit tests | 0 | 28 | +28 |
| CI workflows | 0 (README claimed they existed) | 2 | +2 |

**Verification-status distribution (companies):** 85 verified / 32 partial / 1 unverified.
**Verification-status distribution (events):** 156 verified / 37 partial.
**Category distribution:** AI/ML 24, Robotics 20, Generative AI 19, DevTools 12, AI Agents 10, FinTech 9, HealthTech 7, SaaS 7, Cybersecurity 6, EdTech 4.
**Geographic distribution:** USA 94, UK 6, China 4, Germany 3, France 3, Sweden 3, Japan 1, India 1, Singapore 1, Canada 1, Switzerland 1.
**Status distribution:** active 104, acquired 6, public 5, pending_acquisition 2, majority_acquired 1.

---

## 6. Corrections to Existing Records

| Company | Before | After | Source |
|---------|--------|-------|--------|
| Crusoe | $3B+ at ~$30B, dated 2026-09-03 | $3.9B at $30.9B post-money, 2026-09-17 | Official newsroom + Reuters |
| Mistral AI | Series C €1.7B at €11.7B (Sep 2025); talks noted | Series D €3B at €21B (~$24.4B), 2026-09-08; €830M debt kept out of funding_amount | Official + TechCrunch + Reuters |
| Cognition | Series C $1B at $26B (May 2026) | Series E $2B at $48B, 2026-09-08 | Official blog + Bloomberg |
| Harvey | Series G $200M at $11B (Mar 2026) | $550M at $15.5B, 2026-09-09 (stage "Late Stage" — label undisclosed) | Official + Reuters |
| Ramp | $750M at $44B (Jun 2026) | $1.85B at $60B, 2026-10-15 (Late Stage) | PRNewswire + Reuters |
| xAI | active; merger "unconfirmed report" | acquired by SpaceX (announced Feb 2, finalized May 6, 2026) | Forge Global, TSG, Reuters (IPO) |
| Anysphere | pending_acquisition (announced Jun 16) | acquired (closed ~Aug 14, 2026) | SatNews + contemporaneous reporting |
| ElevenLabs | $11B (Feb 2026 Series D) | valuation_display carries the $22B tender mark with the primary/secondary distinction; funding fields unchanged | TechCrunch + Bloomberg + Reuters |
| Groq | Series E (Aug 2026) | Series A per official branding of the restructured Groq LLC; restructuring documented | Official newsroom |
| OpenRouter | pending; URL mismatch | pending with deal context ($7.5B per NYT); corrected Stripe URL | Stripe newsroom + NYT + Bloomberg |
| Physical Intelligence (event) | round-112 dated 2025-11-25 | aligned to canonical 2025-11-20 | Master record / company blog |

Plus context-notes updates (no round changes): OpenAI, Anthropic, Perplexity, Scale AI, Applied Intuition, Anduril, Legora.

---

## 7. Pipeline & Validation Changes

1. **`scripts/build_master_csv.py`** — regenerates the master CSV from canonical JSON; `--check` mode for CI. Verified byte-identical against the hand-maintained file before first use.
2. **`scripts/build_funding_rounds_csv.py`** — same for the events CSV; derives a clean `source_domain` (168/172 → 168/193 populated).
3. **`scripts/validate_data.py`** — five new checks: master/rounds CSV parity, content-level duplicate events (company+date+amount), coverage honesty, cutoff enforcement (events after `metadata.cutoff` are errors), registry name-variant and staleness cross-checks; plus an amount-equals-valuation heuristic warning.
4. **`scripts/build_snapshots.py`** — `--date` support for pre-month-end snapshots; dead code removed; stats carry `date_published`/`snapshot_type`.
5. **`scripts/build_categories.py`** — dates derived from master metadata.
6. **`tests/test_validate.py`** — 28 tests (vocabularies, required fields, duplicates, URL/date formats, name normalization including the Maven AGI non-conflation case, ValidationResult contract, live-data integration).
7. **`.github/workflows/validate.yml`** — validation, both CSV sync checks, and unit tests on every push/PR.
8. **`.github/workflows/monthly-reminder.yml`** — opens the monthly checklist issue on the 28th.

**Final validation run (2026-10-24):** 0 errors. Warnings are limited to (a) the five legacy 2026 Jan–May snapshot categories that are preserved as historical records, (b) the September snapshot's 103-vs-118 count — intentional, historical preservation, (c) the DeepSeek round-193 staleness signal — intentional: the reported-in-progress round is newer than the last *confirmed* master round, exactly the signal the check exists to emit, and (d) two amount-equals-valuation heuristic notes on acquisition-priced records (OpenRouter, Brex) where the match is legitimate.

---

## 8. Limitations & Next Steps

**Honest limitations of this refresh:**
- Several auxiliary fields for new international companies (websites, founding years, HQs for Zhipu/MiniMax/Manus) rest on established public records rather than a source URL captured in this window; those records are `partial` with the limitation named. The link check (below) retroactively verified all 15 new websites as live (14 reachable, CMR Surgical bot-blocked). The next window should still capture primary citations for the founding years and HQs.
- Month-precision dates (Etched July/September, Groq June, Norm Ai July) use the month-end convention and are flagged in each event's notes.
- DeepSeek's October ~$15B round, OpenAI's $30B+ talks, and similar reported-but-unconfirmed items are recorded as partial events or notes only; totals labeled "verified capital" exclude them.
- Link check re-run on 2026-10-24 across all 118 websites: 104 reachable, 13 bot-blocked (HTTP 403/429 — not failures), 1 failing (Starship Technologies, ERR:URLError reproduced on three attempts; needs manual browser verification and was not flagged in September). Bot-blocked sites were not re-verified manually in a browser this window.
- The October window could not verify Fluidstack, Flapping Airplanes, Atlas Atomics, ASI, and Armadin to the intake bar — see the research-gaps table above.

**Recommended next steps:**
1. Complete verification for the six gap candidates and add them if they clear the bar.
2. Capture primary sources for the public-record fields on new international entries (websites, founding years, HQs).
3. Watch the November pipeline events: Anthropic's IPO marketing (week of Nov 9), the OpenAI $30B+ round, the Stripe–OpenRouter close, and DeepSeek's round finalization.
4. Run the full link check (`scripts/check_links.py`) with manual review of 403/429 results before the October 30 snapshot.
5. Consider a `source_urls`-per-event lint that requires at least one URL resolving to a domain already cited twice (anti-typo measure).
