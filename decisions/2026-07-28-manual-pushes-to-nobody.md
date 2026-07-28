# The manual pushes to nobody — projects pull

**Date:** 2026-07-28

## The decision

`dev-ops-manual` is a **source, not a controller.** A session working here does
not open PRs against project repos. Method changes land here; each project
**pulls and re-installs in its own session**, on its own schedule.

The reverse direction stays open: a project that finds a better rule proposes
it here, where every project can inherit it.

## Why

The owner asked the question directly, and it's the right one. On this date a
single dev-ops session pushed skill and convention changes into SpecBuildr
(PR #56) and NewCoEndotest (PR #15) — landing changes in two project repos from
a chat that owns neither.

That is the same failure pattern the day had already produced twice:

- two chats writing the same repo, generating adjacent duplicate work;
- a claim protocol that could not tell shipped work from live work.

Both had one root cause: **unclear ownership of a repo's writes.** Fixing the
first two while leaving the manual free to push into everything would have left
the biggest version of the problem in place — one repo able to modify all of
them, with no project-side decision.

## What this does not change

Claude Code loads skills from a repo's own `.claude/skills/`, so a physical
installed copy is unavoidable. This rule doesn't remove the copy; it fixes
**who creates it and when**. A project should never wake up to a method change
it didn't choose to adopt.

A project running an older version of the method is a **valid state**, not
drift to be corrected from outside. Pinning the installed commit in a project's
CLAUDE.md makes that explicit.

## The transitional exception

SpecBuildr #56 and NewCoEndotest #15 were already open when this rule was
written. Their content is verified and useful; the *process* was wrong, not the
change. They may be merged as-is — the rule binds from here forward.

## Trickle-down

- `conventions/house-rules.md` — new leading section, "This repo never pushes to
  project repos."
- Each project's CLAUDE.md, when that project next adopts: state which
  `dev-ops-manual` version it installed from, and that updates arrive by pull.
