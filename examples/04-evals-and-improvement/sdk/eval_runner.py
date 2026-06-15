"""
Eval Runner — Agent SDK version
Migrated from: .claude/commands/eval-skill.md

Runs a skill's test cases, grades each output with Claude-as-judge,
and produces a structured eval report.
"""

import asyncio
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


@dataclass
class Criterion:
    text: str
    passed: bool | None = None
    notes: str = ""


@dataclass
class TestCase:
    name: str
    input: str
    criteria: list[Criterion] = field(default_factory=list)
    output_path: str | None = None
    score: float | None = None


@dataclass
class EvalReport:
    skill_name: str
    run_date: str
    test_cases: list[TestCase] = field(default_factory=list)
    overall_score: float | None = None
    failure_patterns: list[dict] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


def parse_test_cases(test_cases_md: str) -> list[TestCase]:
    """Parse test-cases.md into TestCase objects."""
    test_cases = []
    current_case = None
    in_criteria = False

    for line in test_cases_md.splitlines():
        line = line.strip()

        # New test case
        if line.startswith("## Test"):
            if current_case:
                test_cases.append(current_case)
            name = line.lstrip("#").strip()
            current_case = TestCase(name=name, input="")
            in_criteria = False

        elif current_case is not None:
            if line.startswith("**Input:**"):
                current_case.input = line.replace("**Input:**", "").strip()
                in_criteria = False

            elif line.startswith("**Criteria:**"):
                in_criteria = True

            elif in_criteria and (line.startswith("- [ ]") or line.startswith("- [x]") or line.startswith("- [X]")):
                passed = line.startswith("- [x]") or line.startswith("- [X]")
                criterion_text = re.sub(r"^- \[.?\]\s*", "", line)
                current_case.criteria.append(Criterion(text=criterion_text, passed=None))

    if current_case:
        test_cases.append(current_case)

    return [tc for tc in test_cases if tc.input and tc.criteria]


RUN_SKILL_PROMPT = """
Run this skill on the given input. Follow the skill instructions exactly.

SKILL INSTRUCTIONS:
{skill_instructions}

INPUT: {skill_input}

Execute all steps in the skill. When done, confirm what was produced and where it was saved.
"""

GRADE_PROMPT = """
You are grading the output of an AI agent against quality criteria. Be strict and honest.

SKILL: {skill_name}
INPUT: {skill_input}

WHAT THE AGENT PRODUCED:
{agent_result}

OUTPUT FILE CONTENTS (if a file was written):
{output_contents}

CRITERIA TO EVALUATE:
{criteria_list}

For each criterion, respond with EXACTLY this format (one line per criterion):
CRITERION: [exact criterion text]
RESULT: PASS or FAIL
NOTES: [one sentence explaining why, citing specific evidence from the output]

Grade strictly — if in doubt, mark FAIL. Do not give benefit of the doubt.
After all criteria, add:
SUMMARY: [one sentence overall assessment]
"""

ANALYZE_PATTERNS_PROMPT = """
You are analyzing eval results to find failure patterns in an AI skill.

SKILL: {skill_name}

FAILED CRITERIA ACROSS ALL TEST CASES:
{failures_json}

Identify the top 2-3 failure patterns. For each pattern:
- What is failing?
- Which test cases does it affect?
- What is the root cause in the skill instructions?
- What specific change would fix it?

Respond as JSON:
{{
  "patterns": [
    {{
      "name": "short name",
      "description": "what is failing",
      "affected_tests": ["test 1", "test 2"],
      "root_cause": "why the skill instructions cause this",
      "fix": "specific change to make in SKILL.md"
    }}
  ],
  "recommendations": [
    "Recommendation 1 as a complete sentence",
    "Recommendation 2"
  ]
}}
"""


