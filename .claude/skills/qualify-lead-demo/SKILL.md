---
name: qualify-lead-demo
description: A deliberately weak first-draft lead qualifier. Used to demonstrate the eval+improve loop — starts simple, gets better through iteration. Not for production.
---

# Lead Qualifier (Demo — Iteration 1)

This skill qualifies a company as a sales lead. Our ICP is **B2B SaaS companies, roughly Seed–Series C, with ~20–500 employees**. Consumer (B2C) companies are not a fit. Companies far above the size range are a weaker fit.

## Input

A company name.

## Steps

1. Search the web for the company. Look specifically for: **industry / business model (B2B vs B2C), funding stage, headcount, and any buying signals** (hiring, recent raise, product launches).
2. Assign a tier using the rubric below.
3. Write the assessment using the exact Output format below. Emit every field **inline in your response**, not only in a file.

## Tier rubric

Assign exactly one tier:

- **HOT** — Clear ICP fit: B2B SaaS, Seed–Series C, ~20–500 employees, with an active buying signal.
- **WARM** — ICP fit on business model and stage, but missing a strong signal, OR slightly outside the size range.
- **COLD** — Tangential fit: B2B but wrong stage/size, or weak/uncertain match.
- **DISQUALIFIED** — Not a fit at all: consumer/B2C company, or fundamentally outside our market.

## Output

REQUIRED: Output all of the following fields inline in your response. Also save a copy as a markdown file in `output/leads/<company-slug>.md`.

1. **`Tier: <HOT | WARM | COLD | DISQUALIFIED>`** — This MUST be the first line, and MUST contain exactly one of the four labels verbatim. An output with no tier label, or a freeform verdict like "Good fit", is INVALID.
2. **Reasoning** — 3–5 sentences covering business model, stage, size, and signals against the ICP.
3. **Recommended next step** — A single concrete action with an **owner and a channel**. It must name who does what, where.
   - ✅ Good: "Email the VP of Engineering at Retool to book a 30-min discovery call about their internal-tooling spend."
   - ✅ Good (DISQUALIFIED): "Deprioritize — do not route to an AE."
   - ❌ Bad: "Treat as a competitive enterprise sale." / "Pursue this lead." (no owner, no channel)
   - IMPORTANT: If public info is thin, the next step MUST be a specific research/outreach action, e.g. "Find the Head of Sales on LinkedIn and verify headcount before outreach." Never omit this field.
4. **Sources** — Provide an inline citation on **every specific numeric/factual claim** (headcount, funding, valuation, stage), e.g. "Headcount ~450 [Crunchbase]". A bulk footer list is NOT sufficient. Any specific number without an inline source is a FAILURE.

## Success criteria

- Exactly one of HOT/WARM/COLD/DISQUALIFIED appears verbatim, as the first line.
- A recommended next step with an owner and channel is present inline.
- Every specific number carries an inline citation.
- If you cannot find a data point (e.g. headcount), say so explicitly — do NOT fabricate or silently omit it.
