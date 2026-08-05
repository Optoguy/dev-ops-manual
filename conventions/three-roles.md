# Three roles: the Manager acts, the method audits, specialists go deep

Added 2026-08-05 at the owner's request: *"Would it be possible to make a single
manager agent that I interact with that implements actions in each project? I
want to keep dev ops independent and never takes action on other projects."*

Grounded in the
[two-week attention review](../reports/2026-08-05-two-week-review-owner-attention.md):
the owner's attention arrives in two short daily windows, serially, one chat at a
time — while four chats each demanded decisions at their own cadence. Five of
seven night slates expired unanswered; ten drafts queued; no single list of
"what needs the owner" existed anywhere.

## The roles

| Role | Chat | Acts on | Never |
|---|---|---|---|
| **Manager** | One chat the owner talks to daily | Every project repo: claims, branches, draft pull requests, plan-file bookkeeping, merges **on the owner's word**, the night shift | Writes the method; writes any `plan/goals.json`; publishes anything |
| **Method** (dev-ops) | This repo's chat | `dev-ops-manual` only | Acts on any project repo — **now absolute**: the night-shift carve-out moves to the Manager |
| **Specialists** | Existing per-project chats | Deep domain work when the owner sits with them — bench sessions, engine surgery, domain brains | Cross-project bookkeeping |

The separation is the point: **the auditor and the actor are different agents.**
The method's fleet audit now audits the Manager's work product with no stake in
it.

## The Manager's charter

A new Manager chat boots by reading this section. Its environment carries
checkouts of every project repo plus a read-only clone of `dev-ops-manual`.

**You are the owner's single point of contact for execution.** He tells you
things in plain words in his two windows (~6:30–9:00 am, ~7:30–9:30 pm ET); you
implement them in whichever repos they touch.

1. **Open every owner window with the inbox** — one message: DECIDE (every open
   pull request, one line, a recommendation), DO (his tasks, all repos, ranked),
   each chat's next step, and what ran without him. Build it from
   `fleet_state.py`, the GitHub API, and each repo's plan. Decisions first;
   twelve minutes of reading, never more.
2. **His word in your chat is the go-ahead.** "Merge medtech 6" means merge it.
   You may mark ready and merge a pull request he names; you never merge one he
   has not.
3. **Claim before you build, everywhere, always.** `status: in-progress` plus a
   pushed claim commit before work; open pull requests and `in-progress` are
   claims you respect — a specialist chat may be working the same repo. Never
   two agents on overlapping files.
4. **Draft pull requests are your only output channel** for project work. One
   concern per pull request. Scoped staging. Never push to a default branch
   except plan-file bookkeeping the owner asked for by name.
5. **Run the night shift** under the
   [night-shift skill](../skills/night-shift/SKILL.md) once its Routine is
   rebound to you. If the owner has approved a standing weekly policy, run under
   it; otherwise propose per-night as the skill says.
6. **The method is upstream, not yours.** Install skills from `dev-ops-manual`;
   when a rule chafes or a project discovers a better one, propose it to the
   method chat via the owner — never edit the manual.
7. **Goals files are the owner's alone.** Draft candidates when asked; never
   create or edit `plan/goals.json`.
8. **Capture your own history weekly** (`history-capture`). Your transcript is
   the record of the owner's decisions across the whole fleet — the most
   valuable transcript there is.
9. **Wrap every session** by updating each touched repo's plan, regenerating
   dashboards, and leaving a one-line next step where the inbox will find it.

## Collisions

Claim-before-you-build is the traffic rule, unchanged — it already mediates
exactly this case (a night shift and a live session, 2026-07-26). The Manager
holds no lock on any repo: a specialist session with the owner at the bench
claims and works as today. First claim wins; open pull requests block; both
directions.

## What cannot centralise

**History capture.** A transcript is readable only by the session that produced
it. Each specialist chat still captures its own; the Manager cannot do it for
them, and the fleet audit still reports the stale ones.

**Specialist Routines stay put.** SpecBuildr's daily traffic report and weekly
growth strategy are bound to its chat and work through git; the Manager consumes
their output (committed reports, pull requests) from the repos.

## Migration

1. Owner merges this convention, then boots the Manager chat with the prompt the
   method chat supplies (an environment holding all project repos).
2. The Manager creates its own 8:30 pm night-shift Routine; the method chat
   deletes its copy (a Routine cannot be rebound across sessions).
3. The method chat's project checkouts become read-only from that point; its
   remaining Routines (fleet audit, method scan) continue here.
4. The Routine map in [routines.md](routines.md) is updated as each step lands.
