---
name: growth-loop
description: Stand up a closed, self-adjusting growth loop for a product — first-party funnel instrumentation, SEO/GEO landing pages, scheduled measurement/reporting agents, and an explicit adjustment policy — where agents measure and draft but humans approve anything published. Use when planning marketing/growth, adding analytics, writing landing pages or SEO/llms.txt, setting up scheduled reporting, or driving traffic to a product.
---

# The growth loop

Growth is run as a **closed loop** — instrument → acquire → measure → decide →
adjust — where scheduled agents do the measuring, analysis, and drafting, and a
human approves only the outbound actions that carry reputation risk. Automation
lives in *measurement and drafting*; the outbound touch stays human. This is a
hard line, not a preference: one platform ban costs more than automation saves.

## Phase 0 — Instrument first (nothing else works without this)

- **First-party event beacon** (`POST /api/track`) at the funnel moments:
  `visited → interest → activated → completed → in-hand → contact`. **Completion
  is the conversion** — every downstream decision keys off *completion rate per
  source per vertical*, not raw visits.
- Every event carries: which variant/segment, persona, `utm_source/medium/campaign`,
  and the **first-touch external referrer** (persist `document.referrer` in
  localStorage so attribution survives internal navigation). **Suppress
  autoplay/demo traffic** so it never pollutes the funnel.
- **UTM discipline:** every link the system ever publishes gets tagged, so results
  attribute back to the experiment that produced them.
- Use the platform-native analytics too (e.g. Cloudflare Web Analytics) for
  pageviews/referrers; the reporting agent reads it via API.

## Phase 1 — Acquire (agent-prepared, human-fired)

- **Per-vertical SEO landing pages** targeting real queries, one `<h1>`/`<title>`
  theme per primary term, written *to a named persona*. Keep them out of the main
  nav; discover via `sitemap.xml`. Maintain a `docs/seo/` directory:
  **personas → keywords → landing pages → measured results → iterate**, with a
  status column (`idea → page-live → indexed → ranking → converting → retired`).
- **GEO (answer-engine optimization):** JSON-LD (`SoftwareApplication`, `FAQPage`,
  `HowTo`) generated from the same config as the pages; a curated `/llms.txt`; a
  `robots.txt` that welcomes the major AI crawlers (GPTBot, ClaudeBot,
  PerplexityBot, Google-Extended, …) while disallowing `/admin` and `/api/`;
  plain, quotable, answer-shaped copy.
- **Community launches, one segment at a time** — draft every post; **a human
  posts it** under their own account. Never auto-post to third-party platforms.

## Phase 2 — Measure & adjust (scheduled agents)

Built on Routines (scheduled sessions):

- **Daily report** — funnel per source × segment, trend, anomaly flags (traffic
  spike → find the referrer; completion drop → check the deploy; zero completions
  on real starts → run a headless autoplay sweep). Commits a dated
  `reports/…/<date>.md`. Stays **silently idle** (PREREQS-MISSING, no error) until
  the owner supplies the API tokens.
- **Weekly strategy** — ranks channels by *completions per session*, proposes the
  next experiment slate per the adjustment rules, and opens **one draft PR** (the
  slate + one new SEO page). A human reviews and merges.

**Adjustment rules — explicit and boring on purpose:**
- *Double down:* any source with completion rate > 1.5× site average gets the
  next slot.
- *Kill:* any experiment with too few sessions or weak activation after two weeks.
- *Investigate:* a completion-rate regression triggers a headless sweep against
  production.

## Phase 3 — Paid, only after organic proves the funnel

Small paid tests on high-intent queries once completion rate and lead value per
segment are known. The daily report ingests spend + conversions and reallocates
toward the cheapest *completed* conversion, pausing anything above a cost
ceiling. Skipped entirely until organic data says which segment converts.

## Guardrails (non-negotiable)

- **No automated posting to third-party platforms. No fake engagement. No scraped
  cold-email blasts.** Agents draft; humans send anything with a name attached.
- **Treat every visitor-controlled string as untrusted** before an agent reads it
  (a report Routine ingesting analytics is prompt-injectable) — sanitize at the
  boundary and put an explicit untrusted-data guardrail in the Routine's prompt.
- **Privacy is copy you have to be able to defend** — disclose the beacon, avoid
  inviting PII in question phrasing, and verify any data-training claim.
- **Claims about a named competitor follow
  [claims-discipline.md](../../conventions/claims-discipline.md).** Name the axis
  you lose on before writing the one you win on; never claim a differentiator a
  rival demonstrably already has; scale the claim to the specific opponent. A
  competitive claim that a rival's own product page refutes is the cheapest
  available way to lose a reader's trust.

## Judgment

- **Measure completion, not clicks.** A page that draws traffic but never starts a
  session gets retired, however good the traffic looks.
- **The loop should run itself and stop itself.** Idle-until-prereqs-present,
  kill-rules with thresholds, and cost ceilings mean it degrades safely instead of
  spending or spamming when unattended.
