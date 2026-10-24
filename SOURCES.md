# Data Sources & Collection Methodology

Every number in this dataset points back to a source that anyone can open and check.
This page documents the full chain: where the data comes from, how it was collected,
how it was verified, and the exact source used for each of the 118 companies.

> Last updated: 2026-10-24 · Dataset: [118 companies](data/master/startups_master.json) · Evidence appendix: [docs/evidence_log.md](docs/evidence_log.md) · Query log: [docs/search_queries.md](docs/search_queries.md) · October audit: [docs/DATA_AUDIT_2026-10-24.md](docs/DATA_AUDIT_2026-10-24.md)

---

## Where the dataset comes from

No single database was dumped into this repo. Each company entry was assembled from
public reporting, and each entry stores its own `source` labels and `source_urls` array
inside [the master dataset](data/master/startups_master.json). The sources fall into
five groups:

| Group | Sources | Used for |
|-------|---------|----------|
| Company announcements | Official blogs, press releases, investor pages (e.g. cursor.com, anduril.com, stripe.com, blog.fal.ai) | Round terms, valuations, M&A — the primary record |
| Financial press | Reuters, Bloomberg, CNBC, The Wall Street Journal, Financial Times | Independent confirmation of round size, valuation, investors |
| Tech press | TechCrunch, The Information, Newcomer | Funding details, product context, early-stage coverage |
| Funding databases | Crunchbase, Tracxn, Sacra | Round histories and cross-checks (never used alone) |
| Accelerator & rankings | Y Combinator directory, Forbes lists | Early-stage company facts, founded year, HQ |

Across the 103 companies the dataset cites 91 distinct source domains
(103 source URLs in total). The most-used domains:

| # | Source domain | Entries citing it |
|---|---------------|-------------------|
| 1 | ycombinator.com | 7 |
| 2 | reuters.com | 3 |
| 3 | techcrunch.com | 3 |
| 4 | sacra.com | 2 |
| 5 | stripe.com | 2 |
| 6 | 1x.tech | 1 |
| 7 | abnormal.ai | 1 |
| 8 | abridge.com | 1 |
| 9 | adaptivesecurity.com | 1 |
| 10 | anduril.com | 1 |
| 11 | appliedintuition.com | 1 |
| 12 | apptronik.com | 1 |
| 13 | arena.ai | 1 |
| 14 | baseten.co | 1 |
| 15 | bfl.ai | 1 |

---

## How the dataset was collected

The September 2026 rebuild was collected between **September 5–7, 2026** in six steps.
Nothing was generated from memory — every entry below traces to a search result or a page
that was actually fetched during this window.

### Step 1 — Seed list

The 61 unique companies already tracked in the January–May 2026 snapshots formed the
starting list. Each was re-verified from scratch rather than carried over on trust: old
fields were treated as *claims*, not facts.

### Step 2 — 197 targeted searches

A tiered query plan was executed against the live web (145 core queries, 28 follow-ups,
24 late additions — full log in [docs/search_queries.md](docs/search_queries.md)):

| Pass | Queries | Purpose |
|------|---------|---------|
| Core (Tier A) | 45 | Latest funding round + valuation for each tracked company |
| Core (Tier A2) | 45 | Second pass per company: investors, round dates, conflicting reports |
| Core (Tier B) | 35 | Landscape sweeps per category (who raised recently that we are missing) |
| Core (Tier C) | 20 | Macro context (global VC totals, AI share of funding) |
| Follow-up (FU) | 28 | Gaps found in pass 1: conflicting numbers, missing dates, investors |
| Late additions (D) | 24 | Companies discovered during the rebuild (e.g. late-August / September rounds) |
| **Total** | **197** | |

Each search returned dated snippets with source domains; every result was stored on disk,
so the evidence trail can be re-audited without re-running anything.

### Step 3 — Two-pass verification

For every company, two independent source types were preferred before marking an entry
`verified`:

1. **Primary** — the company's own announcement (blog post, press release, investor page)
2. **Financial press** — Reuters / Bloomberg / CNBC / WSJ / FT confirming the same figures

