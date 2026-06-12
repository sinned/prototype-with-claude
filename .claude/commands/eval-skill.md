You are running evals on a Claude Code skill to measure its quality and find failure modes.

## Your task

**If the user provided a skill name in their command input, use that. Otherwise list available skills and ask which to evaluate.**

## Steps

### 1. Set up

Find and read:
- The skill: `.claude/skills/<skill-name>/SKILL.md`
- Test cases: `.claude/skills/<skill-name>/evals/test-cases.md`

If `test-cases.md` doesn't exist, tell the founder to create it using `examples/04-evals-and-improvement/test-cases-example.md` as a template. Stop here.

### 2. Run each test case

For each test case in `test-cases.md`:

1. Read the input and criteria
2. **Run the skill** — invoke the skill's actual steps on the test input (search, fetch, write — do the real job)
3. **Grade the output** — check each criterion: ✅ pass or ❌ fail, with a one-line explanation

Be honest in grading. If a criterion is borderline, mark it ❌ and explain why.

### 3. Calculate scores

For each test case:
- Score = (criteria passed / total criteria) × 100%

Overall skill score:
- Score = (total criteria passed / total criteria across all tests) × 100%

### 4. Identify failure patterns

Group failures by type:
- **Missing content** — the output is missing required sections or information
- **Wrong format** — output structure doesn't match what's specified
- **Tool failure** — search returned nothing, URL was inaccessible
- **Instruction not followed** — Claude did something other than what the step said
- **Quality too low** — technically followed instructions but result isn't good enough

### 5. Write the eval report

Save to `output/evals/<skill-name>-report.md`:

```markdown
# Eval Report: <skill-name>
*Run: [date] | Score: [X]% ([N passed] / [M total criteria])*

## Summary
**Overall score: X%** — [Pass/Needs improvement/Failing]

| Test case | Score | Status |
|-----------|-------|--------|
| [name] | X% | ✅/⚠️/❌ |

## Failures

### [Failure pattern 1]
Affects: [test cases N, M]
Root cause: [what's wrong in the skill instructions]
Example: [specific failure instance]

### [Failure pattern 2]
...

## Recommendations
1. [Specific change to make in SKILL.md to fix failure pattern 1]
2. [Specific change to make in SKILL.md to fix failure pattern 2]

## Test case details

### Test: [name]
Input: [input]
Score: [X/Y criteria]

| Criterion | Result | Notes |
|-----------|--------|-------|
| [criterion] | ✅/❌ | [explanation] |
```

### 6. Report to the founder

Print:
- Overall score
- Top 2-3 failure patterns
- Whether to run `/improve-skill <skill-name>` next (recommended if score < 80%)

## Grading principles

- Grade against the criterion as written, not against your own judgment of what's "good"
- If a criterion is ambiguous, note the ambiguity in your grading notes
- Don't give partial credit — each criterion is pass or fail
- If the skill crashes or produces no output on a test case, all criteria for that test fail
