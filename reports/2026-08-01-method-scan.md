# Method scan — 2026-08-01

First scan under `/method-scan`. Report only: nothing here changes a convention.
Adopting any of it is a decision that gets its own dated record.

---

## What got smaller

**The method can stop copying itself into every repository.**

This is the finding to read first, and the only one that deletes rather than adds.

`install.sh --repo <path>` copies `skills/` into each project's
`.claude/skills/`. `scripts/skills_drift.py` exists to detect what that copying
causes — its own docstring says so: *"Two copies of a skill always drift
eventually — that risk is why this repo exists."* Every adoption is then a
hand-run install plus a per-repo pull request, and every pull request touching
`skills/` has to list which repositories need the install re-run.

Claude Code's plugin system removes the second copy entirely. A marketplace is a
`.claude-plugin/marketplace.json` catalogue in this repository; each project
names it in its own `.claude/settings.json` and installs from it. There is one
source, versioned, and no local copy to drift.

**What breaks today.** Drift is not hypothetical here, and it is currently
producing a false green:

- `medtech-intel-QMSR`'s installed `scripts/goal_gate.py` is the pre-ladder
  version. `grep -c end_goal_faults` returns **0**. It reports `CLEAR` while the
  repository has **no end goal at all** — the current gate on its own unmerged
  pull request #6 reports `BLOCKED` on the same data. A stale copy is telling the
  owner work may proceed when the rule says it may not.
