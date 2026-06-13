# Example 3: Content Generator

**Pattern: Generate & Iterate**

An AI agent that takes a content brief and produces 3 variations — so you can pick the best angle or combine elements.

## The job

Input → a content brief  
Output → 3 variations saved to `output/content/<slug>/`, plus a brief summary and recommendation

## Why this pattern matters

The Generate & Iterate pattern powers some of the most valuable AI features in startups:

- Marketing: generate copy variations for A/B testing
- Sales: personalized outreach at scale
- Product: draft feature announcements, changelogs, help docs
- Ops: draft SOPs, policies, templates
- Any domain where you need consistent output in large quantities

The key insight: you don't just generate once — you generate *multiple options* because the value is in the variation. Claude is great at holding a brief in mind and expressing it multiple ways.

## How to prototype (Phase 1)

1. Copy the skill:
   ```bash
   mkdir -p .claude/skills/generate-content
   cp examples/03-content-generator/SKILL.md .claude/skills/generate-content/SKILL.md
   ```

2. Optionally create brand voice guidelines:
   ```bash
   cp examples/03-content-generator/brand-voice-example.md brand-voice.md
   # Edit brand-voice.md to match your brand
   ```

3. Run in Claude Code:
   ```
   /generate-content "cold email for a sales productivity tool, target: VP Sales at Series B startups"
   /generate-content "LinkedIn post about our product launch"
   /generate-content "blog post: 5 reasons your sales pipeline is lying to you"
   ```

4. Check `output/content/` for the variations.
5. Tune `brand-voice.md` and the skill instructions until the output sounds like you.

## What to tune

- The 3 variation angles — what dimensions matter for your content? (tone, audience, format, length)
- The format guidelines — adjust word counts and structure for your channels
- The brand voice file — this has the biggest impact on output quality
- The research step — for some content, research matters a lot; for others, skip it

## How to ship (Phase 2)

See `sdk/agent.py`. The production version can:

- Generate content for a list of topics from a CSV
- Post directly to a CMS via API
- Send to a review queue in Notion or Airtable
- Run nightly to fill a content calendar

```bash
cd sdk
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
source ../../../.env   # or: export ANTHROPIC_API_KEY=your-key

# Single brief
python3 agent.py "cold email for enterprise SaaS, target: CTO"

# Batch from file
python3 agent.py --batch briefs.csv
```

## Adapting for other generation use cases

The same pattern works for any generation-at-scale need:

```python
# Code generation: generate test cases for a function
# Doc generation: generate help articles from a feature list
# Email personalization: generate personalized emails from lead data
# Social content: generate a month of posts from a content calendar
```

## The skill → SDK mapping

| Skill concept | SDK equivalent |
|---------------|---------------|
| Brand voice file | Read at startup, inject into prompt prefix |
| WebSearch for research | `allowed_tools=["WebSearch"]` |
| Write 3 files | `allowed_tools=["Write"]` + `permission_mode="acceptEdits"` |
| Brief as input | Function parameter → f-string in prompt |
| Generate for a list | Loop in Python, one agent call per brief |
