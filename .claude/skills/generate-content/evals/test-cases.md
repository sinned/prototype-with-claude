# Test Cases: generate-content

These test cases run automatically with `/eval-skill generate-content`.
Edit them to match the kinds of briefs you'll run in production.

---

## Test 1: Cold email (typical brief)
**Input:** "cold email for a sales productivity tool, target: VP Sales at Series B SaaS, tone: direct"

**Criteria:**
- [ ] Three variation files are produced in `output/content/<slug>/`
- [ ] Each variation has a subject line and body
- [ ] Each variation is under 150 words
- [ ] Each variation has a clear CTA
- [ ] brief-summary.md is produced with a comparison table and recommendation
- [ ] No variation uses banned phrases ("leverage" as a verb, "utilize", "cutting-edge", "we are excited to")

---

## Test 2: LinkedIn post
**Input:** "LinkedIn post: why most sales dashboards are lying to you"

**Criteria:**
- [ ] Three variations produced
- [ ] Each variation's first line works as a standalone hook (no "see more" cliffhanger)
- [ ] Posts are between 100 and 300 words each
- [ ] Variations represent distinct angles (not just word-swapped versions of each other)
- [ ] brief-summary.md identifies which angle to use and why

---

## Test 3: Blog post intro
**Input:** "blog post intro about async work, target audience: engineering managers"

**Criteria:**
- [ ] Three variations produced
- [ ] Each variation is 100-250 words (intro length)
- [ ] Each variation states a clear opinion or thesis, not just a topic overview
- [ ] Tone matches "engineering manager" audience (specific, not fluffy)

---

## Test 4: Vague brief (resilience test)
**Input:** "something about AI"

**Criteria:**
- [ ] Three variations are still produced
- [ ] brief-summary.md explicitly states the assumptions made
- [ ] Output is concrete enough to be useful, not generic filler
- [ ] Variations make different assumption choices (e.g., different formats or audiences)

---

## Test 5: Word-count constraint
**Input:** "tweet (under 280 chars) announcing our Series A"

**Criteria:**
- [ ] Three variations produced
- [ ] Every variation is under 280 characters (not words)
- [ ] Each variation includes the core fact (Series A announcement)
- [ ] Variations differ in angle (announcement-led, customer-led, vision-led, etc.)
