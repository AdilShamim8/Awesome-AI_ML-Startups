#!/usr/bin/env python3
"""Regenerate categories/*.md from the master dataset.

Tables are generated from live data; the 'Spotlight' and 'Key Trends' sections
come from curated CATEGORY_INSIGHTS below (updated each monthly rebuild).
"""

import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).parent.parent
MASTER = REPO / "data" / "master" / "startups_master.json"

CATEGORY_FILES = {
    "AI/ML": ("ai-ml", "🤖", "Core AI & machine learning platforms"),
    "Generative AI": ("generative-ai", "✨", "LLMs, image gen, video gen, creative AI"),
    "AI Agents": ("ai-agents", "🕵️", "Autonomous AI agents & agentic systems"),
    "SaaS": ("saas", "💻", "AI-powered SaaS products"),
    "DevTools": ("devtools", "🛠️", "Developer tools & infrastructure"),
    "FinTech": ("fintech", "💰", "AI-driven financial technology"),
    "HealthTech": ("healthtech", "🏥", "AI in healthcare & biotech"),
    "Robotics": ("robotics", "🦾", "AI robotics, defense & autonomous systems"),
    "Cybersecurity": ("cybersecurity", "🔒", "AI security & threat detection"),
    "EdTech": ("edtech", "📚", "AI in education & learning"),
}

