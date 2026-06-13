# 5-Minute Demo Script

A structured walkthrough for showing `prototype-with-claude` to a reviewer, investor, or founder. Designed to make the core idea viscerally clear without requiring them to run anything.

**Goal:** Leave them understanding: (1) what the prototype loop looks like, (2) why Skills are the right abstraction, (3) how the graduation to production works.

**Setup:** Have Claude Code open in this repo, terminal visible, `icp.md` already created.

---

## Minute 1: The hook (set up the problem)

**Say:**
> "The hardest part of building an AI product isn't the code. It's figuring out what the agent should actually do. Most founders jump straight to writing SDK code before they've validated the core behavior. They end up iterating on Python strings instead of the actual logic.
>
> This repo flips that. You define the behavior in plain text — a Skill — and Claude Code runs it immediately. You find out in 30 seconds if the job is doable. Then when it's working reliably, you export it to production code with one command."

**Show:** The repo root in Claude Code. Point to `.claude/skills/qualify-lead/SKILL.md`.

> "This is all the agent needs. A job description in markdown. No Python, no API calls, no setup."

Open the file. Scroll through it — show the structure: steps, output format, error handling.

> "This is what Claude reads when you invoke the command. Let's run it."

---

## Minute 2: Run the skill live

**Type in Claude Code:**
```
/qualify-lead Retool
```

**While Claude is working, narrate:**
> "It's searching the web right now. LinkedIn job postings, Crunchbase funding data, their website. This usually takes 30-60 seconds."

**When it finishes:**
> "It saved a file. Let's look at it."

Open `output/leads/retool-qualification.md`. Point out:

1. The tier (HOT/WARM/COLD)
2. The ICP scorecard with evidence — "Notice these aren't guesses. Each score has a citation."
3. The recommended next step — "This is the part that's actually useful for a rep. Not 'good fit' — 'book discovery and mention the SDR build-out.'"

**Key point to make:**
> "This took 45 seconds. A rep would spend 20 minutes getting to this and still miss half of it."

---

## Minute 3: Show the eval loop

**Say:**
> "But 'it worked once' isn't enough. Let me show you how we measure whether this actually works reliably."

Open `.claude/skills/qualify-lead/evals/test-cases.md`.

> "These are binary quality criteria — yes or no. Does the output have a source URL? Is the tier correct for a consumer company? The criteria are what 'good' means for this agent."

**Type:**
```
/eval-skill qualify-lead
```

**While running:**
> "Claude is running the skill on each test case, then grading its own outputs against the criteria. This is LLM-as-judge — the same model that produced the output is evaluating it. Works because the criteria are specific enough that it's not subjective."

**When it finishes, show the report:**
> "77% — needs improvement. Look at the failure patterns. It's not random — there are two specific things wrong: missing source citations on low-info companies, and no handling for non-company inputs. These map directly to things we can fix in the SKILL.md."

**Type:**
```
/improve-skill qualify-lead
```

> "It reads the report, edits the SKILL.md to fix those specific issues, and I can re-run the eval to see if the score went up. This is the loop. Usually takes 2-3 cycles to get above 85%."

---

## Minute 4: Show the graduation to production

**Say:**
> "Once the behavior is validated — it passes evals consistently — you graduate to production with one command."

**Type:**
```
/export-to-sdk
```

> "It generates a Python file. Let me show you what that looks like."

Open `examples/02-lead-qualifier/sdk/agent.py`. Point to the `PROMPT_TEMPLATE`:

> "See this? It's the same instructions from the SKILL.md, now in a Python string. The agent behavior is identical. But now it runs without a human in the loop."

Scroll to the `qualify_batch` function:

> "This runs on a list. Import your CRM export as a CSV, point this at it, come back in the morning with every lead scored. Or wire it to a FastAPI endpoint and qualify leads in real-time as they come in."

**Key point to make:**
> "The mental model is: SKILL.md is the source of truth. The Python file is just a runtime wrapper. If you need to change the behavior, you change the skill, run evals, and update the Python. The code doesn't own the logic."

---

## Minute 5: The bigger picture

**Say:**
> "Three built-in skills work right after cloning — lead qualifier, research agent, content generator. These cover the most common patterns: score & classify, research & synthesize, generate & iterate.

> `/new-skill` is a guided wizard that asks you the right questions and writes the SKILL.md for you. Most people have a working first version in under 10 minutes.

> The path is always the same: define the job → run it → write test cases → eval → improve → export. The tools handle the iteration. You just write the job descriptions and criteria."

**Point to the repo map in README.md:**
> "Everything is here. The examples show the full pattern including SDK migrations. The docs cover the patterns, anti-patterns, and how to wire agents into products."

**Close with:**
> "The thing I find compelling about this approach is that it separates 'figuring out what the AI should do' from 'writing the code to run it.' Those are different problems on different timescales. Skills let you solve the first problem fast, cheaply, with no infrastructure. The Agent SDK solves the second problem once you know what you're building."

---

## Q&A prompts

**"How much does it cost to run?"**
> "Phase 1 — prototyping in Claude Code — uses your Claude subscription, no per-call billing. Phase 2 — running the Agent SDK in production — goes through the API. A lead qualifier running on 100 leads costs roughly $1-3 depending on how much research each one requires."

**"What if Claude is wrong about a company?"**
> "The eval loop exists specifically for this. You write a test case for the tricky case — 'what if the company is B2C but has a B2B product?' — and add it as a criterion. The skill gets better at handling those cases through the improve loop. It's the same process as fixing any software bug, just in markdown."

**"Can this handle [specific domain]?"**
> "The pattern works for any job where: (1) Claude has the information it needs via web search or files you provide, (2) the output has a defined structure, and (3) you can write yes/no quality criteria. Most research, scoring, and generation tasks fit."

**"What about TypeScript?"**
> "The Agent SDK has a TypeScript version with the same API. The Python examples here are directly portable — it's `for await (const message of query(...))` instead of `async for message in query(...)`."

---

## What not to show

- Don't demo with a company Claude might not know well — it risks a bad output during the live demo. Use Retool, Notion, or Linear.
- Don't show the raw Python SDK code first — start with the skill, then show the SDK as the migration path.
- Don't run `/eval-skill` without test cases in place — you'll get an error.
- Don't claim the improvement loop is fully automatic — it edits SKILL.md but you review the changes.
