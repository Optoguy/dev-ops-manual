# Branch-ahead is not a claim signal — open PRs and task status are

**Date:** 2026-07-28
**Amends:** [2026-07-26 — claim before you build](2026-07-26-claim-before-you-build.md)
(that protocol stands; only its third detection signal is withdrawn)

## The decision

A task is claimed — in flight, not available — when its **status says
`in-progress`** or an **open PR touches its files**. Nothing else. The
"or a branch is ahead of the default branch on the same files" test is
**removed** from the protocol.

## Why

We squash-merge everything. A squash merge replays a branch's content as one
new commit on the default branch; the branch's own commits never become
ancestors of it. So **no git-topology test can tell you a squash-merged branch
is finished** — not `rev-list main..branch`, not a merge-base diff. A shipped
branch reads as "ahead of main, touching these files" permanently.

Found while cleaning up after PR #52: all thirteen `claude/*` branches on
SpecBuildr read as ahead of `main`, including `claude/retire-dev-skills` —
merged four minutes earlier. Since a night shift creates one or more branches
per run, the poisoned signal grows daily.

The consequence was not cosmetic. The night shift's availability rule would
have seen phantom claims on `plan/plan.json`, `dashboard/index.html`, and much
of `demo/` — the files nearly every branch touches — and skipped genuinely
available tasks, silently, on every future run.

## Why the remaining signals are sound

- **Open PR state** is authoritative and *self-clearing*: merging or closing a
  PR removes the claim with no extra bookkeeping.
- **`status: in-progress`** is explicit, pushed before work starts, and cleared
  to `done` or back to `todo` when the work resolves.

Both are checked directly (GitHub API, plan file) rather than inferred from
history shape. Inferring intent from git topology was the mistake.

## Trickle-down

- `skills/night-shift/SKILL.md` — selection rule 2 rewritten, with the reason
  stated so it isn't "simplified" back in later.
- `conventions/house-rules.md` — claim-before-you-build step 1.
- The night-shift Routine prompt — same rule, all repos.
- `SpecBuildr/CLAUDE.md`, `NewCoEndotest/CLAUDE.md` — claim conventions.
- Installed `.claude/skills/` copies in every project repo (re-install).

## Related practice

**Delete merged branches after merging.** It doesn't fix the signal — the rule
change does that — but it keeps branch lists readable and stops a session from
mistaking shipped work for work in flight when reading by eye. Exceptions:
branches with an open PR, a session's designated working branch, and any
branch a deploy target references.