CATEGORY_INSIGHTS = {
    "Generative AI": {
        "spotlight": [
            ("OpenAI", "closed a $122B round at an $852B valuation (Mar 2026) and is in talks for $30B+ more at ~$1.25-1.4T as of late October 2026"),
            ("Anthropic", "filed its IPO prospectus in September 2026; share marketing is expected the week of November 9 after $16.8B Q3 revenue"),
            ("DeepSeek", "raised $7.4B+ in its first external round at $50B+ (Jun 2026), then reportedly ~$15B more at ~$74B ahead of a China IPO"),
            ("Mistral AI", "closed a €3B Series D at €21B led by Samsung (Sep 8, 2026) — the largest European tech equity round ever"),
            ("ElevenLabs", "doubled to a $22B mark via a $300M employee tender (Sep 30, 2026) after its $500M Series D at $11B"),
        ],
        "trends": (
            "Foundation-model financing reached unprecedented scale in 2026 — and then globalized. OpenAI ($122B, Mar), Anthropic ($65B, "
            "May), and xAI ($20B, Jan — before merging into SpaceX) concentrated capital at the top, while China's open-weight labs "
            "arrived as a new pole: DeepSeek ($7.4B first external round at $50B+), Moonshot AI (~$2B at $20B), and the Hong Kong "
            "listings of Z.ai and MiniMax created a public-market window for Chinese frontier AI. Sovereign AI became a business model "
            "(Mistral's €3B Series D, Sarvam's India stack), and specialists converted vertical excellence into multi-billion marks "
            "(ElevenLabs' $22B tender, Suno at $5.4B). The October watch item: Anthropic's IPO — the first frontier-lab listing — with "
            "marketing expected the week of November 9, 2026."
        ),
    },
    "AI/ML": {
        "spotlight": [
            ("Etched", "raised $700M at a $21B valuation led by Jane Street (Sep 2026) for transformer-only inference silicon, with $40-50B offers reported in October"),
            ("TypeSafe AI", "landed an $870M Series A at $7.5B (Oct 9, 2026) for Jev, a non-text model outputting calibrated decisions"),
            ("Crusoe", "announced a $3.9B Series F at $30.9B post-money (Sep 17, 2026) with $140B+ in total contracted value"),
            ("Sakana AI", "anchors Japan's frontier research with a $135M Series B at $2.65B plus strategic investments from Google and Salesforce Ventures"),
            ("Sarvam AI", "raised $234M at $1.5B with HCLTech as lead strategic investor to build India's sovereign AI stack"),
        ],
        "trends": (
            "The AI infrastructure stack absorbed the majority of 2026's non-lab funding, and the frontier widened geographically and "
            "technologically. Inference economics now drive the biggest checks: inference clouds (Fireworks at $17.5B, Baseten at $13B, "
            "Together AI at $8.3B), GPU/energy clouds (Crusoe's $3.9B Series F at $30.9B), and purpose-built silicon (Etched's Sohu at "
            "$21B, with $40-50B offers reported). New archetypes appeared in October: TypeSafe AI's decision-output models (an $870M "
            "Series A at $7.5B weeks after launch) and sovereign research labs in Japan (Sakana) and India (Sarvam). Scale AI's "
            "post-Meta trajectory — $1B revenue expected in 2026 and a Pentagon enterprise agreement expanded to $500M — shows data "
            "infrastructure maturing into defense-grade business."
        ),
    },
    "AI Agents": {
        "spotlight": [
            ("Cognition", "raised $2B at $48B (Sep 8, 2026) — a near-doubling in four months as Devin's run-rate revenue climbed to ~$900M"),
            ("Harvey", "raised $550M at $15.5B (Sep 9, 2026), its third round of 2026, on $350M+ annualized legal-AI revenue"),
            ("Manus AI", "raised $500M+ at $4B (Oct 8, 2026) in its first round since Beijing unwound Meta's $2B acquisition"),
            ("Sierra", "held its $15.8B mark from May 2026 as agentic customer experience became an enterprise standard"),
            ("Norm Ai", "reached a $1.2B valuation on a $120M Series C (Jul 2026) for regulatory-compliance agents"),
        ],
        "trends": (
            "2026 is the year agents went from demos to P&L — and started going global. Software-engineering agents re-rated fastest "
            "(Cognition $26B→$48B in four months; Cursor sold to SpaceX for $60B), professional-services agents compounded (Harvey at "
            "$15.5B with $350M+ ARR; Legora past $100M ARR), and China entered the category directly: Manus raised $500M+ at $4B "
            "after Beijing unwound Meta's acquisition — a geopolitical first for agent M&A. Compliance emerged as a killer vertical "
            "(Norm Ai at $1.2B), and agentic CX (Sierra, Decagon) held its valuations as enterprises moved agents into production."
        ),
    },
    "SaaS": {
        "spotlight": [
            ("Pigment", "raised $250M at $2.3B (Oct 20, 2026) for AI-enabled business planning — one of Europe's largest enterprise rounds of the month"),
            ("EliseAI", "added $350M in early October 2026 after its $250M August 2025 round, on housing-AI recurring revenue"),
            ("Owner", "raised $240M at $2.3B (Aug 2026) as AI growth infrastructure for local restaurants"),
            ("Omnea", "scaled to a $50M Series B as 'agentic procurement' became a category"),
            ("LMArena", "became the standard evaluation layer for frontier models at a $1.7B valuation"),
        ],
        "trends": (
            "Vertical SaaS is being rebuilt around AI-native workflows, and the October window showed the money following proof: "
            "EliseAI's $350M and Pigment's $250M at $2.3B both reward companies with established recurring revenue rather than "
            "promises. The fastest growers sell outcomes — revenue, sourced spend, filled units — instead of seats, and agentic "
            "buyers are emerging as a customer class that purchases via APIs. Evaluation and observability (LMArena, Momentic) "
            "remains must-have infrastructure as enterprises move AI into production."
        ),
    },
    "DevTools": {
        "spotlight": [
            ("Cursor/Anysphere", "acquisition by SpaceX closed in August 2026 — a $60B all-stock deal after ~$4B ARR"),
            ("Supabase", "doubled to $10.5B as the default backend of AI-generated apps"),
            ("Replit", "tripled to $9B as vibe-coding hit the enterprise; made OpenAI its default model provider"),
            ("Lovable", "reached $13.3B — the fastest European software growth story on record"),
            ("Stripe/OpenRouter", "a $7.5B deal put model routing inside payments infrastructure"),
        ],
        "trends": (
            "AI app builders (Cursor, Replit, Lovable, bolt.new) compressed the SaaS creation stack, pulling backend services "
            "(Supabase) and deployment (Vercel) into their wake as the 'AI factory floor' for software. Strategic consolidation "
            "accelerated: SpaceX bought Cursor for $60B, Stripe bought OpenRouter for $7.5B, and inference gateways became "
            "acquisition targets for platforms building agent-facing financial rails. Developer tools are now valued on usage-based "
            "revenue, not seats."
        ),
    },
    "FinTech": {
        "spotlight": [
            ("Ramp", "raised $1.85B at $60B (Oct 15, 2026) led by Dragoneer — annualized revenue topped $2B"),
            ("Stripe", "reached a $159B tender valuation and moved to acquire OpenRouter for $7.5B"),
            ("Plaid", "climbed to an $8B valuation ahead of a long-anticipated IPO"),
            ("Mercury", "hit $5.2B as startup banking rebounded"),
            ("Brex", "was acquired by Capital One for $5.15B — the sector's landmark consolidation"),
        ],
        "trends": (
            "AI-native fintech decoupled from the 2021-22 valuation reset, and October set a new high-water mark: Ramp's $1.85B "
            "primary at $60B (36% above June) with $2B+ ARR makes it the most valuable private fintech outside Stripe. Consolidation "
            "arrived from both directions — Capital One bought Brex, Stripe finalized its $7.5B OpenRouter acquisition to put model "
            "routing inside payments — while agent-payments infrastructure (Maven's PCI-compliant APIs for voice agents) emerged as "
            "the newest sub-sector. IPO pipelines (Stripe, Plaid) should reshape the public fintech landscape in 2027."
        ),
    },
    "HealthTech": {
        "spotlight": [
            ("OpenEvidence", "became the fastest-adopted physician tool in history at a $12B valuation"),
            ("Abridge", "reached $5.3B and ~2,000 employees as ambient documentation became standard"),
            ("Hippocratic AI", "hit $3.5B on safety-certified patient-facing agents"),
            ("Avoca", "scaled vertical AI agents into home services with $125M raised"),
            ("Beacon Health", "is deploying AI employees inside EHRs fresh out of YC W26"),
        ],
        "trends": (
            "Clinical AI crossed from pilot to standard of care: ambient documentation (Abridge) and evidence search (OpenEvidence) "
            "now touch a majority of US health systems and physicians respectively. Patient-facing voice agents (Hippocratic AI) "
            "cleared safety reviews at scale, and revenue-cycle automation became the financing magnet. Vertical agent companies "
            "increasingly blur the health/home-services boundary — the playbook of domain-specific agents with hard ROI applies "
            "across regulated industries."
        ),
    },
    "Robotics": {
        "spotlight": [
            ("Figure AI", "holds the US robotics valuation crown at $39B after a $1B+ Series C"),
            ("Anduril", "closed $5B at $61B (May 2026) with ~$100B talks reported by July"),
            ("Walden Robotics", "launched from stealth with a $300M seed at $1.1B (Jul 15, 2026) — Toyota-led, from MIT's Russ Tedrake"),
            ("CMR Surgical", "received a ~$400M Stryker strategic investment with an exclusive acquisition option (Oct 12, 2026)"),
            ("Atoms", "raised $1.7B led by a16z (Jul 22, 2026) as Travis Kalanick's industrial-automation holding company"),
        ],
        "trends": (
            "Robotics financing split into parallel booms in 2026 — humanoids, robot foundation models, defense autonomy — and "
            "October added a fourth: strategic consolidation. Stryker's ~$400M investment in CMR Surgical with an acquisition option "
            "brings surgical robotics into the mega-cap orbit, while Walden Robotics' $300M Toyota-led seed (Large Behavior Models "
            "out of MIT/TRI) shows research pedigrees converting directly into production deployments. Defense autonomy players "
            "(Anduril, Helsing, Shield AI, Saronic, Castelion, Hadrian) raised $10B+ in 2026 alone, and Atoms' $1.7B round "
            "signals that industrial automation is attracting platform-scale capital. The projected $20B+ humanoid funding wave "
            "remains materially underway, backed by BotQ and Mercedes production commitments."
        ),
    },
    "Cybersecurity": {
        "spotlight": [
            ("Wiz", "was acquired by Google for $32B — completed March 11, 2026"),
            ("Cyera", "raised $600M at $12B to govern what AI can see and do"),
            ("7AI", "closed a $130M Series A for agentic security operations"),
            ("Adaptive Security", "landed NVIDIA and Citi as backers for AI-era human-risk defense"),
            ("Doppel", "scaled social-engineering defense to a $70M Series C"),
        ],
        "trends": (
            "Security spending reoriented around two AI realities: AI is the attacker's tool (deepfake phishing, adaptive social "
            "engineering) and the enterprise's biggest unmanaged asset (data feeding agents). DSPM/data-governance (Cyera) and "
            "agentic SOC automation (7AI, Doppel) captured outsized rounds, while Google's $32B Wiz close validated cloud security "
            "as the sector's premium asset. Human-risk platforms (Adaptive Security) turned deepfake-era training into a growth "
            "category."
        ),
    },
    "EdTech": {
        "spotlight": [
            ("Duolingo", "remains the AI-native consumer learning benchmark at public scale"),
            ("MagicSchool", "scaled teacher AI to millions of educators on a $45M Series B"),
            ("Sana", "was acquired by Workday for ~$1.1B, its largest deal ever"),
            ("Coconote", "grew YC-backed consumer study tools into a global student base"),
            ("Rork", "extends AI app-building into mobile-first learning products"),
        ],
        "trends": (
            "EdTech's recovery is being driven by AI-native product experiences rather than pandemic-era tailwinds: consumer study "
            "tools (Coconote) and teacher copilots (MagicSchool) grow without paid acquisition, while enterprise learning "
            "consolidated into HR platforms (Workday-Sana at $1.1B). Language learning at Duolingo proved AI curriculum generation "
            "at scale, and the next wave is agentic tutors that complete — not just support — learning workflows."
        ),
    },
}


