# 2026-07-30 — Every project carries an end goal, and the ladder is checked

**Decision.** Goals are three levels, not two. Every project carries an **end
goal** — why the project exists at all — restated from its strategy document into
`plan/goals.json`. The monthly goal declares `"supports": "end"`; the weekly goal
declares the month's id. A broken ladder blocks work. The end goal itself is
**reviewed, never scored**, and never blocks.

**Asked for by the owner**, 2026-07-30: *"For the goals structure we need to also
ensure each project has a high level end goal defined that monthly and weekly
goals support. This is part of the strategy as well. Why are we doing this
project."*

## What was missing

The goals convention shipped yesterday with two levels: a monthly goal and a
weekly goal serving it. The weekly goal named what it served. **The monthly goal
named nothing.**

That is a real hole, not a formality. A project could run a tidy, well-measured,
fully-justified ladder — every task naming a goal, every goal carrying a real
number — and still be climbing toward nothing anybody had chosen. The convention
could verify that work served the month, and that the month had a number, but not
that the month was worth having. Every check pointed downward.

This repository was a live example within a day: its August goal was "every
project runs on goals," which is a description of the method's adoption, not a
reason the method exists. Writing its end goal forced the sharper sentence — *any
chat, in any project, works the way Dan works, without Dan having to explain it
again* — and made the August goal legible as a step toward it rather than as the
point.

## Design choices, and why

**The end goal lives in two places, and the strategy document is the source.**
`docs/STRATEGY.md` carries the prose — who it is for, the wedge, the evidence,
what is undecided. `plan/goals.json → end` carries the one-sentence restatement
plus a `strategy` field pointing back. This is the same split the project already
uses for the narrative plan and the task file, and it earns its keep the same way:
prose for humans, structure for generators and checks. **If the two disagree, the
document wins and the goals file is stale.**

**`success`, not a measure.** An end goal gets no number, no target, no progress
bar. A bar on a multi-year ambition is fake precision, and the temptation would be
to invent a countable proxy for something that is not yet countable. Instead the
required field is `success` — *what would have to be true for this to be
achieved* — which must be checkable by a person but need not be arithmetic.
"Specs produced here are quoted as-is by real manufacturers" is a test. "Improve
the quote experience" is not.

**Reviewed, not scored, and never blocking.** The gate reports the end goal's age
on every run and flags it after 90 days without confirmation. It never blocks:
a north star that needs re-checking is not a reason to stop work, and blocking on
it would push people to bump the date rather than think. Confirming it means
saying what evidence confirmed it; **changing it is a decision and gets a record**,
because a north star that moves without a trace is how a project ends up somewhere
nobody chose.

**The ladder check is structural only.** The gate verifies each level *names* what
it serves. It does not and cannot verify that the support is genuine — that is the
monthly review's job, and it is now an explicit step there. The distinction
matters: a script that claimed to judge whether a month truly serves an end goal
would be inventing a verdict.

## What changes for agents

Before: check the weekly goal is current, then propose work that serves it.

After: the same, plus the ladder must be intact. A project with no end goal, or a
month that names nothing above it, is **blocked** — and the way out is writing the
end goal, which is permitted work under the standing exemptions.

## Fleet impact

`goal_gate.py`, `build_dashboard.py`, `build_goals.py`, and the `plan-track`,
`goal-review` and `project-init` skills all changed, so every project repository
needs `./install.sh --repo <path>` re-run on its own schedule, with adoption
instructions per the 2026-07-29 rule. **Every project will be blocked until its
end goal is written** — three of them are already blocked for want of any goals at
all, so this adds a field to a form nobody has filled in yet rather than breaking
something that worked.

## How this could be wrong

- **Three levels may be one too many for a one-person operation.** If the end goal
  is written once and never referenced, it is decoration with extra steps. The
  review step is what should catch that — if a monthly review never once finds a
  drift between month and end goal, the check is not doing work.
- **`success` may prove unwritable for genuinely exploratory projects.** A venture
  whose whole question is "is there a business here" has no honest success
  condition beyond "we found out." That is an acceptable answer, and if it turns
  out to be the *common* answer, the field is wrong rather than the projects.
- **Blocking on a broken ladder is strict.** It is defensible while goals are new,
  because the alternative is a ladder that silently detaches. If it starts firing
  on legitimate mid-month re-aiming, the honest fix is to make the month's
  `supports` easier to update, not to stop checking it.
