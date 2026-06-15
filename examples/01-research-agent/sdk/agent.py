"""
Research Agent — Agent SDK version
Migrated from: examples/01-research-agent/SKILL.md

Researches a company, person, or topic and produces a structured intelligence brief.
"""

import asyncio
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()

PROMPT_TEMPLATE = """
Research {subject} and produce a structured intelligence brief.

Steps:
1. Parse the subject and any specific angle or focus area from: "{subject}"
2. Run 3-5 targeted searches:
   - Official website / overview
   - Recent news (last 12 months)
   - Key facts relevant to any specified focus angle
   - Competitor or comparative context if relevant
3. Fetch and read 2-3 of the most relevant URLs. Prioritize: official site, recent news, credible analysis.
4. Synthesize findings: identify the 5-7 most important facts or insights.
5. Write the brief in the format below.
6. Save to output/{subject_slug}-brief.md (create output/ directory if needed).
7. Print a one-paragraph summary to confirm completion.

Output format — save as output/{subject_slug}-brief.md:

# {subject} — Intelligence Brief
*Generated: [today's date]*

## TL;DR
[2-3 sentences capturing the most important thing to know]

## Overview
[3-4 sentences: what it is, what it does, why it matters]

## Key Facts
- [Fact 1 — specific, with numbers/dates where relevant]
- [Fact 2]
- [Fact 3]
- [Fact 4]
- [Fact 5]

## Recent Developments
- [Development from last 12 months]
- [Development from last 12 months]
- [Development from last 12 months]

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

If web search returns no results, try alternative terms.
If a URL is inaccessible, skip it and note it as "inaccessible" in sources.
If very little information is available, produce the brief with what's found and add a note at the top.
"""


async def research(subject: str) -> str | None:
    """Research a subject and produce a brief. Returns Claude's result summary."""
    subject_slug = subject.lower().replace(" ", "-").replace("/", "-")[:50]
    prompt = PROMPT_TEMPLATE.format(subject=subject, subject_slug=subject_slug)

    result = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "WebFetch", "Write", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            result = message.result

    return result


async def research_batch(subjects: list[str]) -> list[tuple[str, str | None]]:
    """Research a list of subjects sequentially."""
    results = []
    for i, subject in enumerate(subjects, 1):
        print(f"[{i}/{len(subjects)}] Researching: {subject}", flush=True)
        result = await research(subject)
        results.append((subject, result))
        print(f"  Done: {subject}\n", flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Research a company, person, or topic and produce an intelligence brief."
    )
    parser.add_argument(
        "subject",
        nargs="?",
        help="What to research (company name, person, topic)",
    )
    parser.add_argument(
        "--batch",
        metavar="FILE",
        help="Path to a text file with one subject per line",
    )
    args = parser.parse_args()

    if args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            print(f"Error: batch file not found: {args.batch}", file=sys.stderr)
            sys.exit(1)
        subjects = [line.strip() for line in batch_file.read_text().splitlines() if line.strip()]
        print(f"Processing {len(subjects)} subjects from {args.batch}\n")
        results = asyncio.run(research_batch(subjects))
        print("\nBatch complete:")
        for subject, result in results:
            status = "OK" if result else "FAILED"
            print(f"  [{status}] {subject}")
    elif args.subject:
        result = asyncio.run(research(args.subject))
        if result is None:
            print("Error: agent query returned no result. Check ANTHROPIC_API_KEY and network.", file=sys.stderr)
            sys.exit(1)
        print("\n--- Agent summary ---")
        print(result)
        print("\nBrief saved to output/ directory.")
    else:
        subject = input("What do you want to research? ").strip()
        if not subject:
            print("No subject provided.", file=sys.stderr)
            sys.exit(1)
        result = asyncio.run(research(subject))
        if result is None:
            print("Error: agent query returned no result. Check ANTHROPIC_API_KEY and network.", file=sys.stderr)
            sys.exit(1)
        print("\n--- Agent summary ---")
        print(result)
        print("\nBrief saved to output/ directory.")


if __name__ == "__main__":
    main()
