# Test Cases: qualify-lead-demo

The SAME test cases as `qualify-lead`. This lets us measure how much the
improvement loop closes the gap between a weak first draft and a polished skill.

---

## Test 1: Clear fit — B2B SaaS, Series B/C
**Input:** Retool

**Criteria:**
- [ ] Output tier (HOT/WARM/COLD/DISQUALIFIED) is explicitly stated
- [ ] Tier is HOT or WARM (Retool is B2B SaaS, Series C, ~450 employees)
- [ ] At least 4 specific qualification criteria are addressed (size, industry, stage, signals)
- [ ] Output includes a recommended next step (specific action, not generic advice)
- [ ] At least 2 source URLs are cited

---

## Test 2: Clear disqualify — consumer company
**Input:** Duolingo

**Criteria:**
- [ ] Output tier is explicitly stated
- [ ] Tier is COLD or DISQUALIFIED
- [ ] Output explicitly identifies Duolingo as a consumer/B2C company
- [ ] Recommended next step is to deprioritize, not to book a call

---

## Test 3: Borderline — well-known but above ICP size range
**Input:** Notion

**Criteria:**
- [ ] Output tier is explicitly stated
- [ ] Output addresses company size as a qualification factor
- [ ] Output is not overconfident — acknowledges the fit limitation if any
- [ ] Sources are cited for any specific claims (headcount, funding)

---

## Test 4: Limited public information
**Input:** "Runway Financial"

**Criteria:**
- [ ] Output is produced (not an error or refusal)
- [ ] Output does NOT fabricate specific headcount or funding amounts without a source
- [ ] Output acknowledges information limitations when applicable
- [ ] Recommended next step is actionable despite information gaps
