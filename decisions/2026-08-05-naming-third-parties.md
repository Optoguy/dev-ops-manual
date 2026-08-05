# Naming third parties: the test is purpose, not category

**Date:** 2026-08-05
**Status:** adopted
**Changes:** `skills/history-capture/SKILL.md` step 5

## The instruction

The owner, 2026-08-05:

> The rule about 3rd party names is too strict. We need to be able to reference
> them. Relax it.

## What was too strict

Two things, one written and one invented.

**Written.** `history-capture/SKILL.md` step 5 said that if a period included
*"pasted customer data, personal information, or anything under an employer's
confidentiality,"* that content *"does not go in the repository at all."*
"Personal information" read literally covers naming anyone — a vendor engineer,
a competitor, a cited author.

**Invented.** The adoption prompt written for NewCoEndotest earlier the same day
escalated it further, to *"personnel matters and named third parties: same
treatment."* That was never a house rule. It was written into a prompt, and the
prompt was sent before anyone checked it against the skill.

## Why it mattered

The rule would have gutted exactly the project it was written for.
NewCoEndotest's brain is largely *about* third parties: Trioptics as an
instrument vendor, Capital Medical Resources as a competitor, PLOS and AAMI and
Lyon as citations behind claims that are load-bearing for the product's
positioning. A knowledge base that cannot name a vendor cannot record which
vendor's datasheet contradicts itself — which is a finding that repo already
holds.

**A record that cannot name the parties it is about is not a record.**

## The decision

Replace the category list with a purpose test.

**Name freely:** organisations of every kind; published work and its authors,
with the citation, because that is what a citation is; and people acting in a
professional or public capacity where what is recorded is what they said or did
in that capacity and it bears on the project.

**Still leave out**, summarizing the existence instead: contact details and
private identifiers; anything under an employer's confidentiality or a
non-disclosure agreement, which is unchanged and remains the strictest line;
customer material pasted into the chat, as distinct from the customer's name;
private facts about an identifiable person, and anything said in confidence; and
characterisations of a named person that would embarrass them if read back —
record the decision and the reasoning, not the assessment of the human.

Ambiguous cases write the finding without the name and note that a name exists.
**The finding is never dropped.**

## Consequences

- Applies wherever a project writes durable knowledge, not only to history
  capture. The brain skills inherit the same test.
- A correction is owed to the NewCoEndotest chat, which received the stricter
  wording in a prompt before this was caught.
- Fleet-wide: `skills/` changed, so each project re-installs on its own schedule.

## What this is evidence for

The failure was not the written rule alone — it was a prompt that tightened a
rule beyond what any convention said, and shipped without checking. The written
rule was vague; the prompt made it wrong. This is the fourth instance of the
2026-07-30 pattern, a rule broken or bent by whoever wrote it within hours, and
the first where the vehicle was a prompt rather than code.
