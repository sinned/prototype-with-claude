# Example 4: Evals & Looping Improvement

**Pattern: Define → Test → Grade → Improve → Repeat**

How to know if your skill is actually working — and how to make it better, automatically.

## The problem

You build a skill. You run it on 3 examples. It looks okay. But how do you know it will work reliably on your real inputs? How do you find the specific failure modes? How do you systematically improve it?

The answer is evals: a structured set of test cases with quality criteria, graded by Claude itself (LLM-as-judge), used to drive iterative improvement.

## The eval loop

```
1. DEFINE  — Write test cases: input + quality criteria (what does "good" look like?)
2. RUN     — Run the skill on all test cases
3. GRADE   — Use Claude to judge each output against the criteria
4. ANALYZE — Find patterns in the failures
5. IMPROVE — Edit SKILL.md to fix the failure patterns
6. REPEAT  — Until quality meets your bar
```

## Why LLM-as-judge works

You can't write traditional unit tests for AI outputs ("assert output == expected") because outputs vary. But you can ask Claude to evaluate outputs against semantic criteria:

- "Does the output contain a clear recommendation?" → yes/no
- "Is the company size mentioned with a number?" → yes/no  
- "Is the tone professional without being stuffy?" → yes/no

Claude grades these consistently and can explain why something fails, which tells you exactly what to fix in the SKILL.md.

## How to use this in Claude Code (Phase 1)

1. Write test cases for your skill:
   ```bash
   mkdir -p .claude/skills/<skill-name>/evals
   cp examples/04-evals-and-improvement/test-cases-example.md \
      .claude/skills/<skill-name>/evals/test-cases.md
   # Edit test-cases.md with your actual inputs and criteria
   ```

2. Run evals:
   ```
   /eval-skill <skill-name>
   ```

3. Review the report in `output/evals/<skill-name>-report.md`

4. Improve the skill:
   ```
   /improve-skill <skill-name>
   ```
   Claude will edit your SKILL.md directly based on the failure patterns.

5. Repeat until your pass rate is high enough.

## How to automate (Phase 2)

See `sdk/eval_runner.py` — runs evals programmatically. See `sdk/improve.py` — the full improvement loop.

```bash
cd sdk
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt
source ../../../.env   # or: export ANTHROPIC_API_KEY=your-key

# Run evals once
python3 eval_runner.py research-agent

# Run the full improvement loop (evals → improve → repeat)
python3 improve.py research-agent --target-score 0.85 --max-iterations 5
```

## What makes a good test case

Good test cases cover:
- **Happy path** — a typical, clean input that should work easily
- **Edge cases** — tricky inputs: ambiguous names, very little public info, unusual formats
- **Adversarial** — inputs designed to break the skill: empty input, gibberish, out-of-scope requests
- **Regression** — inputs that broke the skill in a previous iteration (add these as you find them)

Aim for 10-20 test cases per skill. More than that is diminishing returns during prototyping.

## What makes a good quality criterion

Good criteria are:
- **Binary** — yes or no, not "sort of"
- **Specific** — "mentions company headcount as a number" not "includes company info"
- **Independent** — can be evaluated without knowing the "right answer"
- **Outcome-focused** — "would this help a sales rep?" not "is it well-formatted?"

Aim for 3-7 criteria per test case.
