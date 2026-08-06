# Monthly method audit — 2026-08-01

Inward half of the monthly scan: which conventions are followed, which are quietly
ignored, which contradict each other, and which have a rule but no mechanical
check. Report only — nothing here changes a convention.

Ranked by the 2026-07-30 finding that *a rule with no check has a known
half-life*.

---

## 1. The goal gate's documented command does not exist

`python src/goal_gate.py` is quoted **10 times across 6 files** — `house-rules.md`,
`goals-and-measures.md`, `global-CLAUDE-snippet.md`, and the `night-shift`,
`goal-review`, `project-init` and `plan-track` skills.

There is no `src/` directory in this repository. The gate is at
`scripts/goal_gate.py`, and that is where it sits in **every repository that has
it**:

| Repo | Actual path |
|---|---|
| dev-ops-manual | `scripts/goal_gate.py` |
| SpecBuildr | `scripts/goal_gate.py` |
| medtech-intel-QMSR | `scripts/goal_gate.py` |
| NewCoEndotest | not installed |

So the command that enforces the method's hardest rule — *no work proceeds
without a goal* — fails with "No such file or directory" for anyone who follows
the convention literally. A session that runs it and sees an error can
reasonably conclude the gate is not installed and proceed ungated. The
`night-shift` skill puts this command at **step 0**.

`project-init` is the origin: it instructs new projects to *"copy
`plan-track/assets/goal_gate.py` to `src/goal_gate.py`"*. Nobody did; every
project used `scripts/`. The convention documented the instruction, not the
practice.

**No check exists for this class of error** — nothing verifies that a command
quoted in a convention or skill actually runs. That is the highest-value gap
here, because it is the cheapest to close.

**Proposed check.** A `scripts/doc_commands_check.py` that extracts
`python <path>` invocations from `conventions/` and `skills/` and asserts each
path exists in the repository. Roughly thirty lines, stdlib-only, exits nonzero
on a broken command. Run it against its own repository first, per the
2026-07-30 report.

---

## 2. A deliberate pin can freeze a safety check, and the rule has no exception

House rule: *"a project running an older method is a valid state, not drift to
be corrected from outside."* Correct as written, and both stale projects have
their pin **in writing** — NewCoEndotest at `ecb67e5`, medtech-intel-QMSR at
`b2d436e`. By the rule, neither is drift.

But medtech's pinned `goal_gate.py` is **241 lines against the current 318**.
The missing 77 lines are the end-goal ladder checks. The consequence, verified
today:

```
medtech-intel-QMSR, installed gate:   CLEAR — work may proceed against 2026-W31
medtech-intel-QMSR, current gate:     BLOCKED — there is no end goal
                                      (its own unmerged pull request #6 reports this)
```

Same repository, same data, opposite answers. The repository has no end goal at
all; the pinned gate cannot see that, so it reports safe.

**The gap:** "being behind is valid" treats a prose skill and a check-bearing
script as the same thing. Being behind on `wrap-session/SKILL.md` costs a bit of
polish. Being behind on `goal_gate.py`, `build_dashboard.py` or
`portability_check.py` produces a **false green** — the failure mode this whole
method exists to prevent.

**Proposed change.** `skills_drift.py` already knows which files differ. Have it
separate **check-bearing assets** from prose and report them as
`STALE CHECK — reports pass where current version fails` rather than plain
`behind:`. Reporting only; adoption stays the project's own decision in its own
chat, per the never-push rule. The mechanical check is the classification
itself.

---

## 3. Adoption instructions: a rule with no check, half-ignored

The 2026-07-29 rule requires that every change touching `skills/` ships
**per-project adoption prompts, as files**, written from `skills_drift.py`
output.

Of the four skills added since, two ship no adoption instructions at all:

| Skill | Adoption instructions |
|---|---|
| `fleet-audit` | present |
| `method-scan` | present |
| `history-capture` | **none** |
| `goal-review` | **none** |

No adoption-prompt artifacts exist anywhere in the repository, so whether the
rule was followed for any past change is **unverifiable** — the prompts, if
written, went to chat and are gone. That also makes this rule a candidate for
the other kind of fix: if the prompts are genuinely ephemeral, the rule should
say so rather than requiring an artifact nobody can find.

**Two honest options**, and this is a decision rather than a fix:
either commit the prompts under `adoption/<date>-<project>.md` so their
existence is checkable, or amend the rule to match what is actually done. A
third state — a rule that sounds enforced and is not — is the worst of the
three.

---

## Also true, not recommended for action this month

- **Claims never expire.** SpecBuildr's `adopt-manual-87a24ac` is still
  `status: in-progress` although the pull request that completed it merged on
  2026-08-01. The rule checks that a claim is *set* and never that it is
  *released*. Already proposed in this morning's external scan as the lease
  pattern; not re-proposed here.
- **`portability_check.py` passes by substring.** It reports a binding
  "justified" when its pattern merely *appears* in the convention file, so a
  green `--strict` means *recorded*, not *approved*. Found and documented in
  medtech's pull request #6, unfixed here. It is a check that cannot meaningfully
  fail — the same category as finding 1, one rung less severe because the
  convention text does exist.

---

## The monthly numbers

**Skills drift**, source `origin/main @ a8a650c`, 34 files:

| Project | State | Written pin | Verdict |
|---|---|---|---|
| **SpecBuildr** | 34/34 identical | `87a24ac` | **current** |
| **medtech-intel-QMSR** | 19/28 identical, 9 behind, 6 missing | `b2d436e` | pinned in writing — but see finding 2 |
| **NewCoEndotest** | 17/29 identical, 6 behind, 11 missing | `ecb67e5` (2026-07-28) | pinned in writing — **valid state, not drift** |

NewCoEndotest is missing the entire goals subsystem (`goal_gate.py`,
`build_goals.py`, `goals.example.json`, `portability_check.py`) plus four skills.
Its unpin has been sitting in draft pull request #19 since 2026-07-30. That is
the project's decision in the project's own chat; this repository does not push
it.

**Portability**, `portability_check.py --strict` → **exit 0**. Five bindings, all
with a written justification and fallback: skill install path, auto-read contract
file, personal preferences path, scheduling, clickable menus. **No new platform
binding arrived this month without justification.** All 14 portable scripts are
stdlib-only.

---

## What was deliberately left alone

- **The interaction rules** — no abbreviations, one ask per message, buttons not
  prose, end with options. Unmechanizable by nature, and the convention already
  scopes itself to owner-facing text (*"technical precision still matters in the
  repo"*). A check here would cost more than it catches.
- **NewCoEndotest's staleness.** Pinned in writing, which the rule calls valid.
  Not this repository's decision to correct.
- **The night-shift carve-out** to *"this repo never pushes to project repos."*
  Read specifically for contradiction; it is explicitly reconciled in the
  convention's own table (the project's own approved work versus the method's
  unrequested changes). Not a contradiction.
- **`plan/plan.json` reformat protection.** The rule has a stated manual check
  (`git diff --stat`, two-to-four lines) and has still been broken twice —
  2026-07-23 and 2026-07-29. It deserves an automated check, but it ranks below
  the three above because the manual check at least exists and the damage is
  reviewability, not a false safety signal.
