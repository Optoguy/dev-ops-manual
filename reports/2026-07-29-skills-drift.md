# Skill drift report — 2026-07-29

**Source of record:** `dev-ops-manual` @ `ddad547` (`origin/main`), 24 files under
`skills/`. Last change under `skills/`: `b2e99af`, 2026-07-28 — *"manual pushes to
nobody; three linked documents cross-linked in HTML."*

**Scope:** the installed `.claude/skills/` copies in SpecBuildr, NewCoEndotest and
medtech-intel-QMSR, each read from that project's default branch, plus the *live*
generator scripts each project actually runs.

**This report changes nothing in any project.** Adopting an update is the
project's own decision, in the project's own session — see
`conventions/house-rules.md`, "This repo never pushes to project repos." The
task's original wording ("open a PR re-installing where they've diverged") was
written before that rule and is superseded by it.

Reproduce with:

```sh
python scripts/skills_drift.py /path/to/SpecBuildr /path/to/NewCoEndotest /path/to/medtech-intel-QMSR
```

---

## Headline

**The fleet is one change behind, and it is the same change everywhere.** Every
divergence found traces to the 2026-07-28 commit that added the HTML-twin rule
and the cross-links between strategy, business plan and task plan. No project has
drifted in the dangerous sense — nobody has locally edited an installed skill and
let it diverge from source. Twenty of 24 files are byte-identical in all three
projects.

One divergence is **not** drift and must not be "corrected": NewCoEndotest's own
generator scripts are a deliberate fork on a different task schema. Details below.

---

## Per project

### SpecBuildr — `origin/main`

23 installed, **20 identical**, 3 behind, 1 missing, 0 unexpected.

| File | Source | Installed | What is missing |
|---|---|---|---|
| `plan-track/SKILL.md` | 149 lines | 106 | The HTML-twin section and the three-linked-documents section |
| `plan-track/assets/build_dashboard.py` | 340 lines | 305 | The cross-link navigation strip (`TRIO`, `render_nav()`, `.nav` styling) |
| `project-init/SKILL.md` | 115 lines | 103 | Scaffolding steps for `render_docs.py`, `STRATEGY.md` and `BUSINESS-PLAN.md` |
| `plan-track/assets/render_docs.py` | 311 lines | *absent* | The markdown-to-HTML renderer itself |

**Already addressed.** Open draft pull request
[#58](https://github.com/Optoguy/SpecBuildr/pull/58) updates all three files and
adds the renderer. Nothing to do here beyond merging it.

**Live script — do not overwrite.** SpecBuildr runs
`scripts/build_dashboard.py`, not the copy under `.claude/skills/`. It is the
source version with the `src/` paths corrected to `scripts/`. A wholesale
re-install would break those paths. Pull request #58 takes the correct approach:
port the navigation feature in, keep the path corrections.

`brain_lint.py` is byte-identical to source.

### NewCoEndotest — `origin/master`

29 installed, **20 identical**, 3 behind, 1 missing, 6 project-owned.

Behind on exactly the same four files as SpecBuildr, for the same reason.

**Declared, not accidental.** Its `CLAUDE.md` pins the installed version to
`dev-ops-manual` commit `ecb67e5` (2026-07-28) and states the manual is a
read-only reference to be adopted on this repo's own schedule. Under the house
rules a project running an older method is a valid state, not drift to be
corrected from outside. This entry is informational.

**Six skills are NewCoEndotest's own** and correctly absent from this repo:
`brain-capture`, `brain-maintain`, `brain-query`, `brain-sync`, `brain-verify`,
`decision`. They predate the portable suite and encode that project's own brain
conventions.

**Its live generator scripts are a deliberate fork, not drift.**
`src/build_dashboard.py` differs from the portable version across ~513 lines
because it reads `brain/_meta/launch-plan.json` — a different schema, with a
different owner vocabulary (`founder` / `agents` / `optoguy` rather than
`me` / `agent`). `src/brain_lint.py` and the two test files under `tests/` are
likewise that project's own. **Re-installing any of these would destroy working
code.** They should never appear in a drift-remediation list.

### medtech-intel-QMSR — `origin/main`

24 installed, **20 identical**, 4 behind, 0 missing, 0 unexpected.

| File | Source | Installed |
|---|---|---|
| `plan-track/SKILL.md` | 149 lines | 131 |
| `plan-track/assets/build_dashboard.py` | 340 lines | 305 |
| `plan-track/assets/render_docs.py` | 311 lines | 250 |
| `project-init/SKILL.md` | 115 lines | 107 |

**One concrete consequence, worth fixing.** This repo was scaffolded on
2026-07-28 and picked up a mid-day copy of `render_docs.py` — the version before
the cross-link navigation was added. Its copy has no `TRIO` table, no `nav()`
function and no `planned` set. Two effects:

1. Rendered pages in this project carry **no navigation between strategy,
   business plan and task plan**, so the house rule that the three documents
   cross-link is silently unmet there.
2. It also predates the fix for the render-order bug, where documents rendered in
   the same pass could not see each other's output files. Adopting the current
   version fixes both at once.

Unlike SpecBuildr, medtech-intel-QMSR's live `scripts/build_dashboard.py` and
`scripts/render_docs.py` are byte-identical to its own installed copies, with no
local path edits — so a straight re-install is safe here.

**Caution on timing.** Open draft pull request
[#1](https://github.com/Optoguy/medtech-intel-QMSR/pull/1) rewrites that repo's
task list and adds four documents, and it tracks this exact gap as
`render-docs-generator`. Adopting the update should happen after that pull
request lands, in that project's own session, or the two will collide.

---

## What this says about the process

- **The guard is working.** The failure this repo exists to prevent — an installed
  copy quietly edited in place until nobody knows which version is real — has not
  happened. Every difference is "older", none is "changed".
- **Drift is now measurable on demand.** `scripts/skills_drift.py` is committed,
  dependency-free, and runs against shipped branches rather than whatever a local
  clone is sitting on. Worth running whenever `skills/` changes.
- **The check needs a fork list.** A naive "re-install everything that differs"
  reading of this data would overwrite NewCoEndotest's schema-specific generators
  and SpecBuildr's corrected paths. Divergence and drift are different things,
  and the tool reports the first while only a human can classify the second.
- **A worthwhile follow-on:** state in `conventions/house-rules.md` which files a
  project is expected to fork, so the distinction lives in the conventions rather
  than in this report.

## Adoption commands, for reference only

Each of these is run **by that project's own session**, from a `dev-ops-manual`
clone, when that project decides to adopt:

```sh
./install.sh --repo /path/to/SpecBuildr           # covered by SpecBuildr #58
./install.sh --repo /path/to/medtech-intel-QMSR   # after medtech #1 lands
./install.sh --repo /path/to/NewCoEndotest        # only if it chooses to unpin from ecb67e5
```

After installing, that project copies `plan-track/assets/render_docs.py` to its
own `scripts/` (or `src/`) location and re-renders, per the plan-track skill.
