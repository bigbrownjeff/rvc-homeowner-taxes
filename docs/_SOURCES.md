# _SOURCES — July 2026 refresh receipt

Verification receipt for `docs/BRIEF_2026-08.md` (and `site/brief-2026-08.html`).
Every figure in the brief traces to a row here. Fetched/verified **July 18, 2026** unless
noted "June receipt" (fetch-verified June 9, 2026; see `docs/findings/`, liveness re-checked
July 18, 2026 with HTTP 200).

## Verified this refresh (fetched 2026-07-18)

| Claim in brief | Source (primary unless noted) | How verified |
|---|---|---|
| RPTL §467 max income limit is $50,000 now; **$75,000 beginning July 1, 2027** (local opt-in) | [RPTL §467(3)(a), NYS Senate statute text](https://www.nysenate.gov/legislation/laws/RPT/467) | Raw HTML fetched; both statutory versions present with "NB Effective until July 1, 2027" / "NB Effective July 1, 2027" markers |
| Ch. 581 of 2025 = A.3698-A/S.5175-A: optional 65/60/55% senior-exemption tiers keyed to (M−$3,000/−$2,000/−$1,000); signed Dec 5, 2025; taxable years on/after Jan 1, 2026; does **not** change income limits | [A3698-A](https://www.nysenate.gov/legislation/bills/2025/A3698/amendment/A) · [S5175-A](https://www.nysenate.gov/legislation/bills/2025/S5175) · [DTF Summary of 2025 RPT Legislation (PDF)](https://www.tax.ny.gov/pdf/publications/orpts/legis/legsum25.pdf) | Bill pages fetched; DTF PDF downloaded + full-text extracted ("Chapter 581 (A.3698-a) RPTL §467(1)(b)(4)…") |
| §467 sliding scale at the $50K option: 50% ≤ $50,000 … 5% at ~$58,400 | [DTF senior citizens exemption page](https://www.tax.ny.gov/pit/property/exemption/seniorexempt.htm) | Fetched (page updated May 14, 2026). DTF shows $58,400; Nassau brochure (June receipt) shows $57,500–58,399 band — cite as ≈$58,400 |
| STAR 2026 changes: automatic Basic→Enhanced upgrade at 65; only one resident owner must be 65+; income test counts resident owners/spouses only | [DTF "It's getting easier to qualify for STAR"](https://www.tax.ny.gov/star/changes/) | Fetched |
| Enhanced STAR income limit: **$110,750 (2026 benefit, 2024 income); $113,550 (2027)**; Basic credit $500K / exemption $250K | [DTF STAR eligibility](https://www.tax.ny.gov/pit/property/star/eligibility.htm) | Fetched |
| Max 2026–27 STAR exemption savings, Rockville Centre SD Class 1: **Basic $1,068 / Enhanced $2,856** (unchanged from 2025 final) | [DTF max 2026–27 STAR savings, Nassau school districts](https://www.tax.ny.gov/pit/property/star/max-savings/school-district/sd28.htm) | Fetched; RVC row quoted |
| 2025 final STAR **credit** amounts, RVC Class 1: Basic $1,089 / Enhanced $3,147.01 (→ state saves ~$2,058/yr per Enhanced→Basic transition) | [DTF 2025 final STAR credit/exemption savings, Nassau](https://www.tax.ny.gov/pit/property/star/comparison/28-nassau.htm) | June receipt; liveness 200. 2026 final credit amounts not yet published as of 7/18/26 — label vintage |
| S3309/A5288 (Enhanced-STAR continuity for mid-year buyers) **did not pass the 2026 session**. S3309: Senate Aging 7-0 Apr 21, 2026 → committed to Finance, no floor vote before adjournment. A5288: referred to Assembly Real Property Taxation Feb 12, 2025, re-referred Jan 7, 2026 — never reported out of that committee | [S3309](https://www.nysenate.gov/legislation/bills/2025/S3309) · [A5288](https://www.nysenate.gov/legislation/bills/2025/A5288) | S3309 fetched (full action history); A5288 Assembly-committee history verified in the July 18 adversarial review pass |
| H.R. 1340 (More Homes on the Market Act): **146 cosponsors**, referred to Ways & Means Feb 13, 2025; NY cosponsors incl. Malliotakis, Suozzi; **Rep. Gillen not a cosponsor** | [H.R. 1340 @ Congress.gov](https://www.congress.gov/bill/119th-congress/house-bill/1340) | Congress.gov bot-blocks (403); verified via [BillTrack50](https://www.billtrack50.com/billdetail/1833162) (fetched: 146 cosponsors, Gillen absent) + [GovInfo](https://www.govinfo.gov/app/details/BILLS-119hr1340ih) |
| S. 3332 Senate companion introduced Dec 3, 2025 (Cornyn, Bennet, Daines, Schiff, Barrasso, Kelly); NAR + AARP endorsed | [S. 3332 @ Congress.gov](https://www.congress.gov/bill/119th-congress/senate-bill/3332) · [Cornyn release](https://www.cornyn.senate.gov/news/cornyn-bennet-colleagues-introduce-bill-to-increase-housing-availability-and-affordability/) · [Bennet release](https://www.bennet.senate.gov/2025/12/03/bennet-cornyn-bipartisan-colleagues-introduce-bill-to-increase-housing-availability-and-affordability/) | Sponsor releases + GovInfo bill text located; Congress.gov bot-blocked |
| School-district tax cap 2026-27: allowable levy growth capped at **2%** (inflation factor 2.63%), 5th straight year | [OSC release, Jan 2026](https://www.osc.ny.gov/press/releases/2026/01/dinapoli-school-district-tax-cap-levy-remains-at-2-percent) | Search + liveness 200 |
| Village of RVC FY2026-27 adopted budget (Apr 30, 2026): total **$63,641,946**; levy **$44,488,056**; village tax rate $69.89 → **$74.91**/$100 AV (**+7.2%**) | [Village FY27 adopted budget (PDF)](https://www.rvcny.gov/sites/g/files/vyhlif4946/f/uploads/village_of_rockville_centre_fy27_adopted_budget.pdf) + [supplemental](https://www.rvcny.gov/sites/g/files/vyhlif4946/f/uploads/village_of_rockville_centre_fy27_adopted_budget_supplemental.pdf) | PDF downloaded; figures machine-verified by pypdf text extraction in the July 18 adversarial review ($63,641,946 / $44,488,056 / $74.91, +7.18% printed in the adopted doc); corroborated by search-engine extraction of the same official PDF and [LI Herald coverage](https://www.liherald.com/rockvillecentre/stories/rockville-centre-proposes-636-million-budget-with-tax-increase,221192): $63.6M, levy $44.5M, rate +7.15% at tentative stage). Levy math: 44.488/41.740 = **+6.6%** vs FY26 levy $41.74M (June receipt, verified exactly) |
| Nassau assessment roll frozen since 2020-21 reassessment; 2026/27 tentative roll published Jan 2, 2026; Class 1 published LOA 0.1%; ARC residential ratio 0.060%; next grievance window opens Jan 2, 2027 | [Nassau ARC FAQ](https://www.nassaucountyny.gov/1517/Frequently-Asked-Questions) · [2026/2027 tentative rolls](https://www.nassaucountyny.gov/5739/20262027-Tentative-Assessment-Rolls) · [Farrell Fritz (freeze, 4th year)](https://www.farrellfritz.com/insights/tax-tracker/for-the-fourth-straight-year-nassau-county-has-chosen-to-freeze-its-annual-tax-roll/) | FAQ fetched (0.060% ARC / 0.062% SCAR quoted); freeze continuation is county practice reported through 2026 — no county press release states it affirmatively; phrased accordingly |
| Blakeman: re-elected county executive Nov 2025; announced for governor Dec 9, 2025; Stefanik exited Dec 20, 2025; Trump endorsement; **GOP nominee**, general Nov 3, 2026 | [CBS New York](https://www.cbsnews.com/newyork/news/bruce-blakeman-running-for-new-york-governor-2026/) · [Wikipedia roundup](https://en.wikipedia.org/wiki/Bruce_Blakeman) | News verification (secondary; no primary gov't source exists for a candidacy) |
| RVC UFSD 2026-27: adopted **$141,323,369** (+1.03%); levy **+2.06%** (~$2.25M); cut 22.2 teaching + 40 TA positions, restored 13 facilitators; passed **1,915–1,195** May 19, 2026; district estimate ≈ $309/yr on typical home | [LI Herald: board adopts $141.3M budget](https://www.liherald.com/rockvillecentre/stories/rockville-centre-school-board-adopts-1413m-budget-preserves-tax-cap,221736) · [LI Herald: budget passes](https://www.liherald.com/stories/school-budget-passes-in-rockville-centre,222477) · [Patch: vote result](https://patch.com/new-york/rockvillecentre/rockville-centre-budget-vote-results-are-see-how-voters-weighed) · [District budget page](https://www.rvcschools.org/43656_3) | June receipts (exact) + July search re-confirmation of all figures |

## Math-audit receipts (fetched 2026-07-18, same-day as the refresh)

| Claim | Source (primary) | How verified |
|---|---|---|
| RVC UFSD 2025-26 school tax rate **$2,247.867/$100 county AV**; library **$84.459**; in-village general (county+town) **$206.397**; out-of-village general $886.816 | Nassau LRV parcel tax tables: [36366++00150 (55 Kennedy Ave, in-village)](https://lrv.nassaucountyny.gov/info/36366++00150/) · [36503++00090 (413 Rose Ln, out-of-village)](https://lrv.nassaucountyny.gov/info/36503++00090/) | Rendered via headless browser (search is reCaptcha-gated; direct parcel URLs load); line items × AV reproduce every printed dollar amount to the penny |
| $15,230.09 = combined 2025-26 **school+library** bill on a typical in-village parcel (AV 653) — NOT a total bill | Same LRV tax table (55 Kennedy Ave) | Printed "Combined School Taxes $15,230.09"; resolves the March-model/June-validation label dispute |
| County Class-1 FMV frozen across displayed roll years; EMV (=AV÷0.1%) lags FMV under the 6%/yr / 20%/5yr caps; 2027/28 tentative values jump toward FMV (+21% on the sample parcel) | Same LRV parcel pages ("Values" tab + Taxpayer Protection Plan notices) | Values table quoted; §1805 cap language printed on page |
| Village of RVC assesses its **own roll**: FY26 AV $59,732,924 / rate $69.89; FY27 AV $59,388,849 / rate $74.91 per $100 village AV | [Village FY27 adopted budget PDF](https://www.rvcny.gov/sites/g/files/vyhlif4946/f/uploads/village_of_rockville_centre_fy27_adopted_budget.pdf) | pypdf extraction; levy ÷ AV × 100 = 74.91 exactly |
| Village level of assessment (equalization rate): **0.87 (2025)**, 0.96 (2024), 0.99 (2023) → village full value ≈ $6.9B | [NYS ORPTS via data.ny.gov (e6pv-77bh, SWIS 282029)](https://data.ny.gov/resource/e6pv-77bh.json?%24q=ROCKVILLE) | Socrata API query returned the village rows |

## Reused June-2026 receipts (fetch-verified 2026-06-09, liveness 200 on 2026-07-18)

| Claim | Source |
|---|---|
| Exemptions shift the levy onto non-exempt taxpayers (fixed-levy mechanics) | [OSC, "Property Tax Exemptions" (PDF)](https://www.osc.ny.gov/files/local-government/publications/pdf/propertytax_exemptions_0.pdf) |
| STAR is state-funded (a state charge, not a district loss) | [RPTL §1306-a](https://www.nysenate.gov/legislation/laws/RPT/1306-A) |
| K-12 enrollment 3,533 (2015-16) → 3,276 (2024-25); district projects 3,260 for 2026-27 | [NYSED data site, RVC UFSD](https://data.nysed.gov/enrollment.php?year=2025&instid=800000049383) |
| 2,076 of 7,453 RVC owner-occupied homes (27.9%) have a householder 65+ | [ACS 2019-23 B25007, Rockville Centre village](https://data.census.gov/table/ACSDT5Y2023.B25007?g=1600000US3663264) — 2020-24 vintage agrees (28.0%) |
| Median owner-occupied home value ≈ $820K (ACS 2020-24: $818,700) | [ACS B25077, RVC — 2020-24 vintage](https://data.census.gov/table/ACSDT5Y2024.B25077?g=1600000US3663264) (2019-23 vintage consulted in June receipts) |
| Empty-nest boomers hold ~2× the share of large homes vs. millennials with kids (28%/16%, 2026 refresh) | [Redfin, 2026](https://www.redfin.com/news/empty-nest-large-homes-2026/) |
| Property-tax/lock-in mechanism (higher holding costs → turnover) | [Minneapolis Fed (Horwich), Nov 2024](https://www.minneapolisfed.org/article/2024/how-higher-property-taxes-increase-home-affordability) |
| Age-based property-tax exemptions measurably increase senior retention in place | [Banzhaf et al., NBER w25468](https://www.nber.org/papers/w25468) |
| ~1.9M senior-owned homes exceed the unindexed §121 exclusion (~$620B unrealized gains) | [AEI](https://www.aei.org/articles/capital-gain-regulations-on-home-sales-and-baby-boomer-lock-in/) |
| NYS real-estate transfer tax $2 per $500 (0.4%); mansion tax 1% ≥ $1M (buyer) | [DTF real estate transfer tax](https://www.tax.ny.gov/bus/transfer/rptidx.htm) |
| Nassau senior exemption brochure (tier table incl. 65% ≤ $47,000) | [Nassau brochure (Rev. 3-26, PDF)](https://www.nassaucountyny.gov/DocumentCenter/View/49404/) |
| Village FY26 levy $41.74M / budget $60.88M (baseline for FY27 comparison) | June receipt: village adopted FY26 budget (verified exactly, `docs/findings/calculator-macro.md`) |

## Derived figures (arithmetic in the brief)

| Figure | Derivation |
|---|---|
| ~$2,058/yr state savings per Enhanced→Basic STAR transition | $3,147.01 − $1,089 = $2,058.01 (2025 final credit amounts, RVC Class 1) |
| ~$3,280 one-time NYS transfer tax per sale | 0.4% × $820,000 median value |
| 27.9% senior-owned share | 2,076 ÷ 7,453 (ACS B25007) |
| ~257-student enrollment decline | 3,533 − 3,276 (NYSED) |
| Village levy +6.6% FY27 | $44,488,056 ÷ $41,740,000 − 1 |
| School levy ≈ $111.5M 2026-27 | adopted +2.06% on 2025-26 levy (June receipt) |

## Verification caveats (disclosed)

1. **Congress.gov** rejects automated fetches (HTTP 403). H.R. 1340 / S. 3332 status verified via GovInfo, BillTrack50, and sponsor press releases; Congress.gov links included because they are canonical and work in a normal browser.
2. ~~Village FY27 PDF text layer could not be machine-extracted~~ **Closed 2026-07-18:** pypdf extraction succeeded in the adversarial review; the adopted PDF prints $63,641,946 / $44,488,056 / $74.91 per $100 (+7.18%).
3. **2026 final STAR credit amounts** (the check amounts) were not yet published by DTF as of July 18, 2026; the brief uses 2025 final credits, labeled.
4. **Enacting chapter for the $75K/2027 income-cap amendment was not identified** (it is *not* in DTF's 2022–2025 legislative summaries; it is *not* Ch. 581). The statutory text itself is the receipt. See `docs/REFRESH_2026-07.md` §Errors.
5. **Nassau parcel-level §467/Enhanced-STAR counts remain unobtained** (FOIL still open, June item E2). No aggregate "exemption gap" dollar figure appears in the brief for this reason.
