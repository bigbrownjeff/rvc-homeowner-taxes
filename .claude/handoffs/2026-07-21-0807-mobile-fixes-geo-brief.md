# Handoff — mobile fixes + fully geo-aware brief
**Date:** 2026-07-21 (session continued from 2026-07-20 evening) · **Project:** rvc-homeowner-taxes

Continuation of `2026-07-20-1943-nassau-fanout-launch-prep.md` (read that first for the fan-out,
outreach waves, daily sweep, and coverage-page context). This note covers the late-night mobile
arc, PRs #22-#25, all merged + deployed + live-verified.

## Goal
Jeff's phone screenshots drove three fixes (endless scroll on the brief; voices page unusable on
mobile) plus two feature asks (sample-address quick links from voices; make the brief's headline /
gist / big numbers follow the resolved address, not just section 03).

## What got done
- **#22 iOS input zoom**: "endless scroll" root cause was NOT layout — iOS Safari auto-zooms on
  focus of any input under 16px and never zooms back (kit inputs were 14px). Inputs → 16px.
  Verified first that no real overflow existed (390px measurement: doc height == content height).
- **#23 mobile collapse**: section-05 evidence rows + geocoder officials cards → native
  `<details class="m-collapse">`. Markup ships `open` with summaries `display:none` above 760px,
  so desktop and no-JS render exactly as before; a matchMedia check closes them at load on
  mobile; cards are created open only on desktop. No new deps.
- **#24 voices mobile + quick links**: voices.html had ZERO responsive rules (fixed 210px/280px
  grid columns). Page-local `@media(max-width:760px)` with attribute-substring selectors
  (`div[style*="grid-template-columns:1fr 280px"]{...!important}`) collapses rows; shell 48px→24px.
  Plus Jeff's ask: named locations deep-link to the brief with verified sample addresses —
  `index.html?addr=<urlencoded>#asks` (Locust Valley hero, Long Beach, Sea Cliff/North Shore,
  Northport + Setauket which intentionally demo the honest outside-Nassau fallback). index.html
  gained the `?addr=` param: prefill + geocode + geo-refresh WITHOUT signup or counter ping
  (keeps engagement metrics honest — only typed lookups count).
- **#25 hero geo-refresh**: `refreshHero(c,d)` swaps eyebrow, H1, lede, gist, and the five-number
  strip from districts.json fields. Direction-aware headline (LV "333 fewer students" / East
  Meadow "grew by 755... Most of Nassau went the other way" / flat variant). Strip tiles rebuild
  with each district's own source_ref links (students Δ · levy · statewide 2% cap · median ·
  Enhanced-STAR parcels); missing field = dropped tile, never a fake. RVC + non-Nassau restore
  the captured base HTML. Hooked inside refreshMoney's loadDistricts() resolve (one data load).

## What worked (and why)
- **Root-cause before patching**: measured document vs content height (no overflow) before
  touching anything — found the 16px-input rule instead of shipping a wrong layout "fix."
- **dump-dom harness**: `chrome --headless=new --virtual-time-budget=9000 --dump-dom
  "http://localhost:PORT/index.html?addr=..."` + grep = fast end-to-end test of the geocode →
  render pipeline with real network. Used for every scenario (decline/growth/default/Suffolk),
  including one against production after deploy.
- **Attribute-substring CSS** overrides inline styles (with !important inside a media query) —
  the only sane way to retrofit responsiveness onto a page of inline styles without touching
  every row.
- **Capture/restore base pattern** (HERO_BASE like MONEY_BASE): geo swaps are always reversible;
  an RVC lookup after an LV lookup restores the exact original page.

## What didn't / dead ends (recorded to agent memory: headless-mobile-render-gotchas.md)
- **Chrome headless clamps window width ~500px** — "390px" screenshots are left-crops of a wider
  layout; text looks clipped mid-word. Cost a full phantom-overflow chase on voices. Verify
  mobile text-wrap at 760px (inside the media query, above the clamp) or on-device.
- **Dark-pixel edge scans false-positive on full-bleed dark bands** (green #1e6b3d avg <100
  luminance) — exclude flat-color edge rows before claiming clipped text.
- **claude-in-chrome tab froze** mid-iframe-test (navigation during eval); fell back to the
  dump-dom harness rather than fighting it.

## Key decisions
- Positions-cut and village-rate tiles have NO per-district equivalent — for other districts they
  are replaced by levy/median/parcel tiles we actually have, not imitated.
- Sample-link visits don't increment counters or signups (synthetic traffic stays out of pillar-c
  instruments).
- Suffolk quick links kept ON the voices page — demoing the honest refusal is persuasive.
- Deck excluded from responsive retrofits (it is the print artifact).

## How to reproduce / pick up
- Test harness: serve `site/` with `python3 -m http.server`, then dump-dom + grep (see above).
  Sample addresses verified against the Census geocoder: 22 Horse Hollow Rd Locust Valley ·
  235 Lido Blvd Long Beach · 112 Franklin Ave Sea Cliff · 101 Carman Ave East Meadow (growth) ·
  158 Laurel Ave Northport + 100 Old Town Rd East Setauket (Suffolk fallback).
- Geo-swap logic all lives in index.html's inline script: `refreshHero`, `refreshMoney`,
  `build(fromUser,sample)`, `?addr=` handling at the bottom.
- Deploy: `npx wrangler pages deploy` from repo root; custom-domain propagation lags 20-60s
  (poll, don't diagnose); missing assets 200 as index.html (SPA fallback).

## Open threads / next steps
Unchanged from the previous handoff (Wave-1 send prep Jul 29, LIBOR call, LWV/Chamber routes,
`[street address]` placeholders, trash stale canzoneri Gmail draft, L5 calculator flow-back,
playwright install for the e2e gate, Glen Cove/Long Beach city-roll rates, officials lane,
disable daily sweep after Aug 1). New this session:
- Consider adding the East Meadow (growth) case to the §7 regression list — it exercises the
  direction-aware headline branch.
- Jeff should sanity-check the collapse + voices pages and a quick-link flow on his actual phone
  (the iOS zoom state needs a tab reload to clear before judging).
