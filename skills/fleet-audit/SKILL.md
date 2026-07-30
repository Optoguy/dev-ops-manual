---
name: fleet-audit
description: Audit every project at once and return a short ranked list of findings with recommendations — what is drifting, stalled, contradicting a convention, or waiting on the owner. Deliberately brief and actionable. Use for a regular cross-project audit, when asked how all the projects are doing, or as the prompt for a scheduled audit Routine.
---

# Fleet audit — all projects, five findings

Owner instruction, 2026-07-30: *"Dev ops must do regular audits of all projects
and share concise actionable findings and recommendations."*

**The gap this fills.** Every other check looks at one slice from inside one
project: the drift check compares skill copies, the night shift sweeps for
available tasks, the weekly review reads one plan. **Nothing looks across the whole
fleet and says "here are the five things worth your attention."** A project can be
individually healthy and collectively wrong — three projects each waiting on the
same owner decision is one finding, not three.

## The brevity rule, first

**At most five findings. Ranked. Each with a recommendation and an owner.**

This is the constraint that makes the audit useful rather than another document.
An audit that lists everything it noticed has moved the sorting work back onto the
owner, which is the opposite of the point. If there are eleven things wrong, the
job is to decide which five matter — and to say plainly that six were left out and
where they are recorded.

**Never paste the raw state dump into the report.** `fleet_state.py` output is
input to your judgment, not the deliverable.

## Procedure

### 1. Collect the mechanical state

```sh
python src/fleet_state.py <each project path> …
```

Per project, from its **default branch**: whether goals exist and the gate is
clear, whether the ladder is intact, task counts by owner and priority, tasks with
no goal or no justification, days since the last commit, and the installed method
version. It deliberately does not judge.

Then add what a script cannot know:

- **Open pull requests** per project — number, title, age, draft or ready, and
  whether any two touch the same files.
- **Skill drift** — `python src/skills_drift.py <projects>` if this repository
  holds the method.
- **Anything the project's own conventions require** that is checkable: its lint
  gate, its `--check` targets, its tests.

### 2. Look for the five patterns that only show up across projects

This is where the audit earns its existence. Single-project reviews cannot see
these:

| Pattern | What it looks like |
|---|---|
| **A shared blocker** | Two or more projects waiting on the same owner decision, credential, or purchase. One finding, not three — and the highest-leverage thing in the report. |
| **A convention that nobody follows** | The same rule unmet in every project. That is a defect in the rule, not in three projects. Propose changing or deleting it. |
| **Divergence that should be shared** | One project solved something the others still suffer. The fix belongs in the method, not in one repo. |
| **Silent stalls** | A project with no commits for longer than its own cadence implies, or in-progress work older than a week. Say whether it is blocked, deprioritized, or forgotten — three different problems. |
| **Ladder mismatch** | A project whose month or week goal no longer serves its end goal, or whose most valuable recent work was labelled as serving no goal at all. |

### 3. Rank by what it costs to leave alone

Not by severity in the abstract. A cosmetic problem blocking three projects
outranks a serious one blocking nothing this month. For each candidate finding ask:
**what does another two weeks of this cost?** Findings that cost nothing are not
findings — they are notes, and they go in the "also seen" line.

### 4. Write each finding as four lines, maximum

- **What** — one sentence, naming the project or projects.
- **Evidence** — the number, file, or command output. Never "it seems".
- **Recommendation** — the specific next action, and **who owns it** (owner or
  agent). Agent recommendations carry the goal they would serve.
- **Cost of waiting** — what another two weeks does. If nothing, cut the finding.

### 5. Verify before reporting

The audit's authority is that its numbers are real. Every claim traces to a command
output or a file, quoted. **A single wrong number destroys the report's usefulness
more than a missing finding does** — and the temptation is to state a pattern
confidently because the pattern feels right.

Re-check anything surprising. "Every project is behind" is exactly the kind of
claim that is either the most important line in the report or an artifact of
running the collector against the wrong branch.

## Output

`reports/<date>-fleet-audit.md`, with its web-page twin. Structure:

1. **One line per project** — a table: gate, open work, last commit, one word of
   state. This is the "is anything on fire" glance.
2. **The five findings**, ranked, four lines each.
3. **Also seen** — one line, listing what was left out and where it is recorded.
   This is what makes the brevity honest rather than a silent truncation.
4. **What the owner should do first** — a single item. Not a list.

Then the options menu, per the house interaction rules. Deliver as a file.

**An audit with nothing to report is a valid and welcome outcome.** Say so in two
lines. Do not manufacture five findings to fill the shape.

## Cadence

**Weekly** is the default — frequent enough that a stall is caught while it is
still a week old, rare enough to stay short. Pair it with, and run it before, each
project's own weekly review: the fleet view says which project deserves the
attention this week.

Suits a Routine (see [routine-design](../routine-design/SKILL.md)), firing into a
persistent session so the findings can be put to the owner as a menu.

## Judgment

- **Five findings is a ceiling, not a target.** Three good ones beat five padded.
- **A shared blocker is always the lead finding when one exists.** It is the only
  kind where one action from the owner unblocks several projects at once.
- **Never audit and fix in the same pass.** The audit reports; fixing is separate,
  claimed, and approved. An auditor who also patches has no independent view of
  whether the patch was needed.
- **Name projects, not people.** There is one person; blame is noise.
- **When a convention is unmet everywhere, suspect the convention.** Three
  independent failures of the same rule is evidence about the rule.
- **Report your own repository too.** The method's own repo is the easiest to
  exempt and the most damaging to leave unaudited.
