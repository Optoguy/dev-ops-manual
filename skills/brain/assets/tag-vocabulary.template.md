---
title: Controlled tag vocabulary
tags: [governance, reference]
date: <YYYY-MM-DD>
status: active
---

# Controlled tag vocabulary

The single most useful piece of brain governance. Without it, tags drift into
hundreds of once-used labels that are decorative rather than retrievable. This
file is the allowed list. **Only tags on this list may be used.** Adding a tag is
a deliberate act — add it here in the same commit and say why. A tag earns its
place only if someone asking "what do we know about X?" would plausibly land on
it. Aim for 2–5 tags per file.

Organize tags into a few **facets**. Most files carry one or two DOMAIN tags,
one ARTEFACT tag, whatever SUBJECT tags apply, and a STATUS tag only when the
file's standing is non-obvious.

## Facet 1 — DOMAIN (what field of knowledge)

| Tag | Use when the file is about… |
| --- | --- |
| `<domain-a>` | <…> |
| `<domain-b>` | <…> |

## Facet 2 — ARTEFACT TYPE (what kind of document this is)

| Tag | Use when the file is… |
| --- | --- |
| `decision` | A dated decision record in `brain/decisions/` |
| `strategy` | Forward-looking strategic thinking: options, theses, positioning |
| `process` | How the project does a thing repeatably — a procedure or operating model |
| `reference` | Look-up material: catalogues, directories, literature summaries |
| `lessons` | Hard-won practical lessons — what went wrong and why |
| `open-questions` | Unresolved questions awaiting an answer |
| `planning` | Schedules, sequencing, the plan |

## Facet 3 — SUBJECT (the business/market/product side)

| Tag | Use when the file concerns… |
| --- | --- |
| `<subject-a>` | <…> |
| `<subject-b>` | <…> |

## Facet 4 — STATUS / PROVENANCE (how this file may be used)

| Tag | Use when… |
| --- | --- |
| `reference-only` | May inform thinking but must not be relied on as project work product |
| `internal-only` | Never leaves the project — sensitive strategy, third-party assets |
| `provenance` | Part of the clean-sheet provenance record |
| `governance` | Constraints, repo rules, permissions, claims discipline |

---

## Notes on judgement calls

- A low-frequency tag is fine if it names something a query will ask for — low
  frequency then means the brain is *thin* on that axis, not that the tag is
  useless.
- Don't create a tag that matches nearly every file (e.g. `knowledge`) — a tag
  that discriminates nothing is noise. Directory structure already says it.
- When you consolidate the vocabulary, record the old-tag → new-tag migration map
  here so the history of why a tag disappeared is visible.
