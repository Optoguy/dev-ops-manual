---
name: decision-log
description: Record a decision as a dated file and trickle it through every file it affects. Use when a decision is stated to record, when asked to log or document a decision, or when a choice is made that changes the project's constraints, plan, or facts.
---

# Record a decision

Decisions are the load-bearing events of a project, and memory of *why* fades
fastest. Every decision gets a dated markdown file the day it's made; the git
history is the provenance record, so the file's timestamp is evidence. A decision
that isn't written down didn't happen — the next session will re-litigate it.

## Procedure

1. **Write the record.** Create `brain/decisions/YYYY-MM-DD-<short-slug>.md`
   (today's date) with frontmatter `title`, `tags` (starting with `decision`),
   `date`, `status: active`. The body covers:
   - **What was decided** — one crisp sentence up top.
   - **Decided by whom** — the human owner; agents record, they don't decide.
   - **Context / why** — the reasoning, so it survives a future "wait, why did we…"
   - **What it supersedes** — the prior state or decision this replaces.
   - **What changed as a result** — the files touched in step 3.

2. **Constraint check first.** If the decision conflicts with a hard constraint
   in `CLAUDE.md`, **stop and say so before writing anything** — constraints
   outrank an instruction to record. Surface the conflict to the owner.

3. **Trickle down.** A decision that lives only in its own file is inert. Update
   every file it affects — `CLAUDE.md`, `brain/constraints.md`, `brain/people/`,
   the plan in `docs/`, any knowledge file whose facts it changes. **Supersede,
   don't delete:** mark the old section superseded with the date and a pointer to
   the decision file. Then grep the key terms to sweep for stale references so no
   file silently contradicts the new state.

4. **Lint.** Run `python src/brain_lint.py --write-index` then
   `python src/brain_lint.py` — must pass.

5. **Commit together.** The decision file and all trickle-down edits go in one
   commit with a plain dated message. Stage only the files this decision touched
   (`git add <paths>`, never `git add -A`). **Do not push** — pushing is the
   owner's call.

## Judgment

- **Scope the trickle honestly.** The failure mode is a decision file that says
  "changed X, Y, Z" while X, Y, Z still read the old way. The grep sweep is not
  optional.
- **Reversals are decisions too.** Lifting or changing an earlier decision gets
  its own dated file that supersedes the old one — don't edit the original record
  to pretend the first decision never happened. The trail of "we thought A, then
  chose B" is worth keeping.
- **Don't over-record.** A decision is a choice that changes constraints, plan,
  or facts. A routine implementation choice with no downstream is just a commit.
