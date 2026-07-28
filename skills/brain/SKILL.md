---
name: brain
description: Build and run a provenance-tracked knowledge base (a "brain") for a project — capture durable findings with sources, answer questions from it with citations, and keep it healthy. Use when asked to remember something, capture lessons or research findings, set up a knowledge base, answer what the project knows/decided/believes, or maintain/audit the brain.
---

# The brain — a project's durable, cited memory

A brain is the accumulated knowledge of a project: rules, numbers, failure modes,
validated procedures, market facts — each **traceable to a source**. It is the
opposite of chat scrollback. The bar for entry is high; the payoff is a project
that answers "what do we know about X?" from its own record, with citations,
instead of from a model's guess.

This one skill covers the whole lifecycle: **set up**, **capture**, **query**,
and **maintain**. For a large project, split it into per-verb project skills
(`/brain-capture`, `/brain-query`, `/brain-maintain`) — but the discipline below
is identical.

## Where knowledge lives

```
brain/
  knowledge/        durable, verified knowledge — the brain proper
    <domain>/       group into a subdir only when a topic has 3+ files; prefer tags over deep nesting
  decisions/        dated decision records (see /decision-log)
  people/           who's who (context, not a CRM)
  _meta/            machine state, not knowledge (tag vocabulary, manifests, eval questions)
  constraints.md    the hard constraints (mirror of CLAUDE.md's)
  open-questions.md unresolved questions awaiting an answer
  INDEX.md          GENERATED — one line per file; the retrieval entry point
```

`docs/` is for sharable output; the brain is internal. Keep the line hard.

## Frontmatter (every brain file)

See `assets/frontmatter-schema.md`. Knowledge files carry
`title, tags, sources, last_synced, confidence, status`; other brain files carry
`title, tags, date, status`. `confidence` is `verified | inferred`; `status` is
`active | deprecated`. Tags come from a **controlled vocabulary**
(`assets/tag-vocabulary.template.md`) — 2–5 per file, and adding a tag is a
deliberate act recorded in the same commit.

## Capture — findings → brain

1. **Select for durability.** Capture rules, numbers, failure modes, validated
   procedures — not a narrative of what happened today. *If it won't matter in
   six months, it doesn't go in.*
2. **Find the home first.** Check `INDEX.md` for files with overlapping tags or
   title terms. Strong overlap → **merge into the existing file** (append a
   source to its frontmatter, update `last_synced`, extend a section). New topic
   → new file in the right subdir with full frontmatter. Never create a parallel
   file for a topic that already has one.
3. **Distill, don't dump.** A knowledge file is shorter and higher-signal than
   its sources. Lead with a 1–3 sentence summary; prefer declarative facts with
   concrete numbers/part-numbers/thresholds over prose.
4. **Provenance on every claim.** Add a `sources:` entry naming what was reviewed
   (document, repo + date, "Claude session — <topic>", a call). Unsourced content
   is not written. If a conclusion is *inferred* rather than stated in a source,
   set `confidence: inferred` and flag it inline with *(inferred)*.
5. **Boundary check before writing** (the CLAUDE.md hard constraints): nothing
   the owner flagged as proprietary; no confidential identifiers. When a source
   mixes open and confidential material, extract the open facts and note the
   exclusion.
6. **Default session findings to reference, not gospel.** Frame session-derived
   findings as recorded observations/candidate methods. Promotion to "validated"
   is an explicit owner call — never write "proven"/"validated" about a claim
   only the session supports.
7. Run the lint gate: `python src/brain_lint.py --write-index` then
   `python src/brain_lint.py` (must pass). Commit with a plain dated message
   describing the *knowledge* (not the session), scoped staging, no push.

## Query — answer from the brain

1. **Start at `INDEX.md`.** Select candidate files by title and tags; read only
   those. Don't sweep the whole tree.
2. **Cite every substantive claim** with a file path (and section where useful).
   Uncited claims don't go in the answer.
3. **Respect frontmatter signals:** flag `confidence: inferred` claims as
   inferred; treat `status: deprecated` as historical context and say so.
4. If sources conflict, present both with dates — newer wins the headline, but
   surface the conflict.
5. **If the brain doesn't cover it, say so plainly.** General knowledge may
   *frame* the answer but must be labeled as background, never presented as a
   project finding. If the gap matters, offer to append it to
   `open-questions.md`.

## Maintain — keep it healthy

Run periodically. Report findings first; apply only mechanical, safe fixes —
anything judgment-laden becomes a proposal for the owner.

1. **Lint** — schema, cross-refs, index freshness.
2. **Staleness** — knowledge older than its subject plausibly is; deprecated
   files still referenced by active ones.
3. **Duplication** — heavily overlapping files → propose merges.
4. **Cross-references** — every "see <file> §N" must land on a real section.
5. **Open-questions grooming** — flag entries answered by later decisions (cite
   the answer); propose removals, never silent-delete.
6. **Tag health** — propose consolidation of near-synonym / once-used tags;
   retrieval by tag only works if the vocabulary stays controlled.
7. **Retrieval evals** — answer a fixed set of eval questions using the query
   discipline; score correct-and-cited / wrong / uncited. Include a couple of
   deliberately-unanswerable questions — a confident answer to those is a
   *failing* grade, not a pass.

## Iron rules

- **Deprecate, never delete.** Set `status: deprecated` with a one-line dated
  reason so git history and inbound references stay intact.
- **A new fact that contradicts an existing file is a finding, not an edit war.**
  Record the new result, mark the superseded claim with a date, surface the
  conflict to the owner.
- **One authoritative statement per fact.** Cross-reference; don't duplicate.
