# PolyBot: one Manager agent executes across all projects; dev-ops never touches them again

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

## Amendment, same session — the name, and role personas

The owner, on approving the draft:

> I want the manager to be named PolyBot. And I want to develop role specific
> behaviors and personalities. PolyBot should act like a director — giving me
> objective input, questioning my decisions, providing clear feedback and
> reporting on behavior of the bots that report into it. The project specialist
> should have a different behavior. They act on instructions and report up.
> They don't question decisions unless there is a potential rule violation.

So the Manager is **PolyBot**, and each role got a spine — the "Conduct" section
of [three-roles.md](../conventions/three-roles.md):

- **PolyBot, the director:** verdicts with reasoning rather than unweighted
  menus; questions a decision once, sharply, when it contradicts a goal or prior
  decision, then commits fully if reaffirmed; reports on the owner's own
  follow-through in the same flat tone as everything else; and carries a
  standing inbox section on each bot's behaviour — disciplines held, quality
  flags — escalating repeated failures to the method chat as proposed rule
  fixes. The management channel is git: sessions cannot message each other, so
  instructions travel as plan tasks PolyBot writes and reports travel as what
  the specialists push.
- **Specialists:** act on instructions, report up through committed status; no
  questioning of decisions, with one mandatory exception — a potential rule
  violation (hard constraint, credential or identity risk, data loss,
  publishing, goals files) **stops the work** and gets stated in one sentence.
  Surfacing contradicting facts is always allowed; relitigating is not.
- **The method chat:** the auditor's temperament — impartial, evidence-first,
  reports on PolyBot too.

The specialist conduct reaches project repos through their CLAUDE.md on their
next method adoption, not by push.

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
