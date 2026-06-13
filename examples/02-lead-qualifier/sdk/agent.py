"""
Lead Qualifier — Agent SDK version
Migrated from: examples/02-lead-qualifier/SKILL.md

Researches a company and scores it against an ICP to produce a qualification decision.
"""

import asyncio
import argparse
import csv
import json
import sys
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions


DEFAULT_ICP = """
## ICP Criteria

### Hard criteria (disqualify if not met)
- Must be B2B (not consumer)
- Must be in software, tech-enabled services, or professional services
- Must have at least 20 employees

### Soft criteria
- Company size: 50-500 employees (ideal: 100-250)
- Geography: North America or Western Europe
- Stage: Series A through Series C, or profitable SMB

### Strong positive signals
- Recently raised funding (last 18 months)
- Actively hiring sales or revenue roles
- Fast headcount growth on LinkedIn

### Qualification tiers
- HOT: 4+ strong matches, no hard mismatches
- WARM: 3+ strong matches, at most 1 mismatch
- COLD: 2 strong matches or many unknowns
- DISQUALIFIED: confirmed mismatch on a hard criterion
"""

PROMPT_TEMPLATE = """
Qualify this company as a sales lead: {company}

ICP Criteria:
{icp_criteria}

Steps:
1. Research the company: search for their overview, size, stage, funding, job postings, and key leadership.
2. Score against each ICP criterion: ✅ strong match, ⚠️ partial/unclear, ❌ mismatch, ❓ no info found.
3. Assign overall tier: HOT, WARM, COLD, or DISQUALIFIED.
4. Write the qualification report in this exact format:

---
QUALIFICATION: [COMPANY NAME]
TIER: [HOT/WARM/COLD/DISQUALIFIED]
DATE: [today]

DECISION: [One sentence explaining the tier]

SCORECARD:
- Company size: [score] — [evidence]
- Industry fit: [score] — [evidence]
- Geography: [score] — [evidence]
- Stage/funding: [score] — [evidence]
- Pain signals: [score] — [evidence]

OVERVIEW: [3-4 sentences about what they do]

NEXT STEP: [Specific recommended action]

SOURCES: [list of URLs used]
---

5. Save to output/leads/{company_slug}-qualification.md
6. Return a JSON summary: {{"company": "...", "tier": "...", "decision": "..."}}

If no information is found: mark all criteria ❓, tier = COLD, note manual research needed.
"""


def load_icp(icp_path: str | None = None) -> str:
    """Load ICP from file, or use defaults."""
    paths_to_try = [icp_path, "icp.md", ".claude/icp.md"] if icp_path else ["icp.md", ".claude/icp.md"]
    for path in paths_to_try:
        if path and Path(path).exists():
            return Path(path).read_text()
    return DEFAULT_ICP


async def qualify(company: str, icp_criteria: str) -> dict:
    """Qualify a single lead. Returns dict with tier and summary."""
    company_slug = company.lower().replace(" ", "-").replace(".", "-")[:50]
    prompt = PROMPT_TEMPLATE.format(
        company=company,
        company_slug=company_slug,
        icp_criteria=icp_criteria,
    )

    result_text = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "WebFetch", "Write", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            result_text = message.result

    # Try to parse JSON summary from result
    if result_text:
        try:
            start = result_text.rfind("{")
            end = result_text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(result_text[start:end])
        except (json.JSONDecodeError, ValueError):
            pass

    return {"company": company, "tier": "UNKNOWN", "decision": result_text or "No result"}


async def qualify_batch(companies: list[str], icp_criteria: str) -> list[dict]:
    """Qualify a list of companies sequentially."""
    results = []
    for i, company in enumerate(companies, 1):
        print(f"[{i}/{len(companies)}] Qualifying: {company}", flush=True)
        result = await qualify(company, icp_criteria)
        results.append(result)
        tier = result.get("tier", "?")
        print(f"  Result: {tier} — {company}\n", flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Qualify a sales lead against your ICP."
    )
    parser.add_argument("company", nargs="?", help="Company name or domain to qualify")
    parser.add_argument("--batch", metavar="CSV_FILE", help="CSV file with a 'company' column")
    parser.add_argument("--output", metavar="CSV_FILE", help="Output CSV file for batch results")
    parser.add_argument("--icp", metavar="FILE", help="Path to ICP definition file (default: icp.md)")
    args = parser.parse_args()

    icp_criteria = load_icp(args.icp)

    if args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            print(f"Error: file not found: {args.batch}", file=sys.stderr)
            sys.exit(1)

        with open(batch_file) as f:
            reader = csv.DictReader(f)
            companies = [row["company"] for row in reader if row.get("company")]

        print(f"Processing {len(companies)} leads...\n")
        results = asyncio.run(qualify_batch(companies, icp_criteria))

        output_path = args.output or "output/qualification-results.csv"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["company", "tier", "decision"])
            writer.writeheader()
            writer.writerows(results)

        print(f"\nResults saved to {output_path}")
        print("\nSummary:")
        for tier in ["HOT", "WARM", "COLD", "DISQUALIFIED"]:
            count = sum(1 for r in results if r.get("tier") == tier)
            print(f"  {tier}: {count}")

    elif args.company:
        result = asyncio.run(qualify(args.company, icp_criteria))
        if result.get("tier") == "UNKNOWN":
            print("Error: agent query returned no usable result. Check ANTHROPIC_API_KEY and network.", file=sys.stderr)
            print(f"Raw output: {result.get('decision')}", file=sys.stderr)
            sys.exit(1)
        print(f"\nResult: {result.get('tier')} — {result.get('decision')}")
        print(f"Full report saved to output/leads/")
    else:
        company = input("Company name or domain to qualify: ").strip()
        if not company:
            print("No company provided.", file=sys.stderr)
            sys.exit(1)
        result = asyncio.run(qualify(company, icp_criteria))
        if result.get("tier") == "UNKNOWN":
            print("Error: agent query returned no usable result. Check ANTHROPIC_API_KEY and network.", file=sys.stderr)
            print(f"Raw output: {result.get('decision')}", file=sys.stderr)
            sys.exit(1)
        print(f"\nResult: {result.get('tier')} — {result.get('decision')}")
        print(f"Full report saved to output/leads/")


if __name__ == "__main__":
    main()
