# 🤝 Contributing to Awesome AI/ML Startups

First off, thank you for considering contributing to this project! 🎉 This repository thrives because of community contributions like yours.

## 🌟 Ways to Contribute

### 1. Add a New Startup

This is the most valuable contribution! If you know of an AI/ML or tech startup that should be listed:

1. **Fork** this repository
2. **Add** the startup to the **current month's** CSV and JSON files in `data/2026/<month>/`
3. **Update** the relevant category file in `categories/`
4. **Submit** a Pull Request with the title: `Add [Startup Name] - [Month Year]`

### 2. Update Existing Data

If a startup has new funding, changed categories, or updated descriptions:

1. **Fork** this repository
2. **Update** the relevant entries in the current month's data files
3. **Submit** a Pull Request with the title: `Update [Startup Name] - [Field Changed]`

### 3. Fix Errors

Found a broken link, incorrect data, or typo? We appreciate fixes!

1. **Fork** this repository
2. **Fix** the error
3. **Submit** a Pull Request with the title: `Fix [Description]`

### 4. Suggest New Categories or Sources

Open an [Issue](https://github.com/your-username/awesome-ai-ml-startups/issues) with:
- The proposed category name and description
- OR the new data source with URL and relevance

---

## 📋 Data Schema Requirements

When adding a startup, use this exact schema:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | 3-digit unique ID (e.g., "061") |
| `startup_name` | string | ✅ | Official company name |
| `about` | string | ✅ | Short tagline (1 line, under 100 chars) |
| `description` | string | ✅ | Detailed description (2-3 sentences) |
| `website` | URL | ✅ | Working direct link to the startup |
| `category` | string | ✅ | One of the defined categories |
| `funding_stage` | string | ✅ | Latest known funding stage |
| `funding_amount` | string | ✅ | Latest known funding amount |
| `headquarters` | string | ✅ | City, Country |
| `founded_year` | integer | ✅ | Year the company was founded |
| `source` | string | ✅ | Where you found the data |
| `date_added` | date | ✅ | YYYY-MM-DD format |

### Valid Categories

- `AI/ML` — Core AI & machine learning platforms
- `Generative AI` — LLMs, image gen, video gen, creative AI
- `AI Agents` — Autonomous AI agents & agentic systems
- `SaaS` — AI-powered SaaS products
- `DevTools` — Developer tools & infrastructure
- `FinTech` — AI-driven financial technology
- `HealthTech` — AI in healthcare & biotech
- `Robotics` — AI robotics & autonomous systems
- `Cybersecurity` — AI security & threat detection
- `EdTech` — AI in education & learning

### Valid Funding Stages

- `Pre-Seed`
- `Seed`
- `Series A`
- `Series B`
- `Series C`
- `Series D`
- `Series E`
- `Series F`
- `Late Stage`
- `IPO`

---

## ✅ Contribution Checklist

Before submitting your Pull Request, verify:

- [ ] The startup has a **working website** (not a parked domain)
- [ ] The startup is **real and operational** (not vaporware or stealth)
- [ ] The data includes a **verifiable source** (YC, Crunchbase, Forbes, etc.)
- [ ] The entry follows the **exact schema** format
- [ ] No **duplicate** entries exist in the current month's data
- [ ] Both **CSV and JSON** files are updated
- [ ] The relevant **category file** is updated
- [ ] The `id` is **unique** for the current month

---

## ❌ What NOT to Contribute

- ❌ **Stealth startups** without public information
- ❌ **Vaporware** — companies with no product or users
- ❌ **Affiliate links** or referral codes
- ❌ **Duplicate entries** — check existing data first
- ❌ **Inaccurate data** — verify before adding
- ❌ **Promotional content** — keep descriptions objective
- ❌ **Startups older than 10 years** without significant AI/ML pivot (we focus on newer companies or older ones with recent AI transformation)

---

## 🔄 Monthly Update Process

On the **30th of each month**, the maintainers will:

1. Review and merge all pending Pull Requests
2. Create the new month's data files
3. Update category files with new entries
4. Update the README with new statistics
5. Archive the previous month's data
6. Publish the monthly update

---

## 📝 Pull Request Template

```markdown
## Type of Change
- [ ] New startup added
- [ ] Existing data updated
- [ ] Error fix
- [ ] New category/source suggestion

## Startup Details (if adding)
- **Name:**
- **Website:**
- **Category:**
- **Source:**

## Checklist
- [ ] Working website verified
- [ ] Data source cited
- [ ] Schema format followed
- [ ] No duplicate entries
- [ ] CSV and JSON both updated
- [ ] Category file updated

## Additional Notes
(Any context about this contribution)
```

---

## 💬 Questions?

Open an [Issue](https://github.com/your-username/awesome-ai-ml-startups/issues) or start a [Discussion](https://github.com/your-username/awesome-ai-ml-startups/discussions) — we're happy to help!

Thank you for contributing! 🚀
