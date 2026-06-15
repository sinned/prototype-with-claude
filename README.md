# prototype-with-claude

Prototype AI features in Claude Code before writing production code.  
Then graduate the working behavior to the Agent SDK.

**The pattern:** Write a plain-text job description (a **Skill**) → Claude Code runs it as an agent → measure quality with built-in evals → auto-improve until it passes → generate production Python with one command.

No boilerplate. No wasted API calls on logic that doesn't work yet. Validate the behavior first, write the code second.

---

## See it work

The built-in lead qualifier runs immediately after cloning. Here's the full loop — prototype, ship, then harden:

**Step 1 — Run the skill in Claude Code:**
```
/qualify-lead Retool
```

Claude searches the web, reads LinkedIn job postings and Crunchbase, scores the company against your ICP, and writes a qualification report:

```markdown
# Lead Qualification: Retool
Qualified: 2026-06-12 | Tier: HOT

## Decision
HOT — Developer tools platform, Series C ($145M), ~450 employees,
12 open AE roles signal active GTM scaling.

## ICP Scorecard
| Criterion       | Score | Evidence                             |
|-----------------|-------|--------------------------------------|
| Company size    | ✅    | ~450 employees (LinkedIn, Jan 2026)  |
| Industry fit    | ✅    | Internal tools platform, B2B SaaS    |
| Geography       | ✅    | SF HQ, US-primary customer base      |
| Stage / funding | ✅    | Series C, $145M (Sequoia, YC)        |
| Pain signal     | ✅    | 12 open AE roles, 3 SDR roles        |

## Recommended next step
Book discovery with VP Sales. Reference the SDR build-out —
they're building outbound motion and likely evaluating sales tools.
```

**Step 2 — Ship your MVP (export to production Python):**
```
/export-to-sdk
→ Generated sdk/qualify-lead/agent.py — runs the same job without a human in the loop
```

Don't wait for perfection. Get the agent running in production first. The prompt stays in `SKILL.md` — you can improve it without redeploying.

**Step 3 — Measure quality with evals:**
```
/eval-skill qualify-lead
→ 77% (17/22 criteria) — report in output/evals/qualify-lead-report.md
```

**Step 4 — Auto-improve:**
```
/improve-skill qualify-lead
→ Edited SKILL.md: added explicit fallback for missing headcount data
→ Re-run /eval-skill to measure improvement
```

Changes to `SKILL.md` automatically improve the already-running production agent — same prompt template, no redeployment.

**That's the full loop.** See [`WALKTHROUGH.md`](WALKTHROUGH.md) for a complete 20-minute build-along with sample inputs, real outputs, and eval results.

---

## Why this order matters

Most founders either jump straight to SDK code (expensive to iterate) or over-engineer evals before they've shipped anything. This repo avoids both traps:

- **Write in minutes, not hours.** A SKILL.md file takes 10 minutes to write and 30 seconds to test.
- **Ship before you perfect.** Export to the SDK as soon as the skill works on a few examples. Real-world inputs reveal failure modes that test cases never predict.
- **The prompt stays editable.** Business logic lives in `SKILL.md`, not buried in Python strings. Fix it without touching agent.py.
- **Evals harden what's already running.** Measure quality on your production agent, find failure patterns, improve the skill. No redeployment needed.
- **Your team can read it.** A PM can review a SKILL.md. They can't review an agent loop.

---

## Why Claude

**Long-context reasoning.** Claude reads a full company website, 10 search results, and a LinkedIn page in one pass and synthesizes coherently. Smaller context windows force chunking that breaks coherence.

**Reliable tool use.** Claude chains multiple tool calls — search, fetch, read, write — without hallucinating results or losing track of the task. Tool reliability matters when your agent needs 8 steps to complete a job.

**The Skills system.** Skills give Claude persistent, on-demand domain knowledge. Your ICP criteria load when qualifying a lead. Your brand voice loads when generating content. Nothing bloats the context that isn't needed.

**Iterative workflow design.** Claude Code is built for the edit-run-fix loop. You edit a SKILL.md, run it, see the output, edit again. The `/improve-skill` command makes this loop automatic.

**Agent SDK as a clean graduation path.** The SDK uses the same model, same tools, and same context management as Claude Code. When you move from prototype to production, the agent behavior doesn't change — only the runtime does.

---

## Repo map

