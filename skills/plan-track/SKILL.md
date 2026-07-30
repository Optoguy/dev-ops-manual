---
name: plan-track
description: Give a project a plan and a prioritized dashboard — a single-source plan.json where every task carries an owner (me|agent) and a priority (P0|P1|P2), plus a generated dashboard that shows your tasks and the agent's tasks separately, ranked. Use when planning a project, sequencing or prioritizing work, writing/updating a plan, tracking tasks, setting up a dashboard, or deciding what to do next.
---

# Plan and track work

**Every project gets a plan and a dashboard.** Tasks live in one machine-readable
source of truth (`plan/plan.json`); a dependency-free generator renders a
dashboard (`dashboard/index.html`) that ranks work by priority and splits **your**
tasks from **the agent's** tasks. Edit the JSON, regenerate the HTML — never the
other way around. A narrative `docs/PLAN.md` carries the "why"; the JSON carries
the "what/who/when."

**If the repo already declares a task source of truth, use THAT.** Check
CLAUDE.md first: a repo may keep its tasks in a different file with a different
schema (e.g. a `launch-plan.json` with `owner: founder|agents|...` and no
status field). In that case this skill's *discipline* applies — every task
carries an owner and a priority signal, generated views are rebuilt never
hand-edited, claims are pushed before building — but its *files* do not: never
create a parallel `plan/plan.json`, never overwrite an existing generator.
(Defect found by an external review 2026-07-25: this file previously said
`plan/plan.json` unconditionally, contradicting a repo whose CLAUDE.md forbids
exactly that.)

## The single source of truth — `plan/plan.json`

Start from `assets/plan.example.json`. Every task carries:

| Field | Values | Meaning |
|---|---|---|
| `owner` | `me` \| `agent` | Who does it. **me** = the human owner; **agent** = Claude. |
| `priority` | `P0` \| `P1` \| `P2` | P0 = must / blocks other work · P1 = strong · P2 = nice-to-have |
| `status` | `todo` \| `in-progress` \| `blocked` \| `done` | Current state |
| `phase` | a phase id | Optional; groups tasks under a phase |
| `goal` | a goal id, or `keeping-the-lights-on` | Which goal this serves. Required on open tasks. |
| `justification` | text | One line naming the **measure** it moves. Required unless the goal is `keeping-the-lights-on`. |
| `blocked_by` | `[task-id, …]` | Optional; what must finish first |
| `note`, `done_date` | text / date | Optional context |

Phases (optional) give the plan an arc: each has `id`, `title`, `goal`, and a
`deliverable` (what "done" looks like).

**Edit the file in place — never reformat it.** A status change is a one-line
diff. `json.load` followed by `json.dump(..., indent=2)` rewrites every task in
the file and turns a two-line change into a three-hundred-line one; the content
survives but the review doesn't, and every other open branch touching the plan
now conflicts. Change the matching line with a targeted edit, then check before
committing:

```sh
git diff --stat plan/plan.json   # a claim or a completion touches 2-4 lines
```

If the diff is large, you reformatted — discard and redo it as a line edit.
Reformatting deliberately is fine as its own commit that changes nothing else.

## Goals — `plan/goals.json`

**A plan without goals is a list of things somebody felt like doing.** Goals are
a **ladder of three**, each level serving the one above:

| Level | Answers | Scored? |
|---|---|---|
| **End goal** | Why are we doing this project at all? | Reviewed, not scored |
| **Monthly** | What must be true this month to get closer? | Against a number |
| **Weekly** | What must happen this week to serve the month? | Against a number |

The end goal is the **strategy document's answer in one sentence**, restated in
`plan/goals.json` so the ladder can be rendered and checked; it carries `goal`,
`why`, `success` (what would have to be true — checkable, not necessarily a
number), `horizon`, `strategy` (the path back to the document) and `reviewed`.
It has no measure and no progress bar: a bar on a multi-year ambition is fake
precision. Report it stale after 90 days; **never block on it.**

**Each level names what it serves** — the month sets `"supports": "end"`, the week
sets the month's id. A broken ladder blocks, because a month goal that supports
nothing above it means the project is busy on something that leads nowhere.

The owner sets all three. Full convention:
[goals-and-measures.md](../../conventions/goals-and-measures.md). Start from
`assets/goals.example.json`.

