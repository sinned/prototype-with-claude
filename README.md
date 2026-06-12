# prototype-with-claude

Build AI features in hours, not weeks. Use Claude Code as your agent runtime to prototype, then ship with the Agent SDK.

## The two-phase approach

```
PHASE 1: PROTOTYPE                    PHASE 2: SHIP
─────────────────────                 ──────────────────────────
Write a Skill (markdown)     ──→      Generate Agent SDK code
Claude Code runs the agent            Your app runs the agent
Iterate in minutes                    Scales in production
No code required                      Python or TypeScript
```

**Phase 1** — You write a Skill: a plain-text job description for your AI. Claude Code has built-in tools (web search, file read/write, bash, browser). You run the Skill interactively to validate the workflow. Iterate on the markdown until Claude reliably does the job.

**Phase 2** — Once the job works, you generate production code using the Agent SDK. Same tools, same Claude, now automatable and scalable.

## Why this works

The hardest part of building AI products isn't the code — it's figuring out *what the AI should actually do*. Skills let you answer that question without writing any code. You prototype the logic, discover the edge cases, and tune the instructions. The Agent SDK migration is then straightforward because you already know what works.

## Quick start

```bash
# 1. Clone the repo
git clone https://github.com/your-org/prototype-with-claude
cd prototype-with-claude

# 2. Open Claude Code
claude

# 3. Try a built-in example
/research-agent Stripe             # Research a company
/qualify-lead Notion               # Qualify a lead against your ICP
/generate-content "launch email"   # Generate content variations

# 4. Create your own skill
/new-skill

# 5. Test and improve it systematically
/eval-skill my-skill               # Run test cases, grade outputs with Claude-as-judge
/improve-skill my-skill            # Auto-improve SKILL.md based on failures

# 6. When it works reliably, export to production code
/export-to-sdk
```

## What's included

| Path | What it is |
|------|-----------|
| `.claude/skills/starter-agent/` | Commented skill template — copy and modify |
| `.claude/commands/new-skill.md` | `/new-skill` — guided wizard to create a skill |
| `.claude/commands/eval-skill.md` | `/eval-skill` — run test cases + grade with Claude-as-judge |
| `.claude/commands/improve-skill.md` | `/improve-skill` — edit SKILL.md based on failures |
| `.claude/commands/export-to-sdk.md` | `/export-to-sdk` — generate Agent SDK code from a skill |
| `examples/01-research-agent/` | Research + synthesize pattern |
| `examples/02-lead-qualifier/` | Score + classify pattern |
| `examples/03-content-generator/` | Generate + iterate pattern |
| `examples/04-evals-and-improvement/` | Eval loop + automated improvement |
| `docs/skill-patterns.md` | Patterns for common agent shapes |
| `docs/sdk-migration-guide.md` | How Skills map to Agent SDK concepts |

## The three skill patterns

Most startup AI features fit one of these shapes:

```
RESEARCH & SYNTHESIZE          SCORE & CLASSIFY           GENERATE & ITERATE
─────────────────────          ────────────────           ──────────────────
Input: a topic or name         Input: structured data     Input: a brief
Search → Gather → Synthesize   Load → Analyze → Score     Research → Plan → Draft
Output: a report/brief         Output: score + reasoning  Output: variations
```

See `examples/` for fully worked examples of each pattern, each with the Skill and the matching Agent SDK code.

## The mental model

```
Skill            =   A job description for your AI
Agent SDK query  =   That job, running autonomously in production
ClaudeAgentOptions  =  Permissions + tools + configuration
```

A Skill is just markdown. Claude Code reads it when you invoke the command and uses it as instructions. The same content becomes your system prompt / task description in the SDK.

## Building your own skill

1. Copy `.claude/skills/starter-agent/SKILL.md` to `.claude/skills/<your-skill-name>/SKILL.md`
2. Edit it: describe the job, the steps, the output format
3. Run `/your-skill-name <input>` in Claude Code to test
4. Iterate on the markdown until it works reliably
5. Run `/export-to-sdk` to generate production Python/TypeScript

## Requirements

- [Claude Code](https://code.claude.com) (for Phase 1)
- Python 3.10+ (for Phase 2 SDK examples)
- `ANTHROPIC_API_KEY` environment variable

## Resources

- [Claude Code docs](https://code.claude.com/docs)
- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Agent SDK demos](https://github.com/anthropics/claude-agent-sdk-demos)
