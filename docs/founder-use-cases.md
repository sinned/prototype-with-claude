# Founder Use Cases

Five startup use cases you can prototype with this repo today. Each maps to one of the three skill patterns and includes a build guide, example ICP/config, and SDK deployment notes.

---

## 1. Lead Qualification

**The problem:** Your sales rep spends 20 minutes researching every inbound lead before deciding whether to respond. At 50 leads/day, that's 1,000 minutes of research that mostly results in "not a fit."

**The agent:** Research the company, score it against your ICP, return Hot/Warm/Cold/Disqualified with a scorecard and recommended next step.

**Pattern:** Score & Classify  
**Built-in skill:** `/qualify-lead <company>`  
**Full walkthrough:** [`WALKTHROUGH.md`](../WALKTHROUGH.md)

**Customize it:**
- Edit `icp.md` to match your actual criteria (company size, industry, stage, signals)
- Add company-specific signals (e.g., "uses Salesforce" or "engineering team > 10")
- Adjust the tier thresholds (what counts as Hot for you?)

**SDK deployment:**
```bash
# Process overnight from CRM export
python examples/02-lead-qualifier/sdk/agent.py --batch crm-export.csv --output qualified.csv

# Webhook trigger (FastAPI)
@app.post("/qualify")
async def qualify_lead(body: dict):
    return await qualify(body["company"], load_icp())
```

**What founders report:** Cuts lead research time from 20 minutes to 2 minutes per lead. Reps review the report and decide in seconds. False positive rate drops because the criteria are explicit and consistent.

---

## 2. Customer Research

**The problem:** Before a customer call, your team does scattered research — LinkedIn, Crunchbase, news, their product — and still walks in without a coherent picture. Important signals get missed.

**The agent:** Input a company name. The agent searches their website, recent news, LinkedIn, Crunchbase, and job postings. Produces a structured pre-call brief in under 3 minutes.

**Pattern:** Research & Synthesize  
**Built-in skill:** `/research-agent <company>`

**Customize it:**
Create `.claude/skills/research-agent/SKILL.md` with your specific research priorities. For enterprise sales, you might want: deal size signals, tech stack, org chart hints, recent executive hires. For VC: traction signals, team background, competitive positioning.

**Example ICP for sales research:**
```markdown
# Research priorities for pre-call briefs

## Always include
- Company overview and primary product
- Headcount and recent growth rate
- Recent funding or financial news
- Current open roles (especially in engineering, product, sales)
- Any recent product launches or announcements

## Include if available
- Key executive names and LinkedIn profiles
- Tech stack signals (Stackshare, job postings mentioning tools)
- Customer logos or case studies on their site
- G2 or Capterra reviews mentioning pain points
```

**SDK deployment:**
```bash
# Run before every call booked in the next 24 hours (cron job)
python examples/01-research-agent/sdk/agent.py --batch upcoming-calls.csv

# Integrate with calendar: Zapier/Make webhook → agent → Notion/Slack summary
```

**What founders report:** Reps show up to calls knowing the company's recent funding round, their latest product update, and 3 relevant talking points. Win rates improve not because the agent is smarter than a rep — it's because reps who know the context are consistently better than reps who don't.

---

## 3. Support Triage

**The problem:** Support tickets come in at all hours. Most can be answered with existing docs. A few are critical bugs or churn risks. Your team treats them all the same.

**The agent:** Classify each ticket into a tier (Critical / High / Normal / Low) and route it. Identify whether it's a bug, a feature request, a docs gap, or a billing issue. Draft a first response for common categories.

**Pattern:** Score & Classify  
**Start from:** `examples/02-lead-qualifier/SKILL.md` (adapt the scoring rubric)

**Build it:**

1. Copy the lead qualifier skill:
   ```bash
   mkdir -p .claude/skills/triage-ticket
   cp examples/02-lead-qualifier/SKILL.md .claude/skills/triage-ticket/SKILL.md
   ```

2. Replace the ICP criteria with your triage rubric. Edit `.claude/skills/triage-ticket/SKILL.md`:

```markdown
---
name: triage-ticket
description: Classify a support ticket by priority and category. Returns tier, category, and a draft first response.
---

## Triage rubric (define in triage-rules.md or use defaults below)

### Priority tiers
- CRITICAL: data loss, security issue, complete product unavailability
- HIGH: core feature broken for the customer, churn risk signal in message
- NORMAL: partial functionality issue, workaround exists
- LOW: feature request, docs question, cosmetic issue

### Categories
- Bug: something that used to work doesn't work
- Feature request: customer wants something new
- Docs gap: customer is confused by existing behavior
- Billing: payment, plan, or invoice issue
- Churn risk: tone signals frustration or threat to cancel
```

3. Test with real anonymized tickets:
   ```
   /triage-ticket "We can't export our data. This is blocking our end-of-month reporting. URGENT."
   /triage-ticket "Would love a dark mode option"
   ```

