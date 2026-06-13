"""
Content Generator — Agent SDK version
Migrated from: examples/03-content-generator/SKILL.md

Takes a content brief and produces 3 variations with different angles.
"""

import asyncio
import argparse
import csv
import sys
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions


DEFAULT_BRAND_VOICE = """
Tone: Direct, confident, and human. No buzzwords or corporate filler.
Write like a smart person talking to another smart person.
Specific > vague. Short sentences for impact, longer for nuance.
Avoid: "leverage" (as a verb), "utilize", "cutting-edge", "best-in-class", passive voice.
"""

PROMPT_TEMPLATE = """
Generate content variations from this brief: {brief}

Brand voice guidelines:
{brand_voice}

Steps:
1. Parse the brief: content type, topic, audience, tone preferences, constraints.
2. Plan 3 distinct variations with different angles (e.g., emotional/story-led, data-driven, contrarian).
3. Write all 3 variations fully. Apply brief constraints to each.
4. Save to output/content/{brief_slug}/:
   - variation-a.md
   - variation-b.md
   - variation-c.md
   - brief-summary.md (table of 3 angles + recommendation)
5. Print a one-line summary of the 3 angles chosen.

Each variation file format:
---
# [Content Type]: [Topic]
*Variation [A/B/C] — [angle description]*

[Full content]

*Word count: N | Angle: description | Tone: description*
---

Brief summary file format:
---
# Content Brief Summary
**Brief:** [brief]  **Date:** [date]

## Variations
| Variation | Angle | Best for |
|-----------|-------|---------|
| A | [angle] | [when to use] |
| B | [angle] | [when to use] |
| C | [angle] | [when to use] |

## Recommendation
[Which to use and why]
---

Format guidelines by content type:
- Email: Subject line + body. Under 150 words for cold outreach. Clear CTA.
- LinkedIn: Hook in first line. 3-5 short paragraphs. Optional CTA.
- Blog post: Title + intro + 3-5 sections + conclusion. 600-1200 words.
- Ad copy: Headline (≤8 words) + body (≤30 words) + CTA.
- Product description: Problem → Solution → Benefits → Proof. Under 200 words.

If brief is vague, make reasonable assumptions and state them in brief-summary.md.
"""


def load_brand_voice(voice_path: str | None = None) -> str:
    """Load brand voice from file, or use defaults."""
    paths_to_try = [voice_path, "brand-voice.md", ".claude/brand-voice.md"] if voice_path else ["brand-voice.md", ".claude/brand-voice.md"]
    for path in paths_to_try:
        if path and Path(path).exists():
            return Path(path).read_text()
    return DEFAULT_BRAND_VOICE


def slugify(text: str, max_len: int = 40) -> str:
    """Convert a brief to a filesystem-safe slug."""
    slug = text.lower()[:max_len]
    slug = "".join(c if c.isalnum() else "-" for c in slug)
    return slug.strip("-")


async def generate(brief: str, brand_voice: str) -> str | None:
    """Generate content variations for a brief. Returns result summary."""
    brief_slug = slugify(brief)
    prompt = PROMPT_TEMPLATE.format(
        brief=brief,
        brief_slug=brief_slug,
        brand_voice=brand_voice,
    )

    result = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "Read", "Write", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            result = message.result

    return result


async def generate_batch(briefs: list[str], brand_voice: str) -> list[tuple[str, str | None]]:
    """Generate content for a list of briefs sequentially."""
    results = []
    for i, brief in enumerate(briefs, 1):
        print(f"[{i}/{len(briefs)}] Generating: {brief[:60]}...", flush=True)
        result = await generate(brief, brand_voice)
        results.append((brief, result))
        print(f"  Done\n", flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate content variations from a brief."
    )
    parser.add_argument("brief", nargs="?", help="Content brief (topic, format, audience, tone)")
    parser.add_argument("--batch", metavar="CSV_FILE", help="CSV with a 'brief' column")
    parser.add_argument("--voice", metavar="FILE", help="Brand voice guidelines file (default: brand-voice.md)")
    args = parser.parse_args()

    brand_voice = load_brand_voice(args.voice)

    if args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            print(f"Error: file not found: {args.batch}", file=sys.stderr)
            sys.exit(1)
        with open(batch_file) as f:
            reader = csv.DictReader(f)
            briefs = [row["brief"] for row in reader if row.get("brief")]
        print(f"Processing {len(briefs)} briefs...\n")
        results = asyncio.run(generate_batch(briefs, brand_voice))
        print(f"\nDone. {len(results)} content sets saved to output/content/")
    elif args.brief:
        result = asyncio.run(generate(args.brief, brand_voice))
        if result is None:
            print("Error: agent query returned no result. Check ANTHROPIC_API_KEY and network.", file=sys.stderr)
            sys.exit(1)
        print("\n--- Agent summary ---")
        print(result)
        print("\nVariations saved to output/content/")
    else:
        brief = input("Content brief: ").strip()
        if not brief:
            print("No brief provided.", file=sys.stderr)
            sys.exit(1)
        result = asyncio.run(generate(brief, brand_voice))
        if result is None:
            print("Error: agent query returned no result. Check ANTHROPIC_API_KEY and network.", file=sys.stderr)
            sys.exit(1)
        print("\n--- Agent summary ---")
        print(result)
        print("\nVariations saved to output/content/")


if __name__ == "__main__":
    main()
