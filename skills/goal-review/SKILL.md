---
name: goal-review
description: Run the goal review — score the current goal against its number, audit whether the work that claimed to move it actually did, then have the owner update and re-prioritize. Use for a weekly or monthly goal review, when asked how a goal is tracking, when goals feel stale or wrong, or as the prompt for a scheduled goal-review Routine.
---

# Goal review

Goals that are set and never scored become decoration. This is the ritual that
keeps them honest: **score the number, audit the justifications, give feedback in
both directions, then let the owner update and re-prioritize.**

Two cadences, same shape:

| | **Weekly** | **Monthly** |
|---|---|---|
| Scores | the weekly goal | the monthly goal, and the weeks inside it |
| Asks | did the number move? | is this the right goal at all? |
| Output | next week's goal + re-ranked tasks | next month's goal, direction confirmed or changed |
| Length | five minutes to read | ten, with the trend |

The weekly review (`/weekly-review`) runs this as its goal section. Run it
standalone when the owner asks how a goal is tracking, or when a goal feels
wrong mid-period.

**This review is exempt from the goal gate**, and is usually the reason the gate
is red. When `src/goal_gate.py` blocks a repo, running this is the permitted way
out — setting the goals is always allowed.

## Procedure

### 1. Score the goal with a number, first

Read `plan/goals.json`. Take the current period's measure and report it as
**baseline → target → actual**, with the date the actual was taken and the
source it came from. Then one word: `hit`, `missed`, or `abandoned`.

**Write the number back.** Set the measure's `current` field in
`plan/goals.json` and regenerate `dashboard/goals.html`. A goal whose `current`
is never updated shows "not measured yet" forever, which is the page telling the
truth about a review that never happened.

If the number cannot be produced, **say that instead of estimating.** "The
measure was never collectible" is the most important finding a review can
return, because it means every decision made against that goal was made blind.
Producing the number becomes the first task of the next period.

### 2. Audit the justifications — did the work do what it claimed?

This is the step that makes the whole convention real rather than ceremonial.

For every task completed this period, read the `justification` it shipped with
and ask whether it turned out true:

| Verdict | Meaning |
|---|---|
| **held** | The work shipped and the measure moved in the direction claimed |
| **didn't move it** | The work shipped, the measure didn't move. Not a failure — a finding. |
| **unmeasurable** | No way to tell, because the measure doesn't isolate it |
| **wasn't really about the goal** | The justification was written to pass the gate |

Report the counts. **A period where every justification "held" is suspicious**,
not excellent — either the measure is too coarse to distinguish anything, or the
justifications are being written to be unfalsifiable. Say so.

The last verdict is the one worth hunting for. Requiring a justification for
every task creates an incentive to invent one; this audit is the only thing that
detects it after the fact. Name the specific task, quote its justification, and
say what it actually served. No blame — the point is to calibrate the next set of
justifications, and a convention nobody checks decays within a month.

### 3. Feedback, in both directions

**On the work:** which completed tasks actually moved the number, which were busy
work, and what the ratio was. Rank the period's output by contribution, not by
effort or by count.

**On the goal itself** — the direction agents cannot give unless invited, so
invite it explicitly:

- Was it *specific enough* to select work against? A goal that admits any task
  isn't a goal.
- Was the measure *honest*? Did it capture what was actually wanted, or the thing
  that was easy to count?
- Was the target *real*? Check `history`: a run of `hit` means targets are set
  too low, a run of `missed` means they are fantasy or the work is blocked
  elsewhere. Both are findings; neither is a moral failing.
- Did anything *outside* the goal turn out to matter more? If the period's most
  valuable work was labelled `keeping-the-lights-on`, the goal was aimed at the
  wrong thing.

**Ask the owner for feedback too**, as a menu, not an open question: was this
goal worth chasing, was the reporting useful, should the cadence change.

### 4. Re-prioritize the open work against the goal

Goals only bite if they change what happens next. Re-rank every open task against
the current (or newly-set) goal and propose the changes as one menu:

- **Promote** — serves the goal directly, currently ranked below something that
  doesn't.
- **Demote** — no longer serves the goal. Not deleted: dropped a level with a
  note saying which goal it used to serve.
- **Re-justify** — still worth doing, but its justification pointed at a goal
  that has now ended. It needs a new one or it becomes `keeping-the-lights-on`.
- **Backlog** — serves no current goal and isn't keeping the lights on. That is
  precisely the work goals exist to postpone.

Propose; never re-prioritize silently. Priority is the owner's signal about their
own attention.

### 5. Set the next goal — the owner decides, you prepare

Two or three candidates as a clickable menu. Each carries:

- the goal in one plain sentence
- the measure it would be scored on
- **a baseline that exists today**, with its source
- one line of evidence for why this one
- which month goal it supports (weekly), or which strategic bet it serves
  (monthly)

The owner picks one or writes their own. Write it into `plan/goals.json` with
`starts` set to today, move the finished goal into `history` with its outcome and
final number, and regenerate the dashboard.

**Never set a goal on the owner's behalf.** An agent-invented goal that nobody
chose is worse than no goal, because it looks like direction.

### 6. Monthly only — check the trend before setting direction

Read the whole `history`, not just the last entry:

- **Every goal hit?** Targets are too low. Say it plainly and propose one that
  might fail.
- **Every goal missed?** Either the targets are fantasy or something outside the
  plan is blocking. Which one is a different conversation, and the review should
  say which it thinks it is.
- **Measures keep changing?** Moving the yardstick between periods means nothing
  is comparable. Propose settling on one measure for a quarter.
- **The monthly goal never changed while weekly goals wandered?** The weeks
  weren't serving the month. Either re-aim the weeks or admit the month goal is
  not what is actually being pursued.

Then ask the direction question the weekly review never asks: **is this still the
right thing to be aiming at?** Point at the project's strategy document. If the
month's goal and the strategy have drifted apart, that mismatch is the review's
headline finding, not a footnote.

## Output

A dated summary, short enough to read in five minutes (ten for monthly):

1. **The number** — baseline → target → actual, and the verdict word.
2. **Justification audit** — the counts, plus any task whose justification did
   not survive contact.
3. **Feedback** — on the work, and on the goal itself.
4. **What changes** — proposed priority moves.
5. **Next goal** — the candidate menu.

Deliver it as a file, not buried in chat text. End with the menu, and with the
written options list.

## Scheduling it

Both cadences suit a Routine (see [routine-design](../routine-design/SKILL.md)
and [conventions/routines.md](../../conventions/routines.md)):

- **Weekly** — end of the working week, so the owner sets the next goal before it
  starts rather than three days into it.
- **Monthly** — the last working day of the month, before the first weekly review
  of the new month, since the weekly goal has to support the monthly one.

A project's goal-review Routines live in **that project's own chat**, like all
its other Routines. Both need `AskUserQuestion`, so they must fire into a
persistent session — a fresh headless session has no way to ask the owner
anything, and a review that cannot ask cannot re-prioritize.

## Judgment

- **Score before you explain.** The number comes first. Reasons after, and
  briefly.
- **A missed goal is information, not a failure to soften.** Writing "we made
  great progress toward" instead of "missed, 2 against a target of 10" destroys
  the only signal the ritual produces.
- **Never quietly retire a goal.** Every goal ends in `history` with an outcome.
  A goal that vanishes is a goal that was missed.
- **Don't propose a new goal that merely restates the missed one** without saying
  what will be different this time. Repetition with no change is how a plan
  stalls for a month without anyone noticing.
- **Re-prioritizing is proposed, never applied.** The owner owns priority.