```json
{
  "end":   { "goal": "why this project exists, in one sentence",
             "why": "who it is for", "success": "what would have to be true",
             "horizon": "roughly when", "strategy": "docs/STRATEGY.md",
             "reviewed": "2026-07-30" },
  "month": { "id": "2026-08", "supports": "end", "goal": "…",
             "measure": {"name": "…", "baseline": 0, "target": 5,
                         "unit": "people", "as_of": "2026-07-29",
                         "source": "where the number comes from"} },
  "week":  { "id": "2026-W31", "starts": "2026-07-29", "supports": "2026-08",
             "goal": "…", "measure": { … } },
  "history": []
}
```

Four things make a measure real: a **baseline**, a **target**, an **as_of** date,
and a named **source**. If nobody can produce the number today, it is not a
measure — say so, and make producing it the first task.

**Every open task names the goal it serves and how it moves that goal's
measure.** The justification names the measure and the direction, not the goal's
title: *"Moves completed-specs-per-week, which is at 0"*, not *"supports the
August goal."* Work that genuinely serves no goal is labelled
`"goal": "keeping-the-lights-on"` — security, breakage, legal, forced platform
changes. That answer is legitimate and carries no penalty; **inventing a
justification is the failure mode, not admitting there isn't one.**

`assets/build_goals.py` (drop it at `src/build_goals.py`) generates
**`dashboard/goals.html`** — a clean goals-and-status page: each goal with a
baseline → now → target meter, the work serving it, the work serving no goal,
and the finished-goal history with outcomes. The optional `current` field on a
measure is what the meter reads; without it the page says "not measured yet"
rather than implying progress. The page is deterministic — elapsed and remaining
days are computed in the browser from embedded dates, so `--check` keeps meaning
"you forgot to rebuild".

`build_dashboard.py` renders the goals at the top of the page and **fails
`--check`** on a missing end goal, a broken ladder, a missing or weak measure, or
an unjustified task. A project that has not adopted goals fails its own build
check, and that is the intended pressure rather than a bug — the first permitted
work there is writing `plan/goals.json`. The one exception is an *ageing* weekly
goal, which is reported and stays advisory: a report that fails a build is a block
by another name.

## The gate — run it before you start

`assets/goal_gate.py` (drop it at `src/goal_gate.py`) is the stop:

```sh
python src/goal_gate.py                # may work proceed in this repo at all?
python src/goal_gate.py --task <id>    # may work proceed on THIS task?
```

Exit `0` = clear; exit `1` = blocked, with the reasons and the permitted
alternatives printed. It blocks on a missing goals file, a missing or unmeasured
goal, a measure without a baseline / target / date / source, a target not above
its baseline, or a weekly goal older than **fourteen** days. `--task` also blocks a task
that names no goal, names one no longer current, or carries no justification.

`build_dashboard.py --check` fails on the same conditions, so a repo that has not
adopted goals fails its own build check. That is the intended pressure: the first
permitted work is writing `plan/goals.json`.

**The weekly goal's age is reported on every run, clear or blocked.** A weekly
goal is meant to last seven days and blocks at fourteen. In between, the gate
stays clear and says `AGEING`, with how many days remain before it blocks — a
softened deadline that says nothing is just a longer silence. Surface that report
to the owner rather than swallowing it, and offer the goal review.

**Three things are always permitted**, or the rule deadlocks — you could not fix
the goals file, because fixing it would be work:

1. Setting or updating the goals, and running the goal review.
2. `keeping-the-lights-on` work. **This outranks the gate**: such a task is
   permitted even in a repo with no goals file at all.
3. Answering the owner. Conversation is not work.

## The dashboard — `dashboard/index.html`

Generated by `assets/build_dashboard.py` (drop it at `src/build_dashboard.py`).
It renders, self-contained and offline:

- **A "Next up" band** — the highest-priority open tasks across both owners, so
  the single most important thing is always at the top.
- **Two columns — 🧑 Your tasks / 🤖 Agent tasks** — each grouped P0 → P1 → P2,
  done items collapsed at the bottom.
- **Completion metrics** — done/total, in-progress, blocked, and per-owner counts.

Rebuild with `python src/build_dashboard.py`; check freshness in CI or a
pre-commit with `python src/build_dashboard.py --check`.

## Markdown plans get an HTML twin

**Every plan or to-do list that exists as markdown also exists as HTML.**
`docs/PLAN.md`, `BACKLOG.md`, `ROADMAP.md`, `OWNER-TASKS.md`, a launch plan, a
content plan, any checklist — each gets a generated `.html` sibling, so it can
be opened and read anywhere without a markdown viewer.