async def run_skill_on_input(skill_instructions: str, skill_input: str) -> str | None:
    """Run a skill on a given input, return the result."""
    prompt = RUN_SKILL_PROMPT.format(
        skill_instructions=skill_instructions,
        skill_input=skill_input,
    )
    result = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["WebSearch", "WebFetch", "Read", "Write", "Bash"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            result = message.result
    return result


async def grade_output(
    skill_name: str,
    skill_input: str,
    agent_result: str | None,
    criteria: list[Criterion],
) -> list[Criterion]:
    """Use Claude as judge to grade an output against criteria."""
    # Try to read any output file that was written
    output_contents = "(no file written or file not found)"
    output_dir = Path("output")
    if output_dir.exists():
        slug = skill_input.lower().replace(" ", "-")[:30]
        for f in output_dir.rglob("*.md"):
            if slug in f.name.lower() or slug in str(f).lower():
                try:
                    output_contents = f.read_text()[:3000]
                    break
                except Exception:
                    pass

    criteria_list = "\n".join(f"{i+1}. {c.text}" for i, c in enumerate(criteria))
    prompt = GRADE_PROMPT.format(
        skill_name=skill_name,
        skill_input=skill_input,
        agent_result=agent_result or "(no result returned)",
        output_contents=output_contents,
        criteria_list=criteria_list,
    )

    grading_text = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read"],
            permission_mode="default",
        ),
    ):
        if hasattr(message, "result"):
            grading_text = message.result

    if not grading_text:
        return criteria

    # Parse grading results
    graded = list(criteria)
    current_criterion = None
    current_result = None
    current_notes = None

    for line in grading_text.splitlines():
        line = line.strip()
        if line.startswith("CRITERION:"):
            current_criterion = line.replace("CRITERION:", "").strip()
        elif line.startswith("RESULT:"):
            current_result = "pass" in line.lower()
        elif line.startswith("NOTES:"):
            current_notes = line.replace("NOTES:", "").strip()
            # Match to a criterion by text similarity
            if current_criterion:
                for c in graded:
                    if c.passed is None and (
                        current_criterion.lower() in c.text.lower() or
                        c.text.lower() in current_criterion.lower()
                    ):
                        c.passed = current_result
                        c.notes = current_notes or ""
                        break
            current_criterion = current_result = current_notes = None

    # Default ungraded criteria to fail
    for c in graded:
        if c.passed is None:
            c.passed = False
            c.notes = "Could not be graded — defaulting to fail"

    return graded


async def analyze_failure_patterns(
    skill_name: str, test_cases: list[TestCase]
) -> tuple[list[dict], list[str]]:
    """Use Claude to find patterns across failures."""
    failures = []
    for tc in test_cases:
        for c in tc.criteria:
            if c.passed is False:
                failures.append({
                    "test_case": tc.name,
                    "input": tc.input,
                    "criterion": c.text,
                    "notes": c.notes,
                })

    if not failures:
        return [], ["All criteria passed — no improvements needed."]

    prompt = ANALYZE_PATTERNS_PROMPT.format(
        skill_name=skill_name,
        failures_json=json.dumps(failures, indent=2),
    )

    result_text = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(allowed_tools=[]),
    ):
        if hasattr(message, "result"):
            result_text = message.result

    if result_text:
        try:
            start = result_text.find("{")
            end = result_text.rfind("}") + 1
            data = json.loads(result_text[start:end])
            return data.get("patterns", []), data.get("recommendations", [])
        except (json.JSONDecodeError, ValueError):
            pass

    return [], ["Run /improve-skill to get improvement suggestions."]