Entries where only one source type could be found are marked `partial` with a note.
One entry where figures could not be confirmed at all is marked `unverified`.
The current split: **76 verified /
26 partial /
1 unverified**.

### Step 4 — Extraction rules

- `funding_amount` = money **raised** in the latest round. `valuation_display` = what the
  company was **worth**. These are separate fields — earlier releases of this repo
  conflated them (e.g. OpenAI's "$110B" was a valuation, not a round).
- Amounts were normalized to `funding_amount_usd` (numeric) for sorting; display strings
  keep the original currency where the source used one (e.g. Mistral's €1.7B).
- Acquisitions record the deal value and acquirer in `status_note`, with `status` set to
  `acquired` / `pending_acquisition` / `majority_acquired`.

### Step 5 — Link check

All 103 website URLs were checked for liveness (103/ responded;
a handful of sites block bots with HTTP 403/429 and were verified manually in a browser).
The latest report: [data/master/link_check_report.json](data/master/link_check_report.json).

### Step 6 — Validation

`scripts/validate_data.py` runs in CI on every push: schema compliance, controlled
vocabularies, duplicate detection by both `id` and `slug`, master CSV/JSON parity,
event cutoff enforcement, coverage honesty, registry cross-checks, and
snapshot-vs-master sync — plus 28 unit tests (`python -m unittest discover -s tests`).

### What this dataset deliberately does not do

- No invented entries — a company is only added if a real, datable source exists
- No scraped-database dumps — database hits are cross-checks, not the record itself
- No silent estimates — every caveat lives in the entry's `notes` field
- No stale "as of" blur — every entry carries `last_verified` (2026-10-24 for this release)
- No reported-as-closed confusion — talks-stage rounds (OpenAI, Applied Intuition,
  Anduril, Etched's $40-50B offers) stay in notes; DeepSeek's reported ~$15B October
  round is a `partial` event explicitly excluded from verified-capital totals
- No primary/secondary blur — ElevenLabs' $22B tender mark is labeled an employee
  tender; its funding fields still describe the last primary round

---

## The October 2026 research window (added 2026-10-24)

The October refresh ran a 46-query research pass against the 2026-09-08 → 2026-10-24
gap plus global expansion sweeps. Conventions added in this window:

| Rule | Application |
|------|-------------|
| Reported ≠ closed | Talks-stage items are recorded in `notes`, never as events; DeepSeek's reported October round is a `partial` event with the in-progress caveat in its notes |
| Primary ≠ secondary/debt | Tenders (ElevenLabs) and debt (Mistral's €830M) are kept out of `funding_amount`; tenders may set `valuation_usd` with the type labeled in `valuation_display` |
| Month-precision dates | When only the month is sourced, the event is dated month-end and flagged in `notes` (e.g. Etched's July/September rounds, Groq's June financing, Norm Ai's July round) |
| Single-source intake | One Tier-3 source → `partial` with the source tier named (Pigment, EliseAI's October round); one Tier-2 source → `partial` (Norm Ai) |
| Public-record fields | Where a new company's funding is fully sourced but an auxiliary field (website, HQ, founding year) was not directly cited, the record is `partial` with that limitation named (Zhipu, MiniMax, Manus) |
| Cutoff enforcement | `funding_rounds.json` now carries `metadata.cutoff: 2026-10-24`; the validator errors on any event beyond it |

New source domains cited in this window include stryker.com, waldenrobotics.com,
sarvam.ai, cognition.com, etched.com, groq.com (newsroom), x.ai, sakana.ai,
atoms.co, wsj.com, scmp.com, nikkei.com, prnewswire.com, globenewswire.com,
theinformation.com, pymnts.com — bringing the dataset to 103 distinct cited domains.

---

## Per-company source registry

The table below lists, for each of the 118 companies, the cited source names,
direct URLs, verification status, and the date the facts were last checked. The fuller
search evidence (dated snippets from each source) is in
[docs/evidence_log.md](docs/evidence_log.md).

| # | Company | Source(s) | Source URL(s) | Last verified | Status |
|---|---------|-----------|---------------|---------------|--------|
| 1 | **Baseten** | Reuters, TechCrunch, Baseten (official) | <https://www.baseten.co/blog/series-f> | 2026-09-07 | verified |
| 2 | **Cleanlab** | Crunchbase, DHRmap, Menlo Ventures | <https://cleanlab.ai/blog/> | 2026-09-07 | partial |
| 3 | **Crusoe** | Crusoe (official), Reuters, GlobeNewswire | <https://www.crusoe.ai/resources/newsroom/crusoe-announces-series-f-funding> | 2026-10-24 | verified |
| 4 | **Databricks** | Cryptobriefing via filings, SeedTable, Chopping Block | <https://www.databricks.com/company/newsroom> | 2026-09-07 | partial |
| 5 | **Emerald AI** | Business Wire, LinkedIn/press, Emerald AI (official) | <https://www.emeraldai.co/news> | 2026-09-07 | verified |
| 6 | **Encord** | Encord (official), LinkedIn/press | <https://encord.com/blog> | 2026-09-07 | verified |
| 7 | **fal** | fal (official), TechCrunch, The Information | <https://blog.fal.ai/series-d/> | 2026-09-07 | verified |
| 8 | **Fireworks AI** | Fireworks AI (official), Sacra, Bloomberg | <https://fireworks.ai/blog/series-d> | 2026-09-07 | verified |
| 9 | **Glean** | Glean (official), TechCrunch, Forbes | <https://www.glean.com/company/news> | 2026-09-07 | verified |
| 10 | **Groq** | Groq (official), Sacra, Yahoo Finance | <https://groq.com/newsroom/groq-closes-usd350-million-series-a-building-the-world-s-leading-ai-inference-cloud> | 2026-10-24 | verified |
| 11 | **Hebbia** | Hebbia (official), Sacra, PitchBook | <https://www.hebbia.com/news> | 2026-09-07 | verified |
| 12 | **Hugging Face** | Reuters, Business Insider via TechCrunch, Tracxn | <https://www.reuters.com/technology/hugging-face-valued-4-5-billion-2023-08-24/> | 2026-09-07 | verified |
| 13 | **Lambda** | Lambda (official), TechCrunch, Tracxn | <https://lambda.ai/blog> | 2026-09-07 | partial |
| 14 | **Listen Labs** | Fortune, Yahoo Finance, Listen Labs (official) | <https://www.listenlabs.com/blog> | 2026-09-07 | verified |
| 15 | **LMArena** | Reuters, TechCrunch, LMArena (official) | <https://arena.ai/blog/lmarena-series-a> | 2026-09-07 | verified |
| 16 | **Mercor** | CNBC, Forbes, Bloomberg | <https://www.cnbc.com/2025/10/27/mercor-350-million-series-c.html> | 2026-09-07 | verified |
| 17 | **Scale AI** | Reuters, Forbes, Turing Post, KuCoin News | <https://scale.com/blog> | 2026-10-24 | verified |
| 18 | **Surge AI** | Reuters, Bloomberg, Sacra | <https://www.reuters.com/technology/surge-ai-hires-advisers-raise-up-to-1-billion-2025-07-01/> | 2026-09-07 | partial |
| 19 | **Together AI** | Reuters, Business Wire, Together AI (official) | <https://www.together.ai/blog/series-c> | 2026-09-07 | verified |
| 20 | **Weights & Biases** | CoreWeave IR, TechCrunch, Tracxn | <https://investors.coreweave.com/news> | 2026-09-07 | verified |
| 21 | **Anthropic** | Reuters, WSJ, Anthropic (official) | <https://www.reuters.com/business/finance/anthropics-ipo-prospectus-shows-sweeping-ai-vision-surging-costs-2026-09-28>; <https://www.reuters.com/legal/transactional/anthropic-ipo-stands-alone-ai-market-jitters-sideline-others-2026-10-22> | 2026-10-24 | verified |
| 22 | **Black Forest Labs** | Black Forest Labs (official), FT, Crunchbase | <https://bfl.ai/blog> | 2026-09-07 | verified |
| 23 | **Cohere** | Cohere (official), TechCrunch, CNBC | <https://cohere.com/blog/series-d-500m> | 2026-09-07 | verified |
| 24 | **ElevenLabs** | ElevenLabs (official), TechCrunch, Reuters, Bloomberg | <https://elevenlabs.io/blog/series-d>; <https://techcrunch.com/2026/09/30/ai-voice-startup-elevenlabs-doubles-valuation-to-22b> | 2026-10-24 | verified |
| 25 | **Midjourney** | Sacra, Tracxn, Contrary Research | <https://sacra.com/c/midjourney/> | 2026-09-07 | partial |
| 26 | **Mistral AI** | Mistral AI (official), TechCrunch, Reuters, Tracxn | <https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier> | 2026-10-24 | verified |
| 27 | **OpenAI** | OpenAI (official), Reuters, CNBC, The Guardian | <https://openai.com/index/accelerating-the-next-phase-ai>; <https://www.reuters.com/legal/transactional/openai-targets-30-billion-funding-14-trillion-valuation-bloomberg-news-reports-2026-09-29> | 2026-10-24 | verified |
| 28 | **Perplexity AI** | Reuters, CNBC, The Information (via Reuters) | <https://tracxn.com/d/companies/perplexity> | 2026-10-24 | verified |
| 29 | **Poolside** | Newcomer, Bloomberg, Crunchbase | <https://www.newcomer.co/p/poolside-strikes-6-billion-licensing> | 2026-09-07 | verified |
| 30 | **Runway** | TechCrunch, Crunchbase News | <https://techcrunch.com/2026/02/10/runway-raises-315m-series-e/> | 2026-09-07 | verified |
| 31 | **Safe Superintelligence** | TechCrunch, Reuters, Bloomberg | <https://techcrunch.com/2025/04/12/safe-superintelligence-reportedly-valued-at-32b/> | 2026-09-07 | verified |
| 32 | **Suno** | Suno (official), Reuters, Variety | <https://suno.com/blog/series-d> | 2026-09-07 | verified |
| 33 | **Synthesia** | Synthesia (official), Investing.com, eWeek | <https://www.synthesia.io/news> | 2026-09-07 | verified |
| 34 | **Thinking Machines Lab** | The Information, Reuters, TechCrunch | <https://www.theinformation.com/briefings/thinking-machines-lab-in-talks-for-1b-at-40b-valuation> | 2026-09-07 | verified |
| 35 | **xAI** | xAI (official), CNBC, Forge Global, Reuters | <https://x.ai/news/series-e>; <https://forgeglobal.com/xai_ipo> | 2026-10-24 | verified |
| 36 | **Clay** | TechCrunch, Crunchbase News, Business Wire | <https://www.clay.com/blog> | 2026-09-07 | verified |
| 37 | **Cognition** | Cognition (official), Bloomberg, TechCrunch | <https://cognition.com/blog/series-e> | 2026-10-24 | verified |
| 38 | **Decagon** | Bloomberg, Forbes, Decagon (official) | <https://decagon.ai/news> | 2026-09-07 | verified |
| 39 | **Harvey** | Harvey (official), Reuters, TechCrunch | <https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence> | 2026-10-24 | verified |
| 40 | **Instinct** | WSJ, Yahoo Finance, AI Pressroom | <https://www.wsj.com/tech/ai> | 2026-09-07 | partial |
| 41 | **LangChain** | LangChain (official), TechCrunch | <https://www.langchain.com/blog> | 2026-09-07 | verified |
| 42 | **Legora** | Legora (official), PYMNTS, Reuters | <https://legora.com> | 2026-10-24 | verified |
| 43 | **Sierra** | Sierra (official), CNBC, TechCrunch | <https://sierra.ai/news> | 2026-09-07 | verified |
| 44 | **Blossom** | StartupIntros, Blossom (official) | <https://www.blossom.team/about> | 2026-09-07 | partial |
| 45 | **DeepJudge** | Startupticker, Forbes, Law.com | <https://www.deepjudge.ai/news> | 2026-09-07 | verified |
| 46 | **Omnea** | Omnea (official), TechCrunch | <https://www.omnea.co/news> | 2026-09-07 | verified |
| 47 | **Owner** | Intellectia, Simplify, Bitpush, Goldman Sachs | <https://owner.com/press> | 2026-09-07 | verified |
| 48 | **Sorce** | Y Combinator, SignalBase | <https://www.ycombinator.com/companies/sorce> | 2026-09-07 | partial |
| 49 | **Anysphere** | Reuters, CNBC, SatNews, NYT | <https://www.reuters.com/legal/transactional/spacex-buy-anysphere-60-billion-2026-06-16> | 2026-10-24 | verified |
| 50 | **ClickHouse** | ClickHouse (official), Bloomberg | <https://clickhouse.com/blog> | 2026-09-07 | verified |
| 51 | **Lovable** | Reuters, TechCrunch, Lovable (official) | <https://lovable.dev/blog> | 2026-09-07 | verified |
| 52 | **Minitap** | French Tech Journal, Tracxn, LinkedIn/press | <https://minitap.ai/blog> | 2026-09-07 | partial |
| 53 | **Momentic** | LinkedIn/press, SaaS Startups | <https://www.momentic.ai/blog> | 2026-09-07 | partial |
| 54 | **OpenRouter** | Stripe (official), NYT, Bloomberg, Fortune | <https://stripe.com/newsroom/news/stripe-agrees-to-acquire-openrouter> | 2026-10-24 | verified |
| 55 | **Replit** | Replit (official), CNBC, TribeTechie | <https://replit.com/news> | 2026-09-07 | verified |
| 56 | **Rork** | Y Combinator | <https://www.ycombinator.com/companies/rork> | 2026-09-07 | unverified |
| 57 | **StackBlitz** | Sacra, Tracxn, Panto | <https://sacra.com/c/stackblitz-bolt-new/> | 2026-09-07 | partial |
| 58 | **StackOne** | Tracxn, StackOne (official) | <https://www.stackone.com/blog> | 2026-09-07 | partial |
| 59 | **Supabase** | Supabase (official), CNBC, TechCrunch | <https://supabase.com/blog> | 2026-09-07 | verified |
| 60 | **Vercel** | Vercel (official), Reuters, GIC | <https://vercel.com/blog/series-f> | 2026-09-07 | verified |
| 61 | **Atmos Financial** | StartupIntros, Climatebase, Impakter | <https://www.joinatmos.com/about> | 2026-09-07 | partial |
| 62 | **Brex** | Crunchbase News, Capital One IR, LinkedIn analysis | <https://investor.capitalone.com> | 2026-09-07 | verified |
| 63 | **Harmonic** | StartupIntros, Harmonic (official) | <https://www.harmonic.ai/about> | 2026-09-07 | partial |
| 64 | **Lemonade** | Startup Nation Finder, Yahoo Finance, Lemonade IR | <https://investor.lemonade.com> | 2026-09-07 | verified |
| 65 | **Maven** | Newcomer, Y Combinator | <https://www.ycombinator.com/companies/maven> | 2026-09-07 | partial |
| 66 | **Mercury** | CNBC, Mercury (official), Crunchbase News | <https://mercury.com/newsroom> | 2026-09-07 | verified |
| 67 | **Plaid** | Bloomberg, Yahoo Finance, Crunchbase News | <https://plaid.com/about/press/> | 2026-09-07 | verified |
| 68 | **Ramp** | Ramp (official, PRNewswire), Reuters, Bloomberg | <https://www.prnewswire.com/news-releases/ramp-reaches-60-billion-valuation-as-annualized-revenue-tops-2-billion-302909315.html> | 2026-10-24 | verified |
| 69 | **Stripe** | CNBC, Yahoo Finance, Stripe (official), NYT | <https://stripe.com/newsroom> | 2026-09-07 | verified |
| 70 | **Abridge** | Abridge (official), Fierce Healthcare, ValueAdd VC | <https://www.abridge.com/blog> | 2026-09-07 | verified |
| 71 | **Avoca** | PitchBook, PR Newswire, Y Combinator | <https://www.ycombinator.com/companies/avoca> | 2026-09-07 | partial |
| 72 | **Beacon Health** | Y Combinator, Extruct, Beacon Health (official) | <https://www.ycombinator.com/companies/beacon-health> | 2026-09-07 | partial |
| 73 | **Hippocratic AI** | Fierce Healthcare, LinkedIn/press, MobiHealthNews | <https://www.hippocraticai.com/news> | 2026-09-07 | verified |
| 74 | **K Health** | Fierce Healthcare, Business Wire, EquityBee | <https://khealth.com/about> | 2026-09-07 | partial |
| 75 | **OpenEvidence** | Becker's Hospital Review, mobihealthnews, PR Newswire | <https://www.openevidence.com/news> | 2026-09-07 | verified |
| 76 | **Viz.ai** | Viz.ai (official), EquityBee, Tracxn | <https://www.viz.ai/company> | 2026-09-07 | partial |
| 77 | **1X Technologies** | Sacra, Nasdaq Private Market, 1X (official) | <https://www.1x.tech/investors> | 2026-09-07 | partial |
| 78 | **Anduril Industries** | Anduril (official), CNBC, NYT, TechCrunch | <https://www.anduril.com/article/series-h> | 2026-10-24 | verified |
| 79 | **Applied Intuition** | Applied Intuition (official), The Information, Seeking Alpha | <https://www.appliedintuition.com/blog/series-f> | 2026-10-24 | verified |
| 80 | **Apptronik** | Apptronik (official), CNBC, Bloomberg | <https://apptronik.com/news> | 2026-09-07 | verified |
| 81 | **Aurora Innovation** | TechCrunch, TTNews, Aurora (official) | <https://ir.aurora.tech> | 2026-09-07 | verified |
| 82 | **Castelion** | TechCrunch, Castelion (official), ValueAdd VC | <https://www.castelion.com/news> | 2026-09-07 | verified |
| 83 | **Figure AI** | Figure AI (official), The Robot Report, Reuters | <https://www.figure.ai/news> | 2026-09-07 | verified |
| 84 | **Generalist AI** | Generalist (official), Bloomberg, Axios | <https://www.generalistai.com/news> | 2026-09-07 | partial |
| 85 | **Hadrian** | TechCrunch, CNBC | <https://techcrunch.com/2026/08/06/hadrian-raises-1-37b/> | 2026-09-07 | verified |
| 86 | **Helsing** | Helsing (official), CNBC, FT | <https://helsing.ai/newsroom> | 2026-09-07 | verified |
| 87 | **Nuro** | Nuro (official), Built In SF, Tracxn | <https://www.nuro.ai/press> | 2026-09-07 | verified |
| 88 | **Physical Intelligence** | The Robot Report, Bloomberg, TechCrunch | <https://www.physicalintelligence.company/blog> | 2026-09-07 | verified |
| 89 | **Saronic** | PR Newswire, CNBC, Reuters | <https://www.saronic.com/news> | 2026-09-07 | verified |
| 90 | **Seeing Systems** | Y Combinator, Tectonic Defense, LinkedIn | <https://www.ycombinator.com/companies/seeing-systems> | 2026-09-07 | partial |
| 91 | **Shield AI** | Shield AI (official), TechCrunch, Tracxn | <https://shield.ai/news> | 2026-09-07 | verified |
| 92 | **Skild AI** | Skild AI (official), Bloomberg, Crunchbase News | <https://www.skild.ai/blog> | 2026-09-07 | verified |
| 93 | **Starship Technologies** | Starship (official), StartupIntros, TechCrunch | <https://www.starship.xyz/newsroom> | 2026-09-07 | partial |
| 94 | **7AI** | WSJ, 7AI (official), Calcalist, Tracxn | <https://blog.7ai.com> | 2026-09-07 | verified |
| 95 | **Abnormal AI** | Crunchbase News, Abnormal (official), Tracxn | <https://abnormal.ai/news> | 2026-09-07 | verified |
| 96 | **Adaptive Security** | Adaptive Security (official), PR Newswire | <https://www.adaptivesecurity.com/news> | 2026-09-07 | verified |
| 97 | **Cyera** | Cyera (official), Reuters | <https://www.cyera.com/news> | 2026-09-07 | verified |
| 98 | **Doppel** | LinkedIn (company), The Cube, SecurityWeek | <https://www.doppel.ai/blog> | 2026-09-07 | partial |
| 99 | **Wiz** | Google Cloud Press, CRN, PR Newswire | <https://cloud.google.com/press-corner> | 2026-09-07 | verified |
| 100 | **Coconote** | Tracxn, Y Combinator | <https://www.ycombinator.com/companies/coconote> | 2026-09-07 | partial |
| 101 | **Duolingo** | Tracxn, EdSurge, TechCrunch | <https://investors.duolingo.com> | 2026-09-07 | verified |
| 102 | **MagicSchool AI** | MagicSchool (official), Forge, Tracxn | <https://www.magicschool.ai/about> | 2026-09-07 | partial |
| 103 | **Sana** | Workday Newsroom, Orrick, Reddit reporting | <https://newsroom.workday.com> | 2026-09-07 | verified |
| 104 | **DeepSeek** | WSJ, TechCrunch, Reuters | <https://www.wsj.com/tech/ai/deepseek-becomes-chinas-most-valuable-ai-startup-after-over-7-4-billion-fundraise-78ef64c0>; <https://techcrunch.com/2026/10/22/deepseek-reportedly-raises-15b-days-after-us-restrictions> | 2026-10-24 | verified |
| 105 | **Moonshot AI** | TechCrunch, Bloomberg, mlq.ai | <https://techcrunch.com/2026/05/07/chinas-moonshot-ai-raises-2b-at-20b-valuation-as-demand-for-open-source-ai-skyrockets>; <https://www.bloomberg.com/news/articles/2026-09-11/china-ai-star-moonshot-eyes-2-billion-annualized-sales-in-2026> | 2026-10-24 | verified |
| 106 | **Zhipu AI (Z.ai)** | TechCrunch, SCMP, 36kr, AI Proem | <https://techcrunch.com/2026/10/22/deepseek-reportedly-raises-15b-days-after-us-restrictions>; <https://www.scmp.com/tech/big-tech/article/3356390/minimax-once-led-zhipu-hong-kongs-ai-stock-race-how-tables-have-turned> | 2026-10-24 | partial |
| 107 | **MiniMax** | Reuters, AI Proem, TechCrunch | <https://www.reuters.com/world/asia-pacific/china-ai-firm-minimax-set-surge-hong-kong-debut-2026-01-09>; <https://techcrunch.com/2026/10/22/deepseek-reportedly-raises-15b-days-after-us-restrictions> | 2026-10-24 | partial |
| 108 | **Manus AI** | Reuters, CNBC, TechCrunch, Nikkei Asia | <https://www.reuters.com/world/china/manus-raises-more-than-500-million-after-meta-exit-2026-10-08>; <https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta> | 2026-10-24 | partial |
| 109 | **Sakana AI** | Sakana AI (official), Bloomberg, Tracxn | <https://sakana.ai/company-info>; <https://www.bloomberg.com/news/articles/2026-01-23/google-invests-in-sakana-ai-to-boost-gemini-s-presence-in-japan> | 2026-10-24 | verified |
| 110 | **Sarvam AI** | Sarvam AI (official), Bloomberg, Tracxn | <https://www.sarvam.ai/announcing-series-b>; <https://www.bloomberg.com/news/articles/2026-04-02/india-ai-startup-sarvam-raises-funds-at-1-5-billion-valuation> | 2026-10-24 | verified |
| 111 | **Etched** | Etched (official), Reuters, TechCrunch, American Bazaar | <https://www.etched.com>; <https://americanbazaaronline.com/2026/10/06/etched-draws-funding-offers-at-over-40-billion-valuation-489501> | 2026-10-24 | verified |
| 112 | **TypeSafe AI** | TechCrunch, Sacra, Channel Insider | <https://techcrunch.com/2026/10/09/the-maker-of-non-text-ai-model-jev-valued-at-7-5b-just-weeks-after-launch>; <https://sacra.com/c/typesafe-ai> | 2026-10-24 | verified |
| 113 | **Walden Robotics** | Walden Robotics (official), TechCrunch, PitchBook, TechFundingNews | <https://www.waldenrobotics.com/news/walden-robotics-launches-from-stealth>; <https://techcrunch.com/2026/07/22/travis-kalanicks-robotics-company-raises-1-7b-led-by-a16z> | 2026-10-24 | verified |
| 114 | **Atoms** | TechCrunch, mlq.ai, AI Funding Tracker | <https://techcrunch.com/2026/07/22/travis-kalanicks-robotics-company-raises-1-7b-led-by-a16z>; <https://atoms.co/vision> | 2026-10-24 | verified |
| 115 | **CMR Surgical** | Stryker (official), Crain's, Yahoo Finance | <https://www.stryker.com/us/en/about/news/2026/stryker-cmr-surgical-announce-strategic-alliance-advance-robotic-assisted-surgery.html> | 2026-10-24 | verified |
| 116 | **Pigment** | AI Funding Track (aifunding.me) | <https://aifunding.me/insights/ai-funding-rounds-october-2026> | 2026-10-24 | partial |
| 117 | **EliseAI** | NewMarketPitch, AI Funding Track | <https://newmarketpitch.com/blogs/news/generative-ai-funding-news> | 2026-10-24 | partial |
| 118 | **Norm Ai** | PYMNTS | <https://www.pymnts.com/news/investment-tracker/2026/harvey-targets-15-5-billion-valuation-as-revenue-surges-past-350-million> | 2026-10-24 | partial |

---

## Reusing or extending this dataset

If you extend the dataset, keep the chain intact:

1. Find a **datable source** (company announcement or financial press) — not a blog aggregator
2. Store the source name in `source` and the direct URL in `source_urls`
3. Set `last_verified` to the date you checked, and an honest `verification_status`
4. Run `python scripts/validate_data.py` before opening a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow and
[docs/search_queries.md](docs/search_queries.md) to see exactly how this release was queried.

---

## The 2025 extension (added September 9, 2026)

The original September 7 rebuild covered each registry company's **latest** round, which
skewed coverage toward 2026. The 2025 extension adds an event-level layer:
[data/master/funding_rounds.json](data/master/funding_rounds.json) — one row per funding
event from January 2025 through September 2026, so the dataset now supports longitudinal
analysis. Monthly event snapshots for all of 2025 live under `data/2025/<month>/`.

### What the 2025 layer contains

| Metric | Value |
|--------|-------|
| Funding events in 2025 | 109 |
| Unique companies raising in 2025 | 91 |
| Tracked capital (2025) | $107.3B |
| Mega-rounds (>= $100M) | 93 |
| Events with direct source URLs | 109/109 |

### How the 2025 data was collected

1. **TechCrunch 2025 mega-round census** — the article "Here are the 55 US AI startups
   that raised $100M or more in 2025" (Rebecca Szkutak, updated Jan 19, 2026,
   <https://techcrunch.com/2026/01/19/here-are-the-49-us-ai-startups-that-have-raised-100m-or-more-in-2025/>) was fetched and parsed into 73 structured
   events (amount, stage, date, valuation, investors), transcribed as stated.
2. **Tracked-company events** — the September 5-7, 2026 evidence base (152 evidence
   blocks in [docs/evidence_log.md](docs/evidence_log.md)) was mined for 2025-dated
   funding events of registry companies; each was re-checked against the captured
   snippets and resolved to a source URL where possible.
3. **Targeted gap searches** — additional queries for international 2025 rounds
   (e.g. Mistral AI's EUR 1.7B Series C, Helsing) and reported-but-unconfirmed events
   (e.g. Poolside's Nvidia-backed round), each stored with its source.
4. **Merge and dedupe** — events were deduplicated by company + month + amount
   (5% tolerance), keeping the record with the strongest sourcing.
5. **Registry latest rounds** — each of the 103 registry companies' latest round was
   added as an event, so 2026 coverage is complete in the same table.

Reported-but-unconfirmed events (e.g. Perplexity's September 2025 round) are marked
`partial` with a note, never silently mixed with confirmed figures.

### Scope note

The 2025 layer is an **events** dataset: it includes rounds by companies that are not in
the 103-company registry (registry membership reflects the September 2026 landscape).
Every event carries `in_registry` so the two views can be separated.
