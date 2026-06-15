# 5-Minute Demo Script

A structured walkthrough for showing `prototype-with-claude` to a reviewer, investor, or founder. Designed to make the core idea viscerally clear without requiring them to run anything.

**Goal:** Leave them understanding: (1) what the prototype loop looks like, (2) how fast you get to a running production agent, (3) how evals harden what's already shipping.

**Setup:** Have Claude Code open in this repo, terminal visible, `icp.md` already created.

---

## Minute 1: The hook (set up the problem)

**Say:**
> "The hardest part of building an AI product isn't the code. It's figuring out what the agent should actually do. Most founders jump straight to writing SDK code before they've validated the core behavior. They end up iterating on Python strings instead of the actual logic.
>
> This repo flips that. You define the behavior in plain text — a Skill — and Claude Code runs it immediately. You find out in 30 seconds if the job is doable. Then when it's working on a few examples, you export it to production code with one command. Ship first. Harden after."

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

## Minute 3: Ship the MVP

**Say:**
> "It worked on Retool. Run it on two more — Notion, Duolingo — and you'll see it handles edge cases. That's enough. Ship it now, before you write a single test case."

**Type:**
```
/export-to-sdk
```

> "It generates a Python file. Let me show you what that looks like."

Open `examples/02-lead-qualifier/sdk/agent.py`. Point to `PROMPT_TEMPLATE`:

> "See this? It's the same instructions from the SKILL.md, now in a Python string. The agent behavior is identical — but now it runs without a human in the loop."

Scroll to `qualify_batch`:

> "This runs on a list. Import your CRM export as a CSV, point this at it, come back in the morning with every lead scored. Or wire it to a FastAPI endpoint and qualify leads in real time as they come in."

**Key point to make:**
> "We just went from a plain-text job description to a production Python agent in three minutes. The prompt lives in SKILL.md — improve it later without touching the Python."

---

## Minute 4: Harden it with evals (after it's running)

**Say:**
> "Now it's shipping. Real inputs start revealing failure modes you'd never predict from test cases. That's when evals become useful — not as a gate before shipping, but as a way to measure and improve what's already running."

Open `.claude/skills/qualify-lead-demo/SKILL.md` — the intentionally weak version:

> "This is a deliberately weak version of the same skill. Watch what happens when you run evals on it."

Open `.claude/skills/qualify-lead-demo/versions/eval-report-v1-100pct.md`:

> "65% on the first run. Two specific failure patterns — missing citations on low-info companies, no handling for non-company inputs. Look what one improve cycle did."

Show `versions/SKILL-v0-initial.md` vs `versions/SKILL-v1-after-improve.md` side by side:

> "That diff is what `/improve-skill` wrote. It read the eval report and fixed the two failure patterns directly in the SKILL.md. Re-ran evals: 100%."

**Type:**
```
/improve-skill qualify-lead
```

> "Same loop on the production skill. Read report → edit SKILL.md → re-run evals. Because the agent.py just reads from SKILL.md, this takes effect immediately — no redeployment."

---

## Minute 5: The bigger picture

**Say:**
> "Three built-in skills work right after cloning — lead qualifier, research agent, content generator. These cover the most common patterns: score & classify, research & synthesize, generate & iterate.

> `/new-skill` is a guided wizard that asks you the right questions and writes the SKILL.md for you. Most people have a working first version in under 10 minutes.

> The order is always: define the job → run it → ship it → measure → improve. You're not waiting for perfection before shipping. You're using real production inputs to find the failures that matter."

**Point to the repo map in README.md:**
> "Everything is here. The examples show the full pattern including SDK migrations. The docs cover the patterns, anti-patterns, and how to wire agents into products."

**Close with:**
> "The thing I find compelling about this approach is that it separates 'figuring out what the AI should do' from 'writing the code to run it' — and both of those from 'making it reliable.' Three different problems on three different timescales. You don't have to solve all three before you ship."

---

## Q&A prompts

**"How much does it cost to run?"**
> "Phase 1 — prototyping in Claude Code — uses your Claude subscription, no per-call billing. Phase 2 — running the Agent SDK in production — goes through the API. A lead qualifier running on 100 leads costs roughly $1-3 depending on how much research each one requires."

**"What if Claude is wrong about a company?"**
> "That's exactly what evals catch once you're running in production. You write a test case for the tricky input, add it as a criterion, and the improve loop fixes it in SKILL.md. Same process as fixing a software bug, just in markdown."

**"Can this handle [specific domain]?"**
> "The pattern works for any job where: (1) Claude has the information it needs via web search or files you provide, (2) the output has a defined structure, and (3) you can write yes/no quality criteria. Most research, scoring, and generation tasks fit."

**"What about TypeScript?"**
> "The Agent SDK has a TypeScript version with the same API. The Python examples here are directly portable — it's `for await (const message of query(...))` instead of `async for message in query(...)`."

---

## What not to show

- Don't demo with a company Claude might not know well — risks a bad output during the live demo. Use Retool, Notion, or Linear.
- Don't show the raw Python SDK code first — start with the skill, then show the SDK as the migration path.
- Don't lead with evals — they're minute 4, not minute 2. The hook is speed to working agent, not test coverage.
- Don't claim the improvement loop is fully automatic — it edits SKILL.md but you review the changes.
