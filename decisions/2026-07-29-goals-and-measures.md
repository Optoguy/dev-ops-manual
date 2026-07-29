# 2026-07-29 — Every project runs on owner-set goals, and every suggestion justifies itself against one

**Decision.** Every project — including this one — carries a current monthly goal
and a current weekly goal in `plan/goals.json`, set by the owner. Each goal
carries exactly one measure with a baseline, a target, a date, and a named
source. Every agent-suggested task names the goal it serves and, in one line, the
measure it moves. Work that serves no goal is labelled
`goal: keeping-the-lights-on` and says so.

**Asked for by the owner**, 2026-07-29: *"We need goals and KPIs across all
projects… every project [must] have me define monthly, weekly goals, each goal
must have a measurable KPI, and all agent suggested work must include
justification as to how it supports achieving the current goals and KPIs."*
Followed by: *"Dev ops must have goals and kpis as well."*

## What this fixes

Agent-suggested work was being selected on **availability** rather than
**importance**. The selection rules were sound — owner-owned, unblocked,
verifiable, unclaimed — and every one of them is a test of whether a task *can*
be done tonight. None of them asks whether it is worth doing at all. The night
shift on 2026-07-29 is a fair example: three tasks were offered, all correctly
qualified, and not one of them stated what it would move.

The result is a plan that stays busy and a project that doesn't obviously
advance. Priorities (`P0`/`P1`/`P2`) were carrying weight they can't hold — a
priority says how urgent something is relative to the other things on the list,
not whether the list is pointed anywhere.

## Design choices, and why

**Goals live in `plan/goals.json`, not inside `plan/plan.json`.** Different
authors and different cadences: goals are written by the owner and change weekly,
tasks are written by agents and change hourly. The plan file is also the busiest
merge point in every repo — two agents editing it in one night is already the
known collision (2026-07-27, five parallel external-agent pull requests). Adding
an owner-edited section to it would make that worse.

**A measure needs four fields, and the fourth is the one people skip.** Baseline,
target, `as_of` date, and a named source. Without a source, "we'll measure
engagement" survives review and dies quietly at reporting time. The rule is: if
nobody can produce the number today, it is not a measure — say so, and make
producing it the first task.

**"Serves no goal" is a legitimate answer.** This is the part most likely to be
misread as a loophole. It isn't: requiring a justification for every piece of
work creates a strong incentive to invent one, and a fabricated link is
indistinguishable from a real one right up until the measure doesn't move. Giving
honest non-goal work a name (`keeping-the-lights-on` — security, breakage, legal,
forced platform changes) keeps the justifications that *are* offered meaningful.

**Warnings, not failures, during adoption.** `build_dashboard.py --check` reports
missing goals and unjustified tasks loudly but still exits zero; `--strict-goals`
makes them fatal. Three project repositories have open tasks written before this
convention existed. A rule that breaks every build the day it lands gets reverted,
not adopted.

**Staleness is checked mechanically.** A weekly goal more than seven days old is
expired, and the night shift's first test — before ownership, before blocking,
before claims — is whether the goal is current. Written rules get forgotten; a
warning printed on every dashboard build does not. The staleness check is
terminal-only and never written into the page, so generated output stays
deterministic and `--check` keeps meaning "you forgot to rebuild."

## What changes for agents

Before: propose available work.
After: propose available work **that serves the current goal**, say which measure
it moves, and if the goal has expired, ask for a new one instead of proposing
anything.

## Fleet impact

`skills/plan-track/`, `skills/night-shift/`, `skills/weekly-review/` and
`skills/project-init/` all changed, so every project repository needs
`./install.sh --repo <path>` re-run — on its own schedule, in its own session, as
always. Each project then writes its own `plan/goals.json`, which only the owner
can fill in.

## How this could be wrong

- **It adds ceremony to a one-person operation.** If setting goals costs more
  than it redirects, the honest response is to drop the monthly goal and keep the
  weekly one, not to keep both and stop filling them in.
- **Weekly may be the wrong period** for projects whose feedback loop is longer
  than a week — a hardware venture waiting on parts cannot move a weekly number.
  The convention should be revisited if `history` fills with `abandoned`.
- **Goals set by an agent's menu are still shaped by the agent's options.**
  Drafting candidates is genuinely useful given the owner's time, but the menu is
  a nudge. Writing one's own goal must stay the obvious path, not the escape
  hatch.
