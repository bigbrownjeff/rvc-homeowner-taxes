# Report: site/validation.html (Fact check + full ledger)

## What was ported
Rebuilt `site/validation.html` on the shared shell (Archivo, `assets/site.css`, `<div id="site-nav" data-current="factcheck">`, `.site-foot`, `assets/nav.js`). Structure:

- Sections 01-04 + hero + stat strip + green closing band: ported 1:1 from `design_handoff_rvc_site_redesign/Fact Check.dc.html` (copy verbatim, inline style values hoisted into a page `<style>` block unchanged, plus mobile media queries at the README's 24px-gutter breakpoint).
- Sections 05-16: the FULL old ledger, restyled to the new system (hairline table rules, uppercase 10.5px headers, zero radius, no cards). Every fact row, `id="f-*"` anchor, source link, verified date, and used-on column survives. Section ids `#demo #schools #star #s467 #village #assess #leg #derived #memos #watch #unknown` kept; new `#ledger` anchor on the ledger intro.

## Content updates (all per task; receipts in DESIGN_CONVENTIONS.md)
1. `f-office`: Sen. Siela Bynoe (D, SD-6) is RVC's senator (nysenate.gov/senators/siela-bynoe/district, verified 7/20/26); Canzoneri-Fitzpatrick (R, SD-9) kept only as S3309 sponsor + RVC resident, explicitly "not RVC's senator"; added Nassau LD-1 Leg. Scott Davis (nassaucountyny.gov/505/District-1---Scott-Davis, 2026 court-settlement map).
2. New row `f-downsize-intent` in Demographics & housing: carries the 68% age-in-place number up front (bolded, plus "Never cite the 68% as downsize demand"), then what each source actually supports, mirroring the Brief .dc's evidence-block phrasing. Sources: pinned Freddie Mac gcs-web release URL, AARP /pri/ 2024 survey URL (task's verified URL, not the .dc's), HousingWire June 2026, NYS HCR Hochul Apr 2025. Used on: brief (index.html).
3. Used-on rewrite: 25× `deck.html` labeled "deck" (was index.html), 26× `index.html` labeled "brief" (was brief-2026-08.html). `grep -c brief-2026-08` = 0.
4. Vintage-watch ACS item reconciled: site standardizes on ACS 2020-24 for value/income ($818,700 / $151,938); pages print 27.9% (2,076 of 7,453, ACS 2019-23) for senior share because that is what `RVC Brief.dc.html` actually prints (checked: hero lede + stat cell), headline rounds to "a quarter of our homes"; both vintages labeled in `f-senior-share` (which now also cites both B25007 vintages with links).

## Deviations from spec (with reason)
- Section 03 closing line: "the full validation page" (absolute URL) became "the full ledger below" → `#ledger`, and reconcile link made relative — the ledger now lives on this page (the agreed structural decision). "Back to the brief" → `index.html`.
- Footer right text: .dc's "Fact check completed June 9, 2026 · math audit July 2026" + appended "· ledger updated July 20, 2026" (the ledger's maintenance stamp must survive).
- All em/en dashes in legacy ledger copy replaced with colons/commas/hyphens per the hard rule (year ranges "2019–23"→"2019-23", vote counts, etc.). Verbatim OSC and Hochul quotes untouched (contain no dashes). Minus signs (U+2212) in derivations kept.
- Old crumbs row dropped (nav replaces it); breakeven/reconcile/governance stay reachable via ledger links.
- Ledger tables get `min-width:640px` inside `overflow-x:auto` wrappers below 760px so 3-column rows stay legible; the container scrolls, the page does not.

## Verification
- Screenshots (READ, all in scratchpad `/private/tmp/claude-501/-Users-jeffpinto/97c86533-267d-4280-ab41-8830382568c8/scratchpad/`): `validation-desktop.png` (1280×2000 top), `validation-desktop-bottom.png` + `tail2.png` (full/tail), `vm-frame.png` + `mob-0..4.png` (true 390px mobile). Nav renders, Fact check underlined green, Archivo only, no cream, hairlines present, band + gold/outline buttons correct; mobile shows Menu button, hero wraps, no page-level overflow.
- **Headless gotcha found (affects ALL page agents):** macOS Chrome headless clamps window width to ~500, so `--window-size=390` screenshots crop a ~500px layout — pages look overflowed when they are not (probe test confirmed; voices.html shows the same artifact). True-mobile verification here used a 390px iframe wrapper (`mobile-frame.html` in scratchpad); Playwright confirmed `scrollWidth` 375 ≤ 390. Orchestrator: re-check other lanes' "mobile OK" claims with this in mind.
- Anchors: python check — 17 in-page `href="#..."` all resolve; all 36 old `f-*` ids + 11 section ids + `f-downsize-intent` + `ledger` present; zero broken `validation.html#...` references from other site pages.
- Greps: `F1ECE2|FAF6EC|Source Serif|IBM Plex|Inter` = 0; `—|–` = 0; `border-radius|box-shadow` = 0; mailto = only the two `jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20` variants.
- JS: nav menu toggle exercised (menu-btn visible <760px, `open` class toggles, 5 links + Act now, current=factcheck).

## For the orchestrator
- A `python3 -m http.server 8765` serving `site/` is still running (started for Playwright, which blocks file://; left up in case parallel lanes are using it). Kill when the fleet is done.
- The shared Playwright MCP browser is being trampled by parallel agents (a screenshot mid-run showed reconcile.html from another lane). Lanes should verify with their own headless Chrome instances.
- `f-attrition` used-on says break-even only; if the new brief also cites the 60-100/yr figure, add `index.html` to that row.
