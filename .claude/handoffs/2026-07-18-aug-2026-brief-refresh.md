# 2026-07-18 — August 2026 politician-brief refresh

## Goal
Refresh the RVC homeowner-tax analysis for presentation to local politicians in August 2026:
re-verify against current data, fix errors, produce a tight politician-ready brief.

## What got done (branch `feature/aug-2026-refresh`, worktree `~/Projects/rvc-homeowner-taxes-refresh`)
- **`docs/BRIEF_2026-08.md`** — the 2-page brief (problem → mechanics → §467 decision window → asks by office).
- **`site/brief-2026-08.html`** — rendered Editorial-DS version, print-friendly; linked from index masthead; headless-Chrome verified (fixed a dark-on-dark `<b>` bug in the darkbox on first render).
- **`docs/_SOURCES.md`** — consolidated receipt: every brief figure → source → how verified, plus disclosed caveats.
- **`docs/REFRESH_2026-07.md`** — delta report vs the June 9 validation.
- Receipt fixes: `docs/findings/exemptions.md` item 12, note in `VALIDATION_REPORT.md` §1.2; `DEPLOY.md` served-paths table.

## Errors found in the June work (the loud part)
1. The **$75K §467 income-cap (eff. 7/1/2027) claim was resting on a wrong citation** — DTF legsum25.pdf does not contain it (verified by full-text extraction of legsum22–25). The claim itself is TRUE: raw statute HTML of RPTL §467(3)(a) carries both versions with NB-effective markers. Statute is now the receipt; enacting chapter remains unidentified — do not name one.
2. VALIDATION_REPORT §1.2 wording conflated Ch. 581 (which created only the 65% tier, A.3698-A) with the separate $75K amendment. Clarified in place.
All other June corrections passed re-derivation spot-checks.

## Key refresh findings (all in _SOURCES.md)
- STAR 2026: auto-upgrade at 65, resident-only income, Enhanced limit $110,750 — strengthens the "lock-in is mostly myth" leg.
- S3309 stalled in Senate Finance at 2026 adjournment (Aging 7-0 in April); A5288 never left Assembly Real Property Taxation → ask flips to advancing both.
- H.R. 1340 now 146 cosponsors; **Gillen still not one** (Suozzi and Malliotakis are) — the federal ask is sharper.
- NEW: Village FY27 budget — rate +7.2% ($69.89→$74.91/$100), levy +6.6% to $44.49M — broadens the story beyond schools.
- Blakeman is the GOP nominee for governor (general Nov 3, 2026) — county asks aimed at the legislature, not the executive.
- §467 65% tier live since Jan 1, 2026; $75K ceiling opt-in window opens 7/1/2027 → the brief's central near-term decision, gated on parcel-level fiscal notes.

## What worked / dead ends
- nysenate.gov statute pages: WebFetch summaries were right but curl-fetching the raw HTML and grepping was the decisive receipt — do that for any statutory claim.
- congress.gov and govtrack 403 all automated fetches; BillTrack50 + GovInfo + sponsor press releases are the workable verification path.
- DTF/OSC PDFs extract fine with stdlib zlib + paren-string regex then whitespace-collapse; the RVC village budget PDF resisted my stdlib approach but pypdf extracts it (adversarial review verified $63,641,946 / $44,488,056 / $74.91, +7.18%; _SOURCES caveat 2 closed).

## Open threads
1. **Deploy**: `npx wrangler pages deploy site --project-name rvc-taxes` after merge (direct-upload project — merge ≠ deploy), then real-browser check of `/brief-2026-08.html` on the live domain.
2. **Merge**: PR from `feature/aug-2026-refresh`; main-push/merge needs Jeff's per-session approval.
3. **Before handing to politicians**: check whether DTF has published 2026 final STAR credit amounts (would replace the 2025-labeled $1,089/$3,147.01). Village FY27 PDF figures are machine-verified (+7.18%).
4. **Still-blocked data** (unchanged): FOIL parcel counts by tier; RVC UFSD §467 resolution; independent $15,230 bill source.
5. The .docx/.xlsx root artifacts remain superseded, not regenerated.
