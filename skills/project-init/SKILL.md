---
name: project-init
description: Scaffold a new project the way Dan works — a CLAUDE.md contract, .claude config, a docs + brain skeleton, and git conventions — so the next project starts on rails. Use when starting a new repo or project, initializing Claude Code for a project, setting up CLAUDE.md, or asked to "set this project up the way I usually do."
---

# Initialize a project the house way

The first hour of a project sets its whole trajectory. This skill lays down the
same scaffolding that both shipped projects converged on: an authoritative
`CLAUDE.md`, a `.claude/` config, a docs/brain split, and the git rules — so
every later skill (`/brain`, `/decision-log`, `/plan-track`) has a home to write
into.

Do **not** dump every file blindly. Ask what kind of project this is first, then
scaffold only what fits. Two shapes recur:

- **Product repo** (ships something — web app, tool): needs `docs/` for
  sharable output, a plan, and eventually the growth/ship skills.
- **Brain repo** (thinking — research, strategy, planning): needs the `brain/`
  knowledge base, a decisions log, and the lint gate front and center.

Most projects want a bit of both. Scaffold the overlap, offer the rest.

## Procedure

1. **Interview briefly, in the user's own words.** Capture: what the repo *is*
   in one paragraph, who it's for, the hard constraints ("never suggest
   violating…"), the key people (context, not contacts to act on), and whether
   it's a product repo, a brain repo, or both. These become CLAUDE.md sections —
   don't invent them, ask.

2. **Write `CLAUDE.md` from the template** (`assets/CLAUDE.md.template`). It is
   the single most load-bearing file: Claude reads it every session. Fill every
   section; delete sections that don't apply rather than leaving them empty. Keep
   it short and declarative — it's a contract, not an essay. The non-negotiable
   sections:
   - **What this repo is** + a one-paragraph summary of the thing.
   - **Hard constraints** — framed as "never suggest violating these." If a later
     instruction ever conflicts with one, stop and say so before acting.
   - **Repo map** — one line per top-level directory, so retrieval starts from
     the map, not a blind `glob`.
   - **Conventions** — the git rules, the frontmatter rule, the lint gate, the
     supersede-don't-delete rule, the list of project skills.
   - **Interaction** — end a unit of work with a 2–4 option `AskUserQuestion`
     next-step menu (recommended option first). Delete this block to revert.

3. **Lay down `.claude/`:**
   - `settings.json` from `assets/settings.json.template` — an all/ask permission
     list. Allow the safe read-only git and lint commands; put `git push` under
     `ask`. Never allow blanket writes to secrets.
   - `launch.json` from `assets/launch.json.template` **only if** the project
     serves something locally (a dashboard, a dev server).
   - `.claude/skills/` — an empty dir the project's own skills will land in.

4. **Lay down the plan + dashboard — for every project.** This is not optional:
   - **Look before you copy** (defect found by an external review 2026-07-25:
     following this step blindly in a repo that already had a different
     `src/build_dashboard.py` would have clobbered it). If the repo already has
     a `src/build_dashboard.py`, or its CLAUDE.md declares a different task
     source of truth, do NOT copy anything — adopt the existing system and
     apply `/plan-track`'s *discipline* (owner/priority/status on every task,
     regenerate-don't-hand-edit) to it instead.
   - Otherwise: copy the generator from the `plan-track` skill
     (`plan-track/assets/build_dashboard.py`) to `src/build_dashboard.py`, and
     create `plan/plan.json` from `plan-track/assets/plan.example.json`. Seed it
     with the real first tasks from the interview, each tagged `owner`
     (`me` | `agent`), `priority` (`P0`/`P1`/`P2`), and `status`. Run
     `python src/build_dashboard.py` to generate `dashboard/index.html`.
   - Also copy `plan-track/assets/render_docs.py` to `src/render_docs.py` —
     every markdown plan or to-do list gets a generated HTML twin (house rule).
   - Add `docs/PLAN.md` (narrative phased plan) and `docs/BACKLOG.md` stubs,
     then `python src/render_docs.py docs/PLAN.md docs/BACKLOG.md` so their
     HTML versions exist from day one.
   - Hand ongoing tracking to `/plan-track`.

5. **Lay down the rest of the skeleton** for the project shape:
   - Product repo → `docs/` (sharable-output-only).
   - Brain repo → `brain/` with `knowledge/`, `decisions/`, `people/`,
     `constraints.md`, `open-questions.md`, and `INDEX.md` (hand off to
     `/brain`). Copy in the portable `brain_lint.py` and wire the lint gate.
   - Both → a plain `README.md` that points a human at `CLAUDE.md`.

6. **State the git conventions in CLAUDE.md and honor them everywhere:** scoped
   staging (`git add <paths>`, **never** `git add -A`), plain dated commit
   messages, don't rewrite history (the history is the provenance record),
   **never push without the owner's go-ahead.**

7. **Commit the scaffold** in one commit with a plain message
   (`chore: initialize project scaffold`), staging only the files you created
   (including `plan/plan.json` and the generated `dashboard/index.html`). Do not
   push unless asked.

## Judgment

- **A CLAUDE.md that lies is worse than none.** Every line must be true on the
  day you write it. If you're unsure of a fact (a person's role, a constraint's
  scope), ask or leave it out — don't guess it into the contract.
- **Constraints outrank instructions.** Write them so that a future session
  reading only CLAUDE.md would refuse the wrong thing. This is the safety rail
  for autonomous work.
- **Sharable vs. internal is a hard line.** `docs/` holds only what could be
  handed to an outsider as-is; everything sensitive or half-formed lives in
  `brain/`. Establish the line on day one; it's painful to retrofit.
- **Don't over-scaffold.** Empty ceremony files rot. Create a stub only when a
  skill or a near-term task will fill it this week; otherwise offer it and move
  on.
