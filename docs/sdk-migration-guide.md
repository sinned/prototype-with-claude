# SDK Migration Guide

How to turn a validated Claude Code Skill into production Agent SDK code.

## When to migrate

Migrate from a Skill to the Agent SDK when:
- You need to run the agent without a human present (automated pipelines, cron jobs)
- You need to process many inputs (batch processing)
- You need to embed the agent in a product (web app, API endpoint)
- You need to chain multiple agents together
- You need to add business logic around the agent (retries, logging, error handling)

**Don't migrate prematurely.** If you're still iterating on the job definition, keep prototyping in Claude Code. The migration is easy — premature migration is just friction.

## The migration

The core of the migration is simple: copy your SKILL.md instructions into a Python prompt template.

### Before (SKILL.md)
```markdown
---
name: research-agent
description: Research a company and produce a brief.
---

# Research Agent

## Steps
1. Search for [topic] using 3 targeted queries
2. Read the top 3 results
3. Write a brief to output/[topic]-brief.md
```

### After (agent.py)
```python
from claude_agent_sdk import query, ClaudeAgentOptions

PROMPT = """
Research {topic} and produce a brief.

Steps:
1. Search for {topic} using 3 targeted queries
2. Read the top 3 results  
3. Write a brief to output/{topic_slug}-brief.md
"""

async def run(topic: str) -> str:
    result = None
    async for message in query(
        prompt=PROMPT.format(topic=topic, topic_slug=topic.lower().replace(" ", "-")),
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "WebFetch", "Write"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            result = message.result
    return result
```

The instructions are identical. Only the container changed.

---

## Mapping concepts

| Claude Code (Skill) | Agent SDK |
|---------------------|-----------|
| SKILL.md instructions | `prompt` parameter |
| Command argument (`/skill input`) | Function parameter → f-string in prompt |
| Listed tools in skill | `allowed_tools=[...]` |
| Writing files | `permission_mode="acceptEdits"` |
| Running bash | `allowed_tools=["Bash"]` |
| Web research | `allowed_tools=["WebSearch", "WebFetch"]` |
| Reading config files | Read at startup, inject into prompt |
| Multi-step with memory | Session resume: `ClaudeAgentOptions(resume=session_id)` |
| Subagent (`/other-skill`) | `ClaudeAgentOptions(agents={...})` |

---

## Common SDK patterns

### Pattern 1: Single input, single output

```python
async def run_agent(input_data: str) -> str | None:
    result = None
    async for message in query(
        prompt=f"Do the job with: {input_data}",
        options=ClaudeAgentOptions(allowed_tools=["WebSearch", "Write"]),
    ):
        if hasattr(message, "result"):
            result = message.result
    return result
```

### Pattern 2: Batch processing

```python
async def run_batch(items: list[str]) -> list[dict]:
    results = []
    for item in items:
        result = await run_agent(item)
        results.append({"input": item, "result": result})
    return results
```

For parallel processing (faster but uses more API quota):
```python
import asyncio

async def run_batch_parallel(items: list[str], max_concurrent: int = 3) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run_one(item):
        async with semaphore:
            result = await run_agent(item)
            return {"input": item, "result": result}
    
    return await asyncio.gather(*[run_one(item) for item in items])
```

### Pattern 3: Multi-step with session continuity

```python
from claude_agent_sdk import SystemMessage

async def run_pipeline(inputs: list[str]) -> list[str]:
    session_id = None
    results = []
    
    for i, prompt_text in enumerate(inputs):
        opts = ClaudeAgentOptions(
            allowed_tools=["Read", "Write"],
            resume=session_id if session_id and i > 0 else None,
        )
        async for message in query(prompt=prompt_text, options=opts):
            if isinstance(message, SystemMessage) and message.subtype == "init":
                session_id = message.data.get("session_id")
            if hasattr(message, "result"):
                results.append(message.result)
    
    return results
```

### Pattern 4: Load context files before running

```python
from pathlib import Path

def build_prompt(task: str) -> str:
    config = Path("config.md").read_text() if Path("config.md").exists() else ""
    return f"""
Context:
{config}

Task:
{task}
"""
```

### Pattern 5: Subagents for parallel specialized work

```python
from claude_agent_sdk import AgentDefinition

async def run_with_subagents(topic: str) -> str | None:
    result = None
    async for message in query(
        prompt=f"Research {topic} — use the web-researcher for gathering data and the analyst for synthesis",
        options=ClaudeAgentOptions(
            allowed_tools=["Agent", "Write"],
            agents={
                "web-researcher": AgentDefinition(
                    description="Searches the web and fetches pages",
                    prompt="Search for information and return what you find",
                    tools=["WebSearch", "WebFetch"],
                ),
                "analyst": AgentDefinition(
                    description="Analyzes information and produces structured summaries",
                    prompt="Analyze the provided information and produce a structured brief",
                    tools=["Read", "Write"],
                ),
            },
        ),
    ):
        if hasattr(message, "result"):
            result = message.result
    return result
```

---

## Embedding in a web app

### FastAPI endpoint

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio

app = FastAPI()

class AgentRequest(BaseModel):
    input: str

class AgentResponse(BaseModel):
    result: str | None
    status: str

@app.post("/run", response_model=AgentResponse)
async def run_endpoint(request: AgentRequest):
    result = await run_agent(request.input)
    return AgentResponse(result=result, status="done" if result else "failed")
```

### Background job (long-running)

```python
from fastapi import BackgroundTasks
import uuid

jobs: dict[str, dict] = {}

@app.post("/run-async")
async def run_async(request: AgentRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running", "result": None}
    
    async def do_work():
        result = await run_agent(request.input)
        jobs[job_id] = {"status": "done", "result": result}
    
    background_tasks.add_task(do_work)
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})
```

---

## Permission modes

| Mode | What it means | Use when |
|------|--------------|---------|
| `"default"` | Prompts for approval on tool use | Development, interactive use |
| `"acceptEdits"` | Auto-approves file edits | Production agents that write files |
| `"bypassPermissions"` | Auto-approves all tools | Trusted automation, fully audited agents |

For production, use `"acceptEdits"` for agents that write files but don't run arbitrary shell commands, and `"bypassPermissions"` only for fully trusted, reviewed agents.

---

## Keeping skill and SDK in sync

The prompt in `agent.py` and the instructions in `SKILL.md` should always match. When you tune the skill, update the SDK code.

A simple convention: keep the prompt as a `PROMPT_TEMPLATE` constant at the top of `agent.py`, and keep a comment pointing back to the source SKILL.md.

```python
# Prompt migrated from: .claude/skills/research-agent/SKILL.md
# When you update the skill, update this template too.
PROMPT_TEMPLATE = """..."""
```
