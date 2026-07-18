# Refresh — July 18, 2026

Delta report against the June 9, 2026 validation (`VALIDATION_REPORT.md` / `CORRECTIONS.md`).
Purpose: bring the record current for the August 2026 legislator brief (`BRIEF_2026-08.md`).
All receipts: `_SOURCES.md`.

## Errors found in the June work (loud, per policy)

1. **Wrong citation under a true claim.** `findings/exemptions.md` item 12 cited the DTF
   *Summary of 2025 RPT Legislation* (legsum25.pdf) as the source for the §467 income cap
   rising to **$75,000 on July 1, 2027**. Full-text extraction of that PDF (and of legsum22–24)
   shows **no such provision in any of them**. The claim itself is TRUE — the raw statute text
   of RPTL §467(3)(a) carries both versions with "NB Effective July 1, 2027" markers — but it
   was resting on a citation that does not contain it. Fixed in `findings/exemptions.md`;
   the statute is now the receipt. The enacting chapter remains unidentified; do not name one.
2. **Ch. 581 adjacency wording.** `VALIDATION_REPORT.md` §1.2 reads as if Ch. 581 of 2025
   brought both the 65% tier *and* the $75K cap. Ch. 581 (A.3698-A/S.5175-A, signed Dec 5,
   2025, taxable years on/after **Jan 1, 2026**) created **only** the optional 65/60/55% tiers
   keyed to (M−$3,000)/(M−$2,000)/(M−$1,000); its sponsor memo states it does not modify
   income limits. Clarifying note added to `VALIDATION_REPORT.md`.
3. Minor: DTF's page shows the 5% sliding-scale ceiling as **$58,400**; the Nassau brochure
   band is $57,500–$58,399. Same tier, rounding presentation. Use "≈$58,400."

No other June corrections failed re-derivation. Spot re-checks all passed:
2,076/7,453 = 27.9%; $3,147.01−$1,089 = $2,058; 0.4%×$820K = $3,280; 3,533−3,276 = 257;
STAR max exemption savings for RVC Class 1 are unchanged for 2026-27 ($1,068/$2,856).

## Status flips and new data since June 9

| Item | June state | July 18 state | Effect on the argument |
|---|---|---|---|
| **STAR administration** | 2025 rules | 2026: automatic Basic→Enhanced upgrade at 65; one-resident-owner-65 rule; resident-only income counting; Enhanced income limit **$110,750** (2026) / **$113,550** (2027) | Strengthens leg 3 (lock-in fear is mostly myth): benefits now follow seniors with even less paperwork |
| **S3309/A5288** (benefit continuity in a move year) | Reported from Aging 7-0 (Apr 21, 2026), pending | **S3309 stalled in Senate Finance when the 2026 session adjourned** (no floor vote); **A5288 never left Assembly Real Property Taxation** (referred 2025-02-12, re-referred 2026-01-07) | The state ask flips from "pass it this session" to "advance both bills + floor commitment in Jan 2027" |
| **H.R. 1340** | 117+ cosponsors; Gillen absent | **146 cosponsors; Gillen still absent** (NY: Malliotakis, Suozzi on) | Federal ask unchanged; two LI-area members of both parties are cosponsors |
| **S. 3332** | cited | Confirmed: introduced Dec 3, 2025 (Cornyn/Bennet + 4); NAR and AARP endorsed | Bipartisan cover for the ask |
| **Village FY27 budget** | not covered (adopted Apr 30, 2026) | **$63.64M; levy $44.49M (+6.6%); rate $69.89→$74.91/$100 (+7.2%)** | New: the village line is now the fastest-growing major piece of the RVC bill — broadens the brief from a schools story to a whole-bill story |
| **School-district tax cap 2026-27** | "final cap ≈2.1%" | OSC: allowable levy growth capped at **2%** for the 5th year (inflation factor 2.63%) — RVC's 2.06% adopted levy sits under its final cap with exclusions | Confirms the structural bind: costs compound faster than the cap |
| **Nassau assessment roll** | freeze noted | Continues: 2026/27 tentative roll published Jan 2, 2026 at Class 1 LOA 0.1%; ARC residential ratio 0.060%; next grievance window opens Jan 2, 2027 | Context only; no aggregate claims until FOIL data lands |
| **County politics** | Blakeman re-elected; "running for governor" | **Blakeman is the GOP nominee for governor** (Stefanik exited Dec 20, 2025; Trump endorsed); general Nov 3, 2026 | County-level asks should be timed for whoever holds the seat in Jan 2027; the county legislature is the durable audience |
| **§467 $75K option** | flagged for 2027 | Statute-verified; **decision window is now ~11 months** (effective July 1, 2027, local opt-in) | Becomes the brief's central near-term decision: opt-in only with parcel-level fiscal notes |

## Still open (unchanged from June, blocking any "exemption gap" number)

- FOIL: parcel counts of §467 and Enhanced STAR in RVC by tier (Nassau Dept. of Assessment).
- RVC UFSD's §467 adopting resolution, current ceiling, and 65%-tier posture (district clerk).
- ~~Independent sourcing for the $15,230 average total bill and the bill-component split.~~ **Closed 2026-07-18 (math audit):** $15,230.09 is a verified school+library-only bill, not a total (Nassau LRV parcel tax table); verified component split and a typical in-village total of ≈$21.1K now in `docs/MATH-AUDIT-2026-07.md` / `site/reconcile.html`.

## Artifacts of this refresh

- `docs/BRIEF_2026-08.md` — the politician-ready brief (new).
- `site/brief-2026-08.html` — rendered version, Editorial DS, print-friendly (new).
- `docs/_SOURCES.md` — consolidated verification receipt (new).
- `docs/findings/exemptions.md` — citation fix (item 12).
- `docs/VALIDATION_REPORT.md` — dated clarifying note at §1.2.
- Legacy root artifacts (`RVC_Tax_Calculator.html`, `.docx`, `.xlsx`) remain superseded by
  `site/` per the June corrections; not re-touched.
