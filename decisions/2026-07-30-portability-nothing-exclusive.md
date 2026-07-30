# 2026-07-30 — Nothing exclusive to one AI platform without a written reason

**Decision.** Every project, this repository included, must be able to move to
another AI platform. Anything that only works on one platform carries a **written
justification and a stated fallback**. Something with neither is a defect and gets
replaced with the portable version. Checked by
`scripts/portability_check.py --strict`.

**Asked for by the owner**, 2026-07-30: *"Another high level goal for dev ops is to
ensure that every project including dev ops can be migrated to another AI platform
if ever needed in the future. Nothing must be exclusive to Claude unless there is a
clear justification."*

## What the audit actually found

The useful part of this decision is that the position was measured before it was
asserted.

**Better than expected.** All twelve portable scripts — the goal gate, both
dashboard builders, the document renderer, the drift check, the fleet collector,
the knowledge-base linter — are **stdlib-only Python**. Not one third-party import.
They run anywhere Python does, including under a different model, a different agent
runner, or a person at a terminal. The data is plain JSON and markdown, the
generated pages are self-contained HTML with no external assets, and the provenance
is git. **None of that would notice a platform change.**

**The lock-in is narrower than it looks and concentrated in one place.** Four
bindings are cosmetic: where skills live (`.claude/skills/`), which file is
auto-read (`CLAUDE.md`), where preferences live (`~/.claude/CLAUDE.md`), and
clickable option menus. Each is a path or a filename with a trivial fallback, and
the menus already degrade gracefully because the house rule *also* requires the
written options list on every reply — the list is the record, the clicking is the
convenience.

**One binding is real: scheduling.** Nothing in the method can schedule itself.
That is the single dependency worth worrying about, and it is why the mitigation is
structural rather than a note: **every scheduled ritual is defined as a skill, with
the cadence written in `conventions/routines.md`.** The trigger points at the skill;
it does not contain the work. A cron job, a continuous-integration schedule, or a
calendar reminder could fire the same prompt. Losing the platform would cost the
timer, not the ritual.

**The honest summary: the substance is portable, the packaging is not.** A migration
would be a day of re-pathing, not a rewrite. That is the claim this convention
exists to keep true — and the check is what stops it quietly becoming false.

## Design choices, and why

**A bar, not a ban.** Vendor neutrality for its own sake would make the method
worse: the platform-specific features are often the good ones, and refusing them to
stay pure is a cost with no benefit. The requirement is only that **leaving stays
cheap**, which is satisfied by writing down the fallback rather than by avoiding the
dependency.

**Justification is per *concept*, not per mention.** `CLAUDE.md` appears 48 times;
that is one binding, not 48. The check groups by concept for exactly this reason —
counting mentions would produce a number that goes up as the documentation improves,
which is the wrong incentive.

**Dated decisions and reports are excluded from the check.** They describe what
happened. A record saying "we chose Claude Code Routines on 2026-07-23" must not be
flagged as unjustified lock-in and must never be "fixed" — rewriting history to look
portable is worse than the lock-in.

**Third-party imports are an objective strict failure.** Unlike a path or a
filename, a dependency is a second artefact that has to exist wherever the method
runs. This is the one part of the check with no judgment in it, and it passes today.

## What changes for agents

Before: use whatever the platform offers.

After: the same, and **write down the fallback**. When adopting a platform
capability, record what you would do without it. When a platform *gains* something
that removes one of our workarounds, that is a method-scan finding and the most
valuable kind — it makes the method smaller.

## How this could be wrong

- **The check is shallow by construction.** It greps for known identifiers. Lock-in
  that arrives as a *behaviour* — a convention that only works because a particular
  model is unusually good at something — is invisible to it. The convention names
  that case and asks for it to be written down, which is an honour system.
- **It cannot see the future.** The binding list is the one we know about today. A
  new platform feature adopted casually would not appear until someone added its
  pattern. The method scan is the intended catch, and it depends on someone running
  it.
- **Skipping its own file is a real blind spot.** The checker defines the patterns,
  so scanning itself matches all of them. It is excluded by name and the docstring
  says so — but lock-in added *inside* the checker would pass silently.
- **A day of re-pathing is an estimate, not a test.** Nobody has migrated anything.
  The claim would be worth far more if it had been tried once, even on a throwaway
  copy, and that has not been done.
