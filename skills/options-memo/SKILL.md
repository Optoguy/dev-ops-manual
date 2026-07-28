---
name: options-memo
description: Structure a decision before it's made — frame the question, set criteria, lay out 2–4 options with evidence and trade-offs, and recommend one with the reasoning shown. Use when weighing alternatives, asked "should we X or Y," facing a build/buy/defer or pricing/positioning choice, or preparing a decision for the owner. Pairs with /decision-log, which records the decision once made.
---

# Options memo — structure the decision, then let the owner make it

`/decision-log` records decisions; this skill is for the step before — turning
"we should probably figure out X" into a document the owner can decide from in
five minutes. The memo recommends; the human decides. Writing the options down
is what stops the best-argued-in-the-moment option from beating the best one.

## Structure (and procedure — write it in this order)

1. **The decision, in one sentence.** A question with discrete answers, not a
   topic. "Which provider do we default to?" not "AI strategy." Add: why now
   (what it gates or what deadline forces it) and the cost of deciding late.

2. **Criteria — 3 to 5, before looking at options.** Drawn from the project's
   constraints and goals (CLAUDE.md hard constraints are automatic criteria —
   an option violating one is dead on arrival). Weight them honestly: name the
   one criterion that dominates. Choosing criteria after examining options is
   how rationalization dresses up as analysis.

3. **Options — 2 to 4, including the honest default.** Always include
   "do nothing / defer" with its real consequences; often include one option
   you expect to reject, stated fairly (steel-man, not straw-man). For each:
   what it is, what it costs (money, time, reversibility), what it forecloses.

4. **Evidence, cited and labeled.** Facts from the project's knowledge base
   cited by file; general background labeled as background; unverified figures
   flagged (candidates for `/verify` before the decision if they carry weight).
   If evidence is thin, say the decision is under-informed and name the one or
   two facts that would firm it — sometimes the right output is "get this fact
   first," not a recommendation.

5. **The trade-off table.** Options × criteria, terse cells. The table's job is
   to make disagreement precise: an owner who picks differently should be able
   to point at the cell where they diverge.

6. **Recommendation — one option, reasons shown, reversal condition stated.**
   "Recommend B because criterion 1 dominates and B wins it; would flip to C if
   <fact> turns out true." Then write the best case *against* your own
   recommendation in two sentences — if you can't, you haven't understood the
   alternatives.

7. **Hand off.** The memo goes to the owner (buttons for the options, per the
   house interaction rule). Once they decide, record it with `/decision-log` —
   the memo becomes the decision file's context section, and the trickle-down
   happens there.

## Judgment

- **Match depth to stakes and reversibility.** A reversible tool choice gets
  half a page; an irreversible identity/money/legal choice gets the full
  structure and a `/verify` pass on its load-bearing facts.
- **Deadlines are criteria.** "Best option we can execute before the window
  closes" legitimately beats "best option."
- **If the owner keeps deferring the same memo, that's data** — either the
  decision doesn't actually gate anything (retire it) or it's missing the fact
  that makes it decidable (go get it).
