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
| 2 | **Continuous improvement** — regular external research bringing in new methods of distributed agent work and agent-human collaboration | **Not built.** Nothing in the method looks outward on any cadence. |
| 3 | **Regular audits of all projects** — concise, actionable findings and recommendations | **Barely built.** The skill drift check and the nightly sweep look at narrow slices. There is no cross-project audit that produces findings and recommendations. |
| 4 | **Clear communication that saves the owner's time** | **Partly built.** Plain-language rules, buttons over prose, a written options list on every reply, deliverables as files. Never measured. |

**Two of the four are gaps, and naming them is the most useful thing this document
does.** An end goal that describes responsibilities the method cannot discharge is
a plan, not a description — and it should be read that way until they exist.

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

## The two missing capabilities, described

Written here rather than invented as tasks, because adding them to the plan is the
owner's call.

**Regular external research.** Someone or something has to read outside this
system on a cadence and bring back what is worth adopting — how other people run
fleets of agents, what patterns have emerged for agent-human handoff, what is
being learned about unattended work, review, and trust. Report-first, as
candidates with evidence, never as automatic changes to the method. Without a
cadence this happens only when something fails, which means the method only ever
learns from its own accidents.

**A cross-project audit.** Regular, all projects at once, producing a short list:
what is drifting, what is stalled, what contradicts a convention, what the owner
is blocking, and what should change. The existing pieces — the drift check, the
nightly sweep, the weekly review — each look at one slice from inside one project.
Nothing looks across the whole fleet and says "here are the five things worth your
attention this week."

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
