# Goals and measures

Added 2026-07-29 at the owner's request: *"We need goals and KPIs across all
projects… every project [must] have me define monthly, weekly goals, each goal
must have a measurable KPI, and all agent suggested work must include
justification as to how it supports achieving the current goals and KPIs."*

This convention binds every project, **including this one**.

## The rule in three sentences

1. **Every project has a current monthly goal and a current weekly goal, and the
   owner sets both.** Agents may draft; only the owner approves.
2. **Every goal carries one measure** with a baseline, a target, a date, and a
   named source. A goal without a number is a wish.
3. **Every piece of agent-suggested work names the goal it serves and how it
   moves that goal's measure** — or is explicitly labelled as work that serves no
   goal, which is allowed and sometimes correct.

## Where goals live — `plan/goals.json`

A separate file from `plan/plan.json`, deliberately. Goals are written by the
owner and change weekly; tasks are written by agents and change hourly. Different
authors and different cadences do not belong in one file, and the plan file is
already the busiest merge point in every repo.

```json
{
  "project": "Example",
  "updated": "2026-07-29",
  "month": {
    "id": "2026-08",
    "goal": "Prove that a finished spec is worth paying for.",
    "measure": {
      "name": "people who ask what it costs after finishing a spec",
      "baseline": 0,
      "target": 5,
      "unit": "people",
      "as_of": "2026-07-29",
      "source": "the contact form, counted by hand"
    }
  },
  "week": {
    "id": "2026-W31",
    "starts": "2026-07-29",
    "supports": "2026-08",
    "goal": "Get ten specs finished by people I did not ask personally.",
    "measure": {
      "name": "completed specs from non-personal referrers",
      "baseline": 0,
      "target": 10,
      "unit": "specs",
      "as_of": "2026-07-29",
      "source": "the specs table, grouped by referrer"
    }
  },
  "history": []
}
```

Rules for the file:

- **Both `month` and `week` are required** once a project has any tasks.
- `week.supports` names the month goal it serves. A weekly goal that supports
  nothing is a red flag worth raising, not a validation error.
- **`history` is append-only.** When a period ends, move the goal into `history`
  with an `outcome` (`hit` | `missed` | `abandoned`) and the measure's final
  value. This is how you find out whether goals are being set honestly.
- The same [never-reformat rule](house-rules.md) applies: edit lines in place.
- **`dashboard/goals.html` is generated from it** by `build_goals.py` — the
  current goals, a progress meter for each, the work serving each one, the work
  serving no goal, and the history of finished goals. Regenerate it whenever the
  goals change, same contract as the task dashboard.

## What counts as a measure

A measure needs four things, and the fourth is the one people skip:

| Part | Why | Bad | Good |
|---|---|---|---|
| **baseline** | A target without a starting point can't show movement | "get more traffic" | "49 visitors last week" |
| **target** | The number that means done | "improve conversion" | "3 completed specs" |
| **as_of** | A baseline with no date rots silently | — | "2026-07-29" |
| **source** | Where the number comes from, and who can check it | "analytics" | "the specs table, grouped by referrer" |

A fifth field, **`current`**, is optional and written by the goal review: where
the number stands right now. Without it the goals page says "not measured yet"
rather than implying progress — a page that fakes a number is worse than one
that admits it has none.

**If nobody can produce the number today, it is not a measure yet.** Say so and
make producing it the first task. A goal measured by a number that does not exist
is worse than no goal, because it looks like rigour.

Vanity measures — page views, commits, tasks closed, lines written — are only
measures if the project genuinely wants more of them. Usually it doesn't. Prefer
counting the thing you actually want: people who came back, people who asked the
price, defects that didn't recur.

## Justifying work

**Every agent-suggested task carries two fields:**

```json
{
  "id": "share-pitch-lines",
  "goal": "2026-W31",
  "justification": "Moves completed-specs-from-non-personal-referrers: personal messages are the only channel that has ever converted (3 of 3, against 49 direct visitors and 0)."
}
```

A justification names **the measure and the direction**, not the goal's title.
"Supports the August goal" is noise. "Moves completed-specs-per-week, which is at
0" is checkable.

**The same sentence appears everywhere the work is proposed** — in the task file,
in every menu put to the owner, and in the pull request body. One line. If it
takes a paragraph to explain how the work serves the goal, it probably doesn't.

### Work that serves no goal — say so plainly

Requiring a justification for everything creates a strong incentive to invent
one. That failure mode is worse than the problem, because a fabricated link is
indistinguishable from a real one until the measure doesn't move.

So **"this serves no current goal" is a valid, non-penalised answer.** Use
`"goal": "keeping-the-lights-on"` for work that has to happen regardless of
strategy:

- security fixes and data-loss risks
- something is broken that used to work
- legal, privacy, or licensing obligations
- a dependency or platform forcing a change

Anything that is neither goal-serving nor keeping-the-lights-on is, by
definition, work that can wait. That is not an insult — it is the entire point of
having goals. Put it in the backlog with a note and move on.

## Cadence — who does what, and when

The owner sets the goals. Agents do the preparation so that setting them takes
minutes, not an evening.

| When | Who | What |
|---|---|---|
| **Start of the month** | Agent drafts, owner decides | Propose 2–3 candidate monthly goals with the evidence behind each, as a clickable menu. Owner picks or writes their own. |
| **Start of the week** | Agent drafts, owner decides | Report last week's measure against its target, then propose this week's goal. Same menu pattern. |
| **Any slate of work** | Agent | Every option carries its goal and its one-line justification. |
| **End of the period** | Agent | Move the goal to `history` with its outcome and final number. Never quietly delete a missed goal. |

