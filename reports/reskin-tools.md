# Re-skin report: reconcile.html + breakeven.html

Agent scope: style-only re-skin to the Modernist/RVC system. Structure, copy, inputs, sliders, and ALL math untouched.

## What changed (both pages)
- Head: Archivo 400/600/800 via Google Fonts + `assets/site.css` (tokens); old Source Serif 4 / Inter / IBM Plex Mono links removed.
- Full replacement of each page's `<style>` block: bg #f3f2f2, ink #201e1d, green #1e6b3d (was navy #1E3A8A), gold #c5a44e spot highlights, error #8a2f1d; 2px strong / 1px hairline rules from tokens; radius 0; no shadows; no cream panels (old `.panel` paper cards became rule-topped transparent sections); numeric cells use Archivo 600 + `font-variant-numeric:tabular-nums` instead of mono.
- Old inline masthead removed → shared nav `<div id="site-nav" data-current="">` (secondary pages, no underline) + `assets/nav.js`.
- Old `.foot` removed → shared `.site-foot` with the canonical `mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20` Contact link; each page keeps its original right-hand footer text (sources line / rvc-taxes.jeffpinto.com).
- Dark ink boxes → green #1e6b3d bands with gold headings/links (matches the system's closing-band idiom).
- Inputs/selects: 1px #201e1d border on #f3f2f2, flush-left, radius 0, green focus outline; sliders `accent-color:#1e6b3d`.
- Stale links: the old masthead was the only place `index.html`-as-deck and `brief-2026-08.html` appeared; it is gone (nav supplies correct links). In-body `validation.html` links kept, already labeled "facts & sources". `fiscal-math.html` link in breakeven kept. Zero grep hits for `brief-2026-08|Deck</a>|fact-check` in both files.

## Page-specific notes
- breakeven.html meter: the JS ternary `'var(--good)' : 'var(--accent)' : 'var(--bad)'` is untouched; the page style block maps `--good:#1e6b3d`, `--accent:#c5a44e` (gold, page-local — text selectors use green directly), `--bad:#8a2f1d`. Rule `.meter .fill[style*="accent"]{color:var(--ink)}` gives ink text on the gold mid state (white on gold fails contrast). Verified computed: red rgb(138,47,29)+white at 23%, gold rgb(197,164,78)+ink at 62%, green rgb(30,107,61)+white at 100%.
- reconcile.html: added `td.num{white-space:normal}` inside the ≤760px media query — the verification table's nowrap cells genuinely overflowed (648px) on phones (pre-existing in the old design too). Style-only fix; scrollWidth now ≤ viewport at 390.

## JS diff proof (math untouched)
Extracted the inline `<script>` block from `git show HEAD:site/<page>.html` and from the new files (`awk` between `<script>`/`</script>`; the new pages' extra `<script src="assets/nav.js">` tag is external and excluded) and diffed:
- reconcile.html: **byte-identical** (diff empty)
- breakeven.html: **byte-identical** (diff empty)
No style strings needed changing; color remapping was done entirely via the CSS var indirection above.

## Verification evidence
Screenshots (READ, all four):
- Desktop 1280×2000 (headless Chrome): scratchpad `reconcile-desktop.png`, `breakeven-desktop.png` — nav renders, no current underline (correct for secondary pages), green/gold bands, tables/sliders styled, no serif/cream remnants, nothing overflows.
- Mobile true 390×900 (Playwright; headless Chrome floors windows at 500px CSS — `innerWidth` reported 500 at `--window-size=390`, so the convention command crops a 500px render; Playwright used for a real 390 viewport): scratchpad `reconcile-mobile-390.png`, `breakeven-mobile-390.png` — menu toggle works (reconcile captured open: stacked links + Act now), scrollWidth 375 ≤ 390 on both, verification table wraps.

Interactive (Playwright on localhost, temp server since `file:` is blocked; server killed after):
- reconcile: built-in self-tests `t1`/`t2` = **PASS** on load; default total $21,083.46 (verified parcel); set AV→900: school $20,230.80 (matches Case B), STAR basic credit rows appear (−$1,089.00, net $26,265.11); back-solve implied AV 647 for $22,800. Only console entry: favicon.ico 404 (server artifact).
- breakeven: defaults compute $1.8M gap / 1.65% δ / $116M/yr / 23% coverage; slider input events drive live recompute through all three meter states and both verdict branches.

Greps (both files): `F1ECE2|FAF6EC|Source Serif|IBM Plex|Inter|1E3A8A|9DB4E8` → 0 hits; `mailto:` → only the bluecamelconsulting pattern (1 per page, footer).

## Flag for the orchestrator
- **Em/en dashes: 20 per page remain**, all in pre-existing page copy, `<title>`s, and the frozen JS output strings. My brief froze content ("change ONLY fonts/colors/rules/nav/footer/links"), so I did not edit copy; the conventions' no-dash grep will hit these. Decide whether legacy-tool copy is "verbatim/final" (my assumption) or needs a dash-scrub pass.
- Old pages' `<h4>`/eyebrow casing kept as-is (CSS uppercases them); copy untouched.
- Not committed, per instructions. Files: `site/reconcile.html`, `site/breakeven.html`.
