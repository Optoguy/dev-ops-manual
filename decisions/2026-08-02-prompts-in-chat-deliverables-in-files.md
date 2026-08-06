# Prompts go in the chat; deliverables go in files

**Date:** 2026-08-02 (instruction given 2026-07-30, recorded here late)
**Status:** adopted

## The instruction

The owner, 2026-07-30, in his own words:

> when I ask for the prompt, give it to me in the chat rather than an MD file to
> download

Given after a set of three per-project adoption prompts was delivered as a file.
The prompts existed to be pasted into three other chats; a download made that a
three-step detour.

## Why this needed recording

`conventions/house-rules.md` already says the opposite-looking thing:

> **Deliverables the owner asks about are files, not chat text.** A report or
> memo that lives only in a reply gets buried; send it with `SendUserFile` and
> summarize in prose afterward.

Both rules are right, and neither states its boundary. Read alone, the house rule
says *file*; the owner's instruction says *chat*. A session following the written
convention would have made exactly the mistake that prompted the correction, and
the correction lived only in the owner's personal preferences file — not in this
repository, where every project inherits from.

## The decision

**The test is what the artefact is for, not what it contains.**

| The thing | Where it goes | Why |
|---|---|---|
| Something to **paste somewhere else** — an adoption prompt, a message to another chat, a snippet | **The chat**, in a fenced code block | Its whole purpose is to be copied. A file adds a download between the owner and the paste. |
| Something to **read or keep** — a report, a memo, an options memo, an audit | **A file**, via `SendUserFile`, with prose after | It gets buried in a reply, and it usually belongs in a repository. |

Short text asked for so it can be used elsewhere follows the first row. Files are
for things that live in a repository.

## Consequences

- `conventions/house-rules.md` gains the boundary alongside the existing
  deliverables rule, so the two are read together rather than in isolation.
- This applies in every project, not only where it was said.

## What this is evidence for

An instruction captured only in the owner's personal preferences does not reach
the projects. It took a history capture reading the transcript to notice that a
rule the owner had stated plainly was absent from the repository that exists to
carry rules between projects — three days after he said it.

**Provenance:** session transcript `9086f1e3-3340-52b3-aa9f-b9dccc26a2ab`,
2026-07-30. Digest: `docs/history/2026-08.md`.
