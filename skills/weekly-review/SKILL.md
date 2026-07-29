---
name: weekly-review
description: Run the project's operating cadence — what moved, what stalled, what's blocked on the owner, is the plan still honest, and what are next week's top priorities. Use when asked for a weekly review, status report, retro, "where are we," or what to focus on next; also suitable as the prompt for a weekly Routine.
---

# Weekly review

The dashboard shows state; the review supplies the rhythm. Once a week (or on
demand), read the project's actual artifacts — task source of truth, commits,
reports — and answer four questions: what moved, what stalled, is the plan
honest, and what matters next. Short enough to read; honest enough to sting.

## Procedure

1. **Read the record, not memory.** The task source of truth (`plan/plan.json`
   or whatever CLAUDE.md declares), the week's commits (`git log --since`), any
   committed reports, and the dashboard. The review is generated from evidence;
   a review written from recollection inherits recollection's optimism.

2. **Score last week's goal — first, and with a number.** Read
   `plan/goals.json`, take the weekly goal's measure, and report where it
   actually landed against its target: baseline → target → final. Then say `hit`,
   `missed`, or `abandoned`. **Move the finished goal into `history` with that
   outcome and the final number** — append-only, never quietly delete a missed
   goal. A run of goals that are always hit means they are set too low; a run of
   goals with no final number means the measure was never real. Both are
   findings worth reporting.

3. **What moved.** Tasks done this week (with dates), meaningful commits,
   metrics that improved. Credit both owners — the human's cleared blockers
   count as much as the agent's shipped features. **Say which of these served
   the week's goal and which didn't** — a busy week that moved nothing toward
   the goal is the single most useful thing a review can surface.

4. **What stalled — with the why.** Tasks in-progress for more than a week,
   P0/P1 items untouched, anything whose status hasn't changed since the last
   review. For each: blocked, deprioritized, or forgotten? Those are three
   different problems with three different fixes.

5. **Blocked-on-owner, front and center.** The human's open P0s and what each
   one gates. This is the single most valuable output — the owner should leave
   the review knowing exactly which 15 minutes of their time unblocks the most
   agent work.

6. **Honesty check on the plan.** Statuses vs. reality (does "in-progress" have
   commits?), priorities vs. behavior (if a P2 got all the attention, either the
   priorities are wrong or the week was — say which), staleness gates
   (`--check` runs clean, dashboard regenerated). Fix mechanical drift on the
   spot; propose judgment calls to the owner.

7. **Groom the edges.** Backlog items ready to graduate into the plan; open
   questions answered by the week's events (cite what answered them); done
   items cluttering the view.

8. **Next week's focus: three items, ranked, with reasons.** Not ten. Each
   names its owner and its "done" looks like. If the honest answer is "same as
   last week because nothing cleared," write that — repetition is information.

9. **Set next week's goal — the owner decides, you prepare.** Propose two or
   three candidate weekly goals as a clickable menu, each with the measure it
   would be scored on, its baseline today, and the evidence for picking it.
   Say which month goal each would support. The owner picks one or writes their
   own; write it into `plan/goals.json` with `starts` set to this week and
   regenerate the dashboard. **At the start of a month, do the same for the
   monthly goal first**, since the weekly goal has to support it. Never set a
   goal on the owner's behalf — an agent-invented goal that nobody chose is
   worse than no goal.

10. **Output:** a dated summary in the reply (and committed to `reports/` if the
   repo keeps them), then regenerate the dashboard and commit any plan edits,
   scoped staging, no push.

## Judgment

- **Measure against deliverables, not activity.** Ten commits on a P2 while a
  P0 sat idle is a bad week that looks busy. Say so plainly.
- **Trends beat snapshots.** "Third week stalled" is a different fact than
  "stalled" — read the previous review before writing this one.
- **The review recommends; the owner reprioritizes.** Propose priority changes
  with reasoning; don't silently rewrite the plan's priorities.
