# One Manager agent executes across all projects; dev-ops never touches them again

**Date:** 2026-08-05
**Status:** adopted on merge of the pull request that carries this file
**Changes:** new `conventions/three-roles.md`; amended `conventions/routines.md`
(designated-chat rule) and `conventions/house-rules.md` (the night-shift
carve-out relocates)

## The instruction

The owner, 2026-08-05, immediately after the two-week attention review:

> Would it be possible to make a single manager agent that I interact with that
> implements actions in each project? I want to keep dev ops independent and
> never takes action on other projects

And the feedback that prompted the review:

> the system is not effective, I often get confused on status, I can't recall
> what is the next step in each chat… I need a very clear list of tasks and
> actions. I feel like a lot of things go missed in these chats.

## What was true before

Four chats of equal rank, each owning one repo's work and Routines, each ending
turns with locally-correct next-step menus. The
[two-week review](../reports/2026-08-05-two-week-review-owner-attention.md)
measured what that did with the owner's actual attention (two short daily
windows, serial): five of seven night slates expired unanswered, ten draft pull
requests queued to nine days, ~22 owner tasks scattered across four plan files,
and a 108-hour silence in one chat while the owner worked another — invisible to
all of them.

The method chat also carried a structural wart: it owned the cross-project night
shift, so the repo whose rule is *"this repo never pushes to project repos"*
was, one carve-out a night, the repo that did.

## The decision

Three roles — see [three-roles.md](../conventions/three-roles.md) for the
binding text:

- **The Manager**: one new chat the owner talks to daily. Executes in every
  project repo under the existing disciplines (claim-before-you-build, draft
  pull requests, one concern each, merges only on the owner's word). Opens each
  owner window with the fleet inbox. Takes the night shift with it.
- **The method** (this repo's chat): audits and improves the method. With the
  night shift gone, *never acts on a project repo* — the owner's requested
  independence, now without exception. The auditor no longer audits its own
  actions.
- **Specialists** (the existing project chats): deep domain work when the owner
  sits with them. They claim like anyone else; their Routines and their history
  capture stay with them, because a transcript is readable only by the session
  that produced it.

## Why this shape

- **It matches the measured attention pattern.** One inbox at the window's
  start, batch decisions in one place, plain-word execution — instead of four
  cadences asking separately.
- **It separates actor from auditor.** The fleet audit now reviews work it had
  no hand in.
- **It is already load-tested.** The night shift has run cross-repo from one
  session for a week under the claim protocol; the Manager is that pattern
  promoted from one night a week to the owner's whole day.
- **The repos were built for it.** Every project carries its context in-repo —
  CLAUDE.md, brain, plan, goals — precisely so a competent agent can pick it up
  cold. The Manager is the first full beneficiary of that discipline.

## What this deliberately does not change

The merge gate, draft-only output, owner-only goals files, agents-never-publish,
claim-before-you-build, per-chat history capture, specialist Routines. Where
decisions reach the owner changes; who holds them does not.

## Risks accepted

- **Shallower per-domain context in the Manager** than a specialist chat with
  weeks of history — mitigated by the in-repo context discipline, and by
  specialists remaining for deep work.
- **One conversation carrying the whole fleet** compacts sooner and its
  transcript matters more — mitigated by weekly history capture, named in the
  charter as the Manager's own duty.
- **A collision window remains** between the Manager and a live specialist
  session; the claim protocol has mediated the identical case since 2026-07-26.