def fmt_money(rec):
    stage = rec["funding_stage"]
    amount = rec["funding_amount"]
    if amount in ("N/A", None, ""):
        return stage
    return f"{stage}, {amount}"


def build_category(cat, insights):
    slug, emoji, blurb = CATEGORY_FILES[cat]
    with open(MASTER, encoding="utf-8") as f:
        master = json.load(f)
    rows = [s for s in master["startups"] if s["category"] == cat]
    rows.sort(key=lambda s: (s.get("funding_amount_usd") or 0), reverse=True)
    as_of = master["metadata"].get("as_of", "unknown")
    try:
        from datetime import date as _d
        y, m, dd = (int(x) for x in as_of.split("-"))
        as_of_pretty = _d(y, m, dd).strftime("%B %-d, %Y") if hasattr(_d(y, m, dd), "strftime") else as_of
    except (ValueError, AttributeError):
        as_of_pretty = as_of

    lines = [
        f"# {emoji} {cat} Startups",
        "",
        f"> {blurb} — last updated {as_of_pretty}",
        "",
        f"{len(rows)} companies tracked. Sorted by latest round size. Data: [master dataset](../data/master/startups_master.json).",
        "",
        "| # | Startup | About | Stage | Round | Valuation | Website |",
        "|---|---------|-------|-------|-------|-----------|---------|",
    ]
    for i, s in enumerate(rows, 1):
        host = s["website"].replace("https://", "").replace("http://", "").rstrip("/")
        val = s.get("valuation_display") or "—"
        lines.append(
            f'| {i} | **{s["startup_name"]}** | {s["about"]} | {s["funding_stage"]} '
            f'| {s["funding_amount"]} | {val} | [{host}]({s["website"]}) |'
        )

    spot = insights.get("spotlight", [])
    trends = insights.get("trends", "")
    lines += ["", f"### Spotlight — {as_of_pretty}", ""]
    for name, note in spot:
        lines.append(f"- **{name}** {note}")
    lines += ["", "### Key Trends", "", trends, ""]
    return "\n".join(lines)


def main():
    counts = Counter()
    for cat in CATEGORY_FILES:
        md = build_category(cat, CATEGORY_INSIGHTS[cat])
        slug = CATEGORY_FILES[cat][0]
        path = REPO / "categories" / f"{slug}.md"
        path.write_text(md, encoding="utf-8")
        counts[cat] = md.count("| **")
    print("Category pages regenerated:")
    for cat, n in counts.items():
        print(f"  {cat:<15} {n} companies")


if __name__ == "__main__":
    main()
