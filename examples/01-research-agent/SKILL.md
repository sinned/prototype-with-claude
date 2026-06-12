---
name: research-agent
description: Research a company, person, or topic and produce a structured intelligence brief. Use when asked to research, analyze, or learn about something. Trigger: "research X", "tell me about X", "brief on X".
---

# Research Agent

Produces a structured intelligence brief on any company, person, or topic by searching the web and synthesizing findings into a clear, actionable document.

## Input

A company name, person's name, topic, or question. Optionally: a specific angle (e.g., "Stripe — focus on their developer ecosystem strategy").

## Steps

1. **Parse the input** — Identify the main subject and any specific angle or focus area.

2. **Run 3-5 targeted searches** — Search for:
   - Official website / overview
   - Recent news (last 12 months)
   - Key facts relevant to the focus angle
   - Competitor or comparative context if relevant

3. **Fetch key pages** — Read 2-3 of the most relevant URLs found. Prioritize: official site, recent news articles, credible analysis.

4. **Synthesize findings** — Identify the 5-7 most important facts or insights. Look for: what makes this subject interesting or important, recent developments, notable strengths/risks.

5. **Write the brief** — Follow the output format below exactly.

6. **Save to file** — Write to `output/<subject>-brief.md` (create `output/` if it doesn't exist). Also print a one-paragraph summary to the terminal.

## Output format

Save as `output/<subject-slug>-brief.md`:

```markdown
# [Subject] — Intelligence Brief
*Generated: [date]*

## TL;DR
[2-3 sentences capturing the most important thing to know]

## Overview
[3-4 sentences: what it is, what it does, why it matters]

## Key Facts
- [Fact 1 — be specific, include numbers/dates where relevant]
- [Fact 2]
- [Fact 3]
- [Fact 4]
- [Fact 5]

## Recent Developments
[2-3 bullet points on what has happened in the last 12 months]

## Notable Strengths
- [Strength 1]
- [Strength 2]

## Risks / Watch Out For
- [Risk 1]
- [Risk 2]

## Sources
- [URL 1]
- [URL 2]
- [URL 3]
```

## If something goes wrong

- If web search returns no results: try alternative search terms (abbreviation, full name, industry + descriptor)
- If a URL is inaccessible: skip it and note in sources as "inaccessible"
- If subject is ambiguous (e.g., "Apple" — company or fruit?): default to the most business-relevant interpretation, note the assumption in the TL;DR
- If very little information is available: produce the brief with what's found, add a note at the top: "Limited public information available — brief based on [X sources]"
