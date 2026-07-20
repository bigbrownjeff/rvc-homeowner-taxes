# Handoff: RVC Housing × Schools — site redesign

## Overview
Redesign of rvc-taxes.jeffpinto.com — an advocacy site that argues for senior-to-family housing turnover as the least-painful fix for Rockville Centre's (and Nassau County's) school budget squeeze. The redesign serves two audiences on one site: residents (readable, shareable, 1-click actions) and legislators/aides (bill numbers, mechanics, receipts).

The site currently lives in the repo at `site/` (static HTML, deployed via `npx wrangler pages deploy site --project-name rvc-taxes` to Cloudflare Pages; see repo `DEPLOY.md`).

## About the design files
The `.dc.html` files in this bundle are **design references created in HTML** — high-fidelity prototypes showing intended look and behavior, not production code to copy directly. The task is to **recreate these designs as plain static HTML/CSS/JS pages in the existing `site/` folder** (the site has no build step and should stay that way — self-contained pages, minimal JS, no framework). Each `.dc.html` file's markup and inline styles ARE the design spec; the `<script>` logic at the bottom of each file documents the interactive behavior to port.

## Fidelity
**High-fidelity.** Recreate pixel-perfectly: exact colors, typography, spacing, and copy. All copy has been deliberately edited (no em dashes, no jargon, claims sourced) — do not rewrite it.

## Design system ("Modernist", retuned to RVC colors)
- **Background**: `#f3f2f2` (light warm gray-white — NOT cream). Ink text: `#201e1d`. Muted text: `rgba(32,30,29,.6)` / `.65` / `.7` / `.75`.
- **Accents (RVC town colors)**: green `#1e6b3d` (primary: eyebrows, buttons, links, section numbers, closing bands), gold `#c5a44e` (spot: CTA-on-green, secondary highlights). Error/red-flag text: `#8a2f1d`. Link hover: `#14522c`.
- **Type**: Archivo only (Google Fonts, weights 400/600/800). Headlines 800 weight, tight leading (1.02), letter-spacing -.025em. H1 50–62px, section body 16–17px, base 15px, small print 11–13px.
- **Structure**: strong 2px horizontal rules `rgba(32,30,29,.4)` between sections; 1px hairlines `rgba(32,30,29,.25)` inside grids/tables. Zero border radius anywhere. No shadows, no cards, no gradients. Flush-left everything — including button labels (buttons are `text-align:left` with extra right padding, e.g. `padding:13px 44px 13px 18px`).
- **Buttons**: primary = solid green, `#f3f2f2` text, 800 weight, 13–14px; secondary = 1px ink outline, transparent fill. On green bands: gold primary + white-outline secondary.
- **Section pattern**: mono-style eyebrow (`font-size:12px; font-weight:800; letter-spacing:.1em; uppercase; color:#1e6b3d`) numbered `01 ·`, `02 ·`…; content in a 200–220px label column + content column grid, or full width.
- **Stat cells**: grid with hairline right-borders, big 800-weight number (30–44px), 11.5px caption with source link.
- **Charts**: flat CSS bars only (segmented div bars, horizontal bar rows). No chart libraries.
- **Copy rules**: no em/en dashes (use periods, commas, colons), no "honestly", no AI-tell phrasing. Every number carries a source link.

