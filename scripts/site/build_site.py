#!/usr/bin/env python3
"""Assemble the final index.html from template parts + the governed dataset.

Run from anywhere inside the repo:  python scripts/site/build_site.py
Reads scripts/site/parts/*.html + 07_app.js and scripts/site/site_data.json,
writes a single self-contained file to the repository root as index.html
(so GitHub Pages can serve it directly from the main branch).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = HERE / "parts"
DATA = HERE / "site_data.json"
OUT = HERE.parents[1] / "index.html"

html = ""
for name in ["01_head.html", "02_header_hero.html", "03_foundation_landscape.html",
             "04_capital_timeline.html", "05_segments_problems_opps.html",
             "06_playbook_team_explorer_footer.html"]:
    html += (PARTS / name).read_text()

app_js = (PARTS / "07_app.js").read_text()
data = json.loads(DATA.read_text())

# compact the payload: companies keep full richness; series already slim
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

html += (
    '<script id="site-data" type="application/json">'
    + payload.replace("</", "<\\/")  # guard against </script> breakouts
    + "</script>\n"
    "<script>\n" + app_js + "\n</script>\n</body>\n</html>\n"
)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html)
print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")
