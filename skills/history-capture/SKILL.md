---
name: history-capture
description: Turn a chat transcript into durable project history and brain knowledge before the container that holds it is reclaimed. Distil the session, append to the project history, promote what is durable into the knowledge base with provenance. Use weekly, at session close, or when asked to capture history, save context, or protect knowledge against a platform change.
---

# History capture — before the container is reclaimed

Owner instruction, 2026-07-30: *"look into how to regularly summarize the history
of a project including the chat records and how to regularly update the project
brain from the chat. I don't want to lose context and knowledge in the case of a
transition to another platform."*

**The chat transcript is the only complete record of why a project looks the way it
does — and it is stored in an ephemeral container.** The repository keeps
conclusions. The chat keeps the options rejected, the corrections, the near-misses,
and the owner's exact words before anyone paraphrased them. When the container goes,
that goes.

**Compaction is the nearer threat than a platform change.** A long session's memory
of its own first week is a summary of a summary; the file on disk is complete. So
this ritual pays for itself immediately, and the migration protection is a bonus.

## Two layers, and they are different jobs

| Layer | What | Who does it |
|---|---|---|
| **Mechanical** | Extract owner turns and prose, drop tool calls and noise, redact secrets | `chat_distill.py` — no judgment, same output every time |
| **Judgment** | Decide what is *durable knowledge*, write it where it will be found | This skill. The expensive half. |

**Never skip straight to the judgment layer using remembered context.** After
compaction your memory of the period is exactly the lossy thing this ritual exists
to replace. Read the file.

## Procedure

### 1. Find the transcript and measure before extracting

```sh
python src/chat_distill.py --find                     # what exists on this machine
python src/chat_distill.py <transcript> --stats        # size of the real signal
```

`--stats` first, always. It tells you whether the period is worth a full pass —
sixty owner turns is a rich week, three is a quiet one that may only need a line in
the history file.

**If no transcript is found, stop and say so.** On a platform that keeps history
elsewhere, the fallback is a reader for that format (see
[portability.md](../../conventions/portability.md)); do not substitute your own
recollection and present it as a record. A history file built from memory is worse
than none, because it looks authoritative.

### 2. Distil, scoped to the period

```sh
python src/chat_distill.py <transcript> --since <last-capture-date> \
  --out docs/history/<YYYY-MM>.md
```

**Per-period files, not one growing document.** Eight days produced 85 KB; a year
in one file is unreadable and unmergeable.

### 3. Read the digest and sort it — this is the actual work

Every line is one of four things. Most are the last one.

| Kind | Where it goes |
|---|---|
| **Durable knowledge** — a fact, a constraint, a measured number, a source | `brain/`, with frontmatter and provenance |
| **A decision** not yet recorded | `/decision-log`, dated, with the reasoning |
| **Narrative** — what happened, in order | the history file, which the digest already is |
| **Transient** — coordination, retries, "continue", answered questions | nothing. Leave it in the digest and move on. |

Three kinds are easy to miss and are the most valuable:

- **Corrections.** Where the agent was wrong and the owner said so. These are the
  strongest evidence about how the work actually goes, and they never appear in a
  diff. Capture the correction, not a face-saving version of it.
- **Rejected options.** Why the road not taken was not taken. Without this the next
  session re-proposes it, and the owner re-explains.
- **The owner's exact words** on anything that became a rule. A paraphrase drifts;
  a quotation does not. Every convention that cites the instruction behind it is
  more persuasive than one that does not.

### 4. Write it where it will be found

- **`docs/history/<YYYY-MM>.md`** — the digest, committed. Append-only: never
  rewrite an earlier period. If an earlier entry was wrong, add a correction dated
  now, in keeping with the supersede-don't-delete rule.
- **`brain/`** — one file per durable finding, following that repo's conventions,
  passing its lint. **Cite the transcript date**, not the digest, so provenance
  survives even if the digest is later trimmed.
- **`docs/HISTORY.md`** — a short index: one line per period, linking its file,
  with the two or three things that period was about. This is what a new agent or a
  new platform reads first.

### 5. Check the redaction before committing

`chat_distill.py` masks known secret shapes — API keys, tokens, JWTs, private keys,
`password:` forms. **It is best-effort, and a transcript contains everything ever
pasted into the chat.**

- Skim the digest for anything credential-shaped that survived.
- **Never commit the raw transcript.** The digest is the artefact.

**Naming people and organisations — the test is purpose, not category**
(relaxed 2026-08-05; see
[the decision](../../decisions/2026-08-05-naming-third-parties.md)).

A project's knowledge is largely *about* other parties, and a record that cannot
name them is not a record. Vendors, competitors, standards bodies and cited
authors are the substance of a brain, not a leak.

