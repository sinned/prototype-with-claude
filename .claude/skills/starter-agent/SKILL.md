---
name: starter-agent
description: Template skill — rename this and replace with your own instructions. Use this as a starting point for building your first AI agent skill.
---

# Starter Agent — Replace Me

This is your starting point. Replace everything below (and the frontmatter above) with your own skill.

## What this skill does

[One paragraph. Start with a verb. Example: "Researches a given topic by searching the web, reading relevant pages, and producing a structured summary."]

## Input

[Describe what you pass to this skill when invoking it. Example: "A company name or domain. Optionally: a specific aspect to focus on (e.g., 'pricing', 'competitors')."]

## Steps

[Step-by-step instructions for what Claude should do. Be specific. The more concrete, the more consistent the results.]

1. [First thing to do]
2. [Second thing to do]
3. [Third thing to do — keep going until the full job is described]

## Output format

[Describe exactly what to produce. Specify: file path or stdout, format (markdown/JSON/plain text), required sections, length.]

Example output structure:
```
## Summary
[2-3 sentences]

## Key findings
- Finding 1
- Finding 2

## Recommendation
[One clear recommendation]
```

## If something goes wrong

- If [tool/resource] is unavailable: [what to do instead]
- If the input doesn't match expectations: [how to handle it]
- If no relevant information is found: [what to tell the user]

---

## How to use this template

1. Copy this folder to `.claude/skills/<your-skill-name>/`
2. Rename the folder and update the `name` field in the frontmatter
3. Replace all placeholder text above
4. Run `/<your-skill-name> <your input>` in Claude Code to test
5. Iterate until it works reliably
6. Run `/export-to-sdk` to generate production Python code

## Need help?

Run `/new-skill` and Claude will guide you through building a skill interactively.
