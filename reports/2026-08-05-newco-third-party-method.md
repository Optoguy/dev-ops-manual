# What NewCoEndotest knows about third parties that the manual doesn't

2026-08-05. Report only — nothing changed. A proposal for one convention, and an
audit of what already flowed upstream.

---

## Already merged — no action needed

Most of NewCoEndotest's third-party method is **already in the manual**, which is
the reverse-direction rule working. Recorded here so nobody re-proposes it.

| Their mechanism | Where it already lives here |
|---|---|
| Verdict set — CORROBORATED / CONTRADICTED / NOT PUBLICLY VERIFIABLE | `skills/verify/SKILL.md` step 3 |
| **Paywall honesty** — mark PAYWALL-LIMITED, say what *could* be checked (edition, designation, date) versus what could not, never infer clause content from an abstract | `skills/verify/SKILL.md` step 3 |
| Severity order, CONTRADICTED-by-public-source highest, paywall-limited as *inventory not failure* | `skills/verify/SKILL.md` |
| **Provenance guard** — public material found while verifying is for checking only; it enters the knowledge base through a separate capture pass with owner review, never automatically | `skills/verify/SKILL.md` step 5 |
| Adversarial fan-out — parallel agents framed "try to refute this claim" | `skills/verify/SKILL.md` step 4 |
| `confidence: verified \| inferred` plus inline *(inferred)* markers | `skills/brain/SKILL.md`, `frontmatter-schema.md` |
| `reference-only` — may inform thinking, must not be relied on as project work product | `tag-vocabulary.template.md` |
| `internal-only` — never leaves the project; **third-party assets** | `tag-vocabulary.template.md` |
| Flagging deprecated or reference-only material cited *as if validated* | `skills/verify/SKILL.md` step 2 |

That is a lot of transfer that already happened. The gap is narrow and specific.

---

## The gap: nothing here governs claims *about a named competitor*

`/verify` checks a claim **after** it is written. Nothing in the manual governs
**composing** one. The tag vocabulary even names *"claims discipline"* under the
`governance` tag — and no file defines it.

NewCoEndotest has it, in
`brain/knowledge/strategy/competitive-positioning.md` under a heading it calls
**"Messaging discipline (the load-bearing part)."** It is domain-specific in its
examples and entirely general in its structure. Five rules, generalized:

**1. Name the dimension you lose on, in the rule itself.**
> *"Against the production benches (Trioptics / Optikos): win on price,
> portability, and target customer — **never on measurement superiority**. They
> are rigorous; claiming to out-measure them is false and will be seen through."*

The discipline is not "be modest." It is that a written rule names the axis where
a named competitor is genuinely better, so no future draft quietly claims it.

**2. Never claim a differentiator the competitor demonstrably already has.**
> *"Don't claim 'we trend results' as a differentiator. ScopeControl already does
> per-scope longitudinal trending. The defensible claim is **what** is trended."*

**3. A category shift is not a differentiator once a competitor markets it.**
Dovideq's own headline is *"5× more accurate than humans."* Same shift being
sold. Their rule: use it to establish the category with a customer, **never** as
the reason to choose you over an incumbent.

**4. Scale the claim to the specific opponent.**
One competitor is 470 kg floor-standing — portability is a headline there. Another
is benchtop — against it, lead with rigor and price instead. The same true
sentence is strong or embarrassing depending on who it is aimed at.

**5. Never attack a competitor's moat.** *"Both are losing games."*

### Why this transfers

It is a **falsifiability discipline for competitive claims** — it forces a claim
to survive contact with what the named third party actually publishes, *before*
it is written rather than after. Every project has this exposure. SpecBuildr
makes claims against other specification tools; medtech-intel-QMSR against
regulatory copilots, and its brain already holds a competitor landscape file.

It also pairs exactly with the naming rule relaxed earlier today: that decision
made it legitimate to **name** a competitor. This governs **what you may then say
about them**. Naming without claims discipline is the more dangerous of the two.

---

## How to merge it — recommended shape

**A new short convention, `conventions/claims-discipline.md`**, holding the five
rules in general form, plus two pointers:

- `skills/growth-loop/SKILL.md` — it already forbids auto-posting and fake
  engagement; it should also govern what a claim may assert. This is where
  marketing copy gets composed.
- `skills/verify/SKILL.md` — a line noting that a CONTRADICTED verdict against a
  competitor's published material is usually a claims-discipline failure at
  composition time, not a research failure.

**Why a convention rather than folding it into a skill:** it binds anything
outward-facing — landing pages, a pitch line, a discovery script, a spec sheet —
not one ritual. Conventions are what every skill inherits.

**The mechanical check, honestly:** there isn't a good one, and the convention
should say so rather than pretend. The nearest thing is a **per-project
never-claim list** — the project names its competitors and, for each, the axis it
must not claim superiority on. That file *is* checkable for existence, and
`/verify` can then test a draft against it. Without a project-specific list the
rule is judgment only, which under this method's own standard means it will decay.
Label it a convention with a known weakness, per `/method-scan`'s rule.

**Provenance to preserve.** The rules were discovered in a specific competitive
analysis and one of them is a live correction to an earlier position — the Lyon
study line exists *because* a proposed differentiator was refuted by a
competitor's own homepage. That is the strongest argument for the rule, and it
should be cited when adopting it rather than presented as abstract good sense.

---

## What not to take

**Their `brain-verify` skill itself.** It is the specialised local version of the
manual's `/verify`, and `/verify`'s own description already defers correctly:
*"If the repo has its own verification skill (e.g. brain-verify), use that
instead."* That deferral is working. Do not merge the skills.

**Their tag vocabulary wholesale.** Their domain tags (`repair-isos`, and so on)
are theirs. The governance tags already transferred.