## The gate — no work without a goal

Added 2026-07-29 at the owner's request: *"Add a check to the dev ops to not
allow any further work unless there is a defined goal to work against."*

This is a **stop**, not a warning. `src/goal_gate.py` answers one question — may
work proceed here? — and an agent runs it before starting anything:

```sh
python src/goal_gate.py                # may work proceed in this repo at all?
python src/goal_gate.py --task <id>    # may work proceed on THIS task?
```

Exit `0` means clear. Exit `1` means blocked, and prints why and what is
permitted instead. Work is blocked when there is no goals file, when either goal
is missing or has no measure, when a measure lacks a baseline, target, date or
source, when a target is not above its baseline, or when the weekly goal is more
than seven days old. With `--task`, also when that task names no goal, names one
that is no longer current, or carries no justification.

`build_dashboard.py --check` enforces the same rule: **goal problems now fail
it.** A project that has not adopted goals fails that check, and that is the
intended pressure rather than a bug — the first permitted work is writing
`plan/goals.json`.

### Three things are always permitted

Without these the rule deadlocks: you could not fix the goals file, because
fixing it would be work.

1. **Setting or updating the goals**, and running the goal review.
2. **`keeping-the-lights-on` work** — security, data loss, something broken that
   used to work, legal or licensing obligations, a forced platform change. This
   genuinely cannot wait for a goal, so **the exemption outranks the gate**: a
   task labelled `keeping-the-lights-on` is permitted even in a repo with no
   goals file at all.
3. **Answering the owner.** Conversation is not work.

Everything else waits. That is the point: if no goal justifies a piece of work,
the honest options are to change the goal or to leave the work undone — not to
do it anyway and write a justification afterwards.

### What this costs, honestly

A blocked repo is a real stop. An expired weekly goal halts agent work until the
owner sets a new one, which is a dependency on one person being available. That
is deliberate — the alternative is agents working against a goal nobody has
looked at in a month — but it is a genuine cost, and if it starts biting, the
right response is to lengthen the period rather than to quietly widen the
exemptions.

## The goal review — weekly and monthly

**A goal that is set and never scored is decoration.** Every period ends with a
review, and the review is what updates and re-prioritizes. The ritual is
[`/goal-review`](../skills/goal-review/SKILL.md); the
[weekly review](../skills/weekly-review/SKILL.md) runs it as its opening section.

Both cadences do the same five things:

1. **Score the goal with a number** — baseline → target → actual, then one word:
   `hit`, `missed`, or `abandoned`. If the number can't be produced, say so;
   that is the most important finding a review can return, because every decision
   made against that goal was made blind.
2. **Audit the justifications.** For each task completed this period, did its
   justification turn out true — *held*, *didn't move it*, *unmeasurable*, or
   *wasn't really about the goal*? **This is what makes the justification rule
   real rather than ceremonial**, and it is the only thing that catches a
   fabricated one after the fact. A period where everything "held" is suspicious,
   not excellent.
3. **Feedback in both directions.** On the work: what actually moved the number
   versus what was busy. On the goal: was it specific enough to select work
   against, was the measure honest, was the target real, and did something
   outside the goal turn out to matter more.
4. **Re-prioritize the open work** against the current goal — promote, demote,
   re-justify, or backlog. **Proposed as a menu, never applied silently.**
   Priority is the owner's signal about their own attention.
5. **Set the next goal**, owner-decided from prepared candidates, and move the
   finished one into `history` with its outcome.

**The monthly review additionally asks the direction question:** read the whole
`history`, not the last entry — every goal hit means targets are too low, every
goal missed means fantasy or an unseen blocker, measures that keep changing mean
nothing is comparable. Then check the month's goal against the project's strategy
document. If they have drifted apart, that mismatch is the review's headline.

**Order matters at a month boundary:** the monthly review runs first, because the
weekly goal has to support the monthly one.

Suggested schedule — each project's own chat owns its Routines:

| Review | When | Why then |
|---|---|---|
| Weekly | End of the working week | The next goal is set before the week starts, not three days in |
| Monthly | Last working day of the month | Ahead of the first weekly review of the new month |

Both need to ask the owner questions, so both must fire into a persistent
session. A review that cannot ask cannot re-prioritize.

**Stale goals are a blocking condition, not a note.** If the weekly goal started
more than seven days ago, the first thing an agent asks the owner is for a new
one — before proposing any work. Work selected against an expired goal is work
selected against nothing. `build_dashboard.py` prints a staleness warning every
time it runs, so this is caught mechanically rather than remembered.

## Honest failure modes

Naming these because the convention is more likely to fail in one of these ways
than to be ignored outright:

- **Goal theater.** Setting targets already known to be met. The `baseline` and
  `as_of` fields exist to make a target below the baseline visible at a glance.
- **Fabricated justifications.** Mitigated by requiring the *measure* to be
  named, and by making "serves no goal" a legitimate answer rather than a
  confession.
- **Measuring what is easy.** If the honest measure is hard to collect, the right
  first task is to make it collectible — not to substitute a proxy and forget the
  substitution happened.
- **Goals that never fail.** If every goal is hit, they are set too low. A
  `history` with no `missed` entries after a few months is itself a finding.