## Pages in this bundle (recreate 1:1)
- `RVC Brief.dc.html` → replaces `site/brief-2026-08.html` (and becomes the main landing). Hero, 60-second gist, five sourced numbers, "Across Nassau" cross-jurisdiction section, "Follow one home sale" money table, **the action kit** (see below), legislator resource grid, downsize-evidence section, green closing band.
- `Mechanics.dc.html` → restyles `site/fiscal-math.html`. Long-form write-up, sticky section labels, Comptroller pull quote, three-number strip.
- `Fact Check.dc.html` → restyles `site/validation.html` (condensed; keep the full tables of the old page reachable or port them fully — developer's call with Jeff).
- `Voices.dc.html` → restyles `site/voices.html`. Quote library; grid rows of quote + attribution + source link.
- `Calculator.dc.html` → replaces `site/calculator.html`. Full port; the math constants and formulas in its script block are the corrected July-2026-audit versions (EFF_RATE 0.0257, in-village component split .696/.214/.059/.026/.005, STAR credit 1089/3147 school-line-only, 2025 federal/NYS brackets, OBBBA SALT cap with 30% phase-out over $500K and $10K floor). Chart.js was deliberately removed; keep the CSS bars.
- `Nav.dc.html` → shared header for ALL pages: brand left; links The brief / Mechanics / Fact check / Voices / Calculator with current-page underline in green; green "Act now" button → brief `#asks`; below 760px collapse to a "Menu" toggle button revealing a stacked link list.

## Pages NOT yet redesigned — apply the same system
Restyle these existing `site/` pages to match (structure/content already good, just re-skin to the system above and add the shared nav):
- `site/reconcile.html` (bill reconciler — keep all math untouched)
- `site/breakeven.html` (break-even instrument — keep sliders/math)
- `site/index.html` (8-page print briefing — KEEP its print-first layout and cream-free restyle is optional; at minimum add a link banner to the new pages. It is the print-to-PDF handout.)
- `site/governance.html`, `site/governance-options.html`, `site/redraw-evidence.html` (secondary pages)
Also update every masthead/footer link across pages to the new nav + `Contact` mailto.

## Interactions & behavior

### Action kit (RVC Brief, section 03) — the key feature
1. Inputs: street address (required), name (optional), email (optional). Prefilled with "1 College Pl, Rockville Centre, NY"; auto-runs the lookup on page load so the cards are visible immediately.
2. On "Build my letters": geocode via **US Census geocoder JSONP** (the API sends no CORS headers — JSONP is required):
   `https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=<ADDR>&benchmark=Public_AR_Current&vintage=Current_Current&layers=all&format=jsonp&callback=<CB>`
   Parse geographies for: congressional district (CD119), state senate (SLDU), assembly (SLDL), unified school district (NAME).
3. Render 5 cards: Federal (H.R. 1340), State Senate (S3309), State Assembly (A5288), Nassau County (data ask), School district & village (§467 fiscal note). Each card: level eyebrow, official name **hotlinked to their page**, district line, one-sentence ask, prewritten letter with the user's name + matched address; primary button = prefilled `mailto:` where a public email exists, else contact-form link; secondary = "Copy letter" to clipboard (label flips to "Copied" for 2s).
4. Verified officials table (extend as more are verified; unknown districts fall back to district number + official lookup link — never guess names):
   - CD-4 Rep. Laura Gillen — gillen.house.gov/contact (form only) — not yet a cosponsor of H.R. 1340
   - CD-3 Rep. Tom Suozzi — suozzi.house.gov/contact — already a cosponsor (thank-you letter variant)
   - SD-6 Sen. Siela Bynoe — Bynoe@nysenate.gov — **RVC's senator under current lines** (site previously said Canzoneri-Fitzpatrick/SD-9; corrected July 2026)
   - SD-9 Sen. Patricia Canzoneri-Fitzpatrick — canzoneri@nysenate.gov — S3309 sponsor, RVC resident
   - AD-21 Asm. Judy Griffin — nyassembly.gov/mem/Judy-Griffin/contact/ (form only)
   - County LD-1 Leg. Scott Davis — SDavis@nassaucountyny.gov — District 1 covers all of RVC (Nassau map redrawn for 2026; non-RVC → nassaucountyny.gov/2803/Find-My-Legislative-District)
5. Letter texts: see the `letters()` method in `RVC Brief.dc.html`'s script. Signature = name + matched address.

### Mailing list (needs a backend — currently prototype-only)
The prototype stores signups (name/email/address/timestamp) in `localStorage` key `rvc-action-signups`, only when the user runs their own lookup (not the auto-run). **Production**: a Cloudflare Pages Function (e.g. `functions/api/signup.js`) that POSTs to KV or D1 — same Cloudflare account as hosting. Keep it dependency-free. Honor the on-page promise: "Email is optional and joins the project's update list. Nothing else is done with it."

### Contact routing
All contact links: `mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20...` — subject always prefixed `[rvc-taxes]` (+ variant tags: `correction`, `voices`, `calculator`) so it can be filtered after forwarding to the real inbox. Never expose any other email.

### Calculator
All inputs recalc live. STAR segmented control (None/Basic/Enhanced). Six entity rows expand/collapse ("Details"/"Close"). Sanity check after porting: MFJ, $820K home, $175K income, $18K mortgage interest, $500 other → property $21,074 / NYS $8,410 / federal $17,771 / total $47,255.

### Nav (mobile)
Breakpoint 760px. Desktop: inline links + Act now button. Mobile: "Menu"/"Close" toggle, stacked links with hairline separators, Act now button at the bottom.

## Design tokens (summary)
bg `#f3f2f2` · ink `#201e1d` · green `#1e6b3d` (hover `#14522c`) · gold `#c5a44e` · error `#8a2f1d` · rules `rgba(32,30,29,.4)` strong / `.25` hairline / `.2` table rows · input borders 1px `#201e1d` · radius 0 · shadows none · font Archivo 400/600/800 · page gutter 48px (24px mobile) · section padding 30–34px vertical · max content width 1100px, prose 720–760px.

## Assets
None. No images anywhere (deliberate). No icon fonts. The only external dependency is Google Fonts (Archivo) and the Census geocoder API.

## Facts corrected during this redesign (do not regress)
- RVC's state senator is **Siela Bynoe (SD-6)**, not Canzoneri-Fitzpatrick (SD-9) — verify against nysenate.gov before shipping.
- Headline framing: "A quarter of our homes hold the fix" with 27.9% (2,076 of 7,453) as supporting detail — not the raw count as headline.
- The "seniors want to downsize" claim must keep its evidence block (Freddie Mac Silver Tsunami Dec 2024; AARP 2024 preferences survey; Realtor.com/HousingWire June 2026; AEI ~1.9M locked homes; Gov. Hochul April 2025 quote). Pin the exact Freddie Mac survey URL before publishing (currently a generic research link).

## Files
- `RVC Brief.dc.html`, `Mechanics.dc.html`, `Fact Check.dc.html`, `Voices.dc.html`, `Calculator.dc.html`, `Nav.dc.html` — the design references (open each in a browser).
- Repo context: `site/` = current live pages; `docs/` = source markdown + validation receipts; `DEPLOY.md` = Cloudflare Pages deploy steps.