def write_report(report: EvalReport, output_path: Path) -> None:
    """Write a human-readable eval report to markdown."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Eval Report: {report.skill_name}",
        f"*Run: {report.run_date} | Score: {report.overall_score:.0%} overall*",
        "",
        "## Summary",
        f"**Overall score: {report.overall_score:.0%}**",
        "",
        "| Test case | Score | Status |",
        "|-----------|-------|--------|",
    ]

    for tc in report.test_cases:
        passed = sum(1 for c in tc.criteria if c.passed)
        total = len(tc.criteria)
        pct = passed / total if total else 0
        status = "✅" if pct >= 0.8 else ("⚠️" if pct >= 0.5 else "❌")
        lines.append(f"| {tc.name} | {pct:.0%} ({passed}/{total}) | {status} |")

    lines += ["", "## Failure Patterns", ""]
    if report.failure_patterns:
        for p in report.failure_patterns:
            lines += [
                f"### {p.get('name', 'Unknown')}",
                f"**Affects:** {', '.join(p.get('affected_tests', []))}",
                f"**Root cause:** {p.get('root_cause', '')}",
                f"**Fix:** {p.get('fix', '')}",
                "",
            ]
    else:
        lines.append("No significant failure patterns found.\n")

    lines += ["## Recommendations", ""]
    for rec in report.recommendations:
        lines.append(f"- {rec}")

    lines += ["", "## Test Case Details", ""]
    for tc in report.test_cases:
        passed = sum(1 for c in tc.criteria if c.passed)
        total = len(tc.criteria)
        lines += [
            f"### {tc.name}",
            f"**Input:** {tc.input}  ",
            f"**Score:** {passed}/{total} criteria",
            "",
            "| Criterion | Result | Notes |",
            "|-----------|--------|-------|",
        ]
        for c in tc.criteria:
            result = "✅" if c.passed else "❌"
            lines.append(f"| {c.text} | {result} | {c.notes} |")
        lines.append("")

    output_path.write_text("\n".join(lines))


async def run_evals(skill_name: str, verbose: bool = False) -> EvalReport:
    """Run the full eval suite for a skill. Returns the report."""
    skill_path = Path(f".claude/skills/{skill_name}/SKILL.md")
    test_cases_path = Path(f".claude/skills/{skill_name}/evals/test-cases.md")

    if not skill_path.exists():
        print(f"Error: skill not found at {skill_path}", file=sys.stderr)
        sys.exit(1)
    if not test_cases_path.exists():
        print(f"Error: test cases not found at {test_cases_path}", file=sys.stderr)
        print(f"Create test cases using examples/04-evals-and-improvement/test-cases-example.md as a template.")
        sys.exit(1)

    skill_instructions = skill_path.read_text()
    test_cases = parse_test_cases(test_cases_path.read_text())

    if not test_cases:
        print("Error: no test cases found in test-cases.md", file=sys.stderr)
        sys.exit(1)

    print(f"Running {len(test_cases)} test cases for skill: {skill_name}\n")

    report = EvalReport(
        skill_name=skill_name,
        run_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    total_criteria = 0
    total_passed = 0

    for i, tc in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] Running: {tc.name} (input: {tc.input[:50]})")

        # Run the skill
        result = await run_skill_on_input(skill_instructions, tc.input)
        if verbose and result:
            print(f"  Agent result: {result[:100]}...")

        # Grade the output
        graded_criteria = await grade_output(skill_name, tc.input, result, tc.criteria)

        passed = sum(1 for c in graded_criteria if c.passed)
        total = len(graded_criteria)
        tc.criteria = graded_criteria
        tc.score = passed / total if total else 0

        total_criteria += total
        total_passed += passed

        status = "✅" if tc.score >= 0.8 else ("⚠️" if tc.score >= 0.5 else "❌")
        print(f"  {status} {passed}/{total} criteria passed ({tc.score:.0%})\n")

        report.test_cases.append(tc)

    report.overall_score = total_passed / total_criteria if total_criteria else 0

    # Analyze failure patterns
    print("Analyzing failure patterns...")
    report.failure_patterns, report.recommendations = await analyze_failure_patterns(skill_name, report.test_cases)

    # Write report
    report_path = Path(f"output/evals/{skill_name}-report.md")
    write_report(report, report_path)
    print(f"\nReport saved to {report_path}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Run evals on a Claude Code skill."
    )
    parser.add_argument("skill_name", help="Name of the skill to evaluate (directory name in .claude/skills/)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print agent results during run")
    args = parser.parse_args()

    report = asyncio.run(run_evals(args.skill_name, verbose=args.verbose))

    print(f"\n{'='*50}")
    print(f"EVAL COMPLETE: {args.skill_name}")
    print(f"Overall score: {report.overall_score:.0%} ({sum(1 for tc in report.test_cases for c in tc.criteria if c.passed)}/{sum(len(tc.criteria) for tc in report.test_cases)} criteria)")
    print(f"{'='*50}")

    if report.failure_patterns:
        print("\nTop failure patterns:")
        for p in report.failure_patterns[:3]:
            print(f"  - {p.get('name')}: {p.get('description')}")

    if report.overall_score < 0.8:
        print(f"\nScore below 80% — run `python improve.py {args.skill_name}` to improve the skill.")
    else:
        print("\nSkill is performing well. Consider adding harder test cases to raise the bar.")


if __name__ == "__main__":
    main()
