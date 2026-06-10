# Corrections — old → new, per artifact
_Companion to [VALIDATION_REPORT.md](VALIDATION_REPORT.md); receipts in [findings/](findings/). Applied corrections: `site/calculator.html` (this branch). The .docx and .xlsx are binaries — corrections below are specified precisely enough to regenerate them; the deck (`site/index.html`) is the corrected replacement for the action plan's external-facing claims._

## A. Concepts to reframe everywhere (not just values)

| # | Replace | With |
|---|---------|------|
| A1 | "$6.9M annual revenue gap"; "recaptured school tax revenue"; "deficit coverage 18–91%" | "Exemptions shift levy onto non-exempt taxpayers" (OSC). Turnover = **taxpayer relief + state savings**, not district revenue. District-revenue channels from turnover: tax-base growth factor (renovations), enrollment-linked aid, budget-vote sustainability. Remove all "deficit coverage" rows. |
| A2 | Enhanced STAR in any district-loss math | STAR is a **state charge** (RPTL §1306-a). Senior→family transition saves **NY State** $2,058/yr (Enhanced credit $3,147.01 → Basic $1,089). |
| A3 | "Prop 19-style portability for NY" as the Level-2 centerpiece | NY has no acquisition-value assessment (RPTL §305); nothing to port; Nassau sales don't trigger reassessment. Replace with: **S3309/A5288** (exemption continuity in a move year), **senior school-tax deferral enabling act** (OR/MA/WA/TX models), S3574 (renewal notices). |
| A4 | "STAR Credit Modernization … shifts $2,680/parcel from local burden to state" | Exemption is already state-funded; credit conversion changes plumbing and lets the benefit grow ≤2%/yr (helps the homeowner, not the levy). |
| A5 | "Loss of §467/STAR benefits upon moving" as a lock-in driver | Mostly myth — Enhanced STAR follows the owner; §467 applies where adopted; Nassau waives the 12-month wait for prior holders. Real frictions: move-**year** timing (S3309 fixes), income re-qualification, capital gains, inventory. |
| A6 | "1,404 senior exempt parcels (18%)" | **2,076 senior-owned owner-occupied homes (27.9%, ACS B25007)** — of which the §467-eligible subset is unknown until county data/FOIL. Never multiply all senior homes by a full benefit stack. |
| A7 | "288 seats of spare capacity" | "~260–290-student enrollment decline since 2015-16" (NYSED 3,533→3,276; district 3,548→3,260 proj.). No public capacity study exists. |
| A8 | Marginal-cost story ($0 / $5K one-time / $12K-yr in different places) | One explicit assumption, stated: low marginal cost only while spare seats last; model's own ratio row (0.3×) must not coexist with "pure upside" prose. |

## B. RVC_Senior_Transition_Financial_Model.xlsx

