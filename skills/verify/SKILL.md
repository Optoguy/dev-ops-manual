---
name: verify
description: Adversarially verify a document, draft, or set of claims — audit every citation, cross-reference key claims against public sources, and report verdicts most-severe-first without editing anything. Use when asked to check work, fact-check, verify claims or citations, red-team a draft, or before anything goes external (a page, a plan, a post, a spec). If the repo has its own verification skill (e.g. brain-verify), use that instead.
---

# Verify a document against its sources and the public record

Report-only: this skill never edits the document under review and never
"fixes" the underlying knowledge — findings become proposals for the owner.
The stance is adversarial: for each claim, try to refute it. A verification
pass that only confirms is a rubber stamp.

## Procedure

1. **Parse into claims.** Extract every substantive claim (quantitative,
   factual, attributive) with whatever citation it carries. An uncited
   substantive claim is an immediate finding — it can't be audited, which is
   the problem.

2. **Internal citation audit** (every cited claim): open the cited source —
   a knowledge file, a doc, a dataset — and judge:
   - **SUPPORTED** — the source says this.
   - **MISQUOTED** — the source says something materially different (quote both).
   - **NOT FOUND** — the citation doesn't contain the claim.
   Also flag claims that cite deprecated or reference-only material as if it
   were validated — that's a status laundering finding, not a citation finding.

3. **External cross-reference** (key quantitative and factual claims): search
   public sources — official documentation, standards catalogs, vendor and
   company sites, published papers. Verdicts:
   - **CORROBORATED** (cite the public source)
   - **CONTRADICTED** (quote what the public source says — highest severity)
   - **NOT PUBLICLY VERIFIABLE**
   **Paywall honesty:** the contents of paywalled sources (standards clause
   text, paid reports) cannot be publicly verified — mark **PAYWALL-LIMITED**
   and state exactly what could be checked (existence, edition, date) versus
   what could not. Never infer clause content from abstracts.

4. **Scale with agents.** For anything longer than a page, fan claims out to
   parallel verification agents with an adversarial framing ("try to refute
   this claim"), one cluster per agent; internal and external checks run
   concurrently.

5. **Keep verification separate from ingestion.** Public material found while
   verifying is for checking only — it enters the project's knowledge base only
   through the normal capture discipline with owner review. A corroborating
   source is a *promotion candidate* for reference-only content; promotion is
   the owner's call, never automatic.

6. **Output: a verdict table** — claim / citation / internal verdict / external
   verdict / note — ordered most severe first, plus summary counts and proposed
   fixes. On request, save it beside the draft as `<name>-VERIFICATION.md`
   (committed only with owner approval, scoped staging as always).

## Severity order

CONTRADICTED-by-public-source > MISQUOTED / NOT-FOUND citation > uncited claim >
reference-only or deprecated content cited as validated > PAYWALL-LIMITED /
NOT PUBLICLY VERIFIABLE (the last two are inventory, not failures).

## Judgment

- **Verify the claims that carry weight.** A wrong number in a headline or a
  price is severe; a wrong adjective in a caption is not. Spend the adversarial
  effort where being wrong costs something.
- **"I couldn't verify it" is a finding, not a failure** — the honest inventory
  of unverifiable claims tells the owner exactly what they're asserting on
  their own authority.
- **Never soften a CONTRADICTED into a "nuance."** Quote both sides verbatim
  and let the owner rule.
