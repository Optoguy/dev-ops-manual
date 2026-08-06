# Goals: the owner decides, PolyBot may type — and PolyBot translates the plumbing

**Date:** 2026-08-06
**Status:** adopted on merge of the pull request that carries this file
**Changes:** `conventions/goals-and-measures.md` (rule 1 refined),
`conventions/three-roles.md` (charter duties 7 and 10)

## The instructions

The owner, 2026-08-05/06, reviewing PolyBot's boot boundaries:

> I'm wondering about boundaries. Shouldn't polybot take my input to create and
> edit plans and goals?

> I also want polybot to help me understand the merge, pull, push process and
> explain that in simple terms for me

## Decision one — deciding and typing are different acts

"Only the owner writes `plan/goals.json`" was written on 2026-07-29, when the
same agent doing a repo's work would have been writing that repo's gate — an
agent authoring its own goals grades its own homework. The guard was right; its
implementation conflated the **decision** with the **file edit**.

The cost was measured, not hypothetical: medtech's end goal sat missing for a
week while its content — the owner's own dictated sentence — waited for him to
become a JSON editor. Two projects stayed gate-blocked on typing, not on
deciding.

**The refinement:** goal *content* originates with or is ratified by the owner,
in a live chat, in his words. The file edit may then be done by PolyBot or by a
project chat working with him directly. Three guards carry the original
protection:

1. **Ratification in the live chat, always** — no unattended run ever touches a
   goals file. An agent cannot unblock its own gate; it can only bring a draft.
2. **Provenance in the commit** — every goals commit quotes the owner's
   approving words and their date.
3. **Independent audit** — the fleet audit verifies the trace on every
   goals-file change. This is why the relaxation is safe now and was not on
   2026-07-29: the three-role split created an auditor with no stake in the
   actor's work.

## Decision two — PolyBot explains git in plain terms, every time

Charter duty 10. Whenever PolyBot asks the owner to merge, or mentions a pull
request, branch, push, or conflict, it says in one plain sentence what the thing
is and what will be true after he acts. Never assuming an earlier explanation
carried over. This extends the 2026-07-28 plain-language rule ("say where to
click and what will be true afterwards") from navigation to the version-control
concepts themselves.

## What did not change

The gate itself; the requirement that a goal carries a measure with a real
baseline; the end goal's review cadence; agents never inventing-and-committing
goals silently; the night shift's inability to write goals under any policy.
