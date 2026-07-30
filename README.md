# Dev Ops Manual

**How I work with Claude.** This repo is the source of record for the method —
the portable skills, the operating conventions, and the decisions behind them.
Every project repo installs from here; nothing here is project-specific.

Readable from anywhere: browse it on GitHub, or clone it locally
(`C:\Users\dancg\OneDrive\Projects\dev-ops-manual` on the PC).

---

## Quick start in a new project

```bash
git clone https://github.com/Optoguy/dev-ops-manual
cd dev-ops-manual
./install.sh --global --prefs        # skills + standing preferences, first-time setup
./install.sh --repo /path/to/project # skills into one project's .claude/skills/
```

Then, in that project, run `/project-init` and answer the interview. You get a
CLAUDE.md contract, a plan and dashboard, and the git conventions on day one.

---

## The skills

Each is a directory under [`skills/`](skills/) with a `SKILL.md` and optional
assets. Invoke with `/<name>` in any session where they're installed.

**Starting and running a project**
| Skill | What it does |
|---|---|
| [`project-init`](skills/project-init/SKILL.md) | Scaffold a repo the house way — CLAUDE.md contract, `.claude/` config, docs/brain skeleton, git conventions |
| [`plan-track`](skills/plan-track/SKILL.md) | `plan/plan.json` as single source of truth + a generated dashboard splitting your tasks from the agent's, ranked P0→P2 |
| [`goal-review`](skills/goal-review/SKILL.md) | Score the goal against its number, audit whether the work that claimed to move it did, then update and re-prioritize — weekly and monthly |
| [`fleet-audit`](skills/fleet-audit/SKILL.md) | Audit every project at once — a short ranked list of findings with recommendations, capped at five |
| [`weekly-review`](skills/weekly-review/SKILL.md) | The operating cadence: what moved, what stalled, what's blocked on you, is the plan still honest |
| [`wrap-session`](skills/wrap-session/SKILL.md) | Close-out ritual — capture findings, log decisions, update statuses, regenerate, commit |

**Knowing things**
| Skill | What it does |
|---|---|
| [`brain`](skills/brain/SKILL.md) | Provenance-tracked knowledge base: capture findings with sources, answer with citations, keep it healthy |
| [`decision-log`](skills/decision-log/SKILL.md) | Record a decision as a dated file and trickle it through every file it affects |
| [`verify`](skills/verify/SKILL.md) | Adversarial fact-check of any document — audit every citation, report verdicts worst-first |
| [`options-memo`](skills/options-memo/SKILL.md) | Structure a decision before it's made: criteria, options, evidence, recommendation |

**Building and shipping**
| Skill | What it does |
|---|---|
| [`ship-web-app`](skills/ship-web-app/SKILL.md) | The web stack playbook — one engine + swappable modules, provider behind a stable contract, CSP-safe frontend, Cloudflare hosting |
| [`deliverable-delight`](skills/deliverable-delight/SKILL.md) | Design the final output so it feels like a prize, not a printout (peak-end, IKEA effect, shareability) |
| [`growth-loop`](skills/growth-loop/SKILL.md) | Instrument → measure → adjust, with agents measuring and drafting and humans approving anything published |

**Working with people and agents**
| Skill | What it does |
|---|---|
| [`night-shift`](skills/night-shift/SKILL.md) | Propose overnight agent work, get slate approval, run only what's approved → one draft PR |
| [`method-scan`](skills/method-scan/SKILL.md) | Look outside on a cadence and bring back what is worth adopting — report-first, never automatic |
| [`routine-design`](skills/routine-design/SKILL.md) | Scheduled agents that run safely unattended — quiet-until-prereqs, untrusted-data guardrails, explicit thresholds |
| [`discovery-call`](skills/discovery-call/SKILL.md) | Prep a customer/advisor conversation and capture what it taught, with provenance |

---

## The conventions

- **[Portability](conventions/portability.md)** — **nothing exclusive to one AI
  platform** without a written justification and a fallback. Audited table of what
  is bound and why; `portability_check.py --strict` fails on unjustified lock-in
  or a third-party import in a portable asset.
- **[Goals and measures](conventions/goals-and-measures.md)** — **no work without
  a goal** (`python src/goal_gate.py` is the stop); owner-set monthly
  and weekly goals, one measurable number each, and the rule that every suggested
  task says which goal it serves. Generates `dashboard/goals.html`.
- **[House rules](conventions/house-rules.md)** — the operating contract: tasks,
  claims, git, ownership split, interaction defaults, untrusted data.
- **[Routines and sessions](conventions/routines.md)** — how scheduled agents
  bind to conversations, what a container is and isn't, and the rules learned
  the hard way.
- **[External agents](conventions/external-agents.md)** — the contract any
  non-Claude agent (Devin) must follow in these repos.
- **[Standing preferences snippet](conventions/global-CLAUDE-snippet.md)** —
  what `install.sh --prefs` writes into `~/.claude/CLAUDE.md`.

## Decisions

Dated records of choices that changed how work happens.
See [`decisions/`](decisions/).

---

## Where this is used

| Repo | What it is |
|---|---|
| `Optoguy/SpecBuildr` | Conversation → build-ready product spec (web product) |
| `Optoguy/NewCoEndotest` | Endoscope test-instrument company brain (research/strategy) |
| `Optoguy/medtech-intel-QMSR` | FDA clearance + QMSR enforcement intelligence |

Each keeps its own `CLAUDE.md` and installed `.claude/skills/`; this repo is
what they install *from*. After editing a skill here, re-run `install.sh
--repo <project>` in each project that should pick up the change.
