# The git proxy serves stale refs, and a merge on a stale base silently drops work

2026-08-02. Found by the first August history capture, reading the transcript for
2026-07-30. Two incidents in one day, one of which was a near-miss caught only by
noticing that a file had lost content nobody had touched.

## Incident one — a push that appeared not to land

A push reported success, but the subsequent local fetch showed the remote ref
unmoved. Checking GitHub directly resolved it:

> The push did land — GitHub's `main` is at `4bb4516`. The local fetch was served
> a stale ref by the git proxy; the remote is correct.

Had the report been trusted, the obvious "recovery" would have been to push
again or to rebuild the commit — both harmless here, but both operating on a
false picture.

## Incident two — the near-miss

Later the same day, merging a branch produced a working tree that had **lost
rows from `conventions/routines.md` that no part of the merge touched**:

> The working tree lost my `routines.md` rows — a sign the merge pulled a
> **stale** `origin/main`. The git proxy served an old ref earlier too. Aborting
> before I build on the wrong base.

The merge had been computed against a `main` that was several commits behind the
real one, so content that existed only on the newer `main` simply vanished from
the result. **This is the dangerous shape**: no error, no conflict, a clean merge
that quietly reverts work. It was caught because the missing rows were recent
enough to be remembered — a weaker signal than any check.

The recovery was to re-resolve the true head (`ec061c4`) and redo the merge
against it, at which point `plan.json` auto-merged correctly and only the two
generated dashboards conflicted, which the regenerate-never-hand-merge rule
already covers.

## Why it matters beyond git

The fleet audit reads repository state across four projects. Its own skill warns
that running the collector against the wrong branch **manufactures false
patterns** — a project can be reported as behind, stalled, or drifting purely
because the proxy served an old ref. The stale-gate finding in
medtech-intel-QMSR was confirmed only after every clone was re-synced to its true
remote state first.

So a stale ref does not just risk losing a commit. It can produce a *confident,
well-formatted, entirely wrong* cross-project report.

## What would reduce it

Report only; no convention changed here.

- **Verify against the remote host, not the local fetch, before acting on
  "the push didn't land."** Checking GitHub directly resolved incident one in one
  step.
- **Re-sync every clone to its true remote state before any cross-repository
  read**, which is what the audit skill already advises and what made the medtech
  finding trustworthy.
- **Treat an unexplained content loss in a merge as a base problem, not a
  conflict problem.** Aborting and re-resolving the head was the correct move and
  cost minutes; hand-fixing the file would have buried the cause.

**Provenance:** session transcript `9086f1e3-3340-52b3-aa9f-b9dccc26a2ab`,
2026-07-30. Digest: `docs/history/2026-08.md`.
