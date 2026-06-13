# Test Cases: research-agent

These test cases run automatically with `/eval-skill research-agent`.
Edit them to match the kinds of subjects you'll research in production.

---

## Test 1: Well-known company (happy path)
**Input:** Stripe

**Criteria:**
- [ ] Output is saved to `output/stripe-brief.md`
- [ ] Contains a TL;DR section
- [ ] Mentions payment processing as core business
- [ ] Includes at least one specific number (employees, revenue, valuation, or growth)
- [ ] Has at least 3 source URLs in the Sources section
- [ ] Recent Developments section mentions something from the last 12 months

---

## Test 2: Less well-known company
**Input:** Linear

**Criteria:**
- [ ] Correctly identifies Linear as a project management / issue tracking tool for software teams
- [ ] Mentions B2B SaaS or developer tools positioning
- [ ] Has at least 4 items in Key Facts
- [ ] Source URLs are included for non-obvious claims
- [ ] Brief is under 800 words (focused, not exhaustive)

---

## Test 3: Person, not company
**Input:** Patrick Collison

**Criteria:**
- [ ] Identifies him as co-founder/CEO of Stripe
- [ ] Includes at least 2 notable achievements or quotes
- [ ] Does NOT conflate him with his brother John Collison
- [ ] Includes information from the last 18 months, not just biographical background

---

## Test 4: Specific focus angle
**Input:** "Notion — focus on their enterprise strategy"

**Criteria:**
- [ ] Brief is focused on enterprise/business aspects, not a generic overview
- [ ] Mentions at least one enterprise-specific feature or initiative
- [ ] Includes competitive context (Confluence, Coda, or similar)
- [ ] Recommendation is relevant to enterprise buyers or sellers

---

## Test 5: Ambiguous input
**Input:** Apple

**Criteria:**
- [ ] Defaults to Apple Inc. (the tech company), not the fruit
- [ ] Notes the disambiguation in TL;DR or Overview
- [ ] Correctly describes their main businesses (hardware, software, services)
- [ ] Output is complete and useful despite the ambiguity

---

## Test 6: Limited public information
**Input:** "Loom before it was acquired by Atlassian"

**Criteria:**
- [ ] Accurately describes Loom's product (async video messaging)
- [ ] Mentions the Atlassian acquisition
- [ ] Does NOT fabricate specifics it can't verify
- [ ] Brief acknowledges information constraints somewhere
