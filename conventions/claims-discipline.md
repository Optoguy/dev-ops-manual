# Claims discipline — what you may say about a named competitor

Added 2026-08-05. Adopted from NewCoEndotest, which wrote these rules for itself
in `brain/knowledge/strategy/competitive-positioning.md` under the heading
*"Messaging discipline (the load-bearing part)."* Generalized here; the examples
below are theirs.

Binds every project, this one included.

## Why this exists, and why now

The [2026-08-05 naming decision](../decisions/2026-08-05-naming-third-parties.md)
made it legitimate to **name** a competitor in a project's own records. This
governs **what may then be said about them** in anything outward-facing.

[`/verify`](../skills/verify/SKILL.md) checks a claim *after* it is written.
Nothing checked one *before*. That is the gap: a competitive claim that a rival's
own published material refutes is not a research failure discovered late — it is
a composition failure that should never have been written.

The rules were not reasoned out in advance. Each is the residue of a proposed
position that a competitor's own homepage or datasheet demolished.

## The rules

**1. Name the axis you lose on, inside the rule.**

> *"Against the production benches: win on price, portability, and target
> customer — **never on measurement superiority**. They are rigorous; claiming to
> out-measure them is false and will be seen through."*

The discipline is not modesty. It is that a **written** rule names the dimension
where a named competitor is genuinely better, so no future draft — by a different
person, months later — quietly claims it. A positioning file that lists only your
strengths has done half the job.

**2. Never claim a differentiator the competitor demonstrably already has.**

> *"Don't claim 'we trend results' as a differentiator. ScopeControl already does
> per-scope longitudinal trending. The defensible claim is **what** is trended."*

The test is public evidence, not impression. If their product page shows it, it
is not a differentiator, and the honest move is to sharpen the claim rather than
drop the subject.

**3. A category shift stops being a differentiator once a competitor markets it.**

A rival's own headline was *"5× more accurate than humans"* — the same shift the
project was selling as its distinguishing idea. The rule: use a category argument
to establish **why the category matters** with a customer, never as the reason to
choose you over an incumbent inside it.

**4. Scale the claim to the specific opponent.**

One competitor is 470 kg and floor-standing, so portability is a headline against
them. Another is benchtop, so against that one you lead with rigor and price
instead. **The same true sentence is strong against one rival and embarrassing
against another.** A claim written once and reused against everyone will be wrong
against someone.

**5. Never attack a competitor's moat.** Turnkey workflow is one rival's;
rigor-at-any-cost is another's. Both are losing games — and a project that picks
those fights is telling its customer to compare on the axis it loses.

## Scope

Anything outward-facing: landing pages, pitch lines, discovery scripts,
specification sheets, posts drafted for the owner, investor material. It does not
govern internal analysis — a private file may say plainly that a competitor is
better, and should.

**This is not a naming restriction, and nothing here limits naming a third
party.** Name customers, prospective customers, partners, vendors and competitors
freely, in records and in outward-facing material alike; see the
[naming decision](../decisions/2026-08-05-naming-third-parties.md). What this
convention governs is narrower: **claims of superiority over a named competitor.**

Two things it deliberately does not touch:

- **Customers and prospects.** Naming them, recording what they asked for, and
  quoting them is encouraged — that is
  [`/discovery-call`](../skills/discovery-call/SKILL.md)'s whole purpose. This
  extends to **public material**: an agent may draft a landing page, a case
  study, a post or a deck that names a customer and quotes them, without
  stopping to ask. Do not water a draft down to "a leading manufacturer" when
  the name is what makes it persuasive.

  The one thing that does not change: **agents never publish.** Every outward
  draft goes to the owner, and pressing send is where any contractual permission
  to use a customer's name is honoured. That gate already exists for every
  outward-facing artefact, so it needs no extra step here — but write the draft
  knowing a human, not the agent, carries that obligation.
- **Neutral factual comparison.** "Their instrument is 470 kg; ours is 4 kg" is a
  fact, and stating it is fine. This convention starts where the claim becomes
  *better than*.

## The check, and its known weakness

**There is no good mechanical check for this, and pretending otherwise would be
worse than admitting it.** This is a convention with a known weakness, in the
sense [`/method-scan`](../skills/method-scan/SKILL.md) defines.

The nearest thing that *is* checkable: a project writes a **never-claim list** —
its named competitors, and for each, the axis it must not claim superiority on,
with the public evidence. That file's existence is checkable, and
[`/verify`](../skills/verify/SKILL.md) can then test a draft against it.

Without such a list this rule is judgment only, and by this method's own standard
— see [rules get broken by their author](../reports/2026-07-30-rules-get-broken-by-their-author.md)
— judgment-only rules decay within about a month. A project doing serious
competitive positioning should write the list. A project with no competitive
claims yet does not need one.

## What a violation looks like

A `CONTRADICTED` verdict from `/verify` against a competitor's published
material is usually **not** a research failure. It is this convention failing at
composition time, caught late. Treat it as a claims-discipline finding and fix
the rule, not just the sentence.
