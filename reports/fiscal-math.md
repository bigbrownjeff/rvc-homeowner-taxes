# Port report: Mechanics.dc.html → site/fiscal-math.html

## What was ported
Full replacement of `site/fiscal-math.html` (old cream/serif long-form page) with the Mechanics design spec, per the conventions transform recipe:

- Standard page shell: Archivo font link, `assets/site.css`, `<div id="site-nav" data-current="mechanics">`, `.site-foot` footer (right-hand text "Every mechanism sourced · June 2026"), `assets/nav.js`.
- All content between `<x-dc>`/`</x-dc>` carried over with inline styles verbatim: eyebrow + 54px hero, "Carrots, not an empty-nester tax" preface grid, sections 01-05 in the 220px/1fr label+content grid with `position:sticky;top:20px` labels, Comptroller pull quote (3px green left border), three-number strip ($2,058/yr, ~$3,300, ~$7,300/yr) with hairline dividers, green closing band with gold + outline buttons.
- The .dc file contains **no** `data-dc-script` blocks; the sticky section labels are pure CSS (`position:sticky` inline). No page JS was needed beyond shared `nav.js`.
- Link fixes per the map: `RVC Brief.dc.html#asks` → `index.html#asks`; `Fact Check.dc.html` → `validation.html`. The in-copy breakeven link stays as the spec's absolute `https://rvc-taxes.jeffpinto.com/breakeven.html`. All source links (OSC PDF, RPTL 1306-a, DTF 2025 table, Census B25007, OSC glossary, NBER w25468) preserved.
- New `<title>` / `<meta description>` (old ones contained an em dash and stale framing); title: "What a Senior Home Sale Is Actually Worth: The Mechanics".

## Deviations from spec (with reason)
1. **Mobile-only `<style>` block** (head). The .dc prototypes are desktop-only; the fixed `220px 1fr` grids and 48px gutters overflow a 390px viewport. Added classes (`px`, `mx`, `sec-grid`, `sec-label`, `num-strip`) and a single `@media(max-width:760px)` block: 24px gutters (per handoff README "page gutter 48px (24px mobile)"), grids collapse to one column, sticky labels become static, number strip stacks with bottom hairlines instead of right hairlines. **No desktop value changed**; all overrides are inside the media query.
2. Dropped the .dc outer wrapper's duplicate body styles (already in `site.css` body rule), matching the voices.html precedent.

## Verification
- Copy diff: extracted visible text of the new page vs the .dc spec with a Python differ — **byte-identical** except the added `<title>` text.
- Greps: `F1ECE2|FAF6EC|Source Serif|IBM Plex|Inter` → 0 hits. `—|–|&mdash;|&ndash;` → 0 hits. `mailto:` → only `mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20` (footer Contact). `x-dc|dc-import|helmet|.dc.html` leftovers → 0.
- Screenshots (READ, both good): `reports/shots/fm-desktop-full.png` (1280 full page) and `reports/shots/fm-mobile-full.png` (390 full page). Nav renders with green "Mechanics" underline; no serif leakage; no cream backgrounds; 2px rules and hairlines present; nothing overflows.
- Behavior exercised via Playwright against a local http server:
  - Sticky labels: scrolled into section 02, label pinned at `top:20px` (measured `getBoundingClientRect().top === 20`).
  - Mobile nav (390px): Menu button visible, toggles `.open`, stacked links render with "Mechanics" as current, Act now button present.
  - Horizontal overflow probe at mobile width: `scrollWidth === clientWidth`, zero elements past the right edge.
  - Console: clean except a `favicon.ico` 404 (site ships no favicon; pre-existing, all pages).

## Notes for the orchestrator
- **Headless-Chrome screenshot gotcha (affects every page agent's verification step):** on this machine, `--window-size=390,...` lays the page out at ~485px (Chrome min window width) while the capture stays 390px wide, so the right side of a *correct* page looks clipped. `reports/shots/fiscal-math-mobile.png` (the raw Chrome capture) shows this artifact; the Playwright capture `fm-mobile-full.png` with a real 390px viewport is the accurate one. Other agents' "mobile overflow" findings from raw `--window-size=390` shots may be false positives — re-check with a real viewport before ordering fixes.
- The old fiscal-math.html sidebar content (fact cards, "what this page is not saying" dark card) is not in the Mechanics spec and was dropped with the replacement, as intended — flagging in case any other page still links to a fragment of it (grep found no `fiscal-math.html#` fragment links in `site/`).
- Not committed, per instructions.
