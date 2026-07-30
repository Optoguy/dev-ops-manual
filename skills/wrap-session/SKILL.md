---
name: wrap-session
description: Close out a working session so the project's artifacts stay honest — capture durable findings into the brain, log decisions, update task statuses, regenerate the dashboard, and commit. Use when asked to wrap up, close out, end the session, hand off, or leave things tidy; also appropriate before a long pause or context switch.
---

# Wrap the session

The whole system — plan, dashboard, brain, decisions — only works if it reflects
reality at the end of every session. A session that ends without a wrap leaves
the next session (or the owner's glance at the dashboard) trusting stale state.
This skill is the close-out ritual: sweep, record, regenerate, commit.

**Run [`history-capture`](../history-capture/SKILL.md) as part of it, and read the
transcript rather than relying on remembered context.** At session close your memory
of the period is the least reliable it will ever be — after compaction it is a
summary of a summary, while the transcript on disk is complete. The transcript also
dies with the container, so session close is the last safe moment to extract it.

## Procedure

1. **Sweep the session for durable findings.** Anything learned that will still
   matter in six months — a validated procedure, a number, a failure mode, a
   market fact — goes into the brain via the repo's capture discipline (`/brain`,
   or the repo's own `brain-capture`-style skill if it has one), with provenance
   ("Claude session — <topic>, <date>"). If nothing durable happened, say so and
   skip — don't pad the brain with narrative.

2. **Log decisions made mid-session.** Any choice that changed constraints,
   plan, or facts gets a dated decision file via `/decision-log` (or the repo's
   own `/decision`), with the trickle-down done, not deferred. A decision made
   verbally in the session but recorded nowhere will be re-litigated next week.

3. **True up the task source of truth.** Update statuses in the repo's declared
   task source (`plan/plan.json`, or whatever CLAUDE.md names — e.g. a
   launch-plan JSON): done things marked done with a date, new tasks added with
   owner + priority, discovered blockers recorded. Statuses are honest:
   in-progress is not done; a thing you *meant* to do stays todo.

4. **Regenerate everything generated.** Dashboard, index, any built docs whose
   source changed this session. Run the repo's check gates (lint, `--check`) so
   nothing ships stale.

5. **Commit, scoped.** One commit (or a few logical ones) with plain dated
   messages, staging only what this session touched — never `git add -A`. Do not
   push without the owner's go-ahead.

6. **Hand off in one paragraph.** End with: what changed, what's now the
   highest-priority open item for each owner (human vs. agent), and anything the
   next session must know that isn't yet in a file — then put that last category
   *into* a file, because "not yet in a file" is the failure mode.

## Judgment

- **The test of a good wrap:** a fresh session reading only CLAUDE.md, the
  dashboard, and the latest commits could continue the work without asking what
  happened. If something essential lives only in this conversation, it isn't
  wrapped.
- **Don't gold-plate.** A ten-minute session gets a one-minute wrap (statuses +
  commit). Scale the ritual to what actually changed.
- **Uncommitted work is a decision too.** If something is deliberately left
  half-done, record where it stands and why in the task's note — don't leave a
  mystery diff in the working tree.
