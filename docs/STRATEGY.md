# Strategy — Dev Operating Manual

**End goal set by the owner, 2026-07-30**, in his own words. Everything below is
written from them.

## The end goal

> **Dan runs more projects in parallel than one person could, because every
> project is operated the same proven way and he is never the bottleneck.**

The owner's statement of it:

> *Dev ops goal is to ensure all my projects are operated consistently and that
> best practices are developed and shared to every project. Dev ops is responsible
> for continuous improvement, doing regular external research to bring in new
> methods of distributed agent work and agent-human work systems and
> collaboration. Dev ops must do regular audits of all projects and share concise
> actionable findings and recommendations. Dev ops must ensure that human
> communication is clear and saves the time of the founder and allows the founder
> to expand his reach through parallel projects run via agents.*

**Reach is the point. The rest are the means.** Consistency, shared practice,
imported methods, audits and clear writing all exist so that adding a fourth or
fifth project costs the owner attention he actually has.

## Four responsibilities

| # | Responsibility | State today |
|---|---|---|
| 1 | **Consistency** — every project operated the same proven way, best practices developed here and shared to all | **Partly built.** Skills, conventions, decisions, a drift check, and per-project adoption prompts. |
| 2 | **Continuous improvement** — regular external research bringing in new methods of distributed agent work and agent-human collaboration | **Built 2026-07-30**, not yet scheduled. The `method-scan` skill: monthly, report-first, five standing questions, a "what breaks today that this fixes" filter, and recorded discards. |
| 3 | **Regular audits of all projects** — concise, actionable findings and recommendations | **Built 2026-07-30**, not yet scheduled. The `fleet-audit` skill plus `fleet_state.py`: weekly, all projects at once, capped at five ranked findings each with a recommendation and an owner. |
| 4 | **Clear communication that saves the owner's time** | **Partly built.** Plain-language rules, buttons over prose, a written options list on every reply, deliverables as files. Never measured. |

**All four now have a mechanism.** Two of them were gaps when this document was
first written on 2026-07-30 and were built the same day; **neither is scheduled
yet**, which is the remaining step. A capability that exists but never runs is
indistinguishable from one that does not exist.

## What would make the end goal true

- **Consistency:** a rule learned in one project reaches all of them, and a chat
  that has read only this repository can run any project correctly without asking
  how it works.
- **Improvement:** new methods for agent and agent-human work arrive on a
  deliberate cadence from outside, not by accident when something breaks.
- **Audits:** every project is audited regularly, and each audit lands as a short
  list of findings with recommendations the owner can act on or dismiss in
  minutes.
- **Communication:** the owner's time goes to decisions. No rule has to be
  explained twice. **And the count of projects he can run in parallel goes up
  while his hours do not.**

**Horizon:** ongoing. This is a standing capability, not a milestone. It can be
lost as easily as built, which is why it is reviewed rather than declared
finished.

## The wedge

Not "documentation" — documentation is read once and rots. Three things make this
different, and each exists because something broke:

1. **Skills, not prose.** The method installs as executable skills a chat loads
   automatically, so following it is the path of least resistance rather than an
   act of discipline.
2. **Mechanical checks over good intentions.** Every rule that matters has a
   command that fails: `goal_gate.py`, `build_dashboard.py --check`,
   `skills_drift.py`, `git diff --stat` on the plan file. A rule with no check is
   a suggestion, and suggestions decay within a month.
3. **Scar tissue attached.** Each convention names what broke, and when. Rules get
   followed when the reader can see the wreck that produced them.

## The two capabilities built on 2026-07-30

**Regular external research — [`method-scan`](../skills/method-scan/SKILL.md).**
Monthly, report-first. Five standing questions (how others run agent fleets, how
handoff is structured, what is known about unattended work, how agent output is
reviewed, how a method is kept from rotting), each mapped to something the house
method already does so a finding lands somewhere. Every candidate must answer
**"what breaks today that this would fix"** or it is discarded however elegant —
that filter is what stops the method bloating, since every rule costs every future
session reading and compliance. Discards are recorded so they are not re-found.
Without a cadence, the method only ever learns from its own accidents.

**A cross-project audit — [`fleet-audit`](../skills/fleet-audit/SKILL.md).**
Weekly, all projects at once, **capped at five ranked findings**, each four lines:
what, evidence, recommendation with an owner, and the cost of waiting. The cap is
the point — an audit that lists everything has pushed the sorting back onto the
owner. It hunts the five patterns single-project reviews cannot see, chief among
them a **shared blocker**: two or more projects waiting on the same decision is one
finding, not three, and the highest-leverage line in any report.
`fleet_state.py` collects the mechanical half; judgment is the agent's.

**Neither is scheduled yet.** That is the next step, and it is the owner's call.

## What is genuinely undecided

- **Whether reach is measurable.** The end goal's real test is *projects run in
  parallel without the owner becoming the bottleneck.* Today that number is four
  and there is no honest way to attribute it to the method. Until there is, the
  monthly goals will measure proxies, and proxies drift from the thing.
- **Whether the ceremony scales down.** Four repositories and one person is a small
  fleet. Goals, gates, reviews and adoption prompts are cheap to write and not
  free to live with. If a month produces more reading than deciding, cut it back
  rather than adding to it.
- **Whether the manual becomes the project.** The clearest failure mode: this
  repository is interesting to work on and the ventures it serves are harder. If a
  month's goals are still about the manual rather than about a venture shipping,
  that is the finding.
- **Whether the current monthly goal is too narrow.** August is "every project
  runs on goals" — one part of responsibility 1, and nothing of 2, 3 or 4. It is a
  defensible first step, but it is not a description of the job.

## Related documents

- [Goals and status](../dashboard/goals.html) — the current ladder and where the
  numbers stand.
- [Task plan](../dashboard/index.html) — what happens next, and who owns it.
- [House rules](../conventions/house-rules.md) — the operating contract itself.
