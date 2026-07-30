# History — Dev Operating Manual

One line per period, newest first. Each links a digest of the chat record for that
period: the owner's instructions in order, and the reasoning behind them.

**Why this exists.** The repository keeps conclusions — decisions, conventions,
reports. The chat kept how they were reached: the options rejected, the corrections,
the owner's exact words. That record lives in an ephemeral container and does not
survive it. These files are what is left when it goes. See
[`history-capture`](../skills/history-capture/SKILL.md).

**Append-only.** Never rewrite an earlier period. If an entry was wrong, add a
correction dated now — the same supersede-don't-delete rule the rest of the method
follows.

| Period | Digest | What it was about |
|---|---|---|
| 2026-07 (22nd–30th) | [2026-07.md](history/2026-07.md) | The method's first eight days: mining two existing projects into a portable skill suite, then the run of rules that came from breaking things — claim-before-you-build, squash-merge defeating branch-based claims, the manual pushing to nobody, plain-language writing, goals with measures, the no-goal-no-work gate, the end goal and the ladder, external research and fleet audits, and platform portability. |

## What the first period contains

95 owner turns across eight days, ~61,000 tokens, extracted from 6,152 transcript
records. 1,301 tool calls discarded as reconstructable from git.

The digest's **"What the owner asked for, in order"** section is the project's
spine — every instruction that shaped the method, dated, in his words. Most of the
conventions in `conventions/` can be traced to a line in it.

## Honest limits of this record

- **Assistant replies are truncated to 300 characters** in the digest. Anything
  important must be promoted into a decision, a convention, or a report — not left
  in the digest.
- **Redaction is best-effort.** Known credential shapes are masked and the file was
  swept before committing, but a secret in an unusual format could survive. Never
  commit the raw transcript.
- **Only this chat's history is here.** A transcript is readable only by the session
  that produced it, so each project captures its own. The
  [fleet audit](../skills/fleet-audit/SKILL.md) reports any project whose history
  has gone stale.
- **Sub-agent transcripts are not yet captured** — 10.7 MB across eight files in
  the first period alone, some containing real research findings.
