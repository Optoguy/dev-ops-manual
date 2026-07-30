# Backlog — Dev Operating Manual

Work that is worth doing and **serves no current goal**. That is not a criticism
of the items; it is the whole point of having goals. Anything here can be pulled
back into `plan/plan.json` the moment a goal makes it relevant — give it a `goal`
and a one-line `justification` when you do.

See [goals-and-measures.md](../conventions/goals-and-measures.md). The rule that
sends work here: *"Anything that is neither goal-serving nor keeping-the-lights-on
is, by definition, work that can wait."*

---

## Evaluate which built-in Claude skills are worth adopting into the house suite

**Owner: Dan · was P2 in the plan until 2026-07-30**

Candidates seen in use:

- `/security-review` — run before a traffic push.
- `skill-creator` — for authoring and evaluating skills properly, including its
  eval harness, which this repo has no equivalent of.
- `fewer-permission-prompts` — cuts interruptions by generating a scoped
  allowlist from transcript history.

Owner call on which become house practice.

**Why it moved here.** It was carrying a `keeping-the-lights-on` label, which is
reserved for security, data loss, breakage, legal obligations, and forced platform
changes. Evaluating optional tooling is none of those — the label was applied in
error on 2026-07-29, hours after the rule against exactly that was written. It
serves neither current goal either, so the backlog is its honest home.

**What would bring it back.** A monthly goal about the quality or coverage of the
house method rather than its adoption. If `skill-creator`'s eval harness turns out
to be the way to test whether a skill actually works, this stops being optional
and becomes the tooling for that goal.
