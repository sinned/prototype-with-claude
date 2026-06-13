# Build a Lead Qualification Agent in 20 Minutes

This walkthrough goes end-to-end: from nothing to a working agent that qualifies leads against your ICP, passes an eval suite, and runs in production via the Agent SDK.

**What you'll have at the end:**
- A working lead qualifier skill (`/qualify-lead <company>`)
- An ICP definition file you can tweak without changing any code
- A test suite with 5 cases and a passing eval score
- A production Python script that processes a CSV of leads overnight

**Time:** ~20 minutes  
**Prerequisites:** Claude Code installed, repo cloned, `cd prototype-with-claude && claude`

---

## Part 1 — Run the built-in skill (2 minutes)

The `qualify-lead` skill is already installed. Try it now:

```
/qualify-lead Retool
```

Claude will:
1. Search for Retool's company overview, headcount, funding stage
2. Search for recent job postings (AE, SDR, revenue roles)
3. Score each criterion against the default ICP
4. Write a report to `output/leads/retool-qualification.md`

**Expected output** (actual Claude output will vary):

```markdown
# Lead Qualification: Retool
*Qualified: 2025-06-12 | Tier: HOT*

## Decision
**HOT** — B2B SaaS internal tools platform, Series C ($145M raised), ~450 employees,
12 open Account Executive roles confirming active GTM investment.

## ICP Scorecard

| Criterion       | Score | Evidence                                          |
|-----------------|-------|---------------------------------------------------|
| Company size    | ✅    | ~450 employees (LinkedIn, May 2025)               |
| Industry fit    | ✅    | Developer tools, internal tooling — B2B SaaS      |
| Geography       | ✅    | Headquarters: San Francisco, CA; US-primary sales |
| Stage / funding | ✅    | Series C, $145M total funding (Sequoia, YC)       |
| Pain signal     | ✅    | 12 open AE roles, 3 SDR roles (LinkedIn, May 2025)|

## Company Overview
Retool is a low-code platform for building internal business applications.
Customers are mid-market and enterprise engineering teams who need custom
dashboards, admin panels, and internal tools without full engineering cycles.
Their pricing is seat-based and scales with team size.

## Recommended next step
Book a discovery call with their VP Sales. Lead with the SDR build-out — they're
constructing an outbound motion and are likely evaluating sales enablement,
sequencing, and enablement tooling. Mention their engineering-led customer profile.

## Sources
- https://retool.com/about
- https://www.linkedin.com/company/tryretool/jobs/
- https://www.crunchbase.com/organization/retool
```

---

## Part 2 — Customize your ICP (5 minutes)

The default ICP (B2B SaaS, 50-500 employees, Series A+) is a starting point. Replace it with yours.

Create `icp.md` in the repo root:

```markdown
# My ICP

## Hard criteria (disqualify if not met)
- Must be a B2B company — not consumer, not marketplace
- Must be in software, tech-enabled services, or professional services
- Must have at least 25 employees

## Soft criteria (score, but don't auto-disqualify)
- Company size: 50–500 employees (sweet spot: 100–250)
- Geography: North America or Western Europe
- Stage: Series A through Series C, or profitable SMB ($2M–$50M ARR)

## Strong positive signals (weight these heavily)
- Raised funding in the last 18 months
- Actively hiring Account Executive or SDR roles
- Fast headcount growth — >25% YoY on LinkedIn
- Using Salesforce or HubSpot (signals they have a sales motion)

## Negative signals (reduce score, don't disqualify)
- No dedicated sales team yet
- Consumer-facing product as primary revenue
- Seed stage with no enterprise customers yet
```

Now re-run:
```
/qualify-lead Retool
```

The skill reads your `icp.md` automatically. The scoring criteria update without touching the skill.

Run a few more to test it:
```
/qualify-lead Notion
/qualify-lead "Duolingo"
/qualify-lead "a16z"
```

Notice how `Duolingo` and `a16z` come back Cold or Disqualified — Duolingo is B2C and a16z is a VC, not a company you'd sell to.

---

## Part 3 — Add test cases (5 minutes)

Running a skill on 3 examples isn't enough. Test cases give you a reproducible quality score.

Create `.claude/skills/qualify-lead/evals/test-cases.md`:

```markdown
# Test Cases: qualify-lead

## Test 1: Clear hot lead (happy path)
**Input:** Retool

**Criteria:**
- [ ] Tier is HOT or WARM
- [ ] ICP Scorecard table is present with 5 rows
- [ ] Every row has a ✅, ⚠️, ❌, or ❓ — no empty scores
- [ ] Recommended next step is specific, not generic
- [ ] At least 2 source URLs are cited

---

## Test 2: Clear disqualify (consumer company)
**Input:** Duolingo

**Criteria:**
- [ ] Tier is COLD or DISQUALIFIED
- [ ] Report mentions consumer focus as the reason
- [ ] Does NOT recommend booking a discovery call
- [ ] Sources cited

---

## Test 3: Edge case — well-known but limited ICP fit
**Input:** Notion

**Criteria:**
- [ ] Tier is WARM (PLG model, large headcount is borderline)
- [ ] Company size is marked ⚠️ or ❌ (Notion has ~600+ employees, above our ICP)
- [ ] Pain signal section notes their sales team size or hiring
- [ ] Recommended next step acknowledges the fit caveat

---

## Test 4: Limited public information
**Input:** "Runway Financial"

**Criteria:**
- [ ] Report is produced (not an error or refusal)
- [ ] Any unverifiable criteria are marked ❓, not guessed
- [ ] Does NOT fabricate employee counts or funding amounts without a source
- [ ] Recommended next step is still useful despite information gaps

---

## Test 5: Non-company input
**Input:** "Series A fundraising trends 2025"

**Criteria:**
- [ ] Report notes that the input is not a company
- [ ] Tier is DISQUALIFIED or skill asks for clarification
- [ ] Does NOT produce a qualification report as if it were a real company
```

