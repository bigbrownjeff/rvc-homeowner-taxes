# Report: calculator.html (full replacement from Calculator.dc.html)

## What was ported
`site/calculator.html` fully replaced. The old Chart.js page (navy/gold cards, CDN chart.umd.min.js) is retired; nothing of it survives. New page follows the shared shell: Archivo + `assets/site.css` + `#site-nav data-current="calculator"` + `.site-foot` + `assets/nav.js`, no libraries, CSS bars only.

Sections ported 1:1 from the .dc file: hero, inputs (market-value slider, income, filing status, STAR segmented control None/Basic/Enhanced, mortgage interest, other deductions), 4-cell summary strip, 01 property split (segmented bar + 5 component rows with STAR note), 02 six entity rows with expand/collapse (Details/Close) and all metrics/insights/source links, 03 NYS (gold bracket bar, detail row, 5 spend bars, State Operating Funds paragraph), 04 federal (green bracket bar, detail row, SALT-and-itemization gold-rule box with 3 live sentences, 7 spend bars, CBO paragraph), 05 compare (income-vs-medians bars + age select, three-effective-rates bars + live snapshot), green closing band, footer.

Math constants verbatim from the .dc script (July 2026 audit): EFF_RATE 0.0257; component split .696/.214/.059/.026/.005; STAR 1089/3147 school-line-only; 2025 federal + NYS brackets for all four filing statuses; FSD/SSD; OBBBA SALT cap 40K (20K mfs) with 30% phase-out over 500K (250K mfs) and 10K floor; FED_SPEND/NYS_SPEND/DEMO tables. All inputs recalc live (inputs are static DOM so focus is never lost; output regions re-render).

## Link fixes (per conventions link map)
- `Mechanics.dc.html` -> `fiscal-math.html` (NYS paragraph)
- `RVC Brief.dc.html#asks` -> `index.html#asks` (band secondary button)
- `https://rvc-taxes.jeffpinto.com/reconcile.html` -> relative `reconcile.html` (hero, special-districts entity, band primary button) so the page works locally and on any host
- Contact mailto kept: `mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20calculator`

## Node sanity check (MANDATED)
Script: `/private/tmp/claude-501/-Users-jeffpinto/97c86533-267d-4280-ab41-8830382568c8/scratchpad/calc-assert.js` (formulas extracted from the ported page). Output:

```
raw   : property 21073.999999999996 | NYS 8409.75 | federal 17771.575 | total 47255.325
render: property $21,074 | NYS $8,410 | federal $17,772 | total $47,255
spec targets 21074 / 8410 / 17771 / 47255 -> prop/NYS/total EXACT ; federal raw 17771.575
(displays $17,772 - identical to the .dc prototype's own render; handoff's 17771 is floor of 17771.575)
```

**Orchestrator must re-check / note:** property, NYS, and total match the spec case exactly. The federal card shows **$17,772**, not the handoff's $17,771. This is not a port error: I rendered the original `Calculator.dc.html` prototype in headless Chrome (`--dump-dom`) and it also displays **$17,772** (raw fTax = 17771.575; the .dc's own `fmt()` uses `Math.round`). The handoff's "17,771" is a floor of the same raw value, and 21,074 + 8,410 + 17,771 = 47,255 only because the handoff floored fed while rounding NYS. Port matches the authoritative prototype exactly; constants untouched.

## Verified in the live page (playwright, localhost:8479)
- Defaults render: $21,074 / $8,410 / $17,772 / $47,255; slider label $820,000; "2.6% of value".
- Enhanced STAR: property $17,927 (= 21,074 - 3,147), "STAR -$3,147" note on the school row, federal rises to $18,464 (smaller SALT), total $44,801. Segmented control highlights the active button.
- Filing Single: NYS $9,452 / federal $23,081.
- Income $600K (mfj): SALT line correctly reports effective cap reduced to $10,000 (phase-out floor branch).
- Slider to $1,000,000: property $25,700 (= 1M x .0257).
- Entity toggle: open -> class `open`, label "Close", body `display:block`; second click reverts. All six rows start "Details".
- Age 65+: snapshot recomputes ("2.2x the RVC median").
- Mobile nav: Menu button visible at 390px, toggles open/Close.
- Console: only a site-wide favicon.ico 404 (no favicon in `site/`; pre-existing).

## Screenshots (READ)
- Desktop 1280 full page: `/private/tmp/claude-501/-Users-jeffpinto/97c86533-267d-4280-ab41-8830382568c8/scratchpad/calc-desktop-full.png` - nav renders with Calculator underlined green, no serif leaks, no cream, hairlines/rules present, bars/segments labeled (fed bar 10%/12%/22%, NYS 4%/5.5%), green band + footer correct.
- Mobile 390 full page: `.../calc-mobile-390.png` - Menu button present, inputs stack, summary 2x2, nothing overflows (verified `scrollWidth` 375 <= 390 and zero elements past the right edge).
- Note: the conventions' `chrome --headless --screenshot --window-size=390,2000` command clamps the window to ~460px minimum on this Chrome build, which fakes a right-edge clip; playwright at a true 390px viewport shows no overflow. Other page agents may hit the same artifact.

## Greps
- `F1ECE2|FAF6EC|Source Serif|IBM Plex|Inter|Chart.js`: only substring false positives on "Inter" ("Interactive", "Interest on the debt" - .dc copy). No font/color/library violations.
- `—|–`: 0 hits.
- `mailto:`: exactly one, the bluecamelconsulting `[rvc-taxes] calculator` pattern.

## Deviations from the .dc spec (all flagged, values preserved)
1. **Bracket-bar label formatter fixed (display only).** The .dc's label code `(r*100).toFixed(...).replace(/\.?0+$/,"")` renders the federal 10% bracket as "1%" (regex strips the trailing zero of "10"); confirmed in the prototype's own headless render. Ported formatter strips zeros only after a decimal point, so it shows "10%" (4.5%/5.25%/6.85% etc. unchanged). Math untouched.
2. **Inline styles hoisted to a page `<style>` block** (values verbatim) to add <=760px rules the .dc lacks: 24px gutters, stacked input grid, 2x2 summary, spend-row name on its own line, narrower bar-label columns, single-column compare grid, h1 38px, band padding 36px 24px. Desktop is pixel-per-spec.
3. Dynamic strings (propSub "· of value", SALT sentences, snapshot) are byte-identical to the .dc script templates.

## Files
- `site/calculator.html` (rewritten, self-contained; only deps Google Fonts + assets/site.css + assets/nav.js)
- Not committed, per conventions.
