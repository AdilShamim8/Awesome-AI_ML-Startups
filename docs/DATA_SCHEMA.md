# Data Schema Dictionary

The canonical dataset is [`data/master/startups_master.json`](../data/master/startups_master.json)
(schema v2.0) with a CSV mirror at `startups_master.csv`. The event-level funding
history lives in [`data/master/funding_rounds.json`](../data/master/funding_rounds.json)
(schema v1.0) with its own CSV mirror. This page documents every field, its type,
its controlled vocabulary, and the rules that keep the two datasets consistent.

> Last updated: 2026-10-24 · 118 companies · 193 funding events

---

## Company record (schema v2.0 — 31 fields)

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | no | Stable 3-digit unique key (`"001"`…`"118"`); validator enforces uniqueness |
| `slug` | string | no | URL-safe unique identifier derived from the name |
| `startup_name` | string | no | Canonical company name (the name evidence is filed under) |
| `about` | string | no | One-line tagline (<100 chars) used in category tables |
| `description` | string | no | 2-4 sentence narrative with the latest verified facts |
| `website` | URL | no | Official site; link-checked (403/429 = bot-blocked, not dead) |
| `category` | enum | no | One of the 10 controlled categories (below) |
| `subcategory` | string | no | Free-text segment (e.g. "Inference Silicon") |
| `funding_stage` | enum | no | Controlled stage vocabulary (below) |
| `funding_amount` | string | no | Display string for the latest **primary** round raised (e.g. `"$1.85B"`, `"€3B (~$3.5B)"`) |
| `funding_amount_usd` | number | yes | Numeric USD equivalent for sorting; null only when no round is known |
| `valuation_display` | string | yes | Worth, with the date and type of the mark (e.g. `"$60B (Oct 2026)"`, `"$22B (employee tender, Sep 2026)"`) |
| `valuation_usd` | number | yes | Numeric USD of the latest known valuation mark |
| `total_raised_display` | string | yes | Cumulative funding context, as sourced |
| `last_round_date` | date | yes | `YYYY-MM-DD` of the latest primary round; month-precision dates use month-end with a note |
| `investors` | array | no | Key investors of the latest round (list of strings) |
| `headquarters` | string | no | `"City, Country"` |
| `city` | string | no | City component |
| `country` | string | no | Country component (`USA`, `UK`, `China`, …) |
| `region` | enum | no | `North America` · `Europe` · `Asia-Pacific` · `Middle East` · `Africa` · `Latin America` · `Other` |
| `founded_year` | integer | no | Founding year (validator warns outside 1990–current year) |
| `status` | enum | no | `active` · `acquired` · `pending_acquisition` · `majority_acquired` · `public` |
| `status_note` | string | yes | Deal context for non-active statuses (acquirer, price, dates) |
| `source` | string | no | Comma-separated source names (e.g. `"Reuters, CNBC, Ramp (official)"`) |
| `source_urls` | array | no | Direct URLs to the cited sources |
| `date_added` | date | no | Date the company entered the tracker (never rewritten) |
| `last_updated` | date | no | Date any field last changed |
| `last_verified` | date | no | Date facts were last checked against sources — the actual check date, never auto-filled |
| `verification_status` | enum | no | `verified` · `partial` · `unverified` (ladder below) |
| `tags` | array | no | Free-form lowercase tags |
| `notes` | string | yes | Caveats, conflicts, reported-in-progress items, field limitations |

### Controlled category vocabulary

`AI/ML` · `Generative AI` · `AI Agents` · `SaaS` · `DevTools` · `FinTech` ·
`HealthTech` · `Robotics` · `Cybersecurity` · `EdTech`

### Controlled stage vocabulary

`Pre-Seed` · `Seed` · `Series A` … `Series K` · `Late Stage` (large rounds
with no disclosed series label) · `IPO` · `Bootstrapped` · `Series Unknown`

### Verification ladder

| Status | Bar |
|--------|-----|
| `verified` | Primary source (company announcement) and/or financial press (Reuters, Bloomberg, CNBC, WSJ, FT); two independent types preferred |
| `partial` | Single source, estimate, Tier-3 aggregator, reported-but-unconfirmed, or public-record fields not directly re-verified — the limitation is named in `notes` |
| `unverified` | Existence confirmed, figures not — explained in `notes` |

---

## Funding event record (schema v1.0 — 19 fields)

One row per funding event (a closed round), spanning 2022-01 through the
current cutoff. Companies in the registry are flagged `in_registry=true`;
events for companies outside the registry are landscape records.

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `event_id` | string | no | Stable key `round-001`…; uniqueness and content-level duplicates enforced |
| `startup_name` | string | no | Company name as evidenced (name variants are normalized by the validator) |
| `round_date` | date | yes | `YYYY-MM-DD`; must fall inside `month`; month-precision events use month-end + note |
| `month` | string | no | `YYYY-MM` bucket |
| `amount_display` | string | no | Display amount, original currency preserved |
| `amount_usd_m` | number | yes | Amount in USD millions (null when undisclosed) |
| `stage` | enum | no | Same vocabulary as the company record |
| `valuation_display` | string | yes | Valuation mark with date |
| `valuation_usd_m` | number | yes | Valuation in USD millions |
| `investors` | string | no | `; `-joined investor list |
| `about` | string | no | One-line company/event description |
| `country` | string | yes | Country of HQ |
| `source` | string | no | Comma-separated source names |
| `source_domain` | derived | — | CSV-only column derived from the first `source_urls` entry |
| `source_urls` | string | no | Direct URL(s) to the evidence |
| `verification_status` | enum | no | `verified` / `partial` / `unverified` |
| `last_verified` | date | no | Actual verification date |
| `in_registry` | boolean | no | Whether the company is in the master registry |
| `notes` | string | yes | Precision caveats, conflicts, deal context |

### Event-level metadata (enforced)

| Field | Rule |
|-------|------|
| `total_events` | Must equal the number of rows (validator error) |
| `coverage` | Must match the actual min–max event months, `YYYY-MM through YYYY-MM` (validator error) |
| `cutoff` | Hard research cutoff; any event dated later is a validator error |
| `generated` | Build date of the event file |

---

## Invariants the validator enforces

1. Unique `id` and `slug` per company; unique `event_id` per event
2. No content-level duplicate events (same company + date + amount)
3. All enum values from the controlled vocabularies
4. Master and events CSV mirrors byte-equivalent to their JSON (regenerate via `scripts/build_master_csv.py` and `scripts/build_funding_rounds_csv.py`)
5. Event `round_date` inside `month`, and `<= metadata.cutoff`
6. Registry name-variant cross-check (an event matching a registry company must carry `in_registry=true`)
7. Event-newer-than-master staleness signal (warning)
8. Generated category pages match the master (company count and names per category)
9. Every registry company has evidence in `docs/evidence_log.md`
10. Monthly snapshots: strict mode (generated from master) must be a subset of the master; stats sums must match file counts

## Serialization conventions (CSV mirrors)

- `investors`, `tags` → `"; "`-joined
- `source_urls` (company records) → `" | "`-joined
- `null` → empty cell
- booleans → `True` / `False`
- The events CSV adds the derived `source_domain` column (registrable domain of the first source URL, `www.` stripped)
