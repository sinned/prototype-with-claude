# Test Cases: &lt;your-skill-name&gt;

**This is a template.** Copy it to `.claude/skills/<your-skill-name>/evals/test-cases.md`
and replace the title and cases below with cases for your skill.

The sample cases below are for `research-agent` (already installed in this repo as
`.claude/skills/research-agent/evals/test-cases.md`). Use them as a structural reference,
then write your own.

Each test case has:
- `input`: what you pass to the skill
- `criteria`: a list of yes/no quality checks

---

## Test 1: Well-known company (happy path)
**Input:** Stripe

**Criteria:**
- [ ] Output is saved to `output/stripe-brief.md`
- [ ] Contains a TL;DR section
- [ ] Mentions payment processing as core business
- [ ] Includes at least one specific number (employees, revenue, valuation, or growth figure)
- [ ] Has at least 3 source URLs
- [ ] Recent developments section exists and mentions something from the last 12 months

---

## Test 2: Less well-known company
**Input:** Linear

**Criteria:**
- [ ] Correctly identifies Linear as a project management / issue tracking tool
- [ ] Mentions that it's used by software teams or engineers
- [ ] Has at least 4 key facts
- [ ] Source URLs are included
- [ ] Output is under 800 words (brief, not exhaustive)

---

## Test 3: Person, not company
**Input:** "Patrick Collison"

**Criteria:**
- [ ] Identifies him as co-founder/CEO of Stripe
- [ ] Includes at least 2 notable personal achievements or quotes
- [ ] Does not confuse him with his brother John Collison
- [ ] Has recent information (not just background/Wikipedia facts)

---

## Test 4: Specific focus angle
**Input:** "Notion — focus on their enterprise strategy"

**Criteria:**
- [ ] Brief is clearly focused on enterprise/business aspects, not general overview
- [ ] Mentions at least one enterprise-specific feature or initiative
- [ ] Includes competitive context (e.g., comparison to Confluence, Coda)
- [ ] Has a clear recommendation relevant to enterprise buyers/sellers

---

## Test 5: Topic (not a company or person)
**Input:** "AI agents market 2025"

**Criteria:**
- [ ] Synthesizes multiple sources, not just one
- [ ] Includes at least 3 concrete data points or statistics
- [ ] Covers both established players and emerging trends
- [ ] Key Facts section has 5 items
- [ ] Does NOT fabricate specific statistics — citations provided for numbers

---

## Test 6: Ambiguous input
**Input:** "Apple"

**Criteria:**
- [ ] Defaults to Apple Inc. (the tech company), not apple the fruit
- [ ] Notes the assumption in the TL;DR or Overview
- [ ] Correctly describes their main business (hardware, software, services)
- [ ] Output is still complete and useful despite the ambiguity

---

## Test 7: Very obscure subject (limited info available)
**Input:** "Loom before it was acquired by Atlassian"

**Criteria:**
- [ ] Acknowledges that some information may be limited or historical
- [ ] Accurately describes Loom's core product (async video messaging)
- [ ] Mentions the Atlassian acquisition
- [ ] Does NOT make up information it can't verify
- [ ] Brief is still useful despite information constraints

---

## Adding your own test cases

Add test cases that match your actual use patterns. Focus on:
- Inputs you actually plan to run in production
- Edge cases you've already encountered
- Cases where previous versions of the skill failed

When the skill fails a test case, fix SKILL.md and add the case to your regression suite.
