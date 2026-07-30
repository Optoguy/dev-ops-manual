# Portability — nothing exclusive to one platform without a written reason

Added 2026-07-30 at the owner's request: *"Another high level goal for dev ops is
to ensure that every project including dev ops can be migrated to another AI
platform if ever needed in the future. Nothing must be exclusive to Claude unless
there is a clear justification."*

Binds every project, this one included.

## The rule

**Anything that only works on one AI platform must carry a written justification
and a stated fallback.** Not a ban — a bar. The justification says why the
platform-specific version is worth the lock-in; the fallback says what you would
do instead if the platform went away, got expensive, or stopped fitting.

Something with neither is a defect, and gets replaced with the portable version.

## Where things actually stand — audited 2026-07-30

Measured, not asserted. Commands are in [the check](#the-check) below.

### Portable today — would survive a platform change untouched

| What | Why it survives |
|---|---|
| **Every script** — `goal_gate.py`, `build_dashboard.py`, `build_goals.py`, `render_docs.py`, `skills_drift.py`, `fleet_state.py`, `brain_lint.py` | **Stdlib-only Python, all twelve copies verified.** No third-party imports at all, so they run anywhere Python does — including under a different model, a different agent runner, or a human at a terminal. |
| **The data** — `plan/plan.json`, `plan/goals.json`, `brain/**`, launch plans | Plain JSON and markdown with no platform semantics. |
| **Generated output** — dashboards, the goals page, every document twin | Self-contained HTML, no external assets, no framework. Opens in any browser, offline, forever. |
| **The provenance** — decisions, reports, commit history | Git. The most portable thing in the stack. |
| **The conventions themselves** — every rule in `conventions/` | Prose about how work happens. A different platform reads them the same way. |
| **The external-agent contract** | Already written for a non-Claude agent (Devin), which is standing evidence the method is not Claude-shaped in principle. |

### Platform-bound, with justification and fallback

| What | Why it is bound | Justification | Fallback if the platform changes |
|---|---|---|---|
| **`.claude/skills/<name>/SKILL.md`** — the install location and auto-loading | Claude Code discovers skills at this path | **Accepted.** The *content* is portable prose; only the directory name and the auto-load are specific. 13 references, all in `install.sh` and skill text. | Move the same directories anywhere and load them however the new platform loads instructions. `install.sh` takes a target path already — one variable, not a rewrite. |
| **`CLAUDE.md`** — the auto-read contract file | Claude Code reads it at session start | **Accepted.** Same reasoning: a filename and a convention, not a format. Every other platform has an equivalent. | Rename, or symlink. The content needs no change. |
| **`~/.claude/CLAUDE.md`** — standing preferences | Where personal preferences are read from | **Accepted**, and deliberately thin: interaction rules only, no project logic. | Re-paste the marked block wherever the new platform keeps preferences. `install.sh --prefs` writes a marked block, so it is a target path change. |
| **Routines** — the scheduling mechanism | Claude Code Remote triggers | **This is the real lock-in, and the only one worth worrying about.** Nothing in the method can schedule itself. | Every scheduled ritual is defined as a **skill** with the schedule written in `conventions/routines.md` — so the *work* is portable and only the *timer* is not. A cron job, a CI schedule, or a human calendar reminder can fire the same prompt. |
| **Chat-transcript reading** — `chat_distill.py` parses `~/.claude/projects/**.jsonl` | The transcript layout is Claude Code's | **Accepted, and it is the reason the whole capture exists.** The alternative is losing the record entirely. What it *produces* — dated markdown digests, brain entries, a history index — is fully portable and is the point. | Write a reader for the new platform's history format and keep the same digest output. One function, and `--find` already looks in more than one location. If a platform exposes no history at all, that is a portability finding about the platform. |
| **`AskUserQuestion`** — clickable option menus | A Claude Code tool | **Accepted, and it degrades gracefully.** 10 references. The underlying rule is "put choices as discrete options, recommended first" — which is why the house rule *also* requires the written "Your options" list on every reply. | The written list is already the record. On a platform without menus, nothing is lost but the clicking. |

### The honest summary

**The substance is portable; the packaging is not.** Scripts, data, generated
output, provenance and the rules themselves would move intact. What is Claude-shaped
is *where files live*, *what gets auto-read*, and *how recurring work fires* — and
of those three, only scheduling has no drop-in replacement.

**A migration would be a day of re-pathing, not a rewrite.** That is the claim this
convention exists to keep true.

## Rules that follow from it

- **Scripts stay stdlib-only.** No third-party dependency in any portable asset
  without a justification, for the same reason: it is a second thing that has to
  exist wherever the method runs. This is already true and worth keeping true.
- **Every scheduled ritual is a skill first, a schedule second.** Never encode the
  work *inside* a Routine prompt only. If the ritual exists only as a trigger's
  text, losing the platform loses the ritual. Write the skill; let the trigger
  point at it.
- **Model-specific behaviour gets named.** If a convention only works because a
  particular model is unusually good or bad at something, say so, so the next
  reader knows to re-test rather than inherit.
- **No project embeds an AI provider without an abstraction.** SpecBuildr is the
  precedent worth copying: a `/api/chat` contract, one provider behind an
  environment variable, and swapping is a one-file change. Any project calling a
  model directly from application code is a portability defect.
- **Generated output stays self-contained.** Already a design rule for other
  reasons; it is also what makes the artifacts outlive the toolchain.
- **Capture the chat record on a cadence.** The reasoning behind a project — the
  options rejected, the corrections, the owner's exact words — exists only in a
  transcript held in an ephemeral container. Committed digests and brain entries
  are what survive a platform change, and they only exist if something writes them
  before the container is reclaimed. See
  [`history-capture`](../skills/history-capture/SKILL.md).
- **When a platform gains a capability, check whether it removes a workaround.**
  That belongs to the [method scan](../skills/method-scan/SKILL.md), and the
  reverse holds too: a capability the method now depends on is new lock-in that
  needs its justification written.

## The check

`scripts/portability_check.py` scans for platform-bound identifiers and reports
each against this file's justification table:

```sh
python scripts/portability_check.py            # scan this repo
python scripts/portability_check.py --strict    # nonzero if anything is unjustified
```

It reports, never rewrites. New lock-in is a decision for a person; the check only
makes sure it is not silent. **Third-party imports in a portable asset fail the
strict check** — that one is objective and worth enforcing.

## What this does not mean

- **Not vendor neutrality for its own sake.** Using the best available tool is
  correct. The requirement is that leaving stays cheap.
- **Not writing everything twice.** No parallel implementations kept warm "in
  case". One implementation, portable where portability is free, justified where
  it is not.
- **Not a reason to avoid new platform features.** Adopt them, and write down what
  the fallback would be. A feature with a known fallback is not lock-in; it is a
  dependency with an exit.
