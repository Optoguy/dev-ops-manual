# CLAUDE.md — Dev Ops Manual

Context file for Claude Code sessions. Read this before doing anything in this repo.

## What this repo is

The **source of record for how work happens** across every project — the
portable skill suite, the operating conventions, and the dated decisions behind
them. Nothing here is project-specific. Project repos install *from* here.

Its companion is the "Dev Operating Manual" chat session, which owns this repo
and the cross-project night shift. Project-specific work and Routines live in
each project's own chat (see `conventions/routines.md`).

## Repo map

- `README.md` — the front door: install commands, the skill index, where the
  method is used. Written to read well on GitHub from a phone.
- `skills/` — the 15 portable skills, each a directory with `SKILL.md` and
  optional `assets/`. **This is the source of record**; project repos hold
  installed copies under their own `.claude/skills/`.
- `install.sh` — copies skills into `~/.claude/skills/` (`--global`) or a
  project's `.claude/skills/` (`--repo <path>`), and optionally writes the
  standing preferences block into `~/.claude/CLAUDE.md` (`--prefs`).
- `conventions/` — `house-rules.md` (the operating contract), `routines.md`
  (scheduled agents, session binding, the container model),
  `external-agents.md` (the Devin contract), `global-CLAUDE-snippet.md` (what
  `--prefs` writes).
- `decisions/` — dated records of choices that changed how work happens.
- `scripts/` — `build_dashboard.py`, `build_goals.py`, `render_docs.py`, and `skills_drift.py`
  (compares each project's installed `.claude/skills/` against `skills/` here;
  **reports only, never fixes** — adoption is the project's own call).
- `reports/` — dated findings that aren't decisions, each with an HTML twin.

## Conventions for working *in* this repo

- **A skill edit is a fleet-wide change.** After editing anything under
  `skills/`, note which project repos need `./install.sh --repo <path>` re-run.
  An installed copy that has drifted from source is the failure mode this repo
  exists to prevent.
- **Skills stay portable.** No project-specific paths, names, or domain
  assumptions inside `skills/` — if a rule only applies to one project, it
  belongs in that project's `CLAUDE.md`, not here.
- **Conventions get dated provenance.** When a rule changes because something
  broke, say what broke and when, and add a `decisions/` record if it changes
  the contract. The rules are more persuasive with the scar tissue attached.
- **`README.md` is a real deliverable**, not an afterthought — the owner reads
  it on a phone. Keep the index accurate when skills are added or renamed.
- **Git:** scoped staging (`git add <paths>`, never `git add -A`), plain dated
  commit messages, don't rewrite history, PR-based for substantive changes,
  **never push without the owner's go-ahead.**

## Interaction — how to talk to the owner

Write so the next step is obvious. (Owner instruction, 2026-07-28: dense,
jargon-heavy replies are hard to act on.)

- **Lead with the ask.** The first sentence says what you need from
  the owner. Reasoning comes after, and is optional.
- **No abbreviations.** Write "pull request", not "PR". Spell out every short
  form the first time it appears — in every message, not just the first one of
  the conversation.
- **No nicknames invented during your own analysis.** Labels like "option A2"
  or "the trio" mean nothing to a reader who wasn't in that thread. Name the
  actual thing.
- **One ask per message.** If two things need deciding, ask the more important
  one and hold the other.
- **Say where to click and what changes.** "Open this link and click the green
  Merge button" beats "merge #53". Then say what will be true afterwards.
- **Short sentences, one idea each.**
- **Send deliverables as files**, not buried in chat text. A report that exists
  only inside a reply gets missed.

**End every response with the choices, clearly marked.** Close with a section
headed **"Your options"**: numbered, plain language, one line each on what
happens if that option is chosen, the recommended one marked, two to four
options, and include the do-nothing option when it is a real choice. Show the
clickable menu as well, but always write the list out too — a menu can be
missed or read on a phone. When there is genuinely nothing to decide, write
**"Nothing for you to do"** instead. Never end with an open-ended "let me know
what you think".

This governs what is said **to the owner**. Everything inside the repo —
code, commit messages, conventions and knowledge files — stays technically
precise.

Everything else in `conventions/house-rules.md` applies here too.

## Local copy

The owner keeps a clone at
`C:\Users\dancg\OneDrive\Projects\dev-ops-manual` for reading offline. Git is
the only sync channel between that copy, this repo, and any session's container.
