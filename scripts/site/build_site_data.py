#!/usr/bin/env python3
"""Compute all statistics for the index.html site from the canonical dataset.

Run from anywhere inside the repo:  python scripts/site/build_site_data.py
Outputs a readable summary to stdout and a machine-readable JSON blob to
scripts/site/site_data.json used to populate the static site and its explorer.
"""
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "site_data.json"

master = json.loads((ROOT / "data/master/startups_master.json").read_text())
funding = json.loads((ROOT / "data/master/funding_rounds.json").read_text())
S = master["startups"]
E = funding["rounds"]

B = 1e9


def fmt_b(x):
    if x is None:
        return None
    if x >= 1e12:
        return f"${x/1e12:.2f}T"
    if x >= B:
        return f"${x/B:.1f}B"
    return f"${x/1e6:.0f}M"


# ---------- company-level aggregates ----------
cat = Counter(c["category"] for c in S)
country = Counter(c["country"] for c in S)
region = Counter(c["region"] for c in S)
city = Counter(c["city"] for c in S)
stage = Counter(c["funding_stage"] for c in S)
verif = Counter(c["verification_status"] for c in S)
status = Counter(c["status"] for c in S)
founded = Counter(c["founded_year"] for c in S)

vals = [c["valuation_usd"] for c in S if isinstance(c.get("valuation_usd"), (int, float))]
amts = [c["funding_amount_usd"] for c in S if isinstance(c.get("funding_amount_usd"), (int, float))]
total_val = sum(vals)
total_amt = sum(amts)

def lrd(c):
    return str(c.get("last_round_date") or "")


# latest-round capital raised in 2026 (by last_round_date)
amt_2026 = [c["funding_amount_usd"] for c in S
            if isinstance(c.get("funding_amount_usd"), (int, float))
            and lrd(c)[:4] == "2026"]
amt_2025 = [c["funding_amount_usd"] for c in S
            if isinstance(c.get("funding_amount_usd"), (int, float))
            and lrd(c)[:4] == "2025"]

# trailing 12 months (Nov 2025 .. Oct 2026) by last_round_date
ttm = [c["funding_amount_usd"] for c in S
       if isinstance(c.get("funding_amount_usd"), (int, float))
       and "2025-11" <= lrd(c)[:7] <= "2026-10"]

billion_rounds = [c for c in S if isinstance(c.get("funding_amount_usd"), (int, float))
                  and c["funding_amount_usd"] >= B]
billion_2026 = [c for c in billion_rounds if lrd(c)[:4] == "2026"]

# concentration: top-5 companies share of total latest-round capital
ranked = sorted(amts, reverse=True)
top5 = sum(ranked[:5]) / total_amt * 100
top10 = sum(ranked[:10]) / total_amt * 100
frontier_cats = {"Generative AI", "AI/ML"}
frontier_amt = sum(c["funding_amount_usd"] for c in S
                   if c["category"] in frontier_cats and isinstance(c.get("funding_amount_usd"), (int, float)))

