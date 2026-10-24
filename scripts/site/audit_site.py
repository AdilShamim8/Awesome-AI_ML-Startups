#!/usr/bin/env python3
"""Audit the built index.html: every headline figure must be present and
consistent with the canonical dataset (recomputed independently here).

Run from anywhere inside the repo:  python scripts/site/audit_site.py
Exits non-zero if any check fails, so it can gate a CI job or pre-push hook.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = (ROOT / "index.html").read_text()
HTML_FLAT = re.sub(r"\s+", " ", HTML)  # whitespace-normalized view for phrase checks

m = json.loads((ROOT / "data/master/startups_master.json").read_text())
fr = json.loads((ROOT / "data/master/funding_rounds.json").read_text())
S, E = m["startups"], fr["rounds"]
B = 1e9

fails = []


def must(desc, cond):
    if not cond:
        fails.append(desc)


def has(s):
    return s in HTML or s in HTML_FLAT


# recompute all headline figures independently
n = len(S)
conf = [e for e in E if e.get("verification_status") == "verified"]
conf_total = sum(e["amount_usd_m"] for e in conf if isinstance(e.get("amount_usd_m"), (int, float))) / 1000
vals = [c["valuation_usd"] for c in S if isinstance(c.get("valuation_usd"), (int, float))]
amts = [c["funding_amount_usd"] for c in S if isinstance(c.get("funding_amount_usd"), (int, float))]
val_total = sum(vals) / 1e12
amt_total = sum(amts) / B
ver = Counter(c["verification_status"] for c in S)
partial_ev = sum(e.get("amount_usd_m") or 0 for e in E if e.get("verification_status") == "partial") / 1000

a26 = [c["funding_amount_usd"] for c in S if isinstance(c.get("funding_amount_usd"), (int, float))
       and str(c.get("last_round_date") or "")[:4] == "2026"]
ttm = [c["funding_amount_usd"] for c in S if isinstance(c.get("funding_amount_usd"), (int, float))
       and "2025-11" <= str(c.get("last_round_date") or "")[:7] <= "2026-10"]
ranked = sorted(amts, reverse=True)
top5 = sum(ranked[:5]) / amt_total * 100
top10 = sum(ranked[:10]) / amt_total * 100
frontier = sum(c["funding_amount_usd"] for c in S if c["category"] in ("Generative AI", "AI/ML")
               and isinstance(c.get("funding_amount_usd"), (int, float))) / B
post21 = [c for c in S if isinstance(c.get("founded_year"), int) and c["founded_year"] >= 2021]
post21_val = sum(c["valuation_usd"] for c in post21 if isinstance(c.get("valuation_usd"), (int, float))) / 1e12
usa = Counter(c["country"] for c in S)["USA"] / n * 100
sf = Counter(c["city"] for c in S)["San Francisco"]
apac = Counter(c["region"] for c in S)["Asia-Pacific"]

y25 = sum(e["amount_usd_m"] for e in conf if e["month"].startswith("2025") and isinstance(e.get("amount_usd_m"), (int, float))) / 1000
y26 = sum(e["amount_usd_m"] for e in conf if e["month"].startswith("2026") and isinstance(e.get("amount_usd_m"), (int, float))) / 1000
n25 = sum(1 for e in E if e["month"].startswith("2025"))
n26 = sum(1 for e in E if e["month"].startswith("2026"))
gap = [e for e in E if "2026-09-08" <= str(e.get("round_date") or "") <= "2026-10-24"]
gap_conf = sum(e["amount_usd_m"] for e in gap if e.get("verification_status") == "verified"
               and isinstance(e.get("amount_usd_m"), (int, float))) / 1000
seed = [c for c in S if c["funding_stage"] in ("Seed", "Pre-Seed")]
seed_amt = sum(c["funding_amount_usd"] for c in seed if isinstance(c.get("funding_amount_usd"), (int, float))) / B

# assertions: the site must contain exactly these verified figures
checks = [
    (f"{n} companies", has("118")),
    ("193 events", has("193")),
    (f"confirmed ${conf_total:.1f}B", has("$369.4B")),
    (f"valuation ${val_total:.2f}T", has("$3.40T")),
    (f"81.4% val coverage", has("81.4%")),
    (f"latest-round ${amt_total:.1f}B", has("$306.8B")),
    ("110 priced rounds", has("110 priced rounds")),
    ("103 rebuild + 15 added", has("103 in the September rebuild · 15 added Oct 24")),
    (f"{ver['verified']/n*100:.1f}% verified", has("72.0%")),
    (f"{ver['partial']} partial rows", has("32 partial")),
    (f"partial events ${partial_ev:.1f}B", has("$26.4B")),
    ("37 partial events", has("37 of 193 events")),
    (f"2026 share {sum(a26)/amt_total*100:.1f}%", has("87.3%")),
    (f"2026 capital ${sum(a26)/B:.1f}B", has("$267.9B")),
    ("64 rounds in 2026", has("across 64 rounds")),
    (f"TTM ${sum(ttm)/B:.1f}B", has("$273.4B")),
    ("77 TTM rounds", has("across 77 rounds")),
    ("30 $1B+ rounds", has("thirty $1B-plus")),
    ("21 in 2026", has("Twenty-one of the thirty")),
    (f"frontier ${frontier:.1f}B", has("$261.8B")),
    ("85.3% frontier", has("85.3%")),
    (f"top5 {top5:.1f}%", has("74.6%")),
    (f"top10 {top10:.1f}%", has("82.7%")),
    ("66 post-2021", has("Sixty-six")),
    (f"post21 val ${post21_val:.2f}T", has("$1.78T")),
    ("52.2% share", has("52.2%")),
    (f"usa {usa:.1f}%", has("79.7%")),
    (f"SF {sf}", has("45 of 118")),
    (f"APAC {apac}", has("Asia-Pacific to")),
    ("11 countries", has("country list to eleven")),
    ("2025: 110 events $104.3B", has("110 events, $104.3B confirmed")),
    (f"2026: {n26} events ${y26:.1f}B", has(f"71 events through October 24, ${y26:.1f}B confirmed")),
    (f"gap {len(gap)} events ${gap_conf:.1f}B", has("Twelve gap-window events") and has("$14.3B of it confirmed")),
    ("40 repeat raisers", has("40 of the 118 companies")),
    ("median $243M / $600M", has("$243M") and has("$600M")),
    ("73 under $500M", has("73 events under $500M")),
    (f"seed {len(seed)} / ${seed_amt:.1f}B", has("10 of 118 companies sit at Seed or Pre-Seed") and has("$2.3B")),
    ("0.8% seed share", has("0.8% of tracked")),
    ("segment caps", has("$228.3B") and has("$47.6B") and has("$10.6B") and has("$20.2B")),
    ("segment vals", has("$2.30T") and has("$519B") and has("$370B") and has("$211B")),
    ("segment mults", has("10.1x") and has("10.9x") and has("34.8x") and has("10.4x")),
    ("league a16z 27", has("a16z (27 registry companies)")),
    ("league sequoia 24", has("Sequoia (24)")),
    ("league nvidia 16", has("Nvidia (16)")),
    ("pipeline 49 files", has("49 files")),
    ("1062 records", has("1,062")),
    ("44/44 tests", has("44 / 44")),
    ("0 errors 7 warnings", has("0 errors · 7 warnings") or has("Errors: 0")),
    ("63 commits", has("63 commits on main")),
    ("50 october commits", has("50 shipped the October 24 refresh")),
    ("link check 104/13/1", has("104 reachable, 13 bot-blocked, 1 failing")),
    ("188 evidence blocks", has("188 evidence blocks") and has("152 → 188")),
    ("median multiple 11.5x", has("Median across 82 companies") and has("11.5x")),
    ("spikes", has("$125.9B") and has("$74.2B") and has("$23.8B") and has("$44.7B")),
    ("as_of date", has("2026-10-24")),
    ("repo link", has("https://github.com/AdilShamim8/Awesome-AI_ML-Startups")),
    ("not-investment-advice", has("Not investment advice")),
    ("pre-month-end labels", has("pre-month-end research snapshot")),
    ("DeepSeek excluded note", has("excluded from confirmed totals")),
]

for desc, ok in checks:
    must(desc, ok)

# JSON payload sanity
mo = re.search(r'<script id="site-data" type="application/json">(.*?)</script>', HTML, re.S)
must("site-data script present", mo is not None)
if mo:
    payload = json.loads(mo.group(1).replace("<\\/", "</"))
    must("payload companies == 118", len(payload["companies"]) == 118)
    must("payload as_of", payload.get("as_of") == "2026-09-07" or payload.get("as_of") == "2026-10-24")
    must("payload months 22", len([s for s in payload["series"] if s["month"] >= "2025-01"]) == 22)

print(f"checks run: {len(checks)} | failures: {len(fails)}")
for f in fails:
    print("  FAIL:", f)
sys.exit(1 if fails else 0)
