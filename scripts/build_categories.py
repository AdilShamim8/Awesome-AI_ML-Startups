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
            ("OpenAI", "closed a $122B round at an $852B valuation (Mar 2026) — the largest private raise ever"),
            ("Anthropic", "raised $65B at $965B post-money in May 2026, overtaking OpenAI as the world's most valuable startup"),
            ("ElevenLabs", "hit an $11B valuation in February 2026 and is weighing an IPO"),
            ("Lovable", "became Europe's most valuable AI startup at $13.3B after a $400M Series C in August 2026"),
            ("Suno", "tripled its valuation to $5.4B in eight months on the back of consumer music generation"),
        ],
        "trends": (
            "Foundation-model financing reached unprecedented scale in 2026: OpenAI ($122B), Anthropic ($65B), and xAI ($20B) "
            "accounted for roughly 43% of all global venture funding in H1 2026 per Crunchbase. Frontier labs are consolidating "
            "capital while specialized generators (ElevenLabs for voice, Suno for music, Runway and Synthesia for video, Black Forest "
            "Labs for images) convert vertical excellence into multi-billion valuations. European labs (Mistral, Black Forest Labs, "
            "Lovable) raised mega-rounds without ceding independence, and code-generation models (Poolside's $6B Nvidia licensing "
            "deal) opened a new licensing-driven business model."
        ),
    },
    "AI/ML": {
        "spotlight": [
            ("Databricks", "reached a $188B valuation in August 2026 with revenue run-rate above $5.4B"),
            ("Together AI", "raised an $800M Series C at $8.3B led by Aramco Ventures (Jul 2026)"),
            ("Fireworks AI", "closed a $1.5B Series D at $17.5B alongside announcing $1B ARR"),
            ("Baseten", "quadrupled its valuation to $13B in 18 months on inference demand"),
            ("Scale AI", "saw Meta take a 49% stake at a $29B valuation, reshaping the data-labeling market"),
        ],
        "trends": (
            "The AI infrastructure stack absorbed the majority of 2026's non-lab funding: inference clouds (Fireworks, Baseten, "
            "Together AI, Groq), GPU clouds (Lambda, Crusoe at $30B), data platforms (Databricks at $188B, ClickHouse at $15B), and "
            "data-labeling suppliers (Surge AI, Mercor, Scale AI post-Meta) all raised mega-rounds. Two structural shifts define the "
            "year: inference — not training — became the volume business, with $1B+ ARR now common; and power/real-estate constraints "
            "turned data-center orchestration (Crusoe, Emerald AI) into a venture category of its own."
        ),
    },
    "AI Agents": {
        "spotlight": [
            ("Sierra", "raised $950M at $15.8B (May 2026) as agentic CX became an enterprise standard"),
            ("Cognition", "doubled to a $26B valuation in eight months on Devin's $492M ARR"),
            ("Harvey", "reached $11B in March 2026, with talks at $15.5B by August"),
            ("Legora", "tripled to $5.6B as European legal AI went mainstream"),
            ("Instinct", "jumped to a $2.5B Series B within roughly a year of founding"),
        ],
        "trends": (
            "2026 is the year agents went from demos to P&L: customer-experience agents (Sierra, Decagon), software-engineering "
            "agents (Cognition's Devin, Anysphere's Cursor), and professional-services agents (Harvey, Legora) all crossed hundreds "
            "of millions in ARR. Horizontal infrastructure consolidated around LangChain's orchestration stack, while consumer "
            "assistants (Instinct) attracted venture-scale bets at unprecedented seed-to-Series-B velocity. Valuations re-rated 2-3x "
            "across the board as agents began replacing — not just assisting — knowledge-work workflows."
        ),
    },
    "SaaS": {
        "spotlight": [
            ("Owner", "raised $240M at $2.3B (Aug 2026) as AI growth infrastructure for local restaurants"),
            ("Omnea", "scaled to a $50M Series B as 'agentic procurement' became a category"),
            ("DeepJudge", "raised $41M to bring precision AI search to large law firms"),
            ("Listen Labs", "tripled down on AI-moderated research with a $100M total raise"),
            ("LMArena", "became the standard evaluation layer for frontier models at a $1.7B valuation"),
        ],
        "trends": (
            "Vertical SaaS is being rebuilt around AI-native workflows rather than AI features bolted onto legacy suites. The "
            "fastest growers (Owner, Omnea) sell outcomes — revenue, sourced spend — instead of seats, and agentic buyers are "
            "emerging as a new customer class that purchases via APIs rather than UIs. Evaluation and observability (LMArena, "
            "Momentic in testing) turned into must-have infrastructure as enterprises moved AI systems into production."
        ),
    },
    "DevTools": {
        "spotlight": [
            ("Cursor/Anysphere", "agreed to a $60B all-stock acquisition by SpaceX (Jun 2026) after $2B+ ARR"),
            ("Supabase", "doubled to $10.5B as the default backend of AI-generated apps"),
            ("Replit", "tripled to $9B as vibe-coding hit the enterprise"),
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
            ("Ramp", "raised $750M at $44B (Jun 2026) with an AI-agent story investors rewarded"),
            ("Stripe", "reached a $159B tender valuation and moved to acquire OpenRouter"),
            ("Plaid", "climbed to an $8B valuation ahead of a long-anticipated IPO"),
            ("Mercury", "hit $5.2B as startup banking rebounded"),
            ("Brex", "was acquired by Capital One for $5.15B — the sector's landmark consolidation"),
        ],
        "trends": (
            "AI-native fintech decoupled from the 2021-22 valuation reset: Ramp nearly tripled to $44B and Stripe more than "
            "recovered its peak, both selling 'AI does the finance work' rather than software licenses. Consolidation arrived from "
            "both directions — Capital One bought Brex, Stripe absorbed OpenRouter — while agent-payments infrastructure (Maven's "
            "PCI-compliant APIs for voice agents) emerged as the newest sub-sector. IPO pipelines (Stripe, Plaid, Cohere-adjacent "
            "processors) should reshape the public fintech landscape in 2027."
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
            ("Anduril", "closed $5B at $61B (May 2026) with $100B talks reported by July"),
            ("Helsing", "set Europe's defense record: $1.8B at $18B"),
            ("Skild AI", "tripled to $14B+ for its general-purpose robot brain"),
            ("Saronic", "doubled to $9.25B while building a $3.2B autonomous shipyard"),
        ],
        "trends": (
            "Robotics financing split into three parallel booms in 2026: humanoids (Figure, Apptronik, 1X), robot foundation models "
            "(Skild, Physical Intelligence, Generalist), and defense autonomy (Anduril, Helsing, Shield AI, Saronic, Castelion, "
            "Hadrian — which together raised $10B+ in 2026 alone). Foundation-model-for-robots became venture's favorite thesis, and "
            "European defense procurement unlocked record rounds. The humanoid sector's projected $20B+ funding wave is now "
            "materially underway, backed by production commitments from Figure's BotQ to Apptronik's Mercedes partnership."
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

    lines = [
        f"# {emoji} {cat} Startups",
        "",
        f"> {blurb} — last updated September 7, 2026",
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
    lines += ["", "### Spotlight — September 2026", ""]
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
