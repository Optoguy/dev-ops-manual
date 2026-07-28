---
name: ship-web-app
description: Build and ship a web product the house way — one shared engine with swappable modules, a provider abstraction behind a stable contract, self-contained/CSP-safe frontend, Cloudflare Pages+Functions+D1 hosting, generation from a single source of truth, and a security-hardening pass. Use when building a web app, tool, or site; choosing a hosting/AI stack; structuring frontend + backend; or preparing something to deploy.
---

# Ship a web product

The architecture that recurs: a **thin, self-contained frontend** over **one
shared engine**, with all vendor/AI coupling isolated behind a **stable contract**
in a single backend file, hosted on **Cloudflare Pages + Functions (+ D1)**, and
generated from **single sources of truth** so nothing can drift. Opinionated,
cheap to run, and boring to operate — on purpose.

## The architecture

1. **One shared engine, swappable modules.** Everything domain-agnostic lives in
   the engine (the session loop, the data model, transport). Everything
   domain-specific is a module registered with it. *Adding a product area = adding
   a module*, not editing the engine. Multiple UIs/skins are **thin views** that
   own *look only* and are driven through a small hook contract — a change to the
   logic is a one-file edit every view inherits.

2. **A stable contract isolates every dependency.** Define the wire contract once
   (e.g. browser POSTs `/api/chat {messages}` → `{reply, updates[], done, ...}`;
   `/api/health` → `{ok, ...}`) and never let the frontend scrape text or know
   which vendor answered. Then swapping providers, or local↔prod, is a
   single-file change behind the contract.

3. **Provider abstraction + cost discipline.** Default to the **cheap, fast**
   model (a flash-lite tier) and keep the premium/alternate provider behind an
   env switch (`PROVIDER=…`). Both share the same input/output shape. Use
   structured output (a response schema) so every model turn parses — the UI
   never regexes a reply. Set a **spend cap** on day one; bound provider calls
   with a timeout and surface real errors instead of a masked 502.

4. **Self-contained, dependency-free, CSP/offline-friendly.** Prefer a
   zero-dependency stdlib dev server; no external assets of any kind (inline CSS/JS,
   embed images as data URIs); generate PDFs/artifacts in-browser without
   libraries. Local dev needs **no build** — the server serves the source files;
   a build step only inlines things for single-file distribution.

5. **Generate from a single source of truth.** Anything that exists in two places
   drifts. Generate the production proxy from the dev server; generate landing
   pages, dashboards, and design-token previews from one config/markdown with a
   `build_*.py` script; label generated files "generated — do not edit by hand."
   The browser only ever calls same-origin endpoints, so the key stays
   server-side and nothing changes between local and prod.

## Hosting (Cloudflare, git-connected)

- **Pages** serves the static thin-view HTML/JS; **Functions** are the same proxy
  the dev server implements, generated from it so they can't diverge.
- **D1** stores structured records (completed sessions, leads); bind it in
  `wrangler.toml`. Watch bindings on deploy — a bad binding can break the build.
- Git-connected: **every push auto-deploys.** Add a `rev` marker to `/api/health`
  so you can confirm which build is live.
- Add a `_headers` file: CSP, `X-Frame-Options`, `Referrer-Policy`.

## Security-hardening pass (do it before real traffic)

- **Protect write endpoints:** origin allowlist on anything that writes; retry on
  serial/id collisions.
- **Rate-limit `/api/*`** (a WAF rule, per-IP), cap request size, cap turn count.
- **Sanitize any visitor-controlled data before an agent or report reads it** —
  strip markdown/control characters, truncate; an analytics row is untrusted
  input, and a downstream Routine reading it is prompt-injectable.
- **Keys never reach the browser.** Verify data-handling claims (a free-tier API
  may train on content) before you print a privacy promise.
- **Unguessable tokens** for anything shared by link; escape everything in a
  renderer once viewer ≠ author (stored XSS becomes real).

## Judgment

- **Isolate the thing most likely to change** (the AI provider, the host) behind
  the narrowest possible contract, *before* you need to swap it. The one-file swap
  is the whole payoff.
- **Ship to validate first.** Hold back monetization/lead machinery until a
  feedback release confirms the core is valuable; a phased PLAN (see
  `/plan-track`) makes the "defer until value confirmed" line explicit.
- **No build for local dev** is a feature — it keeps the edit→see loop instant and
  keeps contributors from fighting a toolchain.
- **Autoplay/self-demo mode** (`?autoplay=1`) pays for itself three times: manual
  QA, headless verification sweeps, and marketing captures. Suppress it from
  analytics so demo runs don't pollute the funnel.
