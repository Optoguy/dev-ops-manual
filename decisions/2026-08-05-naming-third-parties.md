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

**Widened further the same day, same decision, before merge.** The owner, asked
whether to also allow private facts and characterisations where they bear on a
decision: *"2,3"* — merge, and widen. So a private fact or a characterisation of
a named person's conduct **is** recordable when it was the actual cause of a
decision the project made, written as the fact or the conduct, not as judgment
of the person: *"the integration stalled after [name] left the company"* is the
record; *"[name] is unreliable"* is not. The test is whether the fact is
something you would cite in the decision's own reasoning — if not, it does not
belong in the digest either.

**Still leave out, no exception:** contact details and private identifiers;
anything under an employer's confidentiality or a non-disclosure agreement —
load-bearing-to-a-decision does not override this; customer material pasted
into the chat, as distinct from the customer's name; health information unless
the person disclosed it publicly themselves; and anything said in confidence,
regardless of relevance to a decision — a private fact volunteered off the
record is not "load-bearing," it is confidential, full stop.

Ambiguous cases write the finding without the name and note that a name exists.
**The finding is never dropped.**

## Amendment, same day — customers and prospects, and calls are not confidential by default

The owner, on reviewing the claims-discipline pull request:

> I also want to allow for naming customers and potential customers. I don't
> think there should be a hard 3rd party limitation.

Two changes, and the second is the one that mattered.

**Customers and prospects are named explicitly**, as organisations and as the
people at them — including what they said in a discovery call, a sales call or a
meeting. The original wording said "customers as companies," which permitted the
company and left the buyer contact ambiguous.

**A business conversation is not "said in confidence."** The original exclusion —
*"anything said to you in confidence, regardless of relevance"* — read as though a
private setting made a conversation confidential. That would have contradicted
[`/discovery-call`](../skills/discovery-call/SKILL.md), which **mandates** naming
the person, quoting them verbatim, and sourcing the note as
*"call with `<name>`, `<date>`."* Two skills would have given opposite
instructions about the single most valuable knowledge a project acquires.

`/discovery-call` was written first and was already correctly calibrated:
confidence is something the other party **declares** — an explicit "off the
record," an agreement, a confidential identifier — and a call mixing open and
closed material is captured in its open part rather than dropped. That skill is
now named as the authority when the two are read together.

**The framing changed too.** The rule now opens by stating there is no blanket
restriction on naming a third party: the exclusions are a short specific list, and
anything not on it may be named. The previous shape invited a reader to ask "am I
allowed to name this," which is the wrong question and the one that produced the
over-strict prompt in the first place.

### Second amendment, same day — customer names in public material

The owner, asked whether naming a customer in *public* material should also be
pre-authorized rather than referred to him as a permission question: **yes.**

An agent may draft a landing page, case study, post or deck that names a customer
and quotes them, without stopping to ask. The instruction behind it: a draft
watered down to *"a leading manufacturer"* has lost the thing that made it
persuasive, and asking permission mid-draft moves work back onto the owner for no
gain.

**What does not change, and is why this is safe:** agents never publish. Every
outward-facing draft reaches the owner before it goes anywhere, and pressing send
is where any contractual permission to use a customer's name is honoured. The
gate was already there for every outward artefact; this amendment removes a
redundant second gate in front of it, not the real one.

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
