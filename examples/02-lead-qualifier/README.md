# Example 2: Lead Qualifier

**Pattern: Score & Classify**

An AI agent that researches a company and scores it against your Ideal Customer Profile (ICP) to produce a qualification decision.

## The job

Input → a company name or domain  
Output → qualification tier (Hot/Warm/Cold/Disqualified) + scorecard + recommended next step

## Why this pattern matters

The Score & Classify pattern is everywhere in startups:

- Sales: qualify inbound leads before investing rep time
- VC: first-pass filter on a deal list
- Recruiting: screen candidates or companies
- Compliance: categorize transactions or documents
- Support: route tickets by priority or type

The key insight: Claude can apply a consistent rubric to any input, at scale.

## How to prototype (Phase 1)

1. Copy the skill:
   ```bash
   mkdir -p .claude/skills/qualify-lead
   cp examples/02-lead-qualifier/SKILL.md .claude/skills/qualify-lead/SKILL.md
   ```

2. Optionally create your own ICP:
   ```bash
   cp examples/02-lead-qualifier/icp-example.md icp.md
   # Edit icp.md to match your actual ICP
   ```

3. Run in Claude Code:
   ```
   /qualify-lead Notion
   /qualify-lead linear.app
   /qualify-lead "Acme Corp, Series A fintech startup, 80 employees"
   ```

4. Refine the ICP criteria in `icp.md` until the scores match your intuition.

## What to tune

- The ICP criteria — this is everything. Get these right and the scoring is consistent.
- The tier thresholds — what counts as "Hot" vs "Warm"?
- The recommended next step — make this specific to your sales motion
- The research steps — what signals matter most for your product?

## How to ship (Phase 2)

See `sdk/agent.py`. The production version can:

- Process a CSV of leads overnight
- Post results to a Slack channel
- Update a CRM (via webhook or API)
- Write to a database

```bash
cd sdk
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key

# Single lead
python agent.py "Notion"

# Batch from CSV
python agent.py --batch leads.csv --output results.csv
```

## Adapting for other scoring use cases

The same pattern works for:

```python
# Instead of ICP criteria, use your own rubric
RUBRIC = """
Score each item on:
- Criterion A: [description] → 0-10 points
- Criterion B: [description] → 0-10 points
...
Total: Hot (>= 40), Warm (25-39), Cold (< 25)
"""
```

## The skill → SDK mapping

| Skill concept | SDK equivalent |
|---------------|---------------|
| `icp.md` file | Read at startup, inject into prompt |
| WebSearch for research | `allowed_tools=["WebSearch", "WebFetch"]` |
| Scoring rubric in instructions | System prompt / prompt prefix |
| Output file | `allowed_tools=["Write"]` + `permission_mode="acceptEdits"` |
| Batch over a list | Loop in Python, call agent per item |