**SDK deployment:**
```bash
# Process Zendesk/Intercom export in batch
python sdk/agent.py --batch open-tickets.csv --output triage-results.csv

# Real-time: webhook from Zendesk → agent → update ticket priority + add internal note
```

**What founders report:** Reduces time-to-first-response on critical tickets from 4 hours to 15 minutes. Support team starts their day with a sorted queue instead of 50 unread tickets.

---

## 4. Content Generation

**The problem:** Marketing needs 20 LinkedIn posts, 5 cold email sequences, and a product launch email — all due this week. Writing variations is time-consuming. Quality is inconsistent across writers.

**The agent:** Input a brief. The agent researches the topic if needed, then produces 3 variations with distinct angles (story-led, data-driven, contrarian) plus a recommendation for which to use.

**Pattern:** Generate & Iterate  
**Built-in skill:** `/generate-content "<brief>"`

**Example briefs:**
```
/generate-content "cold email for a sales enablement tool, target: VP Sales at Series B SaaS, tone: direct and specific"
/generate-content "LinkedIn post about our product launch — async video messaging for remote teams"
/generate-content "blog post intro: why most sales dashboards are lying to you"
```

**Customize it:**
Create `brand-voice.md` (see `examples/03-content-generator/brand-voice-example.md`). The skill reads it automatically. Include:
- Tone and voice characteristics
- Words and phrases to avoid
- Channel-specific length rules
- 2-3 examples of on-brand vs. off-brand copy

**SDK deployment:**
```bash
# Generate content calendar: 20 posts from a topics CSV
python examples/03-content-generator/sdk/agent.py --batch content-calendar.csv

# Nightly: generate drafts for next week's pipeline → post to Notion for review
```

**What founders report:** Cuts first-draft time by 70%. The 3-variation format forces the team to actually choose an angle rather than defaulting to the same style every time. Brand voice consistency improves when the criteria are written down.

---

## 5. Product Feedback Synthesis

**The problem:** User feedback lives in Intercom, NPS surveys, G2 reviews, Slack conversations, and customer calls. Nobody has time to read all of it. Important signals get lost.

**The agent:** Input a batch of raw feedback (or a URL to pull it from). The agent reads everything, identifies the top themes, quantifies how often each theme appears, highlights the most representative quotes, and flags any urgent signals (churn risk, security concerns, broken features).

**Pattern:** Research & Synthesize (with a batch input variant)  
**Start from:** `examples/01-research-agent/SKILL.md` (adapt for text analysis instead of web search)

**Build it:**

1. Create the skill:
   ```bash
   /new-skill
   # Describe: "Read a batch of customer feedback and produce a synthesis report"
   ```

2. The skill should:
   - Read feedback from a file (CSV, JSON, or plain text dump)
   - Identify the top 5-7 themes with counts
   - Quote the 2-3 most representative examples per theme
   - Flag urgent signals separately
   - Recommend the top 3 product priorities based on frequency and severity

3. Test with a sample:
   Create `feedback-sample.txt` with 20-30 anonymized feedback snippets. Run:
   ```
   /synthesize-feedback feedback-sample.txt
   ```

**Example output structure:**
```markdown
# Product Feedback Synthesis
*Analyzed: 147 responses | Period: May 2025*

## Top themes
1. **Slow export performance** (34 mentions, 23%) — "Export takes 10+ minutes for large datasets"
2. **Missing Slack integration** (28 mentions, 19%) — "Would save us an hour a day"
3. **Confusing onboarding** (21 mentions, 14%) — "Took me 3 days to figure out the basics"

## Urgent signals
- 4 customers mentioned considering switching to [competitor] — all cited export speed
- 1 potential security concern: [quote]

## Recommended priorities
1. Export performance — highest frequency, strongest churn signal
2. Slack integration — high frequency, low complexity based on similar integrations
3. Onboarding flow — affects new customer success metrics
```

**SDK deployment:**
```bash
# Weekly synthesis from Intercom export
python sdk/agent.py --input feedback-export.csv --output synthesis-report.md

# Monthly: pull from multiple sources, synthesize, post summary to Slack
```

**What founders report:** Product teams go from "we sort of know what customers want" to "we have a ranked, evidence-backed priority list every week." The quotes section is the most useful part — it gives product and engineering the language customers actually use.

---

## Picking your first use case

If you're not sure where to start:

- **Sales team with > 10 inbound leads/day** → Lead Qualification
- **Customer-facing team doing research before meetings** → Customer Research
- **Support team with > 20 tickets/day** → Support Triage
- **Marketing team producing more than 5 pieces/week** → Content Generation
- **Product team with an NPS score and no time to read the comments** → Feedback Synthesis

Run the built-in skill first (`/qualify-lead`, `/research-agent`, `/generate-content`). See if the output format is close to useful. Then run `/new-skill` to build the variant you actually need.
