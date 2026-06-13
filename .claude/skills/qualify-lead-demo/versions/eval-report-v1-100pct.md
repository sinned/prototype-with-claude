# Eval Report: qualify-lead-demo
*Run: 2026-06-12 23:39 | Score: 100% overall*

## Summary
**Overall score: 100%**

| Test case | Score | Status |
|-----------|-------|--------|
| Test 1: Clear fit — B2B SaaS, Series B/C | 100% (5/5) | ✅ |
| Test 2: Clear disqualify — consumer company | 100% (4/4) | ✅ |
| Test 3: Borderline — well-known but above ICP size range | 100% (4/4) | ✅ |
| Test 4: Limited public information | 100% (4/4) | ✅ |

## Failure Patterns

No significant failure patterns found.

## Recommendations

- All criteria passed — no improvements needed.

## Test Case Details

### Test 1: Clear fit — B2B SaaS, Series B/C
**Input:** Retool  
**Score:** 5/5 criteria

| Criterion | Result | Notes |
|-----------|--------|-------|
| Output tier (HOT/WARM/COLD/DISQUALIFIED) is explicitly stated | ✅ | The first line reads "Tier: HOT," stating the tier explicitly and up front. |
| Tier is HOT or WARM (Retool is B2B SaaS, Series C, ~450 employees) | ✅ | The agent assigned HOT, correctly matching Retool's B2B SaaS model, Series C stage, and ~466 headcount. |
| At least 4 specific qualification criteria are addressed (size, industry, stage, signals) | ✅ | It addresses business model/industry (B2B SaaS developer platform), stage (Series C), size (~466 employees within ~20–500 range), and buying signals (headcount growth + ~68 sales reps). |
| Output includes a recommended next step (specific action, not generic advice) | ✅ | It specifies an AE emailing the VP/Head of Engineering for a 30-min discovery call, with an SDR verifying the buyer on LinkedIn first — concrete owner, channel, and action. |
| At least 2 source URLs are cited | ✅ | Multiple URLs are cited including GetLatka, Tracxn, Salestools, and FinancialContent links. |

### Test 2: Clear disqualify — consumer company
**Input:** Duolingo  
**Score:** 4/4 criteria

| Criterion | Result | Notes |
|-----------|--------|-------|
| Output tier is explicitly stated | ✅ | The output opens with "Tier: DISQUALIFIED" and the file header states "Tier: DISQUALIFIED," making the tier explicit. |
| Tier is COLD or DISQUALIFIED | ✅ | The assigned tier is DISQUALIFIED, which is one of the two acceptable values. |
| Output explicitly identifies Duolingo as a consumer/B2C company | ✅ | Both the inline response ("consumer-facing (B2C) language-learning app") and the file ("Primarily B2C gamified language-learning app") explicitly label it B2C. |
| Recommended next step is to deprioritize, not to book a call | ✅ | The recommended next step is "Deprioritize — do not route to an AE," with no suggestion to book a call. |

### Test 3: Borderline — well-known but above ICP size range
**Input:** Notion  
**Score:** 4/4 criteria

| Criterion | Result | Notes |
|-----------|--------|-------|
| Output tier is explicitly stated | ✅ | The output states "Tier: COLD" explicitly both inline and at the top of the saved file. |
| Output addresses company size as a qualification factor | ✅ | The reasoning directly cites ~1,000–1,200 employees against the ~20–500 target range and ~$11B valuation against the Seed–Series C target, making size the decisive factor. |
| Output is not overconfident — acknowledges the fit limitation if any | ✅ | It explicitly flags the conflicting headcount sources, calls it "tangential fit at best," and recommends a rep verify FTE count before any outreach rather than asserting certainty. |
| Sources are cited for any specific claims (headcount, funding) | ✅ | Headcount (SQ Magazine), funding/$275M Series C (Crunchbase), valuation (PitchBook), and ARR (getLatka) all carry inline source attributions plus a dedicated Sources section with links. |

### Test 4: Limited public information
**Input:** "Runway Financial"  
**Score:** 4/4 criteria

| Criterion | Result | Notes |
|-----------|--------|-------|
| Output is produced (not an error or refusal) | ✅ | A complete tiered lead assessment (Tier, Reasoning, Next step, Sources) was emitted inline, not an error or refusal. |
| Output does NOT fabricate specific headcount or funding amounts without a source | ✅ | Both the ~26 headcount (Crunchbase/Tracxn) and the $33.5M total / $27.5M Series A funding (TechCrunch/Crunchbase) figures carry explicit inline source citations. |
| Output acknowledges information limitations when applicable | ✅ | It flags conflicting funding figures ($47.5M vs $33.5M), labels headcount as aggregator-sourced and needing verification, and notes the "Runway ML" name-collision risk. |
| Recommended next step is actionable despite information gaps | ✅ | It specifies a concrete owner (SDR), target (Head of GTM/Operations or the hiring manager), channel (LinkedIn/email), and goal (book a 30-min discovery call), plus verifying headcount on the call. |
