"""
Skill Improvement Loop — Agent SDK version
Migrated from: .claude/commands/improve-skill.md

Reads eval results, uses Claude to suggest improvements to SKILL.md,
applies them, and reruns evals until the target score is reached.
"""

import asyncio
import argparse
import sys
from datetime import datetime
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

from eval_runner import run_evals, EvalReport


IMPROVEMENT_PROMPT = """
You are an expert at improving AI agent prompts (called "Skills").
Your job: read an eval report showing where a skill is failing, then edit the SKILL.md to fix the failures.

SKILL FILE: {skill_path}

CURRENT SKILL CONTENT:
{skill_content}

EVAL REPORT (showing failures):
{eval_report}

Your task:
1. Read the failure patterns and recommendations in the eval report.
2. Identify the 2-3 most impactful changes to make to the SKILL.md.
3. Edit the SKILL.md directly (use the Edit tool).

Edit rules:
- Make instructions more specific, not more vague
- Add explicit handling for failure cases ("if X happens, do Y")
- If an output format wasn't being followed, make it more explicit
- Add "REQUIRED:" or "IMPORTANT:" labels to steps Claude keeps skipping
- Add concrete examples for criteria that require specific styles or formats
- Do NOT add fluff — every change should fix a specific failure
- Do NOT remove content that's working

After editing, summarize your changes as JSON:
{{
  "changes": [
    {{"what": "description of change", "why": "which failure pattern this fixes"}}
  ],
  "expected_improvements": ["criterion or pattern that should now pass"]
}}
"""


async def apply_improvements(skill_name: str, report: EvalReport) -> list[dict]:
    """Use Claude to edit SKILL.md based on eval failures."""
    skill_path = Path(f".claude/skills/{skill_name}/SKILL.md")
    report_path = Path(f"output/evals/{skill_name}-report.md")

    skill_content = skill_path.read_text()
    report_content = report_path.read_text() if report_path.exists() else "(no report found)"

    prompt = IMPROVEMENT_PROMPT.format(
        skill_path=str(skill_path),
        skill_content=skill_content,
        eval_report=report_content,
    )

    result_text = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Write"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "result"):
            result_text = message.result

    # Parse changes from result
    changes = []
    if result_text:
        import json
        try:
            start = result_text.rfind("{")
            end = result_text.rfind("}") + 1
            if start >= 0 and end > start:
                data = json.loads(result_text[start:end])
                changes = data.get("changes", [])
        except (json.JSONDecodeError, ValueError):
            changes = [{"what": "Applied improvements based on eval failures", "why": "See eval report"}]

    return changes


def append_changelog(skill_name: str, iteration: int, before_score: float, after_score: float, changes: list[dict]) -> None:
    """Append iteration results to the eval report."""
    report_path = Path(f"output/evals/{skill_name}-report.md")
    changelog = [
        "",
        "---",
        f"## Improvement iteration {iteration} — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Score before:** {before_score:.0%} → **Score after:** {after_score:.0%}",
        "",
        "### Changes applied",
    ]
    for c in changes:
        changelog.append(f"- **{c.get('what', '')}** — {c.get('why', '')}")

    with open(report_path, "a") as f:
        f.write("\n".join(changelog) + "\n")


async def improvement_loop(
    skill_name: str,
    target_score: float = 0.85,
    max_iterations: int = 5,
) -> None:
    """
    The full improvement loop:
    1. Run evals
    2. If score >= target or max iterations reached, stop
    3. Apply improvements
    4. Repeat
    """
    print(f"Starting improvement loop for: {skill_name}")
    print(f"Target score: {target_score:.0%} | Max iterations: {max_iterations}\n")

    for iteration in range(1, max_iterations + 1):
        print(f"{'='*50}")
        print(f"ITERATION {iteration}/{max_iterations}")
        print(f"{'='*50}\n")

        # Run evals
        report = await run_evals(skill_name)
        score = report.overall_score or 0

        print(f"\nCurrent score: {score:.0%}")

        if score >= target_score:
            print(f"\n✅ Target score reached ({score:.0%} >= {target_score:.0%})")
            print(f"Skill is ready. Final report: output/evals/{skill_name}-report.md")
            return

        if iteration == max_iterations:
            print(f"\n⚠️  Max iterations reached. Final score: {score:.0%}")
            print(f"Review output/evals/{skill_name}-report.md and make manual improvements.")
            return

        print(f"\nScore {score:.0%} < target {target_score:.0%}. Applying improvements...")
        changes = await apply_improvements(skill_name, report)

        if changes:
            print(f"\nApplied {len(changes)} improvements:")
            for c in changes:
                print(f"  - {c.get('what', 'change')}")
        else:
            print("No changes applied — skill may have reached its ceiling with current test cases.")
            print("Consider: adding more specific test cases, or redesigning the skill.")
            return

        # Re-run evals to measure improvement
        print("\nRe-running evals to measure improvement...")
        new_report = await run_evals(skill_name)
        new_score = new_report.overall_score or 0

        append_changelog(skill_name, iteration, score, new_score, changes)

        improvement = new_score - score
        if improvement > 0:
            print(f"\n📈 Score improved: {score:.0%} → {new_score:.0%} (+{improvement:.0%})")
        elif improvement == 0:
            print(f"\n⚠️  Score unchanged: {score:.0%}")
            print("The improvements may not have targeted the right issues. Check the report.")
        else:
            print(f"\n⚠️  Score decreased: {score:.0%} → {new_score:.0%}")
            print("The changes may have introduced new issues. Review the skill manually.")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="Iteratively improve a skill based on eval results."
    )
    parser.add_argument("skill_name", help="Name of the skill to improve")
    parser.add_argument(
        "--target-score",
        type=float,
        default=0.85,
        metavar="FLOAT",
        help="Target pass rate (default: 0.85 = 85%%)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        metavar="N",
        help="Maximum improvement iterations (default: 5)",
    )
    parser.add_argument(
        "--improve-only",
        action="store_true",
        help="Apply one round of improvements without the full loop",
    )
    args = parser.parse_args()

    skill_path = Path(f".claude/skills/{args.skill_name}/SKILL.md")
    if not skill_path.exists():
        print(f"Error: skill not found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    if args.improve_only:
        report_path = Path(f"output/evals/{args.skill_name}-report.md")
        if not report_path.exists():
            print(f"No eval report found. Run eval_runner.py {args.skill_name} first.", file=sys.stderr)
            sys.exit(1)

        async def one_round():
            report = EvalReport(
                skill_name=args.skill_name,
                run_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            )
            changes = await apply_improvements(args.skill_name, report)
            if changes:
                print(f"Applied {len(changes)} improvements:")
                for c in changes:
                    print(f"  - {c.get('what')}")
            else:
                print("No improvements applied.")

        asyncio.run(one_round())
    else:
        asyncio.run(improvement_loop(
            args.skill_name,
            target_score=args.target_score,
            max_iterations=args.max_iterations,
        ))


if __name__ == "__main__":
    main()
