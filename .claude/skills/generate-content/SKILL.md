---
name: generate-content
description: Generate content variations from a brief. Researches the topic, produces multiple versions in different tones or formats, and saves them for review. Use when asked to write, draft, generate, or create content.
---

# Content Generator

Takes a content brief and produces 3 variations — different tones, angles, or formats — so you can pick the best one or combine elements.

## Input

A content brief. Can be:
- A topic + format: "blog post about why startups fail"
- A specific brief: "launch email for our new analytics feature, target: growth marketers, tone: direct and punchy"
- A format override: "LinkedIn post — research 3 recent AI agent trends and write about them"

Optionally: a path to a `brand-voice.md` file with tone/voice guidelines.

## Steps

1. **Parse the brief** — Extract:
   - Content type (email, blog post, LinkedIn post, ad copy, product description, etc.)
   - Topic or subject matter
   - Target audience (if specified)
   - Tone preferences (if specified)
   - Any constraints (word count, CTA, specific claims to include/avoid)

2. **Load brand voice** — Check if `brand-voice.md` exists. If yes, read and incorporate. If no, infer from the brief or use a professional-but-approachable default.

3. **Research the topic** — If the topic benefits from current information:
   - Search for 2-3 relevant articles or data points
   - Note key statistics, quotes, or recent developments to weave in

4. **Plan 3 variations** — Before writing, decide on the 3 angles:
   - Variation A: [e.g., emotional/story-led]
   - Variation B: [e.g., data-driven/credibility-led]
   - Variation C: [e.g., contrarian/provocative]

5. **Write all 3 variations** — Each should be fully written, not a sketch. Apply the brief's constraints to all three.

6. **Save output** — Write to `output/content/<brief-slug>/`:
   - `variation-a.md`
   - `variation-b.md`
   - `variation-c.md`
   - `brief-summary.md` (recap of the brief, the 3 angles chosen, and a recommendation for which to use)

7. **Print summary** — Print the 3 angles chosen and a one-sentence recommendation.

## Output format

Each variation file (`variation-a.md`):
```markdown
# [Content Type]: [Topic]
*Variation A — [angle description]*

---

[The full content, formatted appropriately for the content type]

---
*Word count: [N] | Angle: [description] | Tone: [description]*
```

Brief summary (`brief-summary.md`):
```markdown
# Content Brief Summary

**Brief:** [original brief]
**Date:** [date]

## Variations produced

| Variation | Angle | Best for |
|-----------|-------|---------|
| A | [angle] | [when to use this] |
| B | [angle] | [when to use this] |
| C | [angle] | [when to use this] |

## Recommendation
[Which variation to use and why, or how to combine elements]
```

## Format guidelines by content type

- **Email**: Subject line + body. Under 150 words for cold email. Clear CTA.
- **LinkedIn post**: Hook in first line (no ellipsis cut-off). 3-5 short paragraphs. Optional CTA.
- **Blog post**: Title + intro + 3-5 sections with headers + conclusion. 600-1200 words.
- **Ad copy**: Headline (under 8 words) + body (under 30 words) + CTA.
- **Product description**: Problem → Solution → Key benefits → Social proof (if any). Under 200 words.

## If something goes wrong

- If the brief is very vague: make reasonable assumptions, state them in `brief-summary.md`
- If research returns irrelevant results: write from general knowledge, note this in the summary
- If a word count constraint makes 3 variations feel repetitive: vary the structure/format more aggressively
