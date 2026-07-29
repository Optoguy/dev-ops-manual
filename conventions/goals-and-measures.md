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

## What counts as a measure

A measure needs four things, and the fourth is the one people skip:

| Part | Why | Bad | Good |
|---|---|---|---|
| **baseline** | A target without a starting point can't show movement | "get more traffic" | "49 visitors last week" |
| **target** | The number that means done | "improve conversion" | "3 completed specs" |
| **as_of** | A baseline with no date rots silently | — | "2026-07-29" |
| **source** | Where the number comes from, and who can check it | "analytics" | "the specs table, grouped by referrer" |

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

The [weekly review](../skills/weekly-review/SKILL.md) is where the weekly goal
gets set; the monthly goal is set in the first weekly review of the month.

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
