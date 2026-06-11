# Fact-Check: RVC Homeowner Tax Calculator — Macro Claims
Verified 2026-06-09 against primary sources. Calculator built March 2026 for tax year 2025.
Verdicts: CONFIRMED / CLOSE / WRONG / OUTDATED / UNVERIFIED.

## FEDERAL

### 1. 2025 federal brackets — CONFIRMED
Every breakpoint matches IRS Rev. Proc. 2024-40 exactly. MFJ: 10% to $23,850; 12% to $96,950; 22% to $206,700; 24% to $394,600; 32% to $501,050; 35% to $751,600; 37% above. Single: $11,925 / $48,475 / $103,350 / $197,300 / $250,525 / $626,350.
Source: IRS Rev. Proc. 2024-40 (https://www.irs.gov/pub/irs-drop/rp-24-40.pdf); Tax Foundation 2025 brackets (https://taxfoundation.org/data/all/federal/2025-tax-brackets/). Vintage: Oct 2024, final for TY2025.

### 2. 2025 standard deductions (post-OBBBA) — CONFIRMED
MFJ $31,500; Single/MFS $15,750; HoH $23,625. OBBBA (P.L. 119-21, July 2025) raised the originally announced amounts.
Source: IRS newsroom OBBBA pages (https://www.irs.gov/newsroom/one-big-beautiful-bill-act-tax-deductions-for-working-americans-and-seniors); Tax Foundation. Vintage: July 2025, final.

### 3. OBBBA SALT cap — CONFIRMED for 2025; hardcoding $40K/$500K is WRONG for 2026+
2025: cap $40,000 ($20,000 MFS); phase-down at 30% of MAGI over $500,000 ($250,000 MFS), floor $10,000. **Correct 2026 values: cap $40,400 ($20,200 MFS); MAGI threshold $505,000 ($252,500 MFS).** Both rise 1%/yr through 2029; cap reverts to $10,000 ($5,000 MFS) in 2030. A calculator hardcoding $40K/$500K understates the 2026 cap by $400 and starts the phase-down $5,000 too early.
Source: Venable SALT alert (https://www.venable.com/insights/publications/2025/08/salt-alert-final-obbba-temporarily-expands-salt); HCVT (https://www.hcvt.com/alertarticle-SALT-Deduction-Cap-Increase-Under-OBBBA); Thomson Reuters. Vintage: statute, fixed schedule.

### 4. Federal spending shares FY2025 — CLOSE on shares, several dollar figures OUTDATED (FY2024 values)
FY2025 actuals (CBO MBR Summary for FY2025, pub. 61307, Nov 2025): total outlays **$7.0T** (claim $7.1T close); deficit $1.8T.
- Social Security **$1.65T = 23.5%** — claim 21% is LOW.
- Medicare **$987B net (14.1%)**; + Medicaid $669B + other health ≈ 27-28% — claim "Medicare+Health 30%" slightly high but in range.
- Net interest **~$1.03T (14.7%)** — first time over $1T. Claim $962B/14%: dollar figure matches no year (FY2024 = $949B); share OK.
- Defense (function 050) **$916.6B FY2025 (13.1%)** per Treasury Combined Statement — claim $872B is the FY2024 value (~$874B); 13% share still right.
- Income security ~$670-690B ≈ 9-10% (claim 8%/$656B slightly low; FY2024 function 600 was $671B).
- Transportation ~$135-140B ≈ 2% — CLOSE.
- "Education/Science/Other 12%": not verifiable as a bucket; note Dept. of Education outlays collapsed to **$34B** in FY2025 (vs $268B FY2024) due to student-loan re-estimates (CBO), so any education slice is unstable.
Sources: CBO MBR FY2025 summary (https://www.cbo.gov/publication/61307); AAF summary (https://www.americanactionforum.org/insight/cbo-fy-2025-budget-deficit-totaled-1-8-trillion/); Treasury outlays by function (https://www.fiscal.treasury.gov/files/reports-statements/combined-statement/cs2025/outlay.pdf). Vintage: FY2025 final (Oct-Nov 2025).

### 5. Social Security — OUTDATED (all figures are mid/late-2024 vintage)
- Outlays: FY2025 = **$1.6T** (FY2024 was $1.5T). Claim $1.5T outdated.
- Avg retired-worker benefit: claim $1,922 ≈ Sept-Oct 2024. Jan 2025 = $1,976 (after 2.5% COLA); Jan 2026 = **$2,071** (2.8% COLA); April 2026 actual $2,081 (SSA snapshot).
- Retired workers: claim 51.5M ≈ late 2024; now ~53-54M (April 2026: 57.1M retired workers + family members).
- Total beneficiaries: claim 67.9M ≈ 2024; Jan 2026 COLA applied to **~71M** Social Security beneficiaries.
- OASI depletion: 2025 Trustees Report (June 2025): depletion **2033, 77% payable** (claim's ~79% is the 2024 report figure). A March 2026 build should cite 77%.
Sources: CBO MBR FY2025; SSA 2026 COLA fact sheet (https://www.ssa.gov/news/en/cola/factsheets/2026.html); SSA press 2025-06-18 (https://www.ssa.gov/news/en/press/releases/2025-06-18.html); SSA trustees summary (https://www.ssa.gov/oact/trsum/); SSA monthly snapshot (https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/).

### 6. National debt / interest — OUTDATED/WRONG for a March 2026 build
- Debt: claim $36.2T ≈ Feb-Mar **2025**. As of March 4, 2026: **$38.86T** gross ($113,638/person; $2.64T added YoY) — JEC from Treasury Debt to the Penny. ~120% of GDP matched mid-2025; gross debt is now ~125-127% of GDP.
- Net interest: FY2025 = **~$1.03T** (CBO), not $962B (no year matches $962B; FY2024 = $949B).
- "Exceeds defense for first time": WRONG timing — net interest first exceeded defense in **FY2024** ($949B vs ~$874B); it remained higher in FY2025 ($1.03T vs $917B).
- Interest per person: $1.03T ÷ ~341M ≈ **$3,000**, not $2,640.
Sources: JEC debt update Mar 2026 (https://www.jec.senate.gov/public/index.cfm/republicans/2026/3/national-debt-reaches-38-86-trillion-increased-2-64-trillion-year-over-year-7-23-billion-per-day); Treasury Debt to the Penny (https://fiscaldata.treasury.gov/datasets/debt-to-the-penny/); CBO 61307.

### 7. Health & program grab-bag — MIXED
- Medicare claim $912B: **WRONG/OUTDATED** — CBO FY2025 net Medicare = $987B (FY2024 = $870B). $912B matches neither.
- Federal Medicaid $616B: FY2024 value (actual $618B); FY2025 = **$669B**. OUTDATED.
- ACA subsidies $85B: WRONG/OUTDATED — premium tax credits + CSR outlays were **$104B in first 10 months of FY2025** (MTS, July 2025), ~$125B full-year. $85B ≈ FY2023-24 era.
- Medicare Advantage ~51%: OUTDATED — **54% of eligible beneficiaries in 2025** (34.1M) per KFF.
- IRMAA MFJ threshold $206K: that's the **2024** value. 2025 = $212,000; **2026 = $218,000 MFJ ($109,000 single)**; 2026 standard Part B premium $202.90.
- SNAP: 42M participants CONFIRMED (42.4M avg, FY2025 partial); but **$114B is FY2023 cost** — FY2024 ≈ $100B. Mixed vintages.
- EITC $73B: CLOSE — latest IRS stat: ~24M recipients, ~$70B (avg $2,894, TY2024).
- NIH $47B: CONFIRMED ($47.0B FY2025 program level).
- NASA $25B: CLOSE — FY2025 appropriation $24.8B.
Sources: CBO 61307; Treasury MTS July 2025 (https://fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202507.pdf); KFF MA 2025 (https://www.kff.org/medicare/issue-brief/medicare-advantage-enrollment-update-and-key-trends/); Kiplinger/CMS 2026 IRMAA (https://www.kiplinger.com/retirement/medicare/medicare-premiums-2026-irmaa-brackets-and-surcharges-for-parts-b-and-d); Pew/USDA FNS (https://www.pewresearch.org/short-reads/2025/11/14/what-the-data-says-about-food-stamps-in-the-us/); IRS EITC stats (https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit/earned-income-tax-credit-statistics); STAT/NIH (https://www.statnews.com/2025/09/12/nih-spending-47-billion-budget/); Planetary Society NASA FY2025 (https://www.planetary.org/space-policy/nasas-fy-2025-budget).

### 8. Title I to RVC UFSD "$3,700 per disadvantaged student" — WRONG/MISLEADING
Actual 2025-26 NYSED final Title I Part A allocation for Rockville Centre UFSD: **$126,911** (BEDS 280221030000). At ~3,300 enrolled students that's ~$38/student; the "$3,700 per disadvantaged student" framing would require only ~34 formula children, far below the district's low-income count (hundreds). National Title I averages run ~$1,200-1,500 per eligible child. The dollar total is tiny relative to the district's $139.9M budget (~0.09%).
Source: NYSED 2025-26 final Title I allocations (https://www.nysed.gov/essa/2025-26-final-allocations-title-i-part). Vintage: 2025-26 final.

## NEW YORK STATE

### 9. NYS 2025 brackets & standard deductions — CONFIRMED
Nine rates 4%/4.5%/5.25%/5.5%/6%/6.85%/9.65%/10.3%/10.9% with MFJ breakpoints as claimed ($17,150/$23,600/$27,900/$161,550/$323,200/$2,155,350/$5M/$25M); standard deduction $16,050 MFJ / $8,000 single. Unchanged for TY2025.
Source: tax.ny.gov 2025 tax tables (https://www.tax.ny.gov/pit/file/tax-tables/2025.htm); standard deductions (https://www.tax.ny.gov/pit/file/standard_deductions.htm). Vintage: TY2025 official.

### 10. "2026 Relief" claim — PARTIALLY WRONG (scope), schedule confirmed
FY2026 enacted budget cuts the **bottom five brackets only** (4%, 4.5%, 5.25%, 5.5%, 6%), i.e., taxable income up to $215,400 single / **$323,200 MFJ**: **-0.1pp in TY2026** and another -0.1pp in TY2027 (permanent).
- Exact 2026 rates: **3.9% / 4.4% / 5.15% / 5.4% / 5.9%** (2027: 3.8% / 4.3% / 5.05% / 5.3% / 5.8%).
- The claim's "3.9%-5.9%" endpoints are correct **for 2026**, but "from 4%-6.85%" is wrong: the 6.85% bracket ($323,200-$2,155,350 MFJ) is NOT cut and does not fall to 5.9%.
Source: budget.ny.gov enacted press (https://www.budget.ny.gov/pubs/press/2025/fy26-enacted-budget-new-legislation-cut-taxes-middle-class-nys.html); governor.ny.gov (https://www.governor.ny.gov/news/money-your-pockets-governor-hochul-signs-new-legislation-cut-taxes-middle-class-new-yorkers); Tax Foundation 2026 state rates (https://taxfoundation.org/data/all/state/state-income-tax-rates-2026/). Vintage: enacted May 2025.

### 11. NYS spending shares — CLOSE but basis mismatch
FY2026 enacted All Funds total = **$254B** (CONFIRMED). But the claimed shares (Medicaid/Health 33%, Education 27%, Transportation/MTA 12%, Public safety 6%) fit **State Operating Funds (~$143B)**, not the $254B All Funds base: on an All-Funds basis Medicaid alone (with federal share) is ~$110B ≈ 43%, and school aid $37.6B ≈ 15%. Internally inconsistent labeling; shares are defensible only if relabeled "state-funds share."
Source: DOB FY2026 Enacted Budget (https://www.budget.ny.gov/pubs/archive/fy26/en/index.html); agreement release (https://www.budget.ny.gov/pubs/press/2025/fy26-enacted-agreement.html). Vintage: May 2025.

### 12. School aid — CONFIRMED
FY2026 enacted: total School Aid **$37.6B** (+$1.7B, 4.9%); Foundation Aid **$26.4B** (+$1.4B). STAR "~$2.7B": UNVERIFIED/likely low — current STAR delivers >$2.2B in credits to ~3M homeowners plus exemption savings; total program ~$3.0-3.4B depending on year/definition.
Source: NY Assembly enacted release (https://nyassembly.gov/Press/?sec=story&story=113950); governor release (https://www.governor.ny.gov/news/governor-hochul-signs-legislation-make-historic-education-investments-and-promote-distraction); STAR (https://www.governor.ny.gov/news/money-your-pockets-governor-hochul-highlights-next-phase-star-tax-relief-going-millions-new). Vintage: May 2025.

### 13. Per-pupil spending — figures real but VINTAGE-MIXED (and the prompt's "FY2023" guess is off)
- **$36,293** = projected NY per-pupil for **2024-25 school year** (Empire Center/Governing, NYSED data), "nearly double the national average," "19 consecutive years #1."
- **"91% above" matches Census F-33 FY2022** (released May 2024): NY $29,873 vs US $15,633 → +91.1%.
- $36,293 vs $15,633 = +132% mixes NYSED 2024-25 projection with Census FY2022 US average — that's the page's inconsistency.
- Latest Census (FY2024, released **May 7, 2026**): **NY $31,918 (#1) vs US $17,619 → +81%**. (FY2023: US $16,526.)
Recommended fix: use one vintage — Census FY2024: NY $31,918, +81% above US $17,619.
Sources: Census FY2022 release (https://www.census.gov/newsroom/press-releases/2024/public-school-spending-per-pupil.html); Census FY2024 release (https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html); Governing (https://www.governing.com/number/36-293). 

### 14. NAEP 2024 NY vs national — WRONG (most scores and the flattering 8th-grade gaps)
Actual 2024 average scale scores, NY vs nation-public (NCES state snapshot reports):
- Grade 4 reading: **NY 215, natl 214** (claim: 214 vs 216 — both numbers wrong AND direction reversed; NY is slightly above, not below).
- Grade 4 math: **NY 234, natl 237** (claim 233 vs 236 — off by 1 each; direction right; NY lower than 18 states, higher than 3).
- Grade 8 reading: **NY 257, natl 257** (claim 266 vs 259 — wildly wrong; NY is exactly at national average, lower than 5 states, higher than 6).
- Grade 8 math: **NY 271, natl 272** (claim 279 vs 274 — wrong; NY at/below national, lower than 20 states).
- Claimed ranks (4R 32nd, 4M 46th, 8R 9th): NAEP doesn't publish ranks; "8th reading 9th" is unsupportable given NY = national average. UNVERIFIED/WRONG.
Source: NCES 2024 state snapshots NY G4/G8 reading & math (https://nces.ed.gov/nationsreportcard/subject/publications/stt2024/pdf/2024220NY4.pdf, .../2024219NY4.pdf, .../2024220NY8.pdf, .../2024219NY8.pdf). Vintage: NAEP 2024 (released Jan 2025).

### 15. "$7.6B Local Gov't Aid (AIM)" — WRONG (flagged)
AIM is **$715.2M/yr** (unchanged for years; cities/towns/villages outside NYC). $7.6B matches no AIM-related line; possibly conflates total state aid to all local governments or a multi-year sum. Should read ~$715M.
Source: OSC AIM page (https://www.osc.ny.gov/local-government/data/aid-and-incentives-municipalities-aim-and-temporary-municipal-assistance-tma); DOB FY2026 AIM runs (https://www.budget.ny.gov/pubs/archive/fy26/en/fy26en-aim-towns.pdf). Vintage: FY2026.

### 16. SUNY/CUNY/DOCCS/police/courts — MIXED
- SUNY 64 campuses CONFIRMED; ~368K students (Fall 2023) — claim ~380K CLOSE/high.
- CUNY: **26 colleges** (claim 25 campuses CLOSE); enrollment ~233K degree (+~30K adult ed) — claim ~255K CLOSE.
- "Combined state support ~$13.1B": MISLEADING/UNVERIFIED — state **operating** support for SUNY+CUNY ≈ $7.6B (FY2025); $13B+ resembles SUNY's own all-funds budget. Assembly cites $23.3B total higher-ed investment FY2026 incl. capital/TAP.
- DOCCS $4.3B: official FY2026 ops budget **$3.3B** (+capital ≈ $3.8B); $4.3B only if centrally-paid fringe is added — flag basis. Population ~**33,500** (claims "31,000 (~33K)" CLOSE). Cost/incarcerated: official 2021 figure $115K; ~$139K plausible with fringe/2024 costs (UNVERIFIED).
- State Police $1.1B: CONFIRMED ($1.10B state ops + $145M capital, FY2026 exec).
- Courts $3.4B: CLOSE — Judiciary FY2026 ask was $3.0B SOF (excl. fringe); $3.4B sits between cash and fringe-inclusive bases.
- "Down ~60% since 1999": OVERSTATED — ~72,600 (1999) → ~33,500 = **-54%**.
Sources: SUNY (https://www.suny.edu/suny-news/press-releases/10-24/10-24-24/top10promise.html); budget.ny.gov FY26 approps for DOCCS/State Police/Judiciary (https://www.budget.ny.gov/pubs/archive/fy26/ex/agencies/appropdata/CorrectionsandCommunitySupervisionDepartmentof.html, .../StatePoliceDivisionof.html, .../Judiciary.html); Vera DOCCS explainer (https://vera-institute.files.svdcdn.com/production/downloads/GJNY_DOCCS-Budget-Explainer_10.25.22.pdf).

### 17. MTA / LIRR — PARTLY WRONG
- MTA operating budget: 2025 adopted **$19.9B** (claim ~$20.5B CLOSE; 2026 adopted is ~$20.5B).
- State aid: dedicated state-administered streams ≈ **$3.7B** (PMT $3.1B + congestion surcharge $328M + MTA Aid $283M) — claim $3.8B CLOSE (definitions vary; total state-related support is much larger).
- LIRR 2024 ridership: **75.5M** (up 15.8% from 65.2M) — claim "89.3M highest since pre-pandemic" is **WRONG** (2019 was ~91M; 89.3M matches no year).
- RVC (Zone 4) fares: claim ~$13.75 peak / ~$349 monthly. Actual: monthly Zone 4 **$253 (2025) → $264.25 (Jan 4, 2026, +4.4%)**; peak one-way ≈ $12.50 (2025) → **$13.50 (2026)**. Peak one-way claim CLOSE to 2026 value; **monthly is wrong by ~$85-96** (matches a higher zone).
- Federal grants ~$1.5B/yr: PLAUSIBLE/UNVERIFIED (formula capital funds in that range).
Sources: MTA 2025 adoption materials (https://www.mta.info/document/160131); NYC Council MTA brief (https://council.nyc.gov/budget/wp-content/uploads/sites/54/2025/03/Metropolitan-Transportation-Authority.pdf); MTA/Hochul LIRR 2024 release (https://www.mta.info/press-release/icymi-governor-hochul-celebrates-long-island-rail-roads-strongest-year-date); 2026 fare change (https://www.mta.info/document/194866; https://lirrmap.com/lirr-fares/).

### 18. NYS Medicaid — DIRECTIONALLY RIGHT, NUMBERS STALE
- Spending: FY2025 state share **$37.7B**, federal $56.8B, total **$103.1B** (FPI from DOB); FY2026 total ~$110B. Claim $34.2B/$109.6B mixes vintages (state share is FY2024-ish; total is FY2026-ish).
- Enrollment: **6.9M (Feb 2025)**, down from peak ~7.9M mid-2023 — claim 6.8M CLOSE; "7.7M peak" slightly low.
- "~1/3 of New Yorkers" — CONFIRMED (≈35%).
- OMH $4.7B, DOH public health $1.2B, Nassau ~180K (~13%), takeover saves Nassau ~$80M/yr: UNVERIFIED in primary sources this pass. Note: the county Medicaid growth takeover was enacted in the **2012-13 budget** (fully phased by 2015), so "2015 agreement" is mislabeled; Nassau enrollment is likely >180K (~20% of 1.4M residents) — needs DOH county data.
Sources: FPI (https://fiscalpolicy.org/strange-accounting-understanding-the-growth-in-new-yorks-medicaid-spending); OSC unwinding note (https://www.osc.ny.gov/files/reports/pdf/medicaid-unwinding-financial-plan-risk.pdf); DOH global cap reports (https://www.health.ny.gov/health_care/medicaid/regulations/global_cap/monthly/sfy_2025-2026/docs/2nd_qtr_rpt.pdf).

## VILLAGE / LOCAL

### 19. Village budget — CONFIRMED exactly
FY2025-26 adopted: **$60,884,752** total; tax levy **$41,744,386** = 68.6% (claim 68.5%).
Source: rvcny.gov adopted budget (https://www.rvcny.gov/comptroller/links/2026-adopted-budget). Vintage: adopted 2025.

### 20. RVC Electric — CONFIRMED on RVC facts; PSEG comparison UNDERSTATED
RVC residential: **$0.1081/kWh first 500 kWh; $0.1144 summer excess** — matches claim. ~75% of energy from NYPA Niagara hydro — CONFIRMED (NYAPP). "One of ~50 muni/co-op utilities" — CONFIRMED (**47 municipal + 4 co-ops**, NYPA). BUT: PSEG-LI "~$0.130/kWh" appears to be supply-only/dated; all-in effective rates are ~19.2¢ (RVC, incl. surcharges) vs ~25-26¢ (PSEG-LI) — RVC runs ~25-40% cheaper, so the claimed $200-350/yr household savings is conservative/plausible (real gap can exceed $400/yr at 7,000 kWh).
Sources: rvcny.gov electric rates (https://www.rvcny.gov/electric-department/pages/electric-rates); NYAPP RVC profile (https://www.nyapp.org/village-of-rockville-centre); NYPA munis/co-ops (https://services.nypa.gov/Services/Clean-Resilient-Economic-Power-Supply-Options/Municipal-Electric-Utilities-and-Rural-Cooperatives); OhmSnap (https://www.ohmsnap.com/utilities/new-york/rockville-centre-electric).

### 21. Volunteer FD "saves $8-12M/yr" — UNVERIFIED (no source found)
No published estimate located (village docs, Herald, FASNY). FASNY's statewide studies value volunteer service in the billions statewide, and a 341-member department plausibly avoids a paid payroll of that order, but the specific $8-12M figure appears to be an unsourced estimate. Label as such or remove.
Source checked: rvcfd.org; usfiredept.com profile (341 volunteers, 5 stations).

### 22. Crime — CONFIRMED
NeighborhoodScout (FBI 2024 data, released late 2025): RVC combined violent+property crime rate **5 per 1,000**; 2024 crime **down 37%** vs 2023.
Source: https://www.neighborhoodscout.com/ny/rockville-centre/crime. Vintage: CY2024 FBI data.

### 23. Library budget — CONFIRMED in every detail
2025-26: budget **$4.2M**; salaries+benefits **just over $3.3M** (~78.6%); operations/maintenance **$288,300** (down from $321,100); materials **$101,450**; passed May 20, 2025 with **2,101 votes**; avg homeowner +**$11.97/yr**; levy increase under the 2.6% cap.
Source: LI Herald (https://www.liherald.com/stories/rockville-centre-library-budget-trustee-election-2025,214993; .../rvc-2025-2026-school-budget-passed,215105). Vintage: May 2025.

### 24. Tax-bill component shares — PLAUSIBLE but no primary source; village share likely understated
No published RVC-specific pie found. Sanity math from actual levies: school levy ≈ $109M (2025-26; 2026-27 allowable ≈ $112M), village levy $41.7M, library ≈ $4.0M. School ≈ 60-62% only if county+town+special ≈ 15-17% — consistent with Nassau guidance that school taxes are ~65% countywide and county ~14%. But village share computes to ~21-23%, above the claimed 18%. Library ~2-3% ✓.
**Library funding mechanism:** RVC Public Library is a **school-district public library** — its budget and trustees are voted at the annual school-district election (May 20, South Side HS, same ballot as RVC UFSD) and its levy is a separate line collected with the school tax bill, NOT part of the village levy (the village's $41.7M levy excludes it). Treating library as separate from both school and village lines (as the claim does) is correct presentation-wise.
Sources: Heller Tax Grievance Nassau guide (https://hellertaxgrievance.com/ultimate-guide-for-handling-property-taxes-in-nassau-county-2026/); Herald school/library vote coverage (above); Herald deficit story for $112M levy (https://www.liherald.com/...3.78M-deficit); rvcny.gov tax office (https://www.rvcny.gov/tax-office).

### 25. Sewage treatment plant — WRONG (important local error)
RVC does **not** operate its own treatment plant. Per the Bay Park Conveyance Project background: "The Village of Rockville Centre is one of **six municipal sewer districts** that collects sewage and **pumps it to county facilities to be treated**" (RVC's plant was taken offline when flows were diverted to Nassau County's Bay Park/South Shore Water Reclamation Facility). The "one of 6" part survives — but as a sewer *collection* district, not a treatment-plant operator.
Source: https://www.bayparkconveyance.org/project-background; RVC project page (https://www.rvcny.gov/home/pages/bay-park-conveyance-project). Vintage: current.

---

## Most important corrections
1. **NAEP (claim 14) is the worst error block**: actual 2024 scores are NY 215/234/257/271 vs national 214/237/257/272 — the page's flattering 8th-grade gaps (266 vs 259; 279 vs 274) don't exist (NY is at/below national in 3 of 4 cells, slightly above only in 4th-grade reading), and the cited ranks are unsupportable.
2. **"$7.6B AIM" (claim 15) is off by ~10x** — AIM is $715.2M/yr; and **Title I to RVC UFSD (claim 8) is $126,911 total**, which cannot support "$3,700 per disadvantaged student."
3. **SALT hardcoding (claim 3) breaks for 2026**: cap $40,400 and phase-down threshold $505,000 (then +1%/yr to 2029, $10K floor intact, reversion 2030).
4. **Debt/interest block (claim 6) is a year stale for a March 2026 build**: debt $38.86T (not $36.2T), FY2025 net interest ~$1.03T (not $962B), ~$3,000/person (not $2,640), and interest first exceeded defense in FY2024, not "now."
5. **NYS 2026 tax cut (claim 10) is mischaracterized**: only the bottom five brackets fall (to 3.9/4.4/5.15/5.4/5.9% in 2026, again in 2027); the 6.85% bracket is untouched — and **LIRR Zone 4 monthly (claim 17) is $264.25 (2026), not ~$349**; LIRR 2024 ridership was 75.5M, not 89.3M.
6. (Bonus, local) **RVC no longer operates its own sewage treatment plant** (claim 25) — it's one of six municipal sewer districts pumping to Nassau County facilities; and most federal benefit stats (claims 5-7) carry 2024 vintages that should be refreshed to FY2025 actuals (SS $1.6T, Medicare $987B, Medicaid $669B, MA 54%, IRMAA 2026 $218K MFJ).