**There is no blanket restriction on naming a third party.** The exclusions below
are a short, specific list. Everything not on it may be named.

**Name freely:**

- Organisations — vendors, competitors, suppliers, partners, **customers and
  prospective customers**, standards bodies, publishers.
- Published work and its authors, with the citation. That is what a citation *is*.
- People acting in a professional capacity, where what is recorded is what they
  said or did in that capacity and it bears on the project — a vendor engineer's
  answer about a datasheet, a reviewer's published objection, a conference talk.
- **People at customers and prospects, and what they told you in a business
  conversation** — a discovery call, a sales call, a meeting. Name them, quote
  them, record which company they are from and what they asked for.

**A business conversation is not "said in confidence."** A discovery call is the
single most valuable knowledge a project acquires, and it exists to be recorded.
It becomes confidential only when the other party says so — an explicit "off the
record", a non-disclosure agreement, or a confidential programme or customer
identifier they let slip. Absent that, capture it.

[`/discovery-call`](../discovery-call/SKILL.md) holds the calibrated version of
this boundary and is the authority when the two are read together: record the
person to `brain/people/`, quote key claims verbatim, source it as
*"call with `<name>`, `<date>`"* — and when a call mixes open and confidential
material, capture the open part rather than dropping the whole call.

**Record when it is the actual reason behind a decision the project made**
(widened further 2026-08-05, same decision):

- A private fact or circumstance about a named person, **if it was load-bearing
  for a decision** — record the fact plainly, as the reason, not as colour.
  *"The integration stalled after [name] left the company"* is the record;
  speculation about why they left is not.
- A characterisation of a named person's **conduct**, if that conduct is what
  the decision responds to — record what happened, in neutral language, not a
  judgment of their character. *"[Name] gave three incompatible answers about
  lead time across two calls"* is a finding; *"[name] is unreliable"* is not.

The test is whether the fact is the **cause** of something the project decided,
not whether it is merely interesting. If you would not cite it in the decision
record's reasoning, it does not belong in the digest either.

**Still leave out, no exception:**

- **Contact details and private identifiers** — personal email addresses, phone
  numbers, home addresses, account numbers. The person can be named; their
  contact card cannot.
- **Anything under an employer's confidentiality or a non-disclosure agreement.**
  The strictest line here, and load-bearing-to-a-decision does not override it.
- **A customer's own material** — their files, specifications or records, pasted
  into the chat. Naming the customer and recording what they wanted is fine;
  reproducing their material is not.
- **Health information**, unless the person disclosed it publicly themselves.
- **Anything the other party explicitly placed off the record**, regardless of
  relevance to a decision. This means a stated confidence — "don't repeat this",
  an agreement, a confidential identifier — not merely a private setting. A
  two-person call is not automatically confidential; a sentence prefaced with
  "between us" is.

When a line is genuinely ambiguous, write the finding without the name and note
that a name exists. Do not drop the finding.

### 6. Commit, scoped

The digest, the brain entries, and the history index in one commit with a plain
dated message. Regenerate the web-page twins. Then say in one line what the period
was about — that sentence is usually the most useful output of the whole ritual.

## Cadence

**Weekly, plus at session close.**

Weekly rather than at milestones, because **the container can be reclaimed at any
time** — waiting for a natural stopping point risks losing everything since the
last one. A quiet week costs two minutes and one line.

At session close, [`wrap-session`](../wrap-session/SKILL.md) runs this rather than
relying on remembered context, which by then is the least reliable it will ever be.

**Each project's chat captures its own history.** A transcript lives in the
container of the session that produced it, so no other chat can reach it — this is
the one ritual that genuinely cannot be centralised. The
[fleet audit](../fleet-audit/SKILL.md) checks freshness across projects and reports
any whose history has gone stale, which is the enforcement.

## Judgment

- **Volume is not the goal.** A week that yields three brain entries and a
  four-line history note has been captured well. Twenty entries usually means
  transient chatter was promoted.
- **The digest is raw material, not a deliverable.** Nobody reads 85 KB. Its job is
  to be *searchable later* and to feed step 3.
- **Quote the owner; paraphrase yourself.** His words are evidence. Yours are
  already in the repository.
- **Capture the correction, not the recovery.** "The first implementation checked
  the gate before the label, so it blocked the work that must never be blocked" is
  worth more than "fixed a bug".
- **A finding whose source has died is still worth recording** — mark it
  `confidence: low` and say the transcript is gone. Better a flagged memory than a
  silent gap.
- **Do not editorialise the history.** It is a record. If a week went badly, the
  record says so; that is what makes the good weeks mean anything.
