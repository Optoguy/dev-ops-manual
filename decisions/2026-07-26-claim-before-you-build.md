---
title: Claim tracked tasks before building, to prevent duplicate work
tags: [decision, process, plan, night-shift, coordination]
date: 2026-07-26
---

# Claim before you build

## Decision

Any worker — a live session **or** the nightly night-shift Routine — must **claim**
a tracked task before doing non-trivial work on it:

1. **Re-read `plan/plan.json` first.** Only start a task whose `status` is `todo`
   *and* that has no open PR or branch already touching the same files.
2. **Claim it before building.** Set `status: in-progress`, add a `note` of the form
   `claimed 2026-07-26 <who>` (e.g. `night-shift` or `live-session`), regenerate the
   dashboard, and **commit + push that one-line claim before starting the work.**
3. **`in-progress` means taken.** Never start a task that is `in-progress`, `blocked`,
   or `done`. Treat `in-progress` the same as an open PR: someone else has it.
4. On finish → `done` (+ `done_date`). On abandon → back to `todo` with a note on what
   happened, so it's available again.

The **night-shift Routine claims its entire approved slate up front** — one push of
`todo → in-progress` for all approved tasks — *before* it builds anything, so a
concurrent daytime session sees them taken.

## Why

On 2026-07-26 the night-shift Routine (PR #39) and a live session **both built the
molding / CNC / PCB how-to guides in parallel**, wasting the live session's effort
(its guides were dropped as redundant duplicates; PR #40 kept only the directory doc).

Root cause: `howto-guides-rest` was `owner: agent, status: todo`. The live session
started building without checking the plan or claiming the task; the night shift's
only in-flight guard was "an open PR exists," which was **false at selection time**
because the live session hadn't pushed yet. Neither worker marked the task
`in-progress` during the run, so it looked available the whole time it was being
worked. `in-progress` already existed as a status in the tooling — it was simply
never used as a claim.

## What changed as a result

- `CLAUDE.md` — new "Claim before you build" convention.
- `dev-skills/skills/night-shift/SKILL.md` (+ installed `.claude/` copy) — claim the
  approved slate up front; skip anything not `todo`.
- `dev-skills/skills/plan-track/SKILL.md` (+ installed copy) — the claim protocol is
  documented as the norm for the `in-progress` status.
- `plan/plan.json` — `_comment` records the protocol; `howto-guides-rest` carries a
  note about the collision.