---

## Part 4 — Run evals (2 minutes)

```
/eval-skill qualify-lead
```

Claude runs each test case, grades the output against every criterion, finds failure patterns, and writes a report to `output/evals/qualify-lead-report.md`.

**Sample eval report** (what you might see on a first run):

```markdown
# Eval Report: qualify-lead
*Run: 2025-06-12 | Score: 74% (17/23 criteria)*

## Summary
**74%** — Needs improvement (target: 85%)

| Test case                | Score      | Status |
|--------------------------|------------|--------|
| Retool (hot lead)        | 100% (5/5) | ✅     |
| Duolingo (disqualify)    | 80% (4/5)  | ⚠️     |
| Notion (edge case)       | 60% (3/5)  | ⚠️     |
| Runway (limited info)    | 60% (3/5)  | ⚠️     |
| Non-company input        | 40% (2/5)  | ❌     |

## Top failure patterns

### 1. Missing source citations on low-information companies
Affects: Runway Financial, Notion
Root cause: Steps don't explicitly require citing a source for every data point in the scorecard.
Fix: Add "cite the source URL for every piece of evidence" to Step 2.

### 2. No handling for non-company inputs
Affects: "Series A fundraising trends 2025"
Root cause: Skill has no instructions for when the input isn't a company name.
Fix: Add a Step 0 to check whether the input looks like a company name. If not, return a clear message.
```

---

## Part 5 — Auto-improve (2 minutes)

```
/improve-skill qualify-lead
```

Claude reads the eval report, identifies the 2 most impactful fixes, and edits `.claude/skills/qualify-lead/SKILL.md` directly. You'll see the changes.

Then re-run evals to measure:
```
/eval-skill qualify-lead
→ 87% (20/23 criteria) — score improved 13pp
```

Repeat until you hit your target (85%+ is a reasonable bar for production). Usually 2-3 cycles.

---

## Part 6 — Export to production Python (2 minutes)

```
/export-to-sdk
```

Claude looks at your `qualify-lead` skill, asks a few questions (batch mode? output format?), and generates `sdk/qualify-lead/agent.py`.

The core of what gets generated:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

# The same instructions from SKILL.md, now in a Python function
PROMPT_TEMPLATE = """
Qualify this company as a sales lead: {company}

ICP Criteria:
{icp_criteria}

Steps:
1. Research the company: search for overview, size, stage, funding, job postings.
2. Score each ICP criterion: ✅ strong match, ⚠️ partial/unclear, ❌ mismatch, ❓ no info.
3. Assign tier: HOT, WARM, COLD, or DISQUALIFIED.
4. Write the qualification report to output/leads/{slug}-qualification.md.
5. Return a JSON summary: {{"company": "...", "tier": "...", "decision": "..."}}
"""

async def qualify(company: str, icp_criteria: str) -> dict:
    result_text = None
    async for message in query(
        prompt=PROMPT_TEMPLATE.format(company=company, icp_criteria=icp_criteria, slug=slugify(company)),
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "WebFetch", "Write", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            result_text = message.result
    return parse_result(result_text)
```

---

## Part 7 — Run on a batch

```bash
export ANTHROPIC_API_KEY=your-key   # from platform.claude.com
pip install claude-agent-sdk

# Single company
python examples/02-lead-qualifier/sdk/agent.py "Retool"

# Batch from CSV (needs a 'company' column)
python examples/02-lead-qualifier/sdk/agent.py --batch leads.csv --output results.csv
```

The batch processor runs each lead sequentially, saves a qualification report for each, and writes a CSV summary with tier and decision for every row. Run it overnight on your CRM export.

---

## What to do next

**Customize the skill further:** Open `.claude/skills/qualify-lead/SKILL.md` and change the scoring criteria, output format, or research steps. Run `/eval-skill qualify-lead` after every change.

**Add your ICP signals:** Add company-specific signals to `icp.md` — tools they use, job titles to watch for, growth indicators that matter for your product.

**Chain with research:** Build a two-step flow: `/research-agent <company>` to get a deep brief, then `/qualify-lead <company>` to score it. Export both as subagents in the SDK.

**Add to your CRM:** Wire the SDK `agent.py` into a webhook. New inbound lead → agent qualifies → result written to CRM field. See [`docs/sdk-migration-guide.md`](docs/sdk-migration-guide.md) for the FastAPI pattern.

---

## Troubleshooting

**"Skill not found"** — Make sure you're running `claude` from the repo root. The skills are in `.claude/skills/`.

**Qualification seems wrong** — Check your `icp.md`. If it doesn't exist, the skill uses default criteria. Run `/qualify-lead Retool` with and without an `icp.md` to see the difference.

**Eval score isn't improving after `/improve-skill`** — Look at the specific failing criteria. If they're subjective ("is the tone professional?"), they're hard for Claude to grade consistently. Rewrite them as binary checks ("does the report contain a source URL for each data point?").

**SDK `ModuleNotFoundError`** — Run `pip install claude-agent-sdk`. Requires Python 3.10+.
