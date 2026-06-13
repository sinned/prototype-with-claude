# Demo: From 65% to 100% in One Iteration

A real, end-to-end demonstration of the eval + improve loop on a deliberately weak skill. Every artifact in this doc is checked into the repo at `.claude/skills/qualify-lead-demo/versions/` — these are actual outputs from the SDK script, not mock-ups.

**TL;DR:** A 22-line skill written in 5 minutes scored 65% on its eval suite. One run of `improve.py --save-versions` rewrote it (47 lines) and the score jumped to 100% on the same test cases. Total time: under 4 minutes of API calls.

---

## The starting point — iteration 0 (intentionally weak)

This is what a founder might write in 5 minutes before knowing what good looks like. It's vague on purpose — to let the improve loop show what it's worth.

**File:** `.claude/skills/qualify-lead-demo/versions/SKILL-v0-initial.md`

```markdown
---
name: qualify-lead-demo
description: A deliberately weak first-draft lead qualifier...
---

# Lead Qualifier (Demo — Iteration 0)

## Input
A company name.

## Steps
1. Look up the company.
2. Figure out if it's a good fit for our product.
3. Write something useful.

## Output
Save your assessment as a markdown file in `output/leads/`.
```

That's it. No ICP, no rubric, no output format, no error handling.

---

## v0 eval results — 65% (11 of 17 criteria)

Run with: `python3 examples/04-evals-and-improvement/sdk/eval_runner.py qualify-lead-demo`

| Test case | Input | Score |
|-----------|-------|-------|
| Clear fit (B2B SaaS) | Retool | **2/5 (40%)** ❌ |
| Clear disqualify (consumer) | Duolingo | 4/4 (100%) ✅ |
| Borderline | Notion | 2/4 (50%) ⚠️ |
| Limited public info | "Runway Financial" | 3/4 (75%) ⚠️ |

**What failed:**
- Output didn't explicitly state a tier label (HOT/WARM/COLD/DISQUALIFIED) — Claude wrote "good fit" or descriptive verdicts
- No explicit recommended next step in most outputs
- Specific numbers (headcount, funding) cited without sources
- No "do not fabricate" guidance — Claude invented headcount for low-info companies

Pattern analysis (from the eval report) called out:
- **Missing tier label** — no required structure for the verdict
- **Vague output format** — Claude improvises differently each run
- **No anti-hallucination rule** — low-info cases get fabricated specifics

---

## One improve.py call later — iteration 1

Run with:
```bash
python3 examples/04-evals-and-improvement/sdk/improve.py qualify-lead-demo --save-versions
```

The script reads the eval report, identifies the top failure patterns, and uses the Write tool to rewrite `SKILL.md` from 22 lines to 47 lines. `--save-versions` saves a snapshot to `versions/SKILL-v1-after-improve.md`.

**What Claude added** (real diff between v0 and v1):

1. **An explicit ICP** in the description:
   > "Our ICP is B2B SaaS companies, roughly Seed–Series C, with ~20–500 employees. Consumer (B2C) companies are not a fit."

2. **Specific search targets** in the steps:
   > "Search the web for the company. Look specifically for: industry / business model (B2B vs B2C), funding stage, headcount, and any buying signals (hiring, recent raise, product launches)."

3. **A tier rubric:**
   > - **HOT** — Clear ICP fit: B2B SaaS, Seed–Series C, ~20–500 employees, with an active buying signal.
   > - **WARM** — ICP fit on business model and stage, but missing a strong signal, OR slightly outside the size range.
   > - **COLD** — Tangential fit...
   > - **DISQUALIFIED** — Not a fit...

4. **A required output format with examples of good vs. bad:**
   > **Recommended next step** — A single concrete action with an owner and a channel.  
   > ✅ Good: "Email the VP of Engineering at Retool to book a 30-min discovery call about their internal-tooling spend."  
   > ❌ Bad: "Treat as a competitive enterprise sale." (no owner, no channel)

5. **An anti-fabrication rule:**
   > "If you cannot find a data point (e.g. headcount), say so explicitly — do NOT fabricate or silently omit it."

6. **An explicit success criteria checklist** at the bottom.

---

## v1 eval results — 100% (17 of 17 criteria)

Same test cases. Same eval runner.

| Test case | Input | v0 | v1 |
|-----------|-------|----|----|
| Clear fit (B2B SaaS) | Retool | 40% ❌ | **100%** ✅ |
| Clear disqualify (consumer) | Duolingo | 100% ✅ | 100% ✅ |
| Borderline | Notion | 50% ⚠️ | **100%** ✅ |
| Limited public info | "Runway Financial" | 75% ⚠️ | **100%** ✅ |
| **Overall** | | **65%** | **100%** |

The full v1 eval report is saved at `.claude/skills/qualify-lead-demo/versions/eval-report-v1-100pct.md`.

---

## Why this matters

This is the value proposition of the prototype-with-claude approach in one diagram:

```
Weak first draft (5 min to write)       Polished skill (3 min to improve)
       65% pass rate              →            100% pass rate
       22 lines                                 47 lines
       Vague instructions                       Specific rubric + format + examples
```

The founder didn't sit there iterating manually for an hour. They wrote a rough first draft, ran the eval suite, and let `/improve-skill` (or `improve.py`) close the gap. The improvements are visible, surgical, and traceable in the version snapshots.

This is what makes Skills + the eval loop a different way to build AI products: you tune the **behavior** in markdown, with measurable quality, before writing any Python.

---

## Try it yourself

The complete demo is reproducible from a fresh clone:

```bash
# 1. Set up your env
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
python3 -m venv .venv && source .venv/bin/activate
source .env
python3 -m pip install claude-agent-sdk

# 2. (Optional) reset the demo skill to its weak starting point
cp .claude/skills/qualify-lead-demo/versions/SKILL-v0-initial.md \
   .claude/skills/qualify-lead-demo/SKILL.md

# 3. Get a baseline score
python3 examples/04-evals-and-improvement/sdk/eval_runner.py qualify-lead-demo

# 4. Run one improvement iteration, saving versions
python3 examples/04-evals-and-improvement/sdk/improve.py qualify-lead-demo --improve-only --save-versions

# 5. Re-evaluate
python3 examples/04-evals-and-improvement/sdk/eval_runner.py qualify-lead-demo

# 6. Compare versions
diff .claude/skills/qualify-lead-demo/versions/SKILL-v0-initial.md \
     .claude/skills/qualify-lead-demo/SKILL.md
```

**Total API cost** of one full demo run: ~$1-3 (varies with how many web searches the agent does per qualification).

---

## Use `--save-versions` for your own skills

The `--save-versions` flag is off by default — git history is the right place to track skill changes in normal use. Turn it on when you want a clean audit trail to show in a presentation, a teaching context, or a regression investigation:

```bash
# Full automated loop with versioning
python3 examples/04-evals-and-improvement/sdk/improve.py my-skill \
  --save-versions --max-iterations 3 --target-score 0.85
```

Snapshots land in `.claude/skills/my-skill/versions/`:
- `SKILL-v0-initial.md` — before any improvements
- `SKILL-v1-after-improve.md` — after iteration 1
- `SKILL-v2-after-improve.md` — after iteration 2
- ... etc.
