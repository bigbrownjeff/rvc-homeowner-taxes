# Re-skin report: four secondary pages

Agent: secondary-pages re-skin. Scope: style + nav + footer + link fixes only; body copy untouched.

## Pages done

### 1. site/governance.html (long memo)
- Old Editorial skin (cream #F1ECE2/#FAF6EC, Source Serif 4 / Inter / IBM Plex Mono, navy #1E3A8A) replaced with the token shell: Archivo 400/600/800, bg #f3f2f2, ink #201e1d, green #1e6b3d, 2px/1px rules, radius 0, no shadows.
- New page `<style>` keyed to the EXISTING class names (.wrap/.masthead/h1-h4/table/blockquote/.foot) so the body markup is byte-identical. All [VERIFIED]/[REPORTED]/[ESTIMATE] labels, citations, and the source list intact.
- Table: ink header band, hairline row rules (rgba(32,30,29,.2)); mobile: table scrolls in place; `overflow-wrap:break-word` on .wrap so the bare source-list URLs wrap on narrow screens.
- Shell nav `data-current=""` (no underline), shared site-foot with `mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20governance`. Original memo footer line kept as content above the shared footer.
- No internal cross-links existed to fix (all links external).

### 2. site/governance-options.html (6-page decision memo)
- Same mechanical approach: full style-block replacement; legacy CSS var names (--accent/--muted/--rule/--ruleSoft/--paper/--serif/--mono, --dollar/--equity) remapped to tokens so the many inline `var(...)` styles in content resolve without touching markup. dollar axis -> green #1e6b3d, equity axis -> error #8a2f1d, oklch colors gone.
- 8.5in "paper card" pages became full-width web sections separated by 2px rules (no cards/borders). Print @page rules dropped (deck.html is the print artifact).
- Dark ink panels kept; their #9DB4E8 accent -> gold #c5a44e. "Draft - for review" badge restyled solid green, moved static above the masthead (was absolutely positioned and collided with the masthead meta after the layout change).
- Two inline style edits (style-only, copy untouched): tag `background:#eee` -> transparent.
- Nav `data-current=""`, site-foot with `%5Brvc-taxes%5D%20governance-options` mailto.

### 3. site/redraw-evidence.html (6-page evidence memo)
- Same treatment. --good -> green, --bad -> error red. Gradient-table Nassau highlight row #e7ecf6 (navy tint) -> rgba(197,164,78,.16) gold tint; scenario "win" row #e6efe8 -> rgba(30,107,61,.08) green tint. Zebra striping removed (paper color banned); tables now ink header band + hairline row rules only.
- Inline `color:#9DB4E8` span in the p.4 dark panel -> #c5a44e (style-only edit inside a dark panel).
- Nav `data-current=""`, site-foot with `%5Brvc-taxes%5D%20redraw-evidence` mailto.

### 4. site/voices-library.html (full quotes archive)
- Retitled: `<title>Voices: The Full Library — What Long Island Says About Its Shrinking Schools</title>`; h1 now "Voices: the full library." Added the one intro line: "This is the complete quotes archive. The curated selection lives on <a href=voices.html>the Voices page</a>." Standfirst, meta line, every quote, every source link, closure file, and provenance note kept verbatim.
- Old masthead mini-nav (Deck / Mechanics / Break-even / Facts & sources) removed - superseded by the shell nav (`data-current="voices"`, underline verified in screenshot). Note: this drops the only link to breakeven.html from this page; breakeven.html is not in the shared nav (flag for orchestrator if it should be linked elsewhere).
- Hero quote block: ink -> green #1e6b3d with gold quote marks and gold source links, matching voices.html. Section heads: green uppercase over 2px rules; quote rows on hairlines.
- Link fixes: provenance-note "the deck" `index.html` -> `deck.html` (it meant the print deck). `<code>` chip's paper background -> hairline border.
- site-foot with `%5Brvc-taxes%5D%20voices-library` mailto; right side "Compiled June 10, 2026 - nothing paraphrased" (mirrors voices.html).

## Link-fix sweep
- `brief-2026-08.html`: 0 occurrences in all four pages.
- Visible "Fact-check" labels: 0 occurrences (the shared nav.js "Fact check" item is orchestrator-owned, not page content).
- Print-deck-meaning `index.html` links: 1 found (voices-library provenance note) -> deck.html. The other three pages had no internal links at all.

## Verification
Screenshots (READ, all eight): `reports/shots/{governance,governance-options,redraw-evidence,voices-library}-{desktop,mobile}.png` (desktop 1280x2000, mobile 390x900). Full-page 1280x14000 checks in scratchpad confirmed mid-page and footer regions (tables, dark panels, source list, shared footer).
- Nav renders on all four; "Voices" underlined green on voices-library only; no underline on the other three. No serif leakage, no cream backgrounds, rules/hairlines present.
- Known baseline quirk: headless mobile shots at 390px show a right-edge crop identical to the pre-existing approved `fiscal-math-mobile.png` (headless Chrome clamps window width; screenshot crops a ~500px layout). Not a page defect; pages carry `overflow-wrap:break-word` and per-table `overflow-x:auto` at narrow widths.

Greps (all four pages):
- `F1ECE2|FAF6EC|Source Serif|IBM Plex|'Inter'|Inter:wght|1E3A8A|0E1116|C9C3B4|9DB4E8|231F1A|oklch|#eee|#fff|Georgia`: 0 hits (case-insensitive "Inter" false-positives were words like "inter-district").
- `mailto:`: exactly one per page, all `jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20<tag>`.
- Em/en dashes: 53/46/50/20 lines per page respectively - ALL pre-existing in preserved body copy, quotes, and original titles. Deviation, deliberate: the task instruction "do not rewrite any body copy" overrides the 0-dash grep, which targets newly ported .dc copy. My one added line (the voices-library intro) is dash-free.

No JS on these pages beyond the shared nav.js (menu toggle exercised implicitly by nav render in shots).

## For the orchestrator to re-check
1. The dash-grep exception above (body copy preserved verbatim).
2. Gold/green rgba row tints in redraw-evidence tables (rgba(197,164,78,.16), rgba(30,107,61,.08)) - token-derived tints used where the old design used navy/green pastels; swap for a rule-based treatment if tints are considered off-spec.
3. voices-library no longer links breakeven.html (old masthead nav removed).
4. Titles/meta descriptions kept verbatim (contain em dashes).