- Four repositories currently sit on **three different method versions**.
  SpecBuildr merged the `87a24ac` adoption this morning (#63); NewCoEndotest's
  equivalent (#19) and medtech's (#6) have been open as drafts since 2026-07-30.
- The adoption ritual is now four pull requests per method change — #62 and #63
  in SpecBuildr, #6 in medtech, #19 in NewCoEndotest — each hand-run, each
  separately reviewable, each able to stall.

**What it would change.** `install.sh` keeps `--prefs` and `--global`, loses
`--repo`. `scripts/skills_drift.py` is deleted. The "re-run `./install.sh
--repo`" clause comes out of `conventions/house-rules.md`, both goal decisions,
and every future pull-request body.

**The mechanical check.** `claude plugin validate ./<plugin>` exits nonzero on a
malformed plugin, and the marketplace entry carries an explicit `version` or
pins to a 40-character commit `sha`, so "which version is this project on" is a
field to read rather than a hash to compute. Replaces `skills_drift.py` with a
lookup.

**Three honest costs.**

1. **Skill names get namespaced** — `/night-shift` becomes
   `/dev-ops-manual:night-shift`. That is in every skill's cross-references and
   in the nightly Routine prompt.
2. **It is a new platform binding**, and this repository adopted
   `conventions/portability.md` two days ago. Marketplaces are Claude Code's
   mechanism. The mitigating fact: the plugin payload is still plain directories
   of `SKILL.md` files, so the content stays portable and only the distribution
   is platform-specific — but it must be recorded as a binding with a fallback,
   not slipped in.
3. **Trust surface.** Anthropic's own warning: *"Plugins and marketplaces are
   highly trusted components that can execute arbitrary code on your machine
   with your user privileges."* This proposal is for a **private, self-owned**
   marketplace — a first-party repository the owner already controls. It is not
   a recommendation to install third-party plugins, and the third-party
   aggregators found during this scan (one advertising 471 plugins and 3,069
   skills) are explicitly out of scope.

**Verdict: adopt** — as a migration with its own decision record, not a
side effect.

Sources: [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) ·
[Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins) ·
[Create plugins](https://code.claude.com/docs/en/plugins)

---

## Adopt

### 1. Plugin-marketplace distribution

Above. Deletes `skills_drift.py`, `install.sh --repo`, and the per-pull-request
re-install clause.

### 2. Claims are leases, not locks — they expire

Distributed systems stopped using permanent locks decades ago for exactly the
failure this method has. The lease pattern: a claim is **time-bound**, must be
renewed, and expires on its own. A holder that pauses or dies does not block the
resource forever. The companion idea is the **fencing token** — a monotonically
increasing number issued with the lease, so a stale holder that wakes up and
tries to act is rejected by the thing it is writing to.

`claim-before-you-build` (2026-07-26) implements the lock half and not the
expiry half. `status: in-progress` is held until someone remembers to clear it.

**What breaks today.** Found in this session, not hypothetically:
SpecBuildr's `adopt-manual-87a24ac` is still `status: in-progress` although the
pull request that completed it (#63) merged this morning. Under the night-shift
rule, `in-progress` means "someone has this" — so that task is now unavailable
to every future session, indefinitely, because of a claim nobody released. The
original 2026-07-26 collision that produced the claim rule was the same class of
failure in the other direction.

**What it would change.** A claim note already carries a date
(`claimed <date> night-shift`). Make it mean something: a claim older than
N days, or whose referenced pull request is merged or closed, is **expired** —
reclaimable by the next session, with a note, no permission needed.

**The mechanical check.** `build_dashboard.py --check` already exits nonzero on
goal faults; add expired claims to it. The rule is computable from data the plan
file already holds — `status`, the claim date in `note`, and the pull-request
state that `fleet_state.py` already reads. This is the cheapest of the three:
one predicate, no new file format.

The fencing-token half is **not** proposed. It guards against a paused holder
resuming and corrupting state; a Claude session that wakes after its claim
expired would re-read the plan file first and see the reclaim. Recorded here so
the idea is not re-found and mistaken for missing.

Sources: [Lease pattern in distributed systems](https://singhajit.com/distributed-systems/lease/) ·
[Beyond the lock: why fencing tokens are essential](https://levelup.gitconnected.com/beyond-the-lock-why-fencing-tokens-are-essential-5be0857d5a6a)

---

## Adapt

**Approval menus should state blast radius and rollback, not just intent.**
Three decades of human-factors work says reviewers drift into rubber-stamping —
the International AI Safety Report 2026 is quoted as warning that automation
bias *"undermines competence by discouraging active reasoning and
verification."* The recommendation that survives the filter is small: replace a
bare "Approve?" with a per-option line naming expected blast radius and the
rollback path.

The house slate already carries goal, measure, verification method and dispatch
tag. The missing half-line is **what this can break and how it is undone**. For
night-shift work the answer is nearly always "a draft pull request, closed
without merging" — which is itself worth saying, because it is the sentence that
makes approving safe rather than habitual.

The larger proposal in the same literature — calibrating interruptions to an
estimated human fatigue curve — is discarded below.

Sources: [Oversight has a capacity (arXiv 2606.08919)](https://arxiv.org/pdf/2606.08919) ·
[Human oversight of agentic systems in practice (arXiv 2606.05391)](https://arxiv.org/pdf/2606.05391)

## Watch

**Per-agent git worktree isolation.** The multi-agent write-ups converge on
isolating each concurrent agent in its own worktree so parallel edits cannot
collide, and Claude Code's Agent tool already exposes `isolation: "worktree"`.
Not applicable yet: this method runs one agent at a time by design, and the
external-agents convention forbids two agents on overlapping file sets. It
becomes applicable the first time a night shift genuinely fans out — at which
point the branch-per-night model is the thing that has to change.

---

## Discard — recorded so they are not re-found next quarter

- **I-PASS / SBAR structured clinical handoff.** Best-evidenced item in the
  whole scan — moderate-certainty evidence across ten studies including two
  randomised trials that I-PASS reduces medical errors. Discarded anyway: it
  fixes verbal handoff between shift workers with no written artefact. This
  method's handoff is already written and durable (the pull-request body, the
  morning summary, `/wrap-session`). Adopting the mnemonic adds vocabulary
  without naming a failure that happened here.
- **Fatigue-calibrated adaptive interruption.** The core proposal of arXiv
  2606.08919. Its own limitations section is disqualifying for this method:
  evaluation is **simulation only, no real-world deployment data**, it assumes
  fatigue degrades oversight monotonically, and it requires estimating an
  individual's fatigue threshold, which the paper concedes "may be difficult to
  obtain in practice." One person and four repositories cannot calibrate a
  curve.
- **The 88-agents-per-operator oversight-ratio literature.** Real finding
  (BCG/UC Riverside numbers on reviewer fatigue: 14% more mental effort, 39%
  higher major-error rates), wrong scale. It describes operators supervising
  fleets. Here the ratio is one owner to at most three proposed tasks a night.
- **"Multi-agent orchestration failure playbooks."** Several 2026 write-ups on
  agents colliding on hotspot files. Their prescriptions — spec-scoped tasks,
  isolate per agent, require tests before merge — are what
  `claim-before-you-build`, the external-agents convention and the
  verify-before-done bar already do. No new mechanism, and none of them
  published post-mortem numbers.
- **Third-party plugin aggregators.** Discovered while researching
  marketplaces. Irrelevant to method and an active trust risk; noted only so the
  marketplace adoption is not misread as endorsing them.

---

## What was scanned

Date range: sources published or current through 2026-08-01. Five kinds:

| Kind | Read |
|---|---|
| **Primary vendor documentation** | Claude Code docs: plugin marketplaces, plugin creation, plugin discovery/installation |
| **Adjacent discipline — distributed systems** | Lease pattern, fencing tokens, stale-lock reclaim |
| **Adjacent discipline — medicine** | I-PASS / SBAR structured handoff systematic reviews (AHRQ *Making Healthcare Safer IV*) |
| **Research** | arXiv 2606.08919 (oversight capacity), 2606.05391 (oversight in practice); limitations read first |
| **Practitioner write-ups** | Multi-agent orchestration and parallel-agent collision playbooks, 2026 |

**Under-covered, said plainly:** the practitioner category is the weak one. What
surfaced was mostly vendor-adjacent blog content restating known advice; nothing
carried post-mortem numbers from a team actually running an agent fleet. That
category should be searched differently next month — conference talks, incident
write-ups, or engineering blogs by name — rather than by keyword.

**Aviation was skipped.** Crew resource management and checklist discipline were
in scope and not read; the medical handoff literature was taken as the
representative of that family. Worth its own pass if the approval-gate question
comes back.

**Untrusted-data check.** Everything fetched was treated as data to summarise.
Nothing read as an attempt to redirect behaviour — no injected instructions, no
"ignore previous" patterns, no requests to fetch or execute anything. The only
notable content-level caution is the plugin trust warning quoted above, which is
Anthropic's own documentation warning users about third-party plugins, not an
attempt to influence this scan.
