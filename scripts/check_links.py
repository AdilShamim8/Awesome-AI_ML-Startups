#!/usr/bin/env python3
"""Check website and source URLs in the master dataset are reachable.

Performs concurrent HEAD (fallback GET) requests with a short timeout.

Exit-status semantics (v2):
- 2xx/3xx            -> reachable
- 403 / 429          -> bot-blocked: many legitimate sites (openai.com, midjourney,
                       etc.) reject automated clients. These are NOT failures —
                       they need a manual browser check, and the report records
                       them separately.
- anything else      -> failing (dead or misconfigured)

Exits non-zero only when verified entries have genuinely failing websites.
With --check-sources, source_urls are checked too (report-only; never affects
the exit status, since press archives churn).

Usage:
    python scripts/check_links.py [--timeout 10] [--check-sources]
"""

import argparse
import concurrent.futures as cf
import json
import urllib.request
import urllib.error
import ssl
from datetime import date
from pathlib import Path

REPO = Path(__file__).parent.parent
MASTER = REPO / "data" / "master" / "startups_master.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; awesome-ai-ml-startups link checker)"}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE  # tolerate internal cert quirks; this is a liveness check

BOT_BLOCKED = {403, 429}


def check_url(url, timeout):
    try:
        req = urllib.request.Request(url, headers=HEADERS, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status
    except Exception:
        try:
            req = urllib.request.Request(url, headers=HEADERS, method="GET")
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception as e:
            return f"ERR:{type(e).__name__}"


def classify(status):
    if isinstance(status, str):
        return "failing"
    if status in BOT_BLOCKED:
        return "bot_blocked"
    if status >= 400:
        return "failing"
    return "reachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=10)
    ap.add_argument("--max-workers", type=int, default=12)
    ap.add_argument("--check-sources", action="store_true",
                    help="also check every source URL (report-only)")
    args = ap.parse_args()

    master = json.loads(MASTER.read_text(encoding="utf-8"))
    urls = {s["slug"]: s["website"] for s in master["startups"]}

    source_urls = {}
    if args.check_sources:
        for s in master["startups"]:
            for i, u in enumerate(s.get("source_urls") or []):
                source_urls[f"{s['slug']}#src{i}"] = u

    results = {}
    with cf.ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        targets = dict(urls)
        targets.update(source_urls)
        futs = {ex.submit(check_url, u, args.timeout): key for key, u in targets.items()}
        for fut in cf.as_completed(futs):
            results[futs[fut]] = fut.result()

    website_results = {k: v for k, v in results.items() if not k.endswith(tuple(f"#src{i}" for i in range(10)))}
    website_results = {k: v for k, v in results.items() if "#" not in k}

    by_class = {"reachable": {}, "bot_blocked": {}, "failing": {}}
    for slug, status in website_results.items():
        by_class[classify(status)][slug] = status

    print(f"Checked {len(website_results)} website URLs:")
    print(f"  reachable:   {len(by_class['reachable'])}")
    print(f"  bot-blocked: {len(by_class['bot_blocked'])} (HTTP 403/429 — not failures; verify manually in a browser)")
    print(f"  failing:     {len(by_class['failing'])}\n")
    if by_class["bot_blocked"]:
        print("BOT-BLOCKED (manual check needed):")
        for slug, status in sorted(by_class["bot_blocked"].items()):
            name = next(s['startup_name'] for s in master['startups'] if s['slug'] == slug)
            print(f"  {name:<28} {status}  {urls[slug]}")
        print()
    if by_class["failing"]:
        print("FAILING:")
        for slug, status in sorted(by_class["failing"].items()):
            name = next(s['startup_name'] for s in master['startups'] if s['slug'] == slug)
            print(f"  {name:<28} {status}  {urls[slug]}")

    source_summary = None
    if args.check_sources:
        src_results = {k: v for k, v in results.items() if "#" in k}
        src_classes = {"reachable": 0, "bot_blocked": 0, "failing": 0}
        for status in src_results.values():
            src_classes[classify(status)] += 1
        source_summary = {"checked": len(src_results), **src_classes}
        print(f"\nSource URLs checked: {len(src_results)} "
              f"(reachable {src_classes['reachable']}, bot-blocked {src_classes['bot_blocked']}, "
              f"failing {src_classes['failing']}) — report-only")

    report = {
        "checked": len(website_results),
        "reachable": len(by_class["reachable"]),
        "bot_blocked": {k: v for k, v in sorted(by_class["bot_blocked"].items())},
        "failing": {k: v for k, v in sorted(by_class["failing"].items())},
        "checked_on": date.today().isoformat(),
        "note": "bot_blocked lists HTTP 403/429 responses — sites that reject automated "
                "clients but are typically fine in a browser; they are not failures. "
                "failing lists genuinely unreachable or invalid URLs.",
    }
    if source_summary:
        report["source_urls"] = source_summary
    (REPO / "data" / "master" / "link_check_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    print("\nReport saved to data/master/link_check_report.json")
    return 0 if not by_class["failing"] else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
