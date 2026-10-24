/* ------------------------------------------------------------------
   AI/ML Startup Intelligence — October 24, 2026 edition
   Vanilla JS. Every chart and table renders from the embedded
   governed dataset in #site-data. No frameworks, no external calls.
   ------------------------------------------------------------------ */
(function () {
"use strict";

const D = JSON.parse(document.getElementById("site-data").textContent);
const COS = D.companies;

/* ---------- tiny DOM helpers ---------- */
function el(tag, cls, html) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html !== undefined) n.innerHTML = html;
  return n;
}
function fmtB(x) {
  if (x === null || x === undefined) return "—";
  if (x >= 1000) return "$" + (x / 1000).toFixed(2) + "T";
  if (x >= 1) return "$" + (x >= 100 ? x.toFixed(0) : x.toFixed(1)) + "B";
  return "$" + Math.round(x * 1000) + "M";
}
function esc(s) {
  return String(s === null || s === undefined ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/* horizontal bar list: rows of [label, value, display, fillClass] */
function hbars(container, rows, opts) {
  opts = opts || {};
  const max = opts.max || Math.max.apply(null, rows.map(r => r[1]));
  const frag = document.createDocumentFragment();
  rows.forEach(r => {
    const w = max > 0 ? Math.max(0.75, (r[1] / max) * 100) : 0;
    frag.appendChild(el("div", "hrow",
      '<span class="hl">' + esc(r[0]) + '</span>' +
      '<span class="track"><span class="fill ' + (r[3] || "") + '" style="width:' + w.toFixed(1) + '%"></span></span>' +
      '<span class="hv">' + esc(r[2]) + '</span>'));
  });
  container.appendChild(frag);
}

/* stacked bar: parts of [label, value, display, color] */
function stackbar(container, parts, keyContainer) {
  const total = parts.reduce((s, p) => s + p[1], 0);
  parts.forEach(p => {
    const w = (p[1] / total) * 100;
    const seg = el("div", null, w > 9 ? esc(p[2]) : "");
    seg.style.width = w.toFixed(2) + "%";
    seg.style.background = p[3];
    seg.title = p[0] + " · " + p[2];
    container.appendChild(seg);
    if (keyContainer) keyContainer.appendChild(el("span", "k",
      '<span class="sw" style="background:' + p[3] + '"></span>' + esc(p[0])));
  });
}

/* sortable table shell */
function table(container, headers, rowsHtml, footNote) {
  const t = el("table");
  const thead = el("thead");
  const tr = el("tr");
  headers.forEach(h => tr.appendChild(el("th", h.num ? "num" : "", esc(h.label))));
  thead.appendChild(tr);
  const tbody = el("tbody");
  tbody.innerHTML = rowsHtml;
  t.appendChild(thead); t.appendChild(tbody);
  container.appendChild(t);
  if (footNote) container.appendChild(el("div", "tblfoot", esc(footNote)));
}

/* ---------- 02 · foundation ---------- */
(function () {
  const ver = 85, par = 32, unv = 1;
  document.getElementById("f-ver").style.width = (ver / 118 * 100) + "%";
  document.getElementById("f-par").style.width = (par / 118 * 100) + "%";
  document.getElementById("f-unv").style.width = Math.max(0.8, unv / 118 * 100) + "%";

  const rows = D.completeness.map(c => {
    const label = {
      funding_amount_usd: "Latest-round amount", valuation_usd: "Valuation",
      investors: "Investors", founded_year: "Founded year", city: "City",
      country: "Country", last_round_date: "Round date", website: "Website",
      source_urls: "Source URLs", tags: "Tags"
    }[c.field] || c.field;
    return [label, c.pct, c.pct.toFixed(1) + "%", c.pct === 100 ? "lt" : ""];
  });
  hbars(document.getElementById("completeness"), rows);
})();

/* ---------- 03 · landscape ---------- */
(function () {
  const cats = Object.keys(D.categories);
  hbars(document.getElementById("catCount"),
    cats.map(c => [c, D.categories[c], String(D.categories[c]), ""]));

  hbars(document.getElementById("catCap"),
    cats.map(c => [c, D.category_amt[c] || 0, "$" + (D.category_amt[c] || 0).toFixed(1) + "B", "mid"]),
    { max: Math.max.apply(null, cats.map(c => D.category_amt[c] || 0)) });

  /* stage ladder in narrative order */
  const order = ["Seed", "Pre-Seed", "Series A", "Series B", "Series C", "Series D",
    "Series E", "Series F", "Series G", "Series H", "Series K", "Late Stage", "IPO",
    "Series Unknown", "Bootstrapped"];
  const stageRows = [];
  order.forEach(s => {
    if (D.stages[s]) stageRows.push([s, D.stages[s], String(D.stages[s]),
      (s === "Seed" || s === "Pre-Seed") ? "lt" : ""]);
  });
  hbars(document.getElementById("stageLadder"), stageRows);

  /* founding cohorts */
  const byYear = {};
  COS.forEach(c => { const y = c.founded; if (y) byYear[y] = (byYear[y] || 0) + 1; });
  const bands = [["2010–15", 2010, 2015], ["2016–17", 2016, 2017], ["2018–19", 2018, 2019],
    ["2020", 2020, 2020], ["2021", 2021, 2021], ["2022", 2022, 2022],
    ["2023", 2023, 2023], ["2024", 2024, 2024], ["2025–26", 2025, 2026]];
  hbars(document.getElementById("foundedCohorts"),
    bands.map(b => {
      let n = 0; for (let y = b[1]; y <= b[2]; y++) n += byYear[y] || 0;
      return [b[0], n, String(n), b[1] >= 2024 ? "lt" : ""];
    }));

  /* regions + countries + cities */
  stackbar(document.getElementById("regionStack"),
    [["North America", 95, "80.5%", "#047857"], ["Europe", 16, "13.6%", "#059669"],
     ["Asia-Pacific", 7, "5.9%", "#10b981"]], null);
  const cts = Object.keys(D.countries);
  hbars(document.getElementById("countryBars"),
    cts.map(c => [c, D.countries[c], String(D.countries[c]),
      (c === "China" || c === "Japan" || c === "India" || c === "Singapore") ? "lt" : ""]));

  const cityCount = {};
  COS.forEach(c => { if (c.city) cityCount[c.city] = (cityCount[c.city] || 0) + 1; });
  const cities = Object.keys(cityCount).sort((a, b) => cityCount[b] - cityCount[a]).slice(0, 10);
  hbars(document.getElementById("cityBars"),
    cities.map(ct => [ct, cityCount[ct], String(cityCount[ct]),
      ct === "San Francisco" ? "" : "mid"]));

  /* round-size + valuation distributions */
  const buckets = [[0, 100, "<$100M"], [100, 500, "$100–499M"], [500, 1000, "$500–999M"],
    [1000, 5000, "$1–4.9B"], [5000, Infinity, "$5B+"]];
  hbars(document.getElementById("roundDist"),
    buckets.map(b => {
      const n = COS.filter(c => c.amount_usd !== null && c.amount_usd !== undefined &&
        c.amount_usd / 1e9 >= b[0] && c.amount_usd / 1e9 < b[1]).length;
      return [b[2], n, String(n), b[0] >= 5000 ? "" : (b[0] >= 1000 ? "mid" : "lt")];
    }));

  const vbuckets = [[0, 0.5, "<$500M"], [0.5, 1, "$500M–1B"], [1, 10, "$1–9.9B"],
    [10, 100, "$10–99B"], [100, Infinity, "$100B+"]];
  hbars(document.getElementById("valDist"),
    vbuckets.map(b => {
      const n = COS.filter(c => c.valuation_usd !== null && c.valuation_usd !== undefined &&
        c.valuation_usd / 1e9 >= b[0] && c.valuation_usd / 1e9 < b[1]).length;
      return [b[2], n, String(n), b[0] >= 100 ? "" : (b[0] >= 10 ? "mid" : "lt")];
    }));
})();

/* ---------- 04 · capital ---------- */
(function () {
  /* monthly chart: SVG area (capital) + bars (events) */
  const series = D.series.filter(s => s.month >= "2025-01");
  const W = 960, H = 300, PL = 46, PR = 10, PT = 18, PB = 34;
  const iw = W - PL - PR, ih = H - PT - PB;
  const maxA = Math.max.apply(null, series.map(s => s.amt));
  const maxN = Math.max.apply(null, series.map(s => s.n));
  /* y-scale tops out at a round number above the data max */
  const nice = Math.ceil(maxA / 50) * 50;
  const x = i => PL + (series.length === 1 ? iw / 2 : (i / (series.length - 1)) * iw);
  const y = v => PT + ih - (v / nice) * ih;
  let svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Confirmed capital by month">';

  /* gridlines at round values: 0, 50, 100, 150 … */
  for (let g = 0; g <= 3; g++) {
    const val = nice * g / 3;
    const gy = y(val);
    svg += '<line class="gridln" x1="' + PL + '" x2="' + (W - PR) + '" y1="' + gy.toFixed(1) + '" y2="' + gy.toFixed(1) + '"/>';
    svg += '<text class="axis" x="' + (PL - 6) + '" y="' + (gy + 3).toFixed(1) + '" text-anchor="end">' +
      (val > 0 ? val.toFixed(0) + "B" : "0") + '</text>';
  }

  /* event count bars (secondary scale, bottom-aligned, translucent gray) */
  const bw = Math.min(14, (iw / series.length) * 0.42);
  series.forEach((s, i) => {
    const bh = (s.n / maxN) * ih * 0.72;
    svg += '<rect x="' + (x(i) - bw / 2) + '" y="' + (PT + ih - bh) + '" width="' + bw +
      '" height="' + bh + '" fill="#a1a1aa" opacity="0.55" rx="1.5"><title>' +
      esc(s.month) + " · " + s.n + " events</title></rect>";
  });

  /* capital area */
  let path = "", line = "";
  series.forEach((s, i) => {
    const px = x(i), py = y(s.amt);
    line += (i === 0 ? "M" : "L") + px.toFixed(1) + " " + py.toFixed(1) + " ";
  });
  path = line + "L" + x(series.length - 1).toFixed(1) + " " + (PT + ih) +
    " L" + x(0).toFixed(1) + " " + (PT + ih) + " Z";
  svg += '<path d="' + path + '" fill="rgba(4,120,87,0.14)"/>';
  svg += '<path d="' + line + '" fill="none" stroke="#047857" stroke-width="2" stroke-linejoin="round"/>';

  /* outlier dots + labels for the three spikes */
  const spikes = { "2026-03": "$125.9B", "2026-05": "$74.2B", "2026-01": "$23.8B", "2025-03": "$44.7B" };
  series.forEach((s, i) => {
    if (spikes[s.month]) {
      svg += '<circle cx="' + x(i) + '" cy="' + y(s.amt) + '" r="3.5" fill="#047857"/>';
      svg += '<text class="axis" x="' + Math.min(W - PR - 4, Math.max(PL + 4, x(i) + 6)) +
        '" y="' + Math.max(PT + 8, y(s.amt) - 8) + '" fill="#047857" style="fill:#047857">' +
        spikes[s.month] + '</text>';
    }
  });

  /* x labels: every 2nd month */
  const MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  series.forEach((s, i) => {
    if (i % 2 === 0 || i === series.length - 1) {
      const lab = MN[parseInt(s.month.slice(5, 7), 10) - 1] + " ’" + s.month.slice(2, 4);
      svg += '<text class="axis" x="' + x(i) + '" y="' + (H - 10) + '" text-anchor="middle">' +
        lab + '</text>';
      svg += '<line class="tick" x1="' + x(i) + '" x2="' + x(i) + '" y1="' + (PT + ih) + '" y2="' + (PT + ih + 4) + '"/>';
    }
  });
  svg += "</svg>";
  document.getElementById("monthlyChart").innerHTML = svg;

  /* concentration stack */
  const ranked = COS.map(c => c.amount_usd || 0).sort((a, b) => b - a);
  const total = ranked.reduce((s, v) => s + v, 0);
  const t5 = ranked.slice(0, 5).reduce((s, v) => s + v, 0);
  const t10 = ranked.slice(5, 10).reduce((s, v) => s + v, 0);
  const rest = total - t5 - t10;
  stackbar(document.getElementById("concStack"),
    [["Top 5 companies", t5, "74.6%", "#047857"],
     ["Next 5", t10, "8.1%", "#059669"],
     ["Other 108", rest, "17.3%", "#10b981"]],
    document.getElementById("concKey"));

  /* multiples */
  hbars(document.getElementById("multBars"),
    D.mults_top.map(m => [m.name + " · " + m.cat, m.m, m.m.toFixed(0) + "x", "mid"]));

  /* top rounds + valuations + exits */
  table(document.getElementById("topRounds"),
    [{ label: "Company" }, { label: "Category" }, { label: "Stage" },
     { label: "Round", num: true }, { label: "Date" }, { label: "Valuation", num: true }],
    D.top_rounds.map(r =>
      "<tr><td class='strong'>" + esc(r.name) + "</td><td class='dim'>" + esc(r.cat) +
      "</td><td class='dim'>" + esc(r.stage) + "</td><td class='num'>" + esc(r.amt) +
      "</td><td class='dim'>" + esc(r.date) + "</td><td class='num'>" + esc(r.val) + "</td></tr>"
    ).join(""),
    "Median multiple across the file: " + D.mults_median + "x (n=" + D.mults_n + " companies with both figures).");

  table(document.getElementById("topVals"),
    [{ label: "Company" }, { label: "Category" }, { label: "Known valuation", num: true }],
    D.top_vals.map(r =>
      "<tr><td class='strong'>" + esc(r.name) + "</td><td class='dim'>" + esc(r.cat) +
      "</td><td class='num'>" + esc(r.val) + "</td></tr>"
    ).join(""),
    "Marks are the latest credible valuation with its date; private marks are unaudited.");

  table(document.getElementById("exitTable"),
    [{ label: "Company" }, { label: "Category" }, { label: "Status" },
     { label: "Last known mark" }, { label: "Note" }],
    D.exits.map(r =>
      "<tr><td class='strong'>" + esc(r.name) + "</td><td class='dim'>" + esc(r.category) +
      "</td><td><span class='pill st-exit'>" + esc(r.status.replace(/_/g, " ")) + "</span></td>" +
      "<td class='num'>" + esc(r.valuation) + "</td><td class='dim' style='white-space:normal'>" +
      esc(r.note).slice(0, 110) + "</td></tr>"
    ).join(""),
    "Plus five public companies: Lemonade, Aurora Innovation, Duolingo, Zhipu AI, MiniMax.");
})();

/* ---------- 05 · timeline ---------- */
(function () {
  table(document.getElementById("monthTable"),
    [{ label: "Month" }, { label: "Events", num: true }, { label: "Confirmed capital", num: true },
     { label: "Largest event" }],
    D.month_rows.filter(m => m.month >= "2025-01").map(m =>
      "<tr><td class='strong'>" + esc(m.month) + "</td><td class='num'>" + m.n +
      "</td><td class='num'>" + (m.amt > 0 ? "$" + m.amt.toFixed(2) + "B" : "—") +
      "</td><td class='dim'>" + esc(m.big) + "</td></tr>"
    ).join(""),
    "October covers 24 of 31 days (pre-month-end snapshot). Partial events count toward the event tally but never toward confirmed capital.");

  table(document.getElementById("repeatTable"),
    [{ label: "Company" }, { label: "Rounds", num: true }, { label: "Confirmed", num: true },
     { label: "Dates" }, { label: "Stages" }],
    D.repeats.slice(0, 15).map(r =>
      "<tr><td class='strong'>" + esc(r.name) + "</td><td class='num'>" + r.rounds +
      "</td><td class='num'>" + (r.amt > 0 ? "$" + r.amt.toFixed(2) + "B" : "—") +
      "</td><td class='dim'>" + r.dates.map(d => esc(d)).join(" · ") +
      "</td><td class='dim'>" + r.stages.map(s => esc(s)).join(" · ") + "</td></tr>"
    ).join(""),
    D.repeats.length + " companies raised two or more times in the window; top 15 shown, sorted by confirmed capital.");
})();

/* ---------- 06 · segments ---------- */
(function () {
  /* category × stage cross-tab */
  const cats = Object.keys(D.categories);
  const bands = ["Seed/Pre", "A–B", "C–D", "E+ / Late / Public", "Other"];
  const band = st => {
    if (st === "Seed" || st === "Pre-Seed") return 0;
    if (st === "Series A" || st === "Series B") return 1;
    if (st === "Series C" || st === "Series D") return 2;
    if (/^Series [EFGHK]$/.test(st) || st === "Late Stage" || st === "IPO") return 3;
    return 4;
  };
  const wrap = document.getElementById("crossTab");
  const tt = el("table");
  const thead = el("thead");
  let hrow = "<tr><th>Category</th>";
  bands.forEach(b => hrow += "<th class='num'>" + b + "</th>");
  hrow += "<th class='num'>Total</th></tr>";
  thead.innerHTML = hrow;
  const tbody = el("tbody");
  let body = "";
  cats.forEach(c => {
    const counts = [0, 0, 0, 0, 0];
    COS.filter(co => co.category === c).forEach(co => counts[band(co.stage)]++);
    body += "<tr><td class='strong'>" + esc(c) + "</td>";
    counts.forEach(n => body += "<td class='num" + (n === 0 ? " dim" : "") + "'>" + (n || "·") + "</td>");
    body += "<td class='num'>" + D.categories[c] + "</td></tr>";
  });
  tbody.innerHTML = body;
  tt.appendChild(thead); tt.appendChild(tbody);
  wrap.innerHTML = ""; wrap.appendChild(tt);
  wrap.appendChild(el("div", "tblfoot",
    "Frontier Model companies are late-stage by default; the A–C bench lives in Applications and Infrastructure."));

  /* investor league table */
  table(document.getElementById("leagueTable"),
    [{ label: "Rank" }, { label: "Investor" }, { label: "Registry companies", num: true }],
    D.league.map((kv, i) =>
      "<tr><td class='num dim'>" + (i + 1) + "</td><td class='strong'>" + esc(kv[0]) +
      "</td><td class='num'>" + kv[1] + "</td></tr>"
    ).join(""),
    "Appearances across named investors of the 118 registry companies; a16z and Sequoia aliases merged. Nvidia's 16 include its strategic compute stakes.");
})();

/* ---------- 09 · playbook: stage funnel ---------- */
(function () {
  const band = st => {
    if (st === "Seed" || st === "Pre-Seed") return "Seed";
    if (st === "Series A" || st === "Series B") return "A–B";
    if (st === "Series C" || st === "Series D") return "C–D";
    if (/^Series [EFGHK]$/.test(st) || st === "Late Stage" || st === "IPO") return "E+ / Late / Public";
    return "Other";
  };
  const rows = [];
  ["Seed", "A–B", "C–D", "E+ / Late / Public"].forEach(b => {
    let n25 = 0, n26 = 0;
    COS.forEach(c => {
      const y = (c.round_date || "").slice(0, 4);
      if (band(c.stage) === b) { if (y === "2025") n25++; if (y === "2026") n26++; }
    });
    rows.push([b + " · 2025", n25, String(n25), "lt"]);
    rows.push([b + " · 2026", n26, String(n26), ""]);
  });
  hbars(document.getElementById("stageFunnel"), rows);
})();

/* ---------- 12 · explorer ---------- */
(function () {
  const tbody = document.querySelector("#expTable tbody");
  const qEl = document.getElementById("q");
  const catEl = document.getElementById("fcat");
  const regEl = document.getElementById("freg");
  const verEl = document.getElementById("fver");
  const cntEl = document.getElementById("cnt");

  const cats = [...new Set(COS.map(c => c.category))].sort();
  catEl.innerHTML = '<option value="">Category · all</option>' +
    cats.map(c => '<option>' + esc(c) + "</option>").join("");
  const regs = [...new Set(COS.map(c => c.region))].sort();
  regEl.innerHTML = '<option value="">Region · all</option>' +
    regs.map(r => '<option>' + esc(r) + "</option>").join("");

  const state = { q: "", cat: "", reg: "", ver: "", k: "amount_usd", dir: -1 };
  let openIdx = -1;

  function filtered() {
    const q = state.q.trim().toLowerCase();
    let out = COS.filter(c => {
      if (state.cat && c.category !== state.cat) return false;
      if (state.reg && c.region !== state.reg) return false;
      if (state.ver && c.verification !== state.ver) return false;
      if (q) {
        const hay = [c.name, c.category, c.sub, c.stage, c.hq, c.country,
          (c.investors || []).join(" "), (c.tags || []).join(" "), c.about].join(" ").toLowerCase();
        if (hay.indexOf(q) === -1) return false;
      }
      return true;
    });
    const k = state.k;
    out.sort((a, b) => {
      let va = a[k], vb = b[k];
      if (k === "name" || k === "category" || k === "stage" || k === "hq") {
        return state.dir * String(va || "").localeCompare(String(vb || ""));
      }
      va = va === null || va === undefined ? -Infinity : va;
      vb = vb === null || vb === undefined ? -Infinity : vb;
      return state.dir * (va - vb);
    });
    return out;
  }

  function statusPill(c) {
    if (c.status === "public") return "<span class='pill st-public'>public</span>";
    if (["acquired", "pending_acquisition", "majority_acquired"].indexOf(c.status) >= 0)
      return "<span class='pill st-exit'>" + esc(c.status.replace(/_/g, " ")) + "</span>";
    return "";
  }

  function render() {
    const rows = filtered();
    cntEl.textContent = rows.length + (rows.length === 1 ? " row" : " rows") +
      (rows.length !== COS.length ? " · of " + COS.length : "");
    let html = "";
    rows.forEach((c, i) => {
      const vd = c.valuation_usd === null || c.valuation_usd === undefined ? "—" :
        fmtB(c.valuation_usd / 1e9);
      const ad = c.amount_usd === null || c.amount_usd === undefined ? "—" :
        fmtB(c.amount_usd / 1e9);
      html += "<tr data-i='" + i + "'>" +
        "<td class='strong'>" + esc(c.name) + (statusPill(c) ? " " + statusPill(c) : "") + "</td>" +
        "<td class='dim'>" + esc(c.category) + "</td>" +
        "<td class='dim'>" + esc(c.stage) + "</td>" +
        "<td class='num'>" + esc(ad) + "</td>" +
        "<td class='num'>" + esc(vd) + "</td>" +
        "<td class='dim'>" + esc(c.round_date || "—") + "</td>" +
        "<td class='dim'>" + esc(c.hq || "—") + "</td>" +
        "<td class='num'>" + esc(c.founded || "—") + "</td>" +
        "<td><span class='pill v-" + esc(c.verification) + "'>" + esc(c.verification) + "</span></td>" +
        "</tr>";
      if (i === openIdx) {
        const inv = (c.investors || []).map(esc).join(" · ") || "—";
        const tags = (c.tags || []).map(t => "<span class='pill st-active' style='margin:0 6px 6px 0'>" + esc(t) + "</span>").join("") || "<span class='dim'>—</span>";
        const links = (c.sources || []).map(u =>
          '<a href="' + esc(u) + '" target="_blank" rel="noopener noreferrer">' + esc(u.replace(/^https?:\/\//, "").slice(0, 64)) + "</a>").join("") || "—";
        const desc = c.description && c.description.trim() ? c.description : c.about;
        html += "<tr class='xrow'><td colspan='9' class='xdetail'><div class='inner'>" +
          "<div><div class='dt'>What it does</div><p>" + esc(desc) + "</p>" +
          (c.website ? "<p style='margin-top:8px'><a href='" + esc(c.website) +
            "' target='_blank' rel='noopener noreferrer' style='color:var(--em7)'>" + esc(c.website.replace(/^https?:\/\//, "")) + "</a></p>" : "") +
          "</div>" +
          "<div><div class='dt'>Investors</div><p>" + inv + "</p>" +
          "<div class='dt' style='margin-top:12px'>Tags</div><div style='margin-top:4px'>" + tags + "</div></div>" +
          "<div><div class='dt'>Provenance</div><p>" + esc(c.source || "—") + "</p>" +
          "<div class='dt' style='margin-top:12px'>Sources</div><div class='links'>" + links + "</div></div>" +
          "</div></td></tr>";
      }
    });
    if (!rows.length) html = "<tr><td colspan='9' class='dim' style='text-align:center;padding:28px'>No companies match the current filters.</td></tr>";
    tbody.innerHTML = html;
    tbody.querySelectorAll("tr[data-i]").forEach(tr => {
      tr.addEventListener("click", () => {
        const i = parseInt(tr.getAttribute("data-i"), 10);
        openIdx = openIdx === i ? -1 : i;
        render();
      });
    });
  }

  qEl.addEventListener("input", () => { state.q = qEl.value; openIdx = -1; render(); });
  catEl.addEventListener("change", () => { state.cat = catEl.value; openIdx = -1; render(); });
  regEl.addEventListener("change", () => { state.reg = regEl.value; openIdx = -1; render(); });
  verEl.addEventListener("change", () => { state.ver = verEl.value; openIdx = -1; render(); });

  document.querySelectorAll("#expTable .th-sort").forEach(th => {
    th.addEventListener("click", () => {
      const k = th.getAttribute("data-k");
      if (state.k === k) state.dir *= -1;
      else { state.k = k; state.dir = -1; }
      document.querySelectorAll("#expTable .th-sort").forEach(o => {
        o.querySelectorAll(".arr").forEach(a => a.remove());
      });
      const a = el("span", "arr", state.dir === -1 ? " ▼" : " ▲");
      th.appendChild(a);
      render();
    });
  });

  render();
})();

/* ---------- header: progress bar + active chapter ---------- */
(function () {
  const bar = document.getElementById("progress");
  const links = Array.prototype.slice.call(document.querySelectorAll("nav.tabs a"));
  const map = {};
  links.forEach(l => { map[l.getAttribute("href").slice(1)] = l; });
  function onScroll() {
    const doc = document.documentElement;
    const max = doc.scrollHeight - doc.clientHeight;
    bar.style.transform = "scaleX(" + (max > 0 ? window.scrollY / max : 0) + ")";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const current = () => {
    let id = "overview";
    Object.keys(map).forEach(sec => {
      const e = document.getElementById(sec);
      if (e && e.getBoundingClientRect().top <= 120) id = sec;
    });
    return id;
  };
  function mark() {
    const id = current();
    links.forEach(l => l.classList.toggle("on", l.getAttribute("href") === "#" + id));
  }
  window.addEventListener("scroll", mark, { passive: true });
  mark();
})();

/* ---------- reveal on scroll ---------- */
(function () {
  const items = Array.prototype.slice.call(document.querySelectorAll(".rv"));
  function sweep() {
    const line = window.innerHeight * 0.95;
    items.forEach(n => {
      if (!n.classList.contains("in") && n.getBoundingClientRect().top < line) {
        n.classList.add("in");
      }
    });
  }
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
  items.forEach(n => io.observe(n));
  window.addEventListener("scroll", sweep, { passive: true });
  window.addEventListener("resize", sweep, { passive: true });
  sweep();
})();

})();
