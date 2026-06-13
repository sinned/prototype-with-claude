# Examples

Three fully worked examples, one for each core agent pattern. Each includes:
- A `SKILL.md` — the Claude Code skill (copy to `.claude/skills/<name>/` to use)
- A `sdk/agent.py` — the production Agent SDK version
- A `README.md` — explanation of the pattern and how to adapt it

## The patterns

| Example | Pattern | Use cases |
|---------|---------|-----------|
| [01-research-agent](./01-research-agent/) | Research & Synthesize | Company research, competitive analysis, due diligence, market research |
| [02-lead-qualifier](./02-lead-qualifier/) | Score & Classify | Lead scoring, content moderation, data enrichment, ticket routing |
| [03-content-generator](./03-content-generator/) | Generate & Iterate | Copy variations, personalized outreach, content at scale, drafting |
| [04-evals-and-improvement](./04-evals-and-improvement/) | Eval & Improve Loop | Measuring skill quality, automated prompt improvement, regression testing |

## How to use an example

**To prototype (Phase 1):**
```bash
# Copy the skill
mkdir -p .claude/skills/<skill-name>
cp examples/<N>-<name>/SKILL.md .claude/skills/<skill-name>/SKILL.md

# Run it in Claude Code
/<skill-name> <your input>
```

**To ship (Phase 2):**
```bash
# Run the SDK version directly
cd examples/<N>-<name>/sdk
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
source ../../../.env   # or: export ANTHROPIC_API_KEY=your-key
python3 agent.py "your input"
```

## Adapting an example

1. Copy the example to a new folder
2. Modify `SKILL.md` — change the job, steps, output format
3. Test the skill in Claude Code until it's reliable
4. Update `sdk/agent.py` to match (the `PROMPT_TEMPLATE` is the key section)

The prompt in `agent.py` should always match what's in `SKILL.md`. If you tune the skill, update the SDK code.
