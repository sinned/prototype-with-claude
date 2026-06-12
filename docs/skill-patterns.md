# Skill Design Patterns

Patterns for the most common AI agent jobs startup founders build.

## The three core patterns

### 1. Research & Synthesize

**Shape:** Input (topic/name) → Search → Gather → Synthesize → Structured output

**When to use:** Any job that requires gathering information and producing a summary, brief, or report.

**Tools needed:** `WebSearch`, `WebFetch`, `Write`

**Skill structure:**
```markdown
## Steps
1. Parse input — what is the subject, what angle/focus?
2. Run N targeted searches
3. Fetch M most relevant pages
4. Synthesize: identify the K most important insights
5. Write output in [specific format]
6. Save to [specific path]
```

**Common mistakes:**
- Searches that are too broad ("AI") instead of specific ("AI agent frameworks 2025")
- No instructions on what to do when results are thin
- Output format left to Claude's discretion — specify it exactly

**Startup use cases:**
- Prospect research before sales calls
- Competitive intelligence
- Market landscape briefs
- Due diligence summaries
- News monitoring and synthesis

---

### 2. Score & Classify

**Shape:** Input (data) → Load context → Analyze → Score/classify → Decision + reasoning

**When to use:** Any job that applies a consistent rubric to an input and produces a categorized output.

**Tools needed:** `Read` (for rubric/config files), `Write` (for output), optionally `WebSearch` (for enrichment)

**Skill structure:**
```markdown
## Steps
1. Load criteria from [file] or use defaults
2. Gather information about the input
3. Score against each criterion: ✅/⚠️/❌/❓
4. Assign overall tier based on [rules]
5. Write output: decision + scorecard + reasoning + next step
```

**Common mistakes:**
- Rubric too vague ("good fit" vs "company size 50-500 employees")
- No handling for missing information (❓ is always a valid score)
- Hard coding criteria — always load from a config file so it's easy to change

**Startup use cases:**
- Lead qualification
- Job application screening
- Support ticket routing and prioritization
- Content moderation
- Investment deal screening

---

### 3. Generate & Iterate

**Shape:** Input (brief/spec) → Research → Plan variations → Generate → Output set

**When to use:** Any job that produces content, code, or documents where having multiple options has value.

**Tools needed:** `Read` (for brand/style guides), `Write` (for output), optionally `WebSearch` (for research)

**Skill structure:**
```markdown
## Steps
1. Parse brief: type, topic, audience, constraints
2. Load style/voice guidelines from [file]
3. Research if needed (recent data, examples)
4. Plan N variations with distinct angles
5. Write all N variations fully
6. Save each + a summary with recommendation
```

**Common mistakes:**
- Variations that are too similar (just different words, not different angles)
- Not specifying the output format in detail (length, structure, channel-specific rules)
- Generating only one version — the whole point is multiple options

**Startup use cases:**
- Marketing copy variations for A/B testing
- Personalized outreach at scale
- Product announcements, changelogs
- Job descriptions, policies, SOPs
- Social media content calendar

---

## Composing patterns

Most complex agent jobs are combinations of the three patterns:

**Research → Score:** Research a prospect, then qualify them
```
/research-and-qualify Figma
```

**Research → Generate:** Research a topic, then generate content about it
```
/research-then-write "Series B fundraising trends"
```

**Score → Generate:** Analyze data, then write a tailored output
```
/analyze-and-respond <support ticket>
```

Build these as separate skills first, then compose them in the SDK using sequential agent calls or the `Agent` tool for subagents.

---

## Skill quality checklist

Before calling a skill "done," check:

- [ ] The job is stated in one sentence starting with a verb
- [ ] Input format is explicit — no ambiguity about what to pass
- [ ] Steps are numbered and concrete — a smart intern could follow them
- [ ] Output format is fully specified — structure, file path, sections
- [ ] Edge cases are handled — what to do when tools fail or info is missing
- [ ] Tested with 3+ inputs covering the range of expected real-world cases
- [ ] Results are consistent across runs (rerun the same input twice)

---

## Anti-patterns

**The "try your best" skill** — Instructions so vague that Claude improvises every time, producing inconsistent results. Fix: be specific about every step.

**The "ask me later" skill** — Skill that interrupts mid-run to ask clarifying questions. Fix: handle ambiguity in the instructions ("if X is unclear, default to Y").

**The "do everything" skill** — One skill that tries to do 5 different jobs. Fix: split into focused skills, compose in the SDK.

**The "copy my mental model" skill** — Instructions that assume Claude understands your implicit context. Fix: make every assumption explicit in the SKILL.md.
