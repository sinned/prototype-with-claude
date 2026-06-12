# prototype-with-claude

This repo is a starter kit for startup founders who want to build AI-enabled products fast. The workflow is:

1. **Prototype** — Build Claude Skills to define what your AI agent should do. Claude Code IS the agent runtime. Skills are plain-text job descriptions that Claude Code executes interactively.
2. **Validate** — Iterate on the Skill until Claude reliably does the job.
3. **Ship** — Migrate to the Claude Agent SDK for production: automatable, scalable, embeddable in any app.

## Your role in this repo

When a founder is working in this repo, help them with:

- **Designing skills** — Ask clarifying questions: What is the job? What are the inputs and outputs? What does success look like? What tools are needed?
- **Writing SKILL.md files** — Clear step-by-step instructions. Concrete output formats. Explicit success criteria.
- **Debugging skills** — When a skill isn't working, diagnose whether it's a prompt issue, tool access issue, or input issue.
- **Generating SDK code** — When asked to export or migrate, write real working Python using `claude-agent-sdk`.

## Skill file format

Skills live in `.claude/skills/<skill-name>/SKILL.md`. Format:

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger phrases.
---

# Skill Name

## What this skill does
[One paragraph]

## Steps
[Step-by-step instructions for Claude]

## Output format
[Exactly what to produce]
```

The `description` field is loaded at startup. The body is loaded when triggered. Keep the description under 200 chars. Make it specific enough that Claude knows when to use it.

## Slash commands in this repo

- `/new-skill` — Guided wizard to create a new skill from scratch
- `/export-to-sdk` — Generates Agent SDK Python code from an existing skill

## Agent SDK patterns

When generating SDK code, use this pattern:

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_agent(prompt: str) -> str:
    result = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Bash", "WebSearch", "WebFetch"],
        ),
    ):
        if hasattr(message, "result"):
            result = message.result
    return result

asyncio.run(run_agent("your prompt here"))
```

Key SDK options:
- `allowed_tools` — list of tools to enable (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion, Agent)
- `permission_mode` — "default" (prompt), "acceptEdits" (auto-approve edits), "bypassPermissions" (auto-approve all)
- `system_prompt` — Additional system context
- `resume` — Session ID to resume a previous session
- `agents` — Dict of subagent definitions for multi-agent workflows
- `mcp_servers` — Dict of MCP server configs for external integrations

## The three skill patterns

### 1. Research & Synthesize
Use for: gathering information, competitive analysis, market research, due diligence
Tools: WebSearch, WebFetch, Write
Shape: Input (topic/name) → Search → Gather → Synthesize → Structured output

### 2. Score & Classify
Use for: lead qualification, content moderation, data enrichment, categorization
Tools: Read, Write, Bash (for data), WebSearch (for enrichment)
Shape: Input (data) → Load → Analyze → Score/classify → Decision + reasoning

### 3. Generate & Iterate
Use for: content generation, code generation, document creation, email drafting
Tools: Read, Write, WebSearch (for research)
Shape: Input (brief) → Research → Plan → Draft → Variations → Output

## Good skill design principles

1. **One job** — A skill should do one thing well. If it needs to do two things, make two skills.
2. **Explicit output format** — Tell Claude exactly what to produce. Bad: "write a report". Good: "write a markdown file with these exact sections: Summary, Key findings, Recommendation".
3. **Concrete success criteria** — Tell Claude what "done" looks like.
4. **Error handling in the instructions** — Tell Claude what to do if it can't find information, if a tool fails, etc.
5. **Input in the command** — Skills should accept their main input via the command invocation, not by asking the user questions mid-run.

## What NOT to do

- Don't write skills that need real-time human approval mid-run — that's a sign the job isn't well-defined
- Don't put business logic in the SDK wrapper — keep it in the prompt/skill, so it's easy to iterate
- Don't create a skill for something Claude can already do without instructions
- Don't make skills dependent on each other in complex chains — keep them composable but independent