```
python src/render_docs.py docs/PLAN.md docs/BACKLOG.md   # writes docs/*.html
python src/render_docs.py --check docs/*.md              # nonzero if stale
```

`assets/render_docs.py` (drop it at `src/render_docs.py`) is dependency-free
and emits self-contained HTML — inline CSS, no external assets, no JS, so it
opens offline and survives a strict CSP. It renders headings, nested lists,
**task checkboxes** (`- [ ]` / `- [x]`), tables, code, blockquotes, and links
(rejecting `javascript:`/`data:` schemes), and follows the reader's light/dark
preference.

The markdown is the source; **the HTML is generated and never hand-edited** —
same contract as the dashboard. Render and commit both in the same commit, or
the pair goes stale and the HTML starts lying.

## The three linked documents

Every project answers three questions in writing, and each answer links to the
other two: **strategy** (`docs/STRATEGY.md` — why this exists and what the
wedge is), **business plan** (`docs/BUSINESS-PLAN.md` — how it makes money and
what must be true), and **task plan** (`plan/plan.json` → `dashboard/index.html`
— what's next and who owns it).

Cross-linking is automatic: `render_docs.py` puts a nav strip on every page it
renders and `build_dashboard.py` puts the same strip on the dashboard. Each
links to whichever of the trio exist and marks the current one, so a project
without a business plan yet shows fewer chips instead of a dead link — write
the file and the links appear on the next render.

Keep them honest together. A strategy change that leaves the task plan
untouched is usually a strategy nobody is executing; the links exist to make
that visible.

## Procedure

1. **Create/refresh `plan/plan.json`.** Break the work into tasks; give each an
   **owner**, a **priority**, and a **status**. Add phases if the project has a
   real arc. If the project already has prose plans, mine them into tasks — the
   JSON becomes the source, the prose stays narrative.

2. **Prioritize honestly.** P0 is reserved for *must-happen / blocks-other-work* —
   if everything is P0, nothing is. A task that blocks others (or that only the
   human can unblock) usually earns P0. Record real blockers with `blocked_by`
   so the ordering reflects reality, not hope.

3. **Split ownership honestly — the important one.** Agents do the work with no
   name attached: build, measure, analyze, draft, refactor. The **owner** (`me`)
   does anything that carries identity or reaches outside the repo: API keys and
   dashboards, spend caps, legal/entity/disclosure, posting under their own name,
   and **pushing to git**. The dashboard's separation is the payoff — at a glance,
   the human sees exactly which of *their* actions are gating everything, and an
   agent sees everything it can do without waiting.

4. **Keep the narrative in `docs/PLAN.md`** (optional but recommended): phased,
   each phase ending in a **Deliverable** line, with a "Suggested sequence" (Done
   / Now / Then / After). And a value-ordered `docs/BACKLOG.md` for things
   identified but not yet scheduled — when a backlog item is picked up, it becomes
   a task in `plan.json`.

5. **Regenerate after every change.** `python src/build_dashboard.py` for the
   plan, and `python src/render_docs.py <changed>.md` for any markdown plan or
   to-do list you touched. Commit each source and its regenerated HTML
   together, scoped staging, plain dated message, no push. A dashboard — or an
   HTML plan — that disagrees with its source is worse than none.

## Judgment

- **Blocked-on-owner is the most valuable thing the dashboard surfaces.** Put
  those P0 and keep the note sharp ("everything downstream waits on this") — it's
  the difference between an agent that stalls and one that works the whole
  non-blocked frontier while the human clears the gate.
- **Defer explicitly.** When you choose not to do something yet, keep it as a P2
  `todo` with a note on *what would change the answer* ("after R1 confirms
  value"), or park it in `BACKLOG.md`. Silent drops lose good ideas.
- **Adjustment rules should be boring and explicit** so a scheduled agent can
  apply them without a judgment call: "promote to P0 anything blocking two+
  tasks; drop any P2 untouched for a month to the backlog."
- **A stale plan is worse than no plan** because people trust it. When work lands,
  update status and regenerate before starting anything new.
- **`in-progress` is a claim, not a courtesy.** When more than one worker can touch
  the plan — e.g. a live session and a nightly Routine — set a task `in-progress`
  (with a `claimed <date> <who>` note) and push it *before* you build, and never
  start a task that is already `in-progress`. This is the mechanism that stops two
  workers doing the same task (learned 2026-07-26; see the project's
  `claim-before-you-build` decision).
