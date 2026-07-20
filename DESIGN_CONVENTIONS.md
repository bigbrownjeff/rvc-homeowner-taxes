# RVC redesign conventions (for all page agents)

Worktree: `/Users/jeffpinto/Projects/rvc-homeowner-taxes/.claude/worktrees/design-refresh/`
Design specs: `design_handoff_rvc_site_redesign/` (repo root copy is identical). READ `README.md` there first.
Do NOT commit or push. Write files + a report; the orchestrator commits.

## Page shell (every page)
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>...</title>
<meta name="description" content="...">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<div id="site-nav" data-current="PAGE_ID"></div>
...content...
<div class="site-foot"><span>Jeff Pinto &middot; Rockville Centre &middot; <a href="mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20">Contact</a></span><span>RIGHT-HAND TEXT</span></div>
<script src="assets/nav.js"></script>
</body>
</html>
```
`data-current` ∈ brief | mechanics | factcheck | voices | calculator (omit/empty for secondary pages — no underline).
`assets/site.css` carries tokens as CSS vars; nav + footer classes. Page-specific styles: keep the .dc file's inline styles verbatim (that IS the spec), or hoist into a page `<style>` block if you must — never change values.

## Porting a .dc.html spec (mechanical transform)
1. Take everything between `<x-dc>` and `</x-dc>`.
2. Drop the `<helmet>` block (shell provides it). Keep any `<style>` INSIDE helmet only if it has page-specific rules beyond body/a defaults (those are already in site.css).
3. `<dc-import name="Nav" current="X">` → `<div id="site-nav" data-current="X"></div>`.
4. `<script type="text/x-dc" data-dc-script>` blocks describe behavior: re-implement as plain vanilla JS at the end of the page. No frameworks, no libraries.
5. `sc-if` / `sc-for` / `{{ }}` are template constructs: expand them into real markup/JS.

## Link map (design file → production)
- `RVC Brief.dc.html` → `index.html` (the brief IS the new landing); `#asks` fragment preserved
- `Mechanics.dc.html` → `fiscal-math.html`
- `Fact Check.dc.html` → `validation.html`
- `Voices.dc.html` → `voices.html`
- `Calculator.dc.html` → `calculator.html`
- Old print deck (previous index.html) → `deck.html`. In re-skinned pages, update any `index.html` link that meant the PRINT DECK to `deck.html`, and any `brief-2026-08.html` link to `index.html`.
- Old cross-links `validation.html` (label "Facts & sources") stay.

## Hard rules (from the handoff README — violations are review-blockers)
- Colors/type/spacing exactly: bg #f3f2f2, ink #201e1d, green #1e6b3d (hover #14522c), gold #c5a44e, error #8a2f1d. Archivo 400/600/800 only. Radius 0. No shadows, no cards, no gradients, no images, no icon fonts, no chart libs (CSS bars only).
- Flush-left everything including button labels (`text-align:left`, asymmetric padding e.g. `13px 44px 13px 18px`).
- Copy from the .dc files is FINAL. Do not rewrite. No em/en dashes in site copy (verbatim quotes keep whatever punctuation the source used).
- Every number keeps its source link.
- Contact links: `mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20<tag>` only. Never any other email.
- Re-skins: NEVER change math, formulas, input wiring, or data values. Style + nav + footer + link fixes only.

## Facts corrected in this redesign (do not regress)
- RVC's state senator: **Siela Bynoe (SD-6)** — verified 7/20/26 at nysenate.gov/senators/siela-bynoe/district (community list includes Rockville Centre). Canzoneri-Fitzpatrick (SD-9) remains the S3309 sponsor and an RVC resident, but she is NOT RVC's senator.
- Nassau County: LD-1 Leg. Scott Davis covers all of RVC on the 2026 court-settlement map (nassaucountyny.gov/505/District-1---Scott-Davis).
- Freddie Mac "Silver Tsunami" Dec 19, 2024 release (pinned URL): https://freddiemac.gcs-web.com/news-releases/news-release-details/silver-tsunami-likely-bring-wave-wealth-children-baby-boomer

## Verification (every agent, before reporting)
1. Headless screenshot desktop (1280×2000) and mobile (390×900):
   `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --screenshot=OUT.png --window-size=1280,2000 --hide-scrollbars "file://$PWD/PAGE.html"`
   READ the screenshots. Check: nav renders, current-page underline right, no serif fonts leaking, no cream (#F1ECE2) backgrounds left, rules/hairlines present, nothing overflows.
2. Grep your page for: `F1ECE2|FAF6EC|Source Serif|IBM Plex|Inter` (must be 0 hits), `—|–` outside verbatim quotes (0 hits), `mailto:` (only the bluecamelconsulting pattern).
3. Interactive pages: exercise the JS in the headless run (`--run-all-compositor-stages-before-draw`) or via node where pure math; report what you tested.

## Report
Write `reports/<page>.md` in the worktree root: what you ported, deviations from spec (if any, with reason), verification evidence (screenshot paths + grep results), and anything the orchestrator must re-check.
