---
name: discovery-call
description: Prepare for a customer/advisor/partner conversation and capture what it taught into the knowledge base with provenance. Use when prepping a discovery call, sales call, advisor meeting, or partner conversation; when writing interview questions; or when processing notes from a call that just happened.
---

# Discovery calls — prep and capture

Conversations with customers, advisors, and partners are the highest-value
evidence a pre-launch company collects, and the most perishable. This skill has
two halves: **prep** (so the call tests something) and **capture** (so what was
learned survives). The human makes the call — agents never contact anyone.

## Prep

1. **Name the riskiest assumption this call can test.** One sentence: the belief
   that, if wrong, most changes the plan ("repair ISOs will pay ~$10k for
   quantitative testing", "PMs will hand our spec to a fabricator"). The call is
   an experiment on that assumption; everything else is bonus.

2. **Write the persona sheet:** who they are, what they already know and don't,
   what they're likely to want from the conversation, and anything the brain
   already holds about them or their segment (cite it). Pull from
   `brain/people/` and `brain/knowledge/customers/` first — walking in ignorant
   of your own notes is the amateur tell.

3. **Draft questions that elicit evidence, not politeness:**
   - Past behavior over hypotheticals: "when did you last X, what did it cost"
     beats "would you use a tool that…"
   - Numbers with units: budgets, frequencies, cycle times, team sizes.
   - The disconfirming question — the one whose answer could kill the idea. If
     no question could change the plan, the call is a demo, not discovery.
   - End-of-call asks: who else should we talk to; what would make this a no.

4. **Define what would change the plan.** Before the call, write down: "if we
   hear X, we do Y." This is what makes the capture step meaningful.

## Capture (same day — memory decays fast)

1. **Record into the brain with provenance:** the person to `brain/people/`
   (role, context, stance, follow-ups), the substance to the right
   `brain/knowledge/` file (merge into existing files per the dedup rules;
   source entry: "call with <name>, <date>"). Quote key claims verbatim rather
   than paraphrasing — "we'd pay for the report, not the box" is data; a
   paraphrase is interpretation.

2. **Mark evidentiary weight honestly.** One person said it once: that's a
   recorded observation (`confidence: inferred` territory), not validation.
   Note what was conspicuously *not* said (no price objection ≠ price
   acceptance).

3. **Boundary check.** Nothing the other party shared in confidence gets used
   beyond the note; no confidential program/customer identifiers; respect any
   "off the record." When a call mixes open and confidential, capture the open
   facts and log the exclusion.

4. **Close the loop:** update `open-questions.md` (answered ones cite the call;
   new ones added), surface any decision the call now forces (hand to
   `/decision-log` — deciding is the owner's move), add follow-up tasks to the
   task source of truth with owners, and draft any thank-you/follow-up email
   **for the owner to send**.

## Judgment

- **The call's success metric is surprise.** If nothing surprised you, the
  questions were leading or the assumption wasn't risky. Say so in the capture.
- **Never average contradictory calls into mush.** Two customers disagreeing is
  segmentation data — record both with attribution.
- **Prep scales with stakes.** A first conversation with a priority segment
  deserves the full ritual; a casual check-in gets the one-line assumption and
  three questions.