| Cell | Old | New (source) |
|------|-----|--------------|
| B7 pop | 25,770 "QuickFacts 2024" | 25,718 (PEP 7/1/2024); 25,770 is ACS 2019-23 — fix label |
| B10 homeownership | 0.78 | **0.745** (ACS DP04 2019-23; 0.751 in 2020-24) |
| B11 owner-occ | 7,808 | **7,453** (ACS B25003) |
| B12 65+ | 0.196 | **0.201** (ACS S0101) |
| B13 income | $144,516 ✓ | keep; note 2020-24 = $151,938 |
| B16 senior parcels | =B11×0.18 → 1,405 | **=B11×0.279 → ~2,079** (ACS B25007: actual 2,076); add separate, explicit "% §467-eligible" assumption cell (UNKNOWN; FOIL) |
| B20 budget | $139.89M ✓ | keep for 2025-26; add 2026-27 adopted **$141,323,369** (+1.03%) |
| B22 levy increase | 2.6% ✓ | keep; add 2026-27 adopted **+2.06%** |
| B23 state aid | $22M "estimated" | **~$20–21M** (LI Herald $19.8M 2024-25; "15% of budget") |
| B25 enrollment | 3,326 "LI Herald/US News" | **3,276 (NYSED 2024-25)**; 3,326 appears in no public source |
| B26 proj. 2026-27 | 3,260 ✓ | keep (district statement) |
| B27 per-pupil | =B20/B25 → 42,060 | label "budget ÷ enrolled"; add **NYSED official $37,973 (2023-24)** and ST-3 actual $40.2K |
| B29 allowable levy | $111,911,163 "2.45%" | **superseded** — final cap ≈2.1%; adopted levy +2.06% (≈$111.49M) |
| B30 deficit | $3.78M | keep as January projection; add outcome: closed via ≈22 teaching + 40 TA cuts; passed 1,915–1,195 (5/19/26) |
| B34 §467 max income for 50% | $58,399 | **$50,000** (50%); $58,399 = ceiling of the 5% tier; **65% ≤ $47,000** since Ch. 581 of 2025; income cap → $75,000 eff. 7/1/2027 |
| B36 sliding max | =B34+8400 → 66,799 | **delete** — no tier above $58,399 exists |
| B38/39 STAR AV | 140 / 50 ✓ | confirmed (DTF 2025-26 Nassau, RVC Class 1) |
| B40/41 STAR savings | $2,680 / $1,220 | **$2,856 / $1,068 (exemption)**; **$3,147.01 / $1,089 (credit)** — DTF 2025 final, RVC Class 1 |
| B42 "Avg School Tax on Median Home" | $15,230 | **mislabeled — that's the TOTAL bill (unverified)**. School-only ≈ 60–62% of bill. Rebuild from levy data or label "estimate" |
| B43 combined savings | $4,900 | split into: STAR (state-funded — exclude from any local-impact math) + §467 school-share by tier (5–65% of school tax, income-gated); do not average across all senior homes |
| B44/45 | =B42−B43; notes wrong | fix formulas + notes (B42−B43; "=B43") after relabeling B42 |
| Scenario sheet | 1,405 base; $4,900/parcel; "deficit coverage" | base 2,076; per-parcel = §467-school-share only for the eligible subset (parameter); delete deficit-coverage row (concept error A1); transfer tax: 0.4% × **$820K** = $3,280/sale (NY State revenue); note buyer-side 1% mansion tax ≥$1M |
| §467 Deep Dive sheet | tiers $58,399→50% … $66,799→5%; "AV reduction" $362,500 etc.; STAR $2,856 ✓ | replace tier table with Nassau brochure (Rev. 3-26): **65% ≤$47,000 → 5% at $57,500–58,399**; delete the "AV reduction" column (Nassau Class 1 LOA = 0.1%; AV of a $735K home ≈ $735 — the column's premise is wrong); keep $2,856/$1,068 |
| Sensitivity sheet | base parcels 1,342; savings $5,500 | align to 2,076 / new per-parcel definition; marginal cost: one concept (see A8) |

## C. RVC_Housing_Transition_Action_Plan.docx

| Item | Old | New |
|------|-----|-----|
| Headline | "$688K–$3.4M annually in recaptured school tax revenue" | Reframe per A1/A2 (see deck p.5 for the corrected per-100-transitions table) |
| Exec summary | "~1,404 parcels… reducing annual school tax revenue by ~$4,900/parcel… $6.9M gap… nearly double the deficit" | Delete; replace with burden-shift framing + the FOIL data ask |
| Budget | "~$135 million budget" | $139.89M (2025-26); $141.32M (2026-27 adopted) |
| Per-pupil | $42,050 | $37,973 NYSED official (2023-24); $40.2K ST-3 actual; "$42.1K" only as budget÷enrolled |
| Deficit/cap | "$3.78M deficit… cap 2.1% (MBJ)" | deficit closed (Apr–May 2026, −22 teachers/−40 TAs, passed 62–38); final cap ≈2.1% ✓; drop the 2.45%/$111.9M projection |
| Reserves | "$8M (8% of budget)" | $8M is 5.7–5.9% of budget; verified components: unappropriated $4.8M (3.5%), appropriated $2.8M→$1.6M, ERS+TRS $4.15M; attribute "$8M/peer 14%/GC $27M" to Joyce analysis; GC budget is **$137.8M**, not $122.7M |
| §467 description | "max income threshold $58,399 … 5–50% … incomes up to $66,799" | Correct tiers (B34 row above); note 65% tier (Ch. 581 of 2025) + $75K cap (7/1/2027) |
| Effective senior tax | "~$4,563 school" / "$7,650 total" / model's $10,330 | Recompute per corrected tiers; only income-eligible seniors get §467; median RVC senior income (~$77–80K) **exceeds** §467 eligibility entirely |
| Lock-in ¶ | "Fed. Reserve Bank of Minneapolis research… 28%/14%" | 28.2%/14.2% is **Redfin (Jan 2024; 2026 refresh 28%/16%)**; cite Minneapolis Fed (Horwich, Nov 2024) separately for the property-tax/lock-in mechanism |
| Federal level | "AEI-style proposal"; Schumer "Majority Leader" | Name the bills: **H.R. 1340 / S. 3332**; Gillen not yet a cosponsor (ask!); Schumer = **Minority** Leader; Gillibrand hook = Approps THUD RM + Aging RM |
| State level | "Sen. Todd Kaminsky (SD-9)"; "Asm. Ed Ra (AD-19)"; "Prop 19-style portability"; "S5175A conditional support" | **Sen. Patricia Canzoneri-Fitzpatrick (R, SD-9, RVC resident)**; **Asm. Judy Griffin (D, AD-21)**; replace portability per A3; S5175A **is law** (Ch. 581, 12/5/2025) — pivot to local opt-in posture + fiscal-note ask |
| County level | "Blakeman ✓"; "56 districts ✓"; budget $3.7B | Blakeman ✓ (re-elected 11/2025; running for governor); 56 ✓; budget **$4.2B** |
| Coalition table | Levittown "TWO schools closed (Pintail Lane, Cherrywood)"; Long Beach "~2,800"; Hempstead "~7,000"; Baldwin "~5,500"; Island Trees "~3,000"; H-W "3,100+"; GC "$122.7M" | Levittown closures were **1976/mid-70s** (use as historical precedent only; 6 elementaries today; budget $274.1M; 7,061 students); Long Beach **East stayed open**, 3,265 students; Hempstead **5,071**; Baldwin **4,309**; Island Trees **2,261**; Hewlett-Woodmere **2,650**; GC **$137.8M**, 3,931. Confirmed: Locust Valley, OBEN (1,569→1,310), Massapequa, Lynbrook, Malverne, Uniondale demographics, Great Neck 6,600. Roosevelt is **growing** (3,020) — drop as decline example |
| ToH row | "18% tax cut" | General-Fund levy only (~$5M; town-wide levy ≈ flat); Supervisor is **John Ferretti** |
| Messaging | "spends $42K/student, scores 55% above state average" | use NYSED $37,973 + note scores are 2021-22 aggregator vintage |
| Sources appendix | "Minneapolis Fed 28%…"; "S5175A (2025)…" | per above; add Nassau brochure, DTF STAR tables, OSC exemption brief, RPTL §1306-a |

## D. RVC_Tax_Calculator.html → applied in `site/calculator.html`

| Area | Old | New |
|------|-----|-----|
| STAR const | basic 1220 / enhanced 2680 | **1089 / 3147** (DTF 2025 final credit, RVC Class 1; exemption $1,068/$2,856 noted) |
| Components | school .62 / village .18 / county .12 / town .03 / library .03 / special .02 | school .61 / **village .21** / county .12 / town .02 / library .025 / special .015 (levy-derived estimate; labeled) |
| Default market value / DEMO.homeValue | $735,000 / {rvc:735000, nassau:660000, nys:384000, us:345000} | **$820,000** / {rvc:818700, nassau:658700, nys:423800, us:332700} (ACS 2020-24) |
| homeOwnership | rvc .78 / nassau .80 / us .66 | rvc **.745** / nassau **.82** / us **.65** |
| avgPropTax | nassau 13680 / nys 6600 / us 3500 | nassau **13059** (ATTOM 2023) / nys **7732** / us **4427** (ATTOM 2025); rvc 15230 kept, labeled estimate |
| pctItemize | .68/.62/.35/.13 | **.257 / .198 / .104 / .096** (IRS SOI TY2022) + rewritten SALT blurb |
| Income-by-age | invented 10-yr brackets | ACS B19049 2020-24 brackets (25-44 $210,409; 45-64 $179,214; 65+ $79,722) mapped to UI; NYS/US shown as all-household approx. |
| School card | $42,050; 3,326; "down from 3,548 (−8%)"; 10:1 "vs 13:1 natl"; deficit-open text; "1% growth in state aid"; reserves "~$8M vs $27M GC" | $42,060 budget-math + **$37,973 NYSED official**; **3,276 NYSED 2024-25** (3,533 in 2015-16); 10:1 "vs 11:1 NY"; budget-passed timeline (−22/−40, 1,915–1,195); "total revenue +~1%"; verified reserve components + attributed Joyce figures (GC budget $137.8M) |
| Per-pupil chart | RVC 42,050 vs ST-3 peers | all ST-3 2023-24 actuals: **RVC $40.2K**, Jericho $40.9K, PW $36.2K, Manhasset $35.1K, GC $32.7K |
| NYS card | $36,293 "91% above"; NAEP 214/233/266/279 vs 216/236/259/274 + ranks; AIM $7.6B; SUNY/CUNY $13.1B·635K; STAR $2.7B; spending shares unlabeled | **Census FY2024: NY $31,918 vs US $17,619 (+81%, #1)**; NAEP 2024 actual **215/234/257/271 vs 214/237/257/272**, ranks removed; **AIM $715M**; SUNY 64 (~368K) + CUNY 26 (~263K), ~$7.6B state operating; STAR ~$3B+; shares labeled "State Operating Funds" |
| 2026 NYS relief box | "4%–6.85% → 3.9%–5.9% under $323K" | bottom **five** brackets only: 3.9/4.4/5.15/5.4/5.9% (2026), again −0.1pt 2027; 6.85% unchanged |
| Federal cards | SS $1.5T/$1,922/51.5M/67.9M/79%; Medicare $912B; Medicaid $616B; ACA $85B; MA 51%; IRMAA $206K; debt $36.2T/$962B/$2,640/"first time > defense"; defense $872B; SNAP $114B; Title I "$3,700/student"; FED_SPEND shares | FY2025/2026 actuals: SS **$1.6T / $2,071 (2026) / ~53M / ~71M / 77% payable**; Medicare **$987B**; Medicaid **$669B**; ACA **~$125B**; MA **54%**; IRMAA 2026 **$218K MFJ**; debt **$38.9T / ~$1.03T / ~$3,000 / "every year since FY2024"**; defense **$917B**; SNAP **~$100B**; Title I **$126,911 total**; shares .28/.23/.15/.13/.10/.09/.02 |
| SALT box | static $40K/$500K | + 2026 schedule note ($40,400/$505,000; +1%/yr→2029; $10K floor; 2030 reversion) |
| MTA card | $20.5B; state aid $3.8B; ridership 89.3M; fares $13.75/$349 | 2026 adopted ~$20.5B ✓ (labeled); dedicated streams **~$3.7B**; **75.5M (2024, +15.8%)**; Zone 4 **$13.50 peak / $264.25 monthly (2026)** |
| Safety card | DOCCS $4.3B; 31,000; $139K; −60%; courts $3.4B | **$3.3B ops (FY2026)**; **~33,500**; **$115K+ (2021 official)**; **−54% since 1999**; courts **~$3.0B** |
| Medicaid card | $34.2B/$109.6B; 6.8M/7.7M peak; "2015 agreement… $80M" | **$37.7B state / $103B total (FY2025)**; **6.9M (2/2025), peak ~7.9M**; takeover enacted **2012-13** (phased by 2015), savings unverified-labeled |
| County/town cards | Nassau "$3.7B"/1.36M; ToH "−18%" | **$4.2B / 1.40M**; "General-Fund levy −18% (~$5M; town-wide ≈ flat)" |
| Sewer text | "RVC is one of 6 municipal sewer districts" (implying own treatment) | one of six districts that **collect and pump to Nassau's Bay Park/South Shore facility** |
| Volunteer FD | "$8–12M saved annually" | labeled unofficial estimate (no published source) |
| Benchmark chart | neighbor rates presented as data | labeled "illustrative estimates" |
| Footer | "Built March 2026" | + "figures revalidated June 9, 2026" |

## E. Still-open data items (cannot be fixed from public sources)

1. **RVC UFSD §467 adopting resolution + current ceiling + 65%-tier posture** — district clerk / FOIL.
2. **Count of §467 and Enhanced STAR parcels in RVC by tier** — Nassau Dept. of Assessment (FOIL drafted in plan Phase 1). Until then, no aggregate "exemption gap" number should be published.
3. **Total average RVC tax bill ($15,230) and bill-component split** — derivable from a sample of actual bills or county levy files; currently an estimate.
4. **Garden City $27M reserves** — only in the Joyce substack; needs GC's audited financials (ST-3/OSC) to cite independently.
