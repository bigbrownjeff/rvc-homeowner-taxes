# Demographics Fact-Check — Rockville Centre village (Nassau County, NY)

Verified 2026-06-09 against primary sources: data.census.gov (ACS 5-year, via the data.census.gov access API — note: api.census.gov now requires a key; data.census.gov internal endpoint used instead, values identical), Census PEP sub-county estimates CSV, 2020 Decennial PL, Data USA, Zillow, Redfin, ATTOM, IRS SOI zip-code file (TY2022 = latest published; TY2023 returns 404 as of today), AEI, Minneapolis Fed, GSU CSLF.

Geography: Rockville Centre village = place FIPS 3663264 (geoid 1600000US3663264). "2023 ACS" = 2019–2023 5-year; "2024 ACS" = 2020–2024 5-year (released Dec 2025, now the latest).

---

## 1. Total population 25,770 ("QuickFacts 2024 estimate")
**VERDICT: CLOSE (right number, wrong label).**
- 25,770 ±27 is the **2019–2023 ACS 5-year** population (B01003), not a 2024 estimate. Source: https://data.census.gov/table/ACSDT5Y2023.B01003?g=1600000US3663264
- Actual **PEP July 1, 2024 estimate (V2024): 25,718** (series: base 26,005; 2020: 25,895; 2021: 25,857; 2022: 25,709; 2023: 25,648; 2024: 25,718). Source: https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/cities/totals/sub-est2024_36.csv — this is the file behind the QuickFacts "Population estimates, July 1, 2024" row (QuickFacts itself blocks automated fetch, HTTP 403).
- **2020 Census count: 26,016** (P1_001N). Source: https://data.census.gov/table/DECENNIALPL2020.P1?g=1600000US3663264
- 2020–2024 ACS pop: 25,765. Vintages: PEP V2024; ACS 2019–2023; Census 2020.

