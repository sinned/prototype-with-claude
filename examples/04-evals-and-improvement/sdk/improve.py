"""
Skill Improvement Loop — Agent SDK version
Migrated from: .claude/commands/improve-skill.md

Reads eval results, uses Claude to rewrite SKILL.md to fix failures,
verifies the file actually changed, and reruns evals until the target score is reached.
"""

import asyncio
import argparse
import hashlib
import sys
from datetime import datetime
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions

from eval_runner import run_evals, EvalReport


IMPROVEMENT_PROMPT = """
You are improving an AI agent skill based on eval failures. The skill is defined in a SKILL.md file.

SKILL FILE PATH: {skill_path}

CURRENT SKILL.md CONTENT:
```markdown
{skill_content}
```

EVAL REPORT (showing where the skill fails):
{eval_report}

YOUR TASK:
1. Use the **Read tool** to load the current {skill_path} (the SDK safety check requires a Read before Write on existing files).
2. Analyze the failure patterns and recommendations in the eval report above.
3. Identify the 2-3 most impactful changes to make to SKILL.md.
4. Use the **Write tool** to overwrite {skill_path} with the COMPLETE updated SKILL.md.
   - Preserve the YAML frontmatter (--- name: ... description: ... ---)
   - Preserve sections that are working correctly
   - Make surgical changes to fix the identified failures
5. After calling Write, output a JSON summary of changes.

EDITING RULES:
- Make instructions more specific, not vague ("search for X and Y" beats "research the company")
- Add explicit handling for failure cases ("If you cannot find headcount data, mark the criterion ❓ — do NOT estimate")
- If a required output element is being skipped, add "REQUIRED:" or "IMPORTANT:" labels
- Add concrete examples when a quality bar is hard to describe in the abstract
- Every change must fix a specific failure pattern from the report — no fluff
- Do NOT remove content that's working

CRITICAL: You MUST call the Write tool to actually update the file. Do not just describe what you would change.

After Write completes, end your response with this JSON summary (and nothing after it):
{{
  "changes": [
    {{"what": "concrete description of what was changed", "why": "which failure pattern from the report this fixes"}}
  ]
}}
"""


def hash_file(path: Path) -> str:
    """Return a short hash of a file's contents, or empty string if missing."""
    if not path.exists():
        return ""
    return hashlib.md5(path.read_bytes()).hexdigest()


def save_version(skill_name: str, label: str) -> Path | None:
    """Save a snapshot of SKILL.md to versions/SKILL-<label>.md. Returns the saved path."""
    skill_path = Path(f".claude/skills/{skill_name}/SKILL.md")
    if not skill_path.exists():
        return None
    versions_dir = Path(f".claude/skills/{skill_name}/versions")
    versions_dir.mkdir(parents=True, exist_ok=True)
    out_path = versions_dir / f"SKILL-{label}.md"
    out_path.write_text(skill_path.read_text())
    return out_path


async def apply_improvements(skill_name: str, report: EvalReport) -> tuple[list[dict], bool]:
    """
    Use Claude to rewrite SKILL.md based on eval failures.
    Returns (changes, file_actually_changed).
    """
    skill_path = Path(f".claude/skills/{skill_name}/SKILL.md")
    report_path = Path(f"output/evals/{skill_name}-report.md")

    skill_content = skill_path.read_text()
    report_content = report_path.read_text() if report_path.exists() else "(no report found)"

    hash_before = hash_file(skill_path)

    prompt = IMPROVEMENT_PROMPT.format(
        skill_path=str(skill_path),
        skill_content=skill_content,
        eval_report=report_content,
    )

    result_text = None
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit"],
            # bypassPermissions is needed here because we're writing to .claude/skills/
            # (a sensitive directory). The script's purpose is to edit SKILL.md files,
            # so bypassing permission prompts for this specific call is correct.
            permission_mode="bypassPermissions",
        ),
    ):
        if hasattr(message, "result"):
            result_text = message.result

    hash_after = hash_file(skill_path)
    file_changed = hash_before != hash_after

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
            pass

    # If the file changed but we couldn't parse a structured summary, still report success
    if file_changed and not changes:
        changes = [{"what": "Updated SKILL.md based on eval failures", "why": "See eval report for failure patterns"}]

    return changes, file_changed


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
    save_versions: bool = False,
) -> None:
    """
    The full improvement loop:
    1. Save v0 of SKILL.md (if save_versions)
    2. Run evals → measure score
    3. If score >= target or max iterations reached, stop
    4. Apply improvements → save vN of SKILL.md (if save_versions)
    5. Re-run evals → measure improvement
    6. Repeat
    """
    print(f"Starting improvement loop for: {skill_name}")
    print(f"Target score: {target_score:.0%} | Max iterations: {max_iterations}")
    if save_versions:
        print(f"Saving versions to .claude/skills/{skill_name}/versions/")
    print()

    # Save the starting version (v0) for the journey
    if save_versions:
        v0_path = save_version(skill_name, "v0-initial")
        if v0_path:
            print(f"📸 Saved initial version: {v0_path}\n")

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
            if save_versions:
                print(f"Version history: .claude/skills/{skill_name}/versions/")
            return

        if iteration == max_iterations:
            print(f"\n⚠️  Max iterations reached. Final score: {score:.0%}")
            print(f"Review output/evals/{skill_name}-report.md and make manual improvements.")
            return

        print(f"\nScore {score:.0%} < target {target_score:.0%}. Applying improvements...")
        changes, file_changed = await apply_improvements(skill_name, report)

        if not file_changed:
            print("\n⚠️  No changes were written to SKILL.md.")
            print("Possible causes: Claude described changes without using Write, or the skill is already at its ceiling.")
            print("Try editing SKILL.md manually based on the report, then re-running.")
            return

        print(f"\nApplied {len(changes)} improvement(s):")
        for c in changes:
            print(f"  - {c.get('what', 'change')}")

        # Save the version after this iteration's improvements
        if save_versions:
            vN_path = save_version(skill_name, f"v{iteration}-after-improve")
            if vN_path:
                print(f"📸 Saved iteration version: {vN_path}")

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
    parser.add_argument(
        "--save-versions",
        action="store_true",
        help="Save a snapshot of SKILL.md before each iteration to .claude/skills/<name>/versions/. "
             "Useful for showing the improvement journey in demos. (In normal use, rely on git history.)",
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
            if args.save_versions:
                v0 = save_version(args.skill_name, f"before-improve-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
                if v0:
                    print(f"📸 Saved pre-improvement snapshot: {v0}")
            report = EvalReport(
                skill_name=args.skill_name,
                run_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            )
            changes, file_changed = await apply_improvements(args.skill_name, report)
            if not file_changed:
                print("⚠️  No changes were written to SKILL.md. (Claude may have described changes without using Write.)")
                sys.exit(2)
            print(f"Applied {len(changes)} improvement(s):")
            for c in changes:
                print(f"  - {c.get('what')}")
            if args.save_versions:
                vN = save_version(args.skill_name, f"after-improve-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
                if vN:
                    print(f"📸 Saved post-improvement snapshot: {vN}")

        asyncio.run(one_round())
    else:
        asyncio.run(improvement_loop(
            args.skill_name,
            target_score=args.target_score,
            max_iterations=args.max_iterations,
            save_versions=args.save_versions,
        ))


if __name__ == "__main__":
    main()
