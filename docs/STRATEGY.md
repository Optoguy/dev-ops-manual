# Strategy — Dev Operating Manual

**Draft for review, 2026-07-30.** The end goal below is the one the monthly and
weekly goals must ladder up to, so it is the owner's to confirm or rewrite.

## Why this repository exists

Dan runs several ventures alone, with agents doing most of the building. The
bottleneck is not agent capability. It is that **method learned in one
conversation is lost to the next one.**

Every chat starts from nothing. Without a written method, each one re-derives how
tasks are tracked, re-argues whether generated files are hand-edited, re-discovers
that two sessions can build the same thing in parallel, and re-learns it the
expensive way. Four repositories multiply that by four.

This repository is the memory. It is the only place where "how work happens" is
written down once and installed everywhere.

## The end goal

> **Any chat, in any project, works the way Dan works — without Dan having to
> explain it again.**

**What would make that true:**

- A chat that has read only this repository can scaffold a new project and run it
  correctly, without asking how any of it works.
- No rule has to be explained twice. When one is broken, the fix is a written
  rule with a mechanical check, not a reminder.
- The owner's time goes to **decisions** — what to build, what it is worth, who
  it is for — rather than to process, review of process, or repeating himself.

**Horizon:** ongoing. This is a standing capability, not a milestone with a date.
It can be lost as easily as it is built, which is why it is reviewed rather than
declared finished.

## The wedge

Not "documentation." Documentation is read once and rots. Three things make this
different, and each exists because something broke:

1. **Skills, not prose.** The method is installed as executable skills a chat
   loads automatically, so following it is the path of least resistance rather
   than an act of discipline.
2. **Mechanical checks over good intentions.** Every rule that matters has a
   command that fails: `goal_gate.py`, `build_dashboard.py --check`,
   `skills_drift.py`, `git diff --stat` on the plan file. A rule with no check is
   a suggestion, and suggestions decay within a month.
3. **Scar tissue attached.** Each convention names what broke, and when. Rules
   are followed when the reader can see the wreck that produced them.

## What is genuinely undecided

- **Whether this earns its keep.** The method has cost real hours this month. It
  has prevented duplicate work at least once, and caught a claim-detection bug
  that would have degraded every night shift. That is suggestive, not proof.
- **Whether the ceremony scales down.** Four repositories and one person is a
  small fleet. Goals, gates, reviews and adoption prompts are cheap to write and
  not free to live with. If a month goes by where the process produces more
  reading than deciding, the honest response is to cut it back, not to add to it.
- **Whether the manual becomes the project.** The clearest failure mode: this
  repository is interesting to work on, and the ventures it serves are harder. If
  a month's goals are still about the manual rather than about a venture shipping,
  that is the finding.

## Related documents

- [Task plan](../dashboard/index.html) — what happens next, and who owns it.
- [Goals and status](../dashboard/goals.html) — the current ladder and where the
  numbers stand.
- [House rules](../conventions/house-rules.md) — the operating contract itself.