## 2. Housing units 10,627 / occupied 10,010 / homeownership 78% / ~7,800 owner-occupied
**VERDICT: first two CONFIRMED; 78% WRONG; ~7,800 WRONG.**
- Total housing units **10,627** ✔ and occupied **10,010** ✔ — exactly the 2019–2023 ACS (B25002/DP04). Source: https://data.census.gov/table/ACSDT5Y2023.B25002?g=1600000US3663264
- Homeownership (owner-occupied rate): **74.5%** (2019–2023 ACS DP04_0046PE); **75.1%** (2020–2024 ACS, also Data USA). Never 78% in any vintage checked (2008–2012: 75.2%; 2011–2015: 69.5%; 2015–2019: 70.5%; 2017–2021: 72.4%). 78% appears fabricated/rounded-up.
- Owner-occupied units: **7,453** (2023 ACS B25003_002), **7,444** (2024 ACS) — not ~7,800 (that's 78% × 10,010; overstates by ~350 homes / ~5%).
- Plausibility of 10,627 units for ~25,770 people: it is the official ACS figure (also the QuickFacts "Housing units" row), but it sits high vs the 2020 Census count (**9,991** units, H1) and the 2020–2024 ACS (**10,332**). Persons per occupied unit = 2.57 with a 26% renter share — not anomalous for the village (large co-op/apartment stock). Treat 10,627 as the upper end of a 10.0K–10.6K range.

## 3. Population 65+ = 19.6%
**VERDICT: CLOSE.** Actual **20.1%** (5,176 people) in 2019–2023 ACS S0101; still **20.1%** (5,179) in 2020–2024. Source: https://data.census.gov/table/ACSST5Y2023.S0101?g=1600000US3663264. The 19.6% on Data USA (https://datausa.io/profile/geo/rockville-centre-ny) is the 65+ share of the **insured/health-coverage universe**, not of total population — wrong denominator for this claim.

## 4. Median age 42.9
**VERDICT: CONFIRMED** for the latest vintage: **42.9** (2020–2024 ACS B01002; also Data USA 2024). The 2019–2023 ACS value was 43.8. Source: https://data.census.gov/table/ACSDT5Y2024.B01002?g=1600000US3663264

## 5. Median household income $144,516 (2023 dollars)
**VERDICT: CONFIRMED exactly.** B19013 = **$144,516 ±$13,140**, 2019–2023 ACS (2023 inflation-adjusted dollars). Source: https://data.census.gov/table/ACSDT5Y2023.B19013?g=1600000US3663264. Superseded by 2020–2024 ACS: **$151,938** (Data USA shows the same).

## 6. Median HH income, 65+ householders ≈ $82,000
**VERDICT: CLOSE (3–7% high).** ACS B19049_005 for RVC: **$76,815** (2019–2023); **$79,722** (2020–2024). Source: https://data.census.gov/table/ACSDT5Y2023.B19049?g=1600000US3663264. Using $82K in a benefit calculator overstates senior income slightly vs ACS.

## 7. Median home value $735,000 "(ACS)"
**VERDICT: WRONG — matches no ACS vintage.**
- ACS B25077 owner-occupied median value, RVC: 2016–2020: $653,300 → 2017–2021: $680,900 → 2018–2022: $763,400 → **2019–2023: $796,100 ±$30,262** → **2020–2024: $818,700**. $735K falls between the 2021 and 2022 vintages; it resembles a stale (early-2023) Zillow ZHVI mislabeled as ACS. Source: https://data.census.gov/table/ACSDT5Y2023.B25077?g=1600000US3663264
- **Zillow (June 2026): average home value $819,418, up 3.7% YoY; ZHVI mid-tier ~$807,009.** Source: https://www.zillow.com/home-values/40613/rockville-centre-ny/
- **Redfin: median sale price $555,000** (3 months ending April 2026, +16.8% YoY; $453/sqft; 37 days on market). Source: https://www.redfin.com/city/16226/NY/Rockville-Centre/housing-market. Redfin's all-property median is dragged far below ZHVI/ACS by RVC's heavy co-op/condo sales mix — do not use it as a single-family value.
- Use ~$800–820K (ACS 2024 / ZHVI) for owner-occupied homes, not $735K.

## 8. Calculator income-by-age table (25-34: $118K; 35-44: $172K; 45-54: $185K; 55-64: $148K; 65+: $82K)
**VERDICT: WRONG / unsupported by ACS.**
- ACS B19049 (place level) only has four brackets. RVC 2019–2023: under 25: suppressed; **25–44: $203,419; 45–64: $178,488; 65+: $76,815** (2020–2024: $210,409 / $179,214 / $79,722). The claimed 10-year brackets do not exist in ACS for places.
- Internal consistency fails: a population whose 25–34 median is $118K and 35–44 median is $172K cannot produce a blended 25–44 median of $203K — the younger-bracket figures are far too low. The 45–54/55–64 pair blends to ~$165K vs actual $178K (low). 65+ $82K is slightly high (see #6). The table looks modeled/invented, not ACS-sourced.

## 9. Nassau County: income ~$146K "#1 in NY"; pop 1.36M; home value $660K; homeownership 80%; avg tax $13,680
**VERDICT: mostly CONFIRMED/CLOSE; population WRONG (low).**
- Median HH income: **$146,202** (2020–2024 ACS) ✔; $143,408 (2019–2023). "#1 in NY State" ✔ — highest of all 62 NY counties (2023 5-yr top: Nassau $143,408 > Suffolk $128,329 > Putnam $127,405 > Westchester $118,411). Source: https://data.census.gov/table/ACSDT5Y2024.B19013?g=0500000US36059
- Population: claim 1.36M is **WRONG/low** — 2020 Census **1,395,774**; 2019–2023 ACS **1,388,138**; PEP V2024 **1,392,438** (co-est2024-alldata.csv). ~1.39M is correct.
- Median home value: **$658,700** (2019–2023 ACS B25077) ≈ $660K ✔.
- Homeownership: **81.9%** (2023 ACS), **82.0%** (2024 ACS) — claim 80% slightly low but CLOSE.
- Avg property tax $13,680: CLOSE. ATTOM reported Nassau average single-family tax **$13,059** (2023-data report; among the top counties nationally with ≥100K SF homes). ATTOM 2024 report lists Westchester $16,351 and Rockland $13,995 in the national top-25; Nassau not broken out but ~$14K is the right neighborhood. ACS county median is top-coded at "$10,000+" (B25103 = 10001), so ACS cannot verify. Sources: https://www.attomdata.com/news/most-recent/property-taxes-on-single-family-homes-up-7-percent-across-u-s-in-2023-to-363-billion/ ; https://www.attomdata.com/news/market-trends/home-sales-prices/2024-annual-tax-report/

## 10. Town of Hempstead ~800K, "largest town in NY"
**VERDICT: CONFIRMED.** 2019–2023 ACS: **789,177**; 2020 Census ~793,409. Largest town in New York (next-largest: Brookhaven ~486K) and the largest "town"-designated municipality in the US. Source: https://data.census.gov/table/ACSDT5Y2023.B01003?g=0600000US3605934000

## 11. "Nassau's 65+ households grew to 38.9% while families with kids dropped"
**VERDICT: CONFIRMED with definition pinned down.**
- The 38.9% = **share of Nassau households with one or more people 65+** (ACS B11007): 177,326 / 456,076 = **38.9%** (2019–2023). Trend: 36.1% (2014–2018) → 38.9% (2019–2023) → **39.6%** (2020–2024). Source: https://data.census.gov/table/ACSDT5Y2023.B11007?g=0500000US36059
- Households with own children <18 (B11005): 35.5% (2014–2018: 158,180/445,517) → 34.7% (2019–2023: 158,227/456,076) — the **share** dropped ~0.8 pt (the count is flat). Directionally supported; phrase precisely as "households including someone 65+."

## 12. "Boomers own 28% of large homes, millennials with kids 14% — Federal Reserve Bank of Minneapolis"
**VERDICT: WRONG ATTRIBUTION; figures CONFIRMED as Redfin.**
- True source: **Redfin, Jan 16, 2024**, "Empty Nesters Own Twice As Many Large Homes As Millennials With Kids": empty-nest baby boomers own **28.2%** of large US homes (3+BR); millennials with kids own **14.2%** (analysis of 2022 Census/ACS microdata). Sources: https://www.redfin.com/news/empty-nesters-own-large-homes/ ; press release https://www.businesswire.com/news/home/20240116359240/en/Empty-Nesters-Own-Twice-As-Many-Large-Homes-As-Millennials-With-Kids
- Redfin's 2026 refresh: empty nesters **28%**, millennial families **16%**. Source: https://www.redfin.com/news/empty-nest-large-homes-2026/
- The Minneapolis Fed piece (see #13) is a separate article about property taxes; fix the citation.

## 13. Minneapolis Fed, "How Higher Property Taxes Increase Home Affordability" (2024)
**VERDICT: CONFIRMED (exists; title as claimed).**
- **"How higher property taxes increase home affordability," Jeff Horwich (senior economics writer), Federal Reserve Bank of Minneapolis, Nov 14, 2024.** https://www.minneapolisfed.org/article/2024/how-higher-property-taxes-increase-home-affordability (page blocks automated fetch; confirmed via search index/snippets).
- Findings: higher property taxes raise the recurring cost of ownership but **capitalize into lower upfront home prices**; they **reduce lock-in** — motivating older/empty-nest owners to downsize and increasing turnover — and **shift homeownership toward younger families**. Notes property taxes ≈17% of the average mortgaged homeowner's housing budget (2021).

## 14. AEI: "~1.9 million homes locked in by capital gains" (2025)
**VERDICT: CONFIRMED (number); article dated Feb 2026.**
- **Edward J. Pinto, AEI Housing Center, "Capital Gains Rules on Home Sales and Senior Homeowner Lock In"** (AEI article dated **Feb 20, 2026**; the analysis circulated from 2025 in Pinto/Tobias Peter commentary). https://www.aei.org/articles/capital-gain-regulations-on-home-sales-and-baby-boomer-lock-in/
- Headline figures: **~1.9M homes owned by seniors (65+)** with gains above the current §121 exclusion (or above current but below doubled caps); **~1.4M** under retroactive inflation-indexing; **$620B** unrealized gains; **$93B** tax at 15%. If one-third respond over 10 years: ~450–600K homes released (~45–60K added sales/yr, +11–15%).
- §121 exclusion **$250K single / $500K joint, set by the Taxpayer Relief Act of 1997, never indexed for inflation** — CONFIRMED: 26 U.S.C. §121, https://www.law.cornell.edu/uscode/text/26/121. Caveat: 1.9M is senior-owned homes specifically, not all locked-in homes.

## 15. GSU CSLF, "Tax Relief for the Elderly, But at What Cost?"
**VERDICT: CONFIRMED in substance (original URL dead).**
- A CSLF news post with that headline existed (dead URL slug: https://cslf.gsu.edu/2016/10/20/tax-relief-elderly-cost/ — now 404 after site reorg), promoting the CSLF report **"Age-Based Property Tax Exemptions in Georgia" (Sept 2016; reissued April 2019), by H. Spencer Banzhaf, Ryan Mickey & Carlianne Patrick**; published academically as NBER WP 25468 and Journal of Urban Economics (2021). https://www.nber.org/papers/w25468
- One-line finding: using 100 years of Georgia exemption laws (quadruple-difference design), age-based property-tax exemptions **significantly increase the number of older homeowners** (location + tenure effects) and increase seniors' housing consumption — i.e., senior tax relief works at attracting/retaining seniors but carries a substantial local (school) revenue cost.

## 16. RVC senior owner-occupancy (model assumes 18% of owner homes senior-owned, ~1,404 parcels)
**VERDICT: model figure WRONG — actual is 27.9%.**
- ACS B25007, RVC 2019–2023: owner households with householder 65+: 1,206 (65–74) + 681 (75–84) + 189 (85+) = **2,076 of 7,453 owner households = 27.9%**. 2020–2024: 2,081 of 7,444 = **28.0%**. Source: https://data.census.gov/table/ACSDT5Y2023.B25007?g=1600000US3663264
- The model's 18% / ~1,404 parcels undercounts senior-owned homes by ~48% (true count ≈ 2,076). Within the user's predicted 25–35% band.
- Bonus: 65+ renter householders = 1,205 (2023), so **63.3% of RVC's 65+ householders own**; senior-owner households are 20.7% of all occupied units.

## 17. Effective tax rates: Freeport 2.45% … RVC 2.07% … Garden City 1.85%
**VERDICT: UNVERIFIED — no public source found; cited source contradicts it.**
- No ATTOM/SmartAsset/county publication lists these village-level effective rates or this ordering. The rates appear **derived, not sourced**: $15,230 ÷ $735,000 = 2.072% (claim 18 ÷ claim 7), and Nassau $13,680 ÷ $660,000 = 2.073% — the "2.07%" is circular arithmetic from the other claimed numbers.
- The cited **Ownwell page (https://www.ownwell.com/trends/new-york/nassau-county/rockville-centre, updated Apr 13, 2026) says: median RVC property tax bill $1,465, effective rate 0.22%, median home value (11570) $643,000; Nassau 0.71%, NY state 1.90%.** It does NOT support $15,230 or 2.07%. Ownwell's figures themselves are unreliable here — they appear to capture only the village-levy portion (RVC school+county+town taxes are billed separately; ACS shows RVC median real-estate taxes top-coded at "$10,000+", B25103). Treat Ownwell trends pages as unusable for total Nassau tax bills.
- Magnitude sanity check: a ~2.0–2.1% total effective rate for RVC (~$16K on a ~$790K home) is plausible vs Nassau norms (tax-rates.org: avg 1.79% of market value, stale 2006–2010 base; https://www.tax-rates.org/new_york/nassau_county_property_tax), and the ordering (Freeport/Baldwin high, Garden City lower) matches school-district lore — but the specific list has no verifiable source.

## 18. Avg property tax: RVC $15,230; NYS avg $6,600; US avg $3,500
**VERDICT: RVC UNVERIFIED (plausible); NYS OUTDATED; US OUTDATED/WRONG.**
- RVC $15,230: no public source (ACS median is top-coded "$10,000+"; Ownwell shows $1,465 village-only — see #17). Plausible for total school+county+village tax on a median RVC home, but cannot be verified; the cited source doesn't say it.
- NYS: ACS 2019–2023 **median** real-estate taxes = **$6,450** (B25103); ATTOM **average** = **$7,821 (2024)** / **$7,732 (2025)**. $6,600 ≈ ATTOM's 2021 average ($6,617) — outdated.
- US: ACS 2019–2023 median = **$2,969**; ATTOM average = **$4,300 (2024, +5.8%)** / **$4,427 (2025, +3%; avg home value $494,231; effective rate ~0.86%)**. $3,500 ≈ 2019–2020 ATTOM vintage — outdated by ~$800–900. Sources: https://www.attomdata.com/news/market-trends/home-sales-prices/2024-annual-tax-report/ ; https://www.attomdata.com/news/market-trends/home-sales-prices/2025-annual-tax-report/
- Specify median vs average — the claims mix the two.

## 19. US median home value $345K-ish; NYS $384K; homeownership US 66%, NYS 54%
**VERDICT: US value CLOSE; NYS value OUTDATED; homeownership rates CONFIRMED/CLOSE.**
- US median owner-occupied value (B25077): **$303,400** (2019–2023 5-yr) / **$332,700** (2020–2024 5-yr); the 2023 ACS 1-year was ~$340K, and Zillow's US ZHVI runs ~$360–370K — "$345K-ish" is defensible only against the 1-year ACS.
- NYS: claim $384K = **exactly the 2018–2022 ACS ($384,100) — OUTDATED**. Current: **$403,000** (2019–2023), **$423,800** (2020–2024).
- Homeownership: US **65.0%** (2019–2023 ACS B25003: 82.89M/127.48M) — 66% CLOSE; NYS **54.3%** (4.16M/7.67M) — 54% CONFIRMED.

## 20. Itemizing: RVC 68%, Nassau 62%, NYS 35%, US 13%
**VERDICT: ALL WRONG — these are pre-TCJA-magnitude numbers.**
- IRS SOI zip-code data, **TY2022** (latest; TY2023 file not yet posted as of 2026-06-09), file https://www.irs.gov/pub/irs-soi/22zpallnoagi.csv:
  - **ZIP 11570 (Rockville Centre): 14,290 returns, 3,670 itemized (N04470) = 25.7%** — vs claimed 68%.
  - **New York State: 9,597,940 returns, 995,970 itemized = 10.4%** — vs claimed 35%.
  - **US: 156.16M returns, 15.03M itemized = 9.6%** — vs claimed 13%.
  - Nassau proxy (all ZIPs 11500–11599): 387,130 returns, 76,810 itemized = **19.8%** — Nassau county-wide cannot be near 62%; even its highest-income ZIPs top out around 30–40%.
- Post-2017 TCJA, itemization collapsed (standard deduction doubled, $10K SALT cap). The claimed figures resemble TY2016 (pre-TCJA) levels and must not be used for current-law modeling. Note: the 2025 OBBBA SALT-cap increase ($40K from TY2025) will raise itemization in high-tax ZIPs like 11570 going forward, but nowhere near 68%.

---

## Most important corrections

1. **Senior-owned share of owner-occupied homes is 27.9–28.0% (ACS B25007: ~2,076 households), not the model's 18% (~1,404)** — the calculator undercounts the affected senior parcel base by ~48%, which inflates per-recipient cost estimates and understates program cost.
2. **Itemization rates are wildly wrong (claim 20): real TY2022 shares are 11570: 25.7%, NY: 10.4%, US: 9.6%** (IRS SOI). Any tax-benefit math assuming 68% of RVC filers itemize is off by ~2.6x.
3. **The "Minneapolis Fed 28%/14% large-homes" stat is actually Redfin (Jan 16, 2024: 28.2% vs 14.2%)**; the Minneapolis Fed piece is the separate Horwich article (Nov 14, 2024) on property taxes and affordability — both real, citations must be swapped.
4. **Median home value $735K matches no ACS vintage**: ACS 2019–2023 = $796,100; 2020–2024 = $818,700; Zillow ZHVI (June 2026) ≈ $807–819K; Redfin median sale $555K (co-op/condo-heavy mix). Using $735K understates owner-home values ~8–10%, and the claimed 2.07% effective rate is circularly derived from $15,230/$735K rather than sourced — Ownwell (the cited source) actually shows $1,465/0.22% (village-levy-only, unusable).
5. **Homeownership is 74.5% (not 78%), owner-occupied units 7,453 (not ~7,800)**; RVC 65+ share is 20.1% (not 19.6%); 65+ householder median income is $76,815–$79,722 (not $82K); Nassau pop is ~1.39M (not 1.36M); NYS/US average property taxes are now $7.7–7.8K/$4.3–4.4K (ATTOM 2024–25), not $6.6K/$3.5K.
