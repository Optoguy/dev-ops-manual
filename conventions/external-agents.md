# External agents

Added 2026-07-27, after five parallel Devin sessions opened PRs that all
collided on the same generated files in one repo.

Any non-Claude agent working these repos follows **the same contract** as a
Claude session. The rules aren't Claude-specific; they're what keeps parallel
workers from destroying each other's work.

## The contract

1. **Point it at the repo's `CLAUDE.md` first.** That file is the contract; an
   agent that hasn't read it can't honor it.
2. **Claim before you build.** Claim as `(claimed <date> devin)` /
   `status: in-progress` with a devin note, **pushed before building** — same
   protocol as everyone else. See [house-rules.md](house-rules.md).
3. **Draft PRs only**, one concern per PR.
4. **Never hand-edit generated files** — regenerate them.
5. **Never two agents on overlapping file sets at once.** This is the rule the
   five colliding PRs violated; the collision was in the *generated dashboards*
   every PR rebuilt.

## What to dispatch

**Suitable:** well-scoped, mechanically verifiable, self-contained file scope —
tests, refactors, security hardening, migrations, mechanical fixes.

**Not suitable:** business content, judgment-laden positions, credentials,
identity, plan reprioritization, anything under the owner's name, or work that
needs an approval gate mid-run.

## The best use

**Adversarial review of agent-built work.** A second, independently-built agent
reviewing the first one's output catches blind spots that more of the same
agent will not. The most valuable Devin PR in this account's history was the one
that reviewed Claude-authored skills and found two real defects — a scaffold
step that would clobber an existing generator, and a skill contradicting the
repo's own declared task source of truth.

Run it in both directions: have Devin audit Claude's work, and have Claude
review and integrate Devin's PRs rather than merging them blind.

## Dispatch tagging

When proposing a slate of agent tasks, tag each one:

- **run-here** — bookkeeping, approval gates, judgment content, Routines,
  credentials, identity.
- **Devin-suitable** — mechanically verifiable, self-contained, no house
  bookkeeping.

The owner decides; the tag just makes the choice one click instead of a
conversation.

## Merging external PRs

Expect conflicts in generated output when several land together. The house
resolution is always the same: **merge one, regenerate, then rebase the next** —
never hand-merge a generated file. For plan files, union by task id and prefer
the more-progressed status. Verify after each merge (tests, lint gate, build)
before taking the next one.
