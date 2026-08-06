# The night shift re-ran its whole sweep 55 times and exhausted the weekly limit

2026-08-02. Found by the first August history capture, reading the transcript for
2026-07-31. **Recorded nowhere else** — it left no commit, no pull request and no
artefact, so a diff-based review cannot see it at all.

## The evidence

The digest for 2026-07-31 contains **55 separate night-shift slate openings**,
each beginning some variant of *"State refreshed across all four repos"* and each
followed by a gate table for all four repositories. They are near-identical. The
sequence ends at:

```
- You've hit your weekly limit · resets 12pm (UTC)
```

No slate from that night was ever approved, and nothing ran.

## What actually happened

The night-shift turn was interrupted and resumed repeatedly. Each resumption
re-entered the skill at step 1 and **re-executed the entire four-repository
sweep** — fetch, gate, task read, open-pull-request listing — then re-composed
the slate from scratch. Fifty-five times.

The sweep is the expensive part of the ritual and it is entirely idempotent: the
same four repositories, the same gates, the same answer. Nothing about it needed
repeating.

## Why this is a method problem, not an accident

The `night-shift` skill has no notion of a **completed step**. It is written as a
linear procedure — sweep, select, propose, claim, run — with the implicit
assumption that a turn runs once from top to bottom. Under any interruption that
assumption fails silently, and the failure mode is not an error but *repetition*:
each retry looks locally correct while collectively burning the budget that the
whole night depended on.

The cost landed on the scarcest shared resource there is. A night that hit the
weekly limit does not just lose its own slate — it degrades every session until
the reset.

## What would fix it

Nothing here is proposed as a convention change; this is the report.

- **Cache the sweep for the night.** The state collection is idempotent and
  cheap to serialise. Writing it to a scratch file keyed by date, and reading it
  back when it exists, makes a resumption cost nothing.
- **Make the approval gate resumable.** The expensive work happens *before* the
  gate, so an unanswered or interrupted slate pays full price every time. If the
  slate were written down when composed, a resumption could re-present it rather
  than rebuild it.
- **Notice the repetition.** Fifty-five identical openings in one day is a signal
  a session could detect about itself.

## The wider point

This is the second instance of the same shape as the 2026-07-30 finding that
*rules get broken by their own author*: the night-shift skill's own text warns
against wasted unattended work, and its structure guaranteed it. The rule was
right; nothing checked the structure.

**Provenance:** session transcript `9086f1e3-3340-52b3-aa9f-b9dccc26a2ab`,
2026-07-31. Digest: `docs/history/2026-08.md`.
