---
name: qualify-lead
description: Qualify a sales lead against your Ideal Customer Profile (ICP). Research the company, score it, and produce a qualification decision with reasoning. Use when given a company name, domain, or lead to evaluate.
---

# Lead Qualifier

Researches a company and scores it against a configurable Ideal Customer Profile (ICP) to produce a qualification decision: Hot, Warm, Cold, or Disqualified.

## Input

A company name, domain, or brief description. Optionally: a path to an ICP definition file (defaults to `icp.md` if it exists in the working directory).

## Steps

1. **Load ICP criteria** — Check if `icp.md` exists in the working directory. If yes, read it. If no, use these default criteria:
   - Company size: 50-500 employees (ideal: 100-250)
   - Industry: B2B SaaS or tech-enabled services
   - Geography: North America or Western Europe
   - Stage: Series A or later, or profitable SMB
   - Pain signal: actively hiring sales/revenue roles, or recent funding

2. **Research the company** — Search for:
   - Company overview (what they do, size, stage)
   - Recent funding or financial news
   - Current job postings (especially sales/revenue roles)
   - Key leadership (CEO, VP Sales)
   - Technology stack if relevant

3. **Score against each ICP criterion** — For each criterion, assign:
   - ✅ Strong match
   - ⚠️ Partial match or unclear
   - ❌ Mismatch
   - ❓ No information found

4. **Assign overall qualification tier**:
   - **Hot** — 4+ strong matches, no mismatches
   - **Warm** — 3+ strong matches, at most 1 mismatch
   - **Cold** — 2 strong matches or many unknowns
   - **Disqualified** — confirmed mismatch on a hard criterion (e.g., wrong industry, too large/small)

5. **Write the qualification report** — Follow the output format below.

6. **Save output** — Write to `output/leads/<company-slug>-qualification.md`.

## Output format

```markdown
# Lead Qualification: [Company Name]
*Qualified: [date] | Tier: [HOT / WARM / COLD / DISQUALIFIED]*

## Decision
**[HOT / WARM / COLD / DISQUALIFIED]** — [One sentence explaining the decision]

## ICP Scorecard

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Company size | ✅/⚠️/❌/❓ | [What was found] |
| Industry fit | ✅/⚠️/❌/❓ | [What was found] |
| Geography | ✅/⚠️/❌/❓ | [What was found] |
| Stage / funding | ✅/⚠️/❌/❓ | [What was found] |
| Pain signal | ✅/⚠️/❌/❓ | [What was found] |

## Company Overview
[3-4 sentences: what they do, who they serve, key facts]

## Recommended next step
[Specific action: "Book a discovery call — mention their recent Series B and the 3 open AE roles", or "Deprioritize — consumer product, not B2B"]

## Sources
- [URL 1]
- [URL 2]
```

## Customizing the ICP

Create `icp.md` in your working directory to replace the default criteria:

```markdown
# My ICP

## Hard criteria (disqualify if not met)
- [Criterion]
- [Criterion]

## Soft criteria (score but don't disqualify)
- [Criterion]
- [Criterion]

## Strong positive signals
- [Signal]
```

## If something goes wrong

- If no information found about the company: produce the report with all criteria marked ❓, tier = Cold, note "Unable to verify — manual research needed"
- If the company name is ambiguous: qualify all plausible matches or ask for clarification via the domain/URL
- If `icp.md` is malformed: use default criteria and note the issue