# founding-year stats
founded_sorted = sorted(f for f in founded if isinstance(f, int))
median_founded = founded_sorted[len(founded_sorted)//2]
post2021 = [c for c in S if isinstance(c.get("founded_year"), int) and c["founded_year"] >= 2021]
post2021_val = sum(c["valuation_usd"] for c in post2021 if isinstance(c.get("valuation_usd"), (int, float)))

# valuation / latest-round multiples
mults = []
for c in S:
    if isinstance(c.get("valuation_usd"), (int, float)) and isinstance(c.get("funding_amount_usd"), (int, float)) \
            and c["funding_amount_usd"] > 0 and lrd(c)[:4] in ("2025", "2026"):
        mults.append((c["valuation_usd"] / c["funding_amount_usd"], c["startup_name"], c["category"]))
mults.sort(reverse=True)

# M&A / status events
exits = [c for c in S if c["status"] in ("acquired", "pending_acquisition", "majority_acquired")]

# date_added (rebuild provenance)
added = Counter(str(c.get("date_added", ""))[:10] for c in S)
legacy = sum(v for k, v in added.items() if k <= "2025-12-31")
rebuild = sum(v for k, v in added.items() if "2026-01-01" <= k <= "2026-09-30")
october = sum(v for k, v in added.items() if k >= "2026-10-01")

# ---------- event-level aggregates ----------
conf = [e for e in E if e.get("verification_status") == "verified"]
partial = [e for e in E if e.get("verification_status") == "partial"]
conf_total = sum(e["amount_usd_m"] for e in conf if isinstance(e.get("amount_usd_m"), (int, float))) / 1000

by_month = defaultdict(lambda: {"n": 0, "amt": 0.0})
for e in E:
    m = e["month"]
    by_month[m]["n"] += 1
    if isinstance(e.get("amount_usd_m"), (int, float)) and e.get("verification_status") == "verified":
        by_month[m]["amt"] += e["amount_usd_m"] / 1000

y2025 = sum(v["amt"] for k, v in by_month.items() if k.startswith("2025"))
y2026 = sum(v["amt"] for k, v in by_month.items() if k.startswith("2026"))
n2025 = sum(v["n"] for k, v in by_month.items() if k.startswith("2025"))
n2026 = sum(v["n"] for k, v in by_month.items() if k.startswith("2026"))

# gap window Sep 8 - Oct 24 additions
gap_events = [e for e in E if "2026-09-08" <= str(e.get("round_date") or "") <= "2026-10-24"]
gap_confirmed = sum(e["amount_usd_m"] for e in gap_events
                    if e.get("verification_status") == "verified" and isinstance(e.get("amount_usd_m"), (int, float))) / 1000

# repeat raisers (companies with >= 2 events in 2025-2026)
ev_by_co = defaultdict(list)
for e in E:
    if e["month"] >= "2025-01":
        ev_by_co[e["startup_name"]].append(e)
repeats = {k: v for k, v in ev_by_co.items() if len(v) >= 2}
thrice = {k: v for k, v in ev_by_co.items() if len(v) >= 3}

# investor league table
inv = Counter()
for e in E:
    if e["month"] >= "2025-01" and e.get("verification_status") == "verified":
        for i in (e.get("investors", "") or "").split(";"):
            i = i.strip()
            if i and not i.lower().startswith(("reported", "undisclosed", "various")):
                inv[i] += 1

# category capital
cat_amt = defaultdict(float)
for c in S:
    if isinstance(c.get("funding_amount_usd"), (int, float)):
        cat_amt[c["category"]] += c["funding_amount_usd"] / B

# ---------- extra tables for the site ----------

# field completeness across 118 rows
FIELDS = ["funding_amount_usd", "valuation_usd", "investors", "founded_year",
          "city", "country", "last_round_date", "website", "source_urls", "tags"]
completeness = []
for f in FIELDS:
    n = sum(1 for c in S if c.get(f) not in (None, "", [], {}))
    completeness.append({"field": f, "n": n, "pct": round(n / len(S) * 100, 1)})

# repeat raisers 2025-2026 (from event ledger)
def rd(e):
    return str(e.get("round_date") or "")


rep_rows = []
for name, evs in sorted(repeats.items(), key=lambda kv: (-len(kv[1]), -sum(
        e.get("amount_usd_m") or 0 for e in kv[1]))):
    conf_amt = sum(e["amount_usd_m"] for e in evs
                   if e.get("verification_status") == "verified" and isinstance(e.get("amount_usd_m"), (int, float)))
    evs_s = sorted(evs, key=rd)
    rep_rows.append({
        "name": name,
        "rounds": len(evs),
        "dates": [e["round_date"] for e in evs_s],
        "amt": round(conf_amt / 1000, 2),
        "stages": [e.get("stage", "") for e in evs_s],
    })

# investor league table from company investor arrays (cleaner than event strings)
ALIAS = {
    "a16z": "Andreessen Horowitz", "Andreessen Horowitz": "Andreessen Horowitz",
    "Sequoia": "Sequoia Capital", "Sequoia Capital": "Sequoia Capital",
    "Kleiner Perkins": "Kleiner Perkins", "Kleiner Perkins Caufield & Byers": "Kleiner Perkins",
    "Lightspeed Venture Partners": "Lightspeed", "Lightspeed": "Lightspeed",
}
league = Counter()
for c in S:
    for i in (c.get("investors") or []):
        i = (i or "").strip()
        if not i or i.lower().startswith(("reported", "undisclosed", "various")):
            continue
        league[ALIAS.get(i, i)] += 1

# exits table
exit_rows = []
for c in sorted(exits, key=lambda c: -(c.get("valuation_usd") or 0)):
    exit_rows.append({
        "name": c["startup_name"], "category": c["category"],
        "status": c["status"], "note": c.get("status_note") or "",
        "valuation": c.get("valuation_display") or "—",
    })

# month-by-month with largest event (months defined below)
month_rows = []


def build_month_rows(months_):
    rows = []
    for m in months_:
        evs = [e for e in E if e["month"] == m]
        big = max((e for e in evs if isinstance(e.get("amount_usd_m"), (int, float))),
                  key=lambda e: e["amount_usd_m"], default=None)
        rows.append({
            "month": m, "n": by_month[m]["n"], "amt": round(by_month[m]["amt"], 2),
            "big": (big["startup_name"] + " · " + big["amount_display"]) if big else "—",
        })
    return rows

# segment economies with valuation multiples
SEGMENTS = {
    "Frontier Models": {"Generative AI"},
    "Infrastructure & DevTools": {"AI/ML", "DevTools", "Cybersecurity"},
    "Applications": {"AI Agents", "SaaS", "FinTech", "HealthTech", "EdTech"},
    "Physical AI & Defense": {"Robotics"},
}
seg_stats = {}
for name, cats in SEGMENTS.items():
    cos = [c for c in S if c["category"] in cats]
    amt_b = sum(c["funding_amount_usd"] for c in cos if isinstance(c.get("funding_amount_usd"), (int, float))) / B
    val_b = sum(c["valuation_usd"] for c in cos if isinstance(c.get("valuation_usd"), (int, float))) / B
    seg_stats[name] = {
        "n": len(cos),
        "amt": round(amt_b, 1),
        "val": round(val_b, 1),
        "mult": round(val_b / amt_b, 1) if amt_b > 0 else None,
    }

# top rounds / valuations
top_rounds = sorted([c for c in S if isinstance(c.get("funding_amount_usd"), (int, float))],
                    key=lambda c: c["funding_amount_usd"], reverse=True)[:12]
top_vals = sorted([c for c in S if isinstance(c.get("valuation_usd"), (int, float))],
                  key=lambda c: c["valuation_usd"], reverse=True)[:12]

# largest single events
top_events = sorted([e for e in E if isinstance(e.get("amount_usd_m"), (int, float))],
                    key=lambda e: e["amount_usd_m"], reverse=True)[:12]

# ---------- print readable summary ----------
p = print
p("=" * 70)
p("HERO")
p(f"  companies={len(S)}  events={len(E)}  confirmed_capital={conf_total:.1f}B")
p(f"  total_known_valuation={fmt_b(total_val)} ({len(vals)} rows, {len(vals)/len(S)*100:.1f}% coverage)")
p(f"  latest_round_capital={fmt_b(total_amt)} over {len(amts)} rows")
p(f"  verification: {dict(verif)} -> {verif['verified']/len(S)*100:.1f}% verified")
p(f"  status: {dict(status)}")
p(f"  date_added: legacy={legacy} rebuild={rebuild} october={october}")
p("=" * 70)
p("EXEC")
p(f"  2026 latest-round capital={fmt_b(sum(amt_2026))} ({sum(amt_2026)/total_amt*100:.1f}% of total) over {len(amt_2026)} rounds")
p(f"  2025 latest-round capital={fmt_b(sum(amt_2025))} ({len(amt_2025)} rounds)")
p(f"  TTM (Nov25-Oct26)={fmt_b(sum(ttm))} across {len(ttm)} rounds")
p(f"  $1B+ rounds: total={len(billion_rounds)}, in 2026={len(billion_2026)}")
p(f"  top5 share={top5:.1f}%  top10 share={top10:.1f}%")
p(f"  frontier (GenAI+AI/ML) latest-round capital={fmt_b(frontier_amt)} = {frontier_amt/total_amt*100:.1f}%")
p(f"  median founded year={median_founded}; post-2021 founded={len(post2021)}, their valuation={fmt_b(post2021_val)} = {post2021_val/total_val*100:.1f}%")
p(f"  USA share={country['USA']/len(S)*100:.1f}%  SF+Bay cities top: {city.most_common(8)}")
p(f"  exits: {len(exits)} ({status['acquired']} acquired, {status['pending_acquisition']} pending, {status['majority_acquired']} majority)")
p("=" * 70)
p("CAPITAL BY YEAR (confirmed)")
p(f"  2025: {y2025:.1f}B over {n2025} events   2026: {y2026:.1f}B over {n2026} events (through Oct 24)")
p(f"  gap-window (Sep 8-Oct 24) events={len(gap_events)}, confirmed={gap_confirmed:.1f}B")
p(f"  repeat raisers 2025-26: {len(repeats)} companies, {len(thrice)} raised 3+")
p(f"  top investors: {inv.most_common(12)}")
p(f"  multiples top: {[(round(m,1), n) for m,n,_ in mults[:8]]}")
p(f"  multiples median: {sorted(m[0] for m in mults)[len(mults)//2]:.1f}x over {len(mults)} cos")
p("=" * 70)
p("SEGMENTS")
for k, v in seg_stats.items():
    p(f"  {k}: n={v['n']} amt={v['amt']}B val={v['val']}B mult={v['mult']}x")
p("COMPLETENESS: " + str([(c['field'], c['pct']) for c in completeness]))
p(f"REPEATS: {len(rep_rows)} companies; top: {[(r['name'], r['rounds'], r['amt']) for r in rep_rows[:10]]}")
p("LEAGUE: " + str(league.most_common(12)))
p("EXITS: " + str([(e['name'], e['status']) for e in exit_rows]))
p("MONTHLY: " + str([(m['month'], m['n'], m['amt']) for m in month_rows]))
p("CATEGORIES: " + str(dict(cat.most_common())))
p("CATEGORY AMT (B): " + str({k: round(v, 1) for k, v in sorted(cat_amt.items(), key=lambda x: -x[1])}))
p("COUNTRIES: " + str(dict(country.most_common())))
p("REGIONS: " + str(dict(region.most_common())))
p("STAGES: " + str(dict(stage.most_common())))
p(f"FOUNDED: {sorted(founded.items())}")
p("=" * 70)
p("TOP ROUNDS: " + str([(c['startup_name'], fmt_b(c['funding_amount_usd'])) for c in top_rounds]))
p("TOP VALS: " + str([(c['startup_name'], fmt_b(c['valuation_usd'])) for c in top_vals]))
p("TOP EVENTS: " + str([(e['startup_name'], e['amount_display'], e['round_date']) for e in top_events]))

# ---------- write machine-readable blob for the site ----------
months = sorted(by_month)
series = [{"month": m, "n": by_month[m]["n"], "amt": round(by_month[m]["amt"], 2)} for m in months]
month_rows = build_month_rows(months)

companies = []
for c in sorted(S, key=lambda c: -(c.get("funding_amount_usd") or 0)):
    companies.append({
        "name": c["startup_name"],
        "category": c["category"],
        "sub": c.get("subcategory") or "",
        "stage": c["funding_stage"],
        "amount": c.get("funding_amount") or "—",
        "amount_usd": c.get("funding_amount_usd"),
        "valuation": c.get("valuation_display") or "—",
        "valuation_usd": c.get("valuation_usd"),
        "round_date": c.get("last_round_date"),
        "hq": c.get("headquarters"),
        "city": c.get("city"),
        "country": c["country"],
        "region": c["region"],
        "founded": c.get("founded_year"),
        "status": c["status"],
        "verification": c["verification_status"],
        "investors": (c.get("investors") or [])[:8],
        "tags": (c.get("tags") or [])[:6],
        "about": c.get("about") or "",
        "description": c.get("description") or "",
        "website": c.get("website"),
        "source": c.get("source") or "",
        "sources": (c.get("source_urls") or [])[:3],
    })

OUT.write_text(json.dumps({
    "as_of": master["metadata"]["as_of"],
    "companies": companies,
    "series": series,
    "month_rows": month_rows,
    "categories": dict(cat.most_common()),
    "category_amt": {k: round(v, 1) for k, v in cat_amt.items()},
    "countries": dict(country.most_common()),
    "regions": dict(region.most_common()),
    "stages": dict(stage.most_common()),
    "segments": seg_stats,
    "completeness": completeness,
    "repeats": rep_rows,
    "league": league.most_common(15),
    "exits": exit_rows,
    "top_rounds": [{"name": c["startup_name"], "cat": c["category"], "stage": c["funding_stage"],
                    "amt": c.get("funding_amount"), "date": c.get("last_round_date"),
                    "val": c.get("valuation_display")} for c in top_rounds],
    "top_vals": [{"name": c["startup_name"], "cat": c["category"],
                  "val": c.get("valuation_display")} for c in top_vals],
    "mults_top": [{"m": round(m, 1), "name": n, "cat": c2} for m, n, c2 in mults[:10]],
    "mults_median": round(sorted(m[0] for m in mults)[len(mults) // 2], 1),
    "mults_n": len(mults),
}, ensure_ascii=False, indent=1))

print(f"\nwrote {OUT} ({OUT.stat().st_size/1024:.0f} KB, {len(companies)} companies)")
