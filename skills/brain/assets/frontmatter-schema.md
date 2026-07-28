# Brain frontmatter schema

Every file under `brain/` (except `_meta/` and `INDEX.md`) opens with YAML
frontmatter. `brain_lint.py` enforces this and fails the commit if it's wrong.

## Knowledge files (`brain/knowledge/**`)

```yaml
---
title: MTF measurement calibration procedure
tags: [metrology, mtf]          # 2–5, from the controlled vocabulary
sources:
  - drive_id: 1AbC...           # or: repo/url/"Claude session — <topic>"
    name: "MTF Cal Notes v3"
    modified: 2026-05-14         # source's own last-modified date
last_synced: 2026-07-06          # when this file was last checked vs its sources
confidence: verified             # verified | inferred
status: active                   # active | deprecated
---
```

- `confidence: verified` means every claim is directly supported by a source.
- `confidence: inferred` means the file draws a conclusion not stated verbatim in
  any source — flag those spots inline with *(inferred)* too.
- `status: deprecated` replaces deletion. Add a one-line dated reason at the top
  of the body; keep the file so history and inbound links survive.

## Other brain files (decisions, people, constraints, open-questions)

```yaml
---
title: Adopt Launch Plan Rev 4 as plan of record
tags: [decision, planning]
date: 2026-07-13
status: active
---
```

## Writing style for knowledge files

- Lead with a 1–3 sentence summary of what the file covers and why it matters.
- Declarative facts over narrative. "The pipeline runs at X fps" beats "we
  explored running the pipeline."
- Concrete numbers, part numbers, thresholds, settings — the highest-value
  content for later retrieval.
- Put uncertainty in a final `## Open questions` section, not mixed into the body.

## Deduplication (before writing a new file)

1. Search `INDEX.md` for existing files with overlapping tags or title terms.
2. Overlap → **merge** into the existing file, append the new source to its
   frontmatter. Don't create a parallel file.
3. Sources conflict → newer `modified` wins; record the conflict under a
   `## Superseded information` section so the history stays visible.
