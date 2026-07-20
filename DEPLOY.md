# Deploying rvc-taxes.jeffpinto.com

Everything in `site/` is static (no build step) plus one advanced-mode worker (`site/_worker.js`) for `/api/signup` and legacy redirects. Hosting: Cloudflare Pages; DNS in the Cloudflare jeffpinto.com zone (moved from Hover 2026-07). Config lives in repo-root `wrangler.toml` (project name, output dir, KV binding).

## Deploy

```bash
npx wrangler pages deploy        # reads wrangler.toml: project rvc-taxes, output site/
```
Pages invalidates its own cache on deploy. Hard-refresh to bypass browser cache.

If wrangler.toml is ever absent, the explicit form is `npx wrangler pages deploy site --project-name rvc-taxes` — but that skips the KV binding; `/api/signup` will 503 until the binding is attached (dashboard → rvc-taxes → Settings → Bindings, KV `SIGNUPS` → namespace id `55371b2ca075430faeeae249f9b036cc`).

## One-time setup (done)

- Pages project `rvc-taxes` created; custom domain `rvc-taxes.jeffpinto.com` attached 2026-07-20 (same-account zone: proxied CNAME auto-created).
- KV namespace `SIGNUPS` (`55371b2ca075430faeeae249f9b036cc`) created 2026-07-20 for the action-kit mailing list. Read signups with:
  ```bash
  npx wrangler kv key list --namespace-id 55371b2ca075430faeeae249f9b036cc --remote
  npx wrangler kv key get "signup:<email>" --namespace-id 55371b2ca075430faeeae249f9b036cc --remote
  ```

## What's served (July 2026 redesign — "Modernist" system, RVC green/gold, Archivo)

| Path | Content |
|------|---------|
| `/` | The brief: main landing + action kit (Census-geocoder letter builder, five cards, prefilled mailtos, copy-letter) |
| `/fiscal-math.html` | Mechanics: long-form fiscal write-up for aides |
| `/validation.html` | Facts & sources: the ledger backing every number on the site |
| `/voices.html` | Curated quote library (condensed); `/voices-library.html` = full archive |
| `/calculator.html` | Tax & outcomes calculator (July 2026 audited constants; no chart libs) |
| `/reconcile.html` | Bill reconciler — real county/village roll mechanics (math untouched by redesign) |
| `/breakeven.html` | Break-even instrument (math untouched by redesign) |
| `/deck.html` | The 8-page print briefing (old landing; print-first layout kept; ⌘P → PDF handout) |
| `/governance.html`, `/governance-options.html`, `/redraw-evidence.html` | Governance memos (re-skinned) |
| `/RVC_Legislator_Deck.pptx` | 26-slide deck; regenerate with `tools/build_deck_pptx.py` |
| `/api/signup` | POST {name,email,address} → KV `SIGNUPS` (email required) |
| `/brief-2026-08(.html)` | 301 → `/` (both `_redirects` and `_worker.js` handle it) |

## Notes

- Design source of truth: `design_handoff_rvc_site_redesign/` (checked into the repo) — tokens, copy rules (no em dashes), component patterns. Shared chrome: `site/assets/site.css` + `site/assets/nav.js`.
- Contact routing: every contact link is `mailto:jeff@bluecamelconsulting.com?subject=[rvc-taxes] …` — never any other email.
- Officials table in `/` (action kit): fetch-verified 2026-07-20 — Gillen CD-4, Suozzi CD-3, Bynoe SD-6 (RVC's senator under current lines), Canzoneri-Fitzpatrick SD-9 (S3309 sponsor), Griffin AD-21 (direct email griffinj@nyassembly.gov), Davis LD-1 (SDavis@nassaucountyny.gov). Re-verify before each politician-facing push.
- A real-browser pass is part of done — `curl` is not sufficient. After deploy: check the custom domain, run the action kit with a real address, and click one Copy letter + one mailto.