```
prototype-with-claude/
│
├── WALKTHROUGH.md              ← Start here: 20-min lead qualifier build-along
│
├── .claude/
│   ├── skills/                 ← Skills that work immediately after cloning
│   │   ├── qualify-lead/       → /qualify-lead <company>
│   │   ├── qualify-lead-demo/  → /qualify-lead-demo (weak skill + saved improvement journey)
│   │   ├── research-agent/     → /research-agent <topic>
│   │   ├── generate-content/   → /generate-content "<brief>"
│   │   └── starter-agent/      → template to copy and modify
│   └── commands/               ← Meta-commands
│       ├── new-skill.md        → /new-skill (guided wizard)
│       ├── eval-skill.md       → /eval-skill <name> (grades outputs)
│       ├── improve-skill.md    → /improve-skill <name> (edits SKILL.md)
│       └── export-to-sdk.md    → /export-to-sdk (generates Python)
│
├── examples/
│   ├── 01-research-agent/      ← Research & Synthesize pattern
│   ├── 02-lead-qualifier/      ← Score & Classify pattern
│   ├── 03-content-generator/   ← Generate & Iterate pattern
│   └── 04-evals-and-improvement/ ← Eval loop + automated improvement
│       └── sdk/
│           ├── eval_runner.py  → Programmatic eval runner
│           └── improve.py      → Automated improvement loop
│
├── docs/
│   ├── founder-use-cases.md    ← 5 real startup use cases with build guides
│   ├── demo-script.md          ← 5-min reviewer walkthrough script
│   ├── skill-patterns.md       ← Design patterns for the 3 skill shapes
│   └── sdk-migration-guide.md  ← How to graduate to production
│
└── CLAUDE.md                   ← Claude's instructions when working in this repo
```

---

## Start here

```bash
# 1. Clone
git clone https://github.com/sinned/prototype-with-claude
cd prototype-with-claude

# 2. Open Claude Code
claude

# 3. Run a skill immediately (no setup needed)
/qualify-lead Retool
/research-agent "Stripe competitors"
/generate-content "cold email for a sales tool, target: VP Sales at Series B"

# 4. Build your own skill (guided wizard)
/new-skill

# 5. Measure quality
/eval-skill your-skill-name

# 6. Fix failures automatically
/improve-skill your-skill-name

# 7. Graduate to production
/export-to-sdk
```

For Phase 2 (running agents in production):
```bash
# Set up your API key (one time)
cp .env.example .env
# Edit .env and add your key from platform.claude.com/settings/api-keys

# Create a venv and install SDK (agent.py reads .env automatically)
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install claude-agent-sdk python-dotenv
python3 examples/02-lead-qualifier/sdk/agent.py "Retool"
python3 examples/02-lead-qualifier/sdk/agent.py --batch leads.csv
```

---

## The three skill patterns

Most startup AI features fit one of these shapes. Each has a full example in `examples/`:

| Pattern | Shape | Built-in skill | Use for |
|---------|-------|---------------|---------|
| **Research & Synthesize** | search → gather → synthesize → report | `/research-agent` | Prospect research, competitive analysis, market briefs |
| **Score & Classify** | load rubric → analyze → score → decision | `/qualify-lead` | Lead scoring, ticket routing, content moderation |
| **Generate & Iterate** | brief → research → 3 variations → recommendation | `/generate-content` | Copy variations, outreach, content at scale |

---

## The eval loop

The difference between "it looks okay on 3 examples" and "it works reliably":

```
Define test cases  →  Run skill on each  →  Claude grades outputs  →  Find failure patterns  →  Improve SKILL.md  →  Repeat
```

Test cases live in `.claude/skills/<skill-name>/evals/test-cases.md`. Each case is an input and a list of binary (yes/no) quality criteria. Claude grades outputs against them — no subjective "does this look good?", just pass/fail on each criterion.

```
/eval-skill qualify-lead     # runs tests, grades outputs, writes report
/improve-skill qualify-lead  # reads report, edits SKILL.md to fix failures
```

See [`examples/04-evals-and-improvement/`](examples/04-evals-and-improvement/) for the full example including an automated improvement loop that runs in the Agent SDK until a target score is hit.

---

## Graduate to production

Once the skill passes evals, one command generates production Python:

```
/export-to-sdk
```

The generated `agent.py` uses the same instructions as your `SKILL.md` — same prompt, same tools, now running autonomously via the Agent SDK:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async def qualify(company: str) -> str:
    async for message in query(
        prompt=PROMPT.format(company=company),  # same instructions as SKILL.md
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "WebFetch", "Write"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            return message.result
```

From there: call it from a FastAPI endpoint, run it on a CSV, trigger it from a cron job. See [`docs/sdk-migration-guide.md`](docs/sdk-migration-guide.md) for patterns.

---

## Go deeper

| Resource | What's in it |
|----------|-------------|
| [`WALKTHROUGH.md`](WALKTHROUGH.md) | Complete 20-min lead qualifier build, with real outputs and eval results |
| [`docs/demo-improvement-journey.md`](docs/demo-improvement-journey.md) | Real before/after: a weak skill goes from 65% → 100% in one improve iteration |
| [`docs/founder-use-cases.md`](docs/founder-use-cases.md) | 5 startup use cases with build guides |
| [`docs/skill-patterns.md`](docs/skill-patterns.md) | Design patterns and anti-patterns for skills |
| [`docs/sdk-migration-guide.md`](docs/sdk-migration-guide.md) | Every SDK pattern: batch, sessions, subagents, FastAPI |
| [`docs/demo-script.md`](docs/demo-script.md) | 5-min live demo script for showing this to others |
| [GitHub Pages site](https://sinned.github.io/prototype-with-claude/) | Full documentation |

---

## Requirements

- [Claude Code](https://code.claude.com) — required for Phase 1
- Python 3.10+ and `ANTHROPIC_API_KEY` — required for Phase 2 SDK examples
