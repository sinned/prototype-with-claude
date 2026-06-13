You are helping a startup founder export a validated Claude Skill into production-ready Agent SDK code.

The founder has been prototyping in Claude Code using Skills. Now they want to turn one of those skills into a Python script (or TypeScript) that can run autonomously — in a pipeline, a cron job, a web server, or a data batch process.

## Your task

1. **Find the skill to export**
   - List the skills in `.claude/skills/` 
   - If the founder specified one in their command input, use that
   - Otherwise, ask which skill they want to export

2. **Read the skill**
   - Read the `SKILL.md` file for the selected skill
   - Understand: the job, the inputs, the outputs, the tools required

3. **Ask about the deployment context** (these change the generated code significantly)
   - How will this agent be triggered? (CLI script, called from an API, cron job, processing a list)
   - What language? (Python or TypeScript — default to Python)
   - Should it process a single input or a batch (list of inputs)?
   - Should it save output to a file, print it, or return it as a value?
   - Is there any external system to integrate with? (database, webhook, Slack, email)

4. **Generate the Agent SDK code**

## Code generation rules

### Python pattern (default)

```python
import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_<skill_name>(input_data: str) -> str:
    """<One-line description from the skill>"""
    prompt = f"""<The skill's instructions, adapted for autonomous use>

Input: {input_data}
"""
    result = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=[<tools from the skill>],
            permission_mode="acceptEdits",  # remove if the agent shouldn't write files
        ),
    ):
        if hasattr(message, "result"):
            result = message.result
    return result

if __name__ == "__main__":
    import sys
    input_data = sys.argv[1] if len(sys.argv) > 1 else input("Enter input: ")
    result = asyncio.run(run_<skill_name>(input_data))
    print(result)
```

### Key things to adapt from the skill

- The `prompt` should contain the full instructions from SKILL.md, not just a summary
- Map the skill's listed tools to the `allowed_tools` list
- If the skill writes files, include `permission_mode="acceptEdits"` 
- If the skill only reads/searches, omit `permission_mode` (defaults to safer mode)

### For batch processing, add a loop

```python
async def run_batch(inputs: list[str]) -> list[str]:
    results = []
    for item in inputs:
        result = await run_<skill_name>(item)
        results.append(result)
        print(f"Processed: {item}")
    return results
```

### For session continuity (multi-step workflows)

```python
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage

async def run_with_session(inputs: list[str]) -> list[str]:
    session_id = None
    results = []
    
    for i, item in enumerate(inputs):
        opts = ClaudeAgentOptions(allowed_tools=[...])
        if session_id and i > 0:
            opts = ClaudeAgentOptions(resume=session_id, allowed_tools=[...])
        
        async for message in query(prompt=item, options=opts):
            if isinstance(message, SystemMessage) and message.subtype == "init":
                session_id = message.data.get("session_id")
            if hasattr(message, "result"):
                results.append(message.result)
    
    return results
```

## Output

Generate these files in `sdk/<skill-name>/`:

1. `agent.py` — The main agent script
2. `requirements.txt` — Python dependencies (always includes `claude-agent-sdk`)
3. `README.md` — How to run it, what it does, example inputs/outputs

## After generating

Show the founder how to run it:
```bash
cd sdk/<skill-name>
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
source ../../.env   # or: export ANTHROPIC_API_KEY=your-key
python3 agent.py "your input here"
```

And point out:
- The prompt in `agent.py` came directly from the skill — edit it there if you want to change behavior
- The `allowed_tools` list matches what was in the skill
- Next steps: wrap in a FastAPI endpoint, add to a cron job, call from their product's backend
