# Test Cases: qualify-lead

These test cases run automatically with `/eval-skill qualify-lead`.
Edit them to match your ICP. Add cases for inputs you'll encounter in production.

---

## Test 1: Clear fit — B2B SaaS, Series B/C
**Input:** Retool

**Criteria:**
- [ ] Tier is HOT or WARM (Retool is B2B SaaS, Series C, ~450 employees)
- [ ] ICP Scorecard table is present with at least 4 rows
- [ ] Every scorecard row has a ✅, ⚠️, ❌, or ❓ — no empty scores
- [ ] Recommended next step is specific (names a team or role to contact)
- [ ] At least 2 source URLs are cited

---

## Test 2: Clear disqualify — consumer company
**Input:** Duolingo

**Criteria:**
- [ ] Tier is COLD or DISQUALIFIED
- [ ] Report explicitly mentions consumer focus or B2C model as a reason
- [ ] Recommended next step says to deprioritize or skip, not to book a call
- [ ] Sources cited

---

## Test 3: Borderline — well-known but above ICP size range
**Input:** Notion

**Criteria:**
- [ ] Report is produced and complete (not an error)
- [ ] Company size criterion is marked ⚠️ or ❌ (Notion has 600+ employees, above 50-500 range)
- [ ] Recommended next step acknowledges the fit limitation
- [ ] Sources cited for employee count

---

## Test 4: Limited public information
**Input:** "Runway Financial"

**Criteria:**
- [ ] Report is produced (not an error or refusal)
- [ ] Criteria that can't be verified are marked ❓, not guessed
- [ ] No employee counts or funding amounts are stated without a source
- [ ] Recommended next step is still actionable despite information gaps

---

## Test 5: Non-company input
**Input:** "Series A fundraising trends 2025"

**Criteria:**
- [ ] Output indicates the input is not a company name
- [ ] Tier is DISQUALIFIED or the skill explicitly flags the issue
- [ ] No fabricated qualification report is produced for a non-company
