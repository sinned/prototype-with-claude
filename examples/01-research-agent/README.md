# Example 1: Research Agent

**Pattern: Research & Synthesize**

An AI agent that researches any company, person, or topic and produces a structured intelligence brief.

## The job

Input → a name or topic  
Output → a markdown brief saved to `output/<subject>-brief.md`

## Why this pattern matters

Research is one of the highest-leverage AI jobs. It's repetitive, time-consuming for humans, and Claude is extremely good at it. This pattern — search, gather, synthesize, format — underlies dozens of startup use cases:

- Sales: research a prospect before a call
- VC: quick due diligence on a company
- Marketing: competitive analysis
- Recruiting: research a candidate or company
- Journalism: background on a topic

## How to prototype (Phase 1)

1. Copy the skill:
   ```bash
   cp -r examples/01-research-agent/.claude/skills/research-agent .claude/skills/
   ```
   Or just copy the `SKILL.md` to `.claude/skills/research-agent/SKILL.md`.

2. Run it in Claude Code:
   ```
   /research-agent Stripe
   /research-agent "Sam Altman"
   /research-agent "vertical SaaS trends 2025"
   ```

3. Check `output/` for the generated briefs.

4. Iterate on `SKILL.md` until the output quality is consistently good.

## What to tune

- The search queries (step 2) — more specific = better results
- The output format — add/remove sections for your use case
- The TL;DR criteria — what's "most important" depends on your context
- The file path — change `output/` to wherever you want files saved

## How to ship (Phase 2)

See `sdk/agent.py` for the production version. It uses the same prompt from the SKILL.md but wraps it in Agent SDK code so you can:

- Call it from an API endpoint
- Run it on a batch of companies from a CSV
- Trigger it from a cron job
- Chain it with other agents

```bash
cd sdk
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
source ../../../.env   # or: export ANTHROPIC_API_KEY=your-key
python3 agent.py "Stripe"
python3 agent.py --batch companies.txt  # process a list
```

## The skill → SDK mapping

| Skill concept | SDK equivalent |
|---------------|---------------|
| SKILL.md instructions | `prompt` parameter |
| WebSearch, WebFetch tools | `allowed_tools=["WebSearch", "WebFetch"]` |
| Write tool | `allowed_tools=["Write"]` + `permission_mode="acceptEdits"` |
| Input via command arg | Function parameter → f-string in prompt |
| Output to file | Handled by Claude via Write tool |
