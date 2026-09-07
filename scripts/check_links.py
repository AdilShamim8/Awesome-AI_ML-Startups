#!/usr/bin/env python3
"""Check website and source URLs in the master dataset are reachable.

Performs concurrent HEAD (fallback GET) requests with a short timeout.
Writes a report and exits non-zero if verified entries have dead websites.
Usage:
    python scripts/check_links.py [--timeout 10]
"""

import argparse
import concurrent.futures as cf
import json
import urllib.request
import urllib.error
import ssl
from pathlib import Path

REPO = Path(__file__).parent.parent
MASTER = REPO / "data" / "master" / "startups_master.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; awesome-ai-ml-startups link checker)"}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE  # tolerate internal cert quirks; this is a liveness check


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=10)
    ap.add_argument("--max-workers", type=int, default=12)
    args = ap.parse_args()

    master = json.loads(MASTER.read_text(encoding="utf-8"))
    urls = {}
    for s in master["startups"]:
        urls[s["slug"]] = s["website"]

    results = {}
    with cf.ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futs = {ex.submit(check_url, u, args.timeout): slug for slug, u in urls.items()}
        for fut in cf.as_completed(futs):
            slug = futs[fut]
            results[slug] = fut.result()

    dead = {k: v for k, v in results.items() if isinstance(v, str) or v >= 400}
    ok = len(results) - len(dead)
    print(f"Checked {len(results)} website URLs: {ok} reachable, {len(dead)} failing\n")
    if dead:
        print("FAILING:")
        for slug, status in sorted(dead.items()):
            name = next(s['startup_name'] for s in master['startups'] if s['slug'] == slug)
            print(f"  {name:<28} {status}  {urls[slug]}")

    report = {"checked": len(results), "reachable": ok, "failing": dead}
    (REPO / "data" / "master" / "link_check_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport saved to data/master/link_check_report.json")
    return 0 if not dead else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
