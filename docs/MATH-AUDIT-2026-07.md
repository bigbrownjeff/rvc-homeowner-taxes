# Math Audit — July 2026: the $900K-vs-$1.1M question

**Trigger.** Jeff's actual 2025 total property-tax bill only reconciles with the project's model
if his house is worth ~$1.1M, while the county's latest assessment notice puts it near $900K.
This audit diagnoses that gap from the repo's own formulas and newly fetched primary rate data,
and fixes what was wrong. Companion tool: `site/reconcile.html` (bill reconciliation calculator
with built-in verification cases).

**Verdict up front.** Both of Jeff's numbers can be simultaneously true. The "discrepancy" is an
artifact of the model, which computes `total tax = market value × 2.073%`. That constant is
(a) circular and (b) built on a **mislabeled bill**: $15,230 is a real RVC **school + library**
bill, not a total bill. Dividing a real total (~$22.8K) by 2.073% manufactures a "$1.1M home."
Meanwhile the ~$900K from the county is a **different roll year and a different value concept**
than the one his 2025 bills were computed on. Nothing about Jeff's bill is anomalous.

---

## 1. Where valuation enters the repo's math

| Place | Formula / figure | Status after audit |
|---|---|---|
| `site/calculator.html` `EFF_RATE = 0.02073` | `grossPropTax = marketValue × 2.073%` | **Wrong basis** — see §3. Understates a median-home total by ~$4.1K (~19%: $16,978 vs ~$21,083 on an $819K home). Fixed. |
| `site/calculator.html` `COMPONENTS` (school .61 / village .21 / county .12 / town .02 / library .025 / special .015) | splits the (understated) gross | **Wrong for in-village parcels** (county 12% is ~2× too high — in-village parcels don't pay the county police-district line; town is ~0.5%, not 2%). Fixed with verified split. |
| `site/calculator.html` `avgPropTax.rvc = 15230` | "RVC average total property tax" | **Mislabel** — $15,230.09 is the verified 2025-26 school+library bill on a typical in-village parcel (see §2). Actual typical total ≈ $21K. Fixed. |
| `site/fiscal-math.html` + `site/index.html` + deck slide: "≈$4,700/yr un-shifted per §467 parcel (50% tier), on a ~$9.4K school bill" | $9,400 = 62% × $15,230 (assumed total) | **Understated ~55%** — the real typical school-only bill is ≈$14.7K, so the 50%-tier figure is ≈$7,300/yr (range ≈$730–$9,500). Fixed in all three places. |
| `docs/VALIDATION_REPORT.md` / `site/validation.html`: "$15,230 labeled as school tax (it's the total)" | June validation re-labeled the model's cell | **The June "correction" was itself wrong.** The March label (school tax) was right. Corrected on the validation page with an addendum. |
| `docs/BRIEF_2026-08.md` / `site/brief-2026-08.html` | levy/rate aggregates only (+7.2%, +6.6%, $141.3M, 2% cap, STAR $2,058, 0.4%×$820K transfer tax, LOA 0.1% context) | **Unaffected** — every figure checked; none depends on the 2.073% constant or the $15,230 mislabel. No change. |
| `docs/BREAKEVEN_SAMPLE.md` / `site/breakeven.html` | assumed district full value $7B ⚠ | Still an assumption, now bounded: village-only full value ≈ $59.7M ÷ 0.87% ≈ **$6.9B** (ORPTS eq rate), and RVC UFSD extends beyond the village, so district full value > $7B. Flag retained; no numeric change. |

## 2. The primary-source mechanics (all fetched 2026-07-18)

**County roll (school + library + county/town general).**
Nassau is a special assessing unit; school, library, county, town, and special-district taxes are
computed on the **county roll** at Class-1 LOA **0.1%** ("For 2026/27 the Assessor has published
residential properties at a level of assessment of .1%" — [county FAQ](https://www.nassaucountyny.gov/1517/Frequently-Asked-Questions);
ARC residential ratio 0.060%). Verified per-parcel tax tables (Nassau Land Records Viewer):

- **55 Kennedy Ave, RVC (SBL 36/366/150, in-village Class 1)** — [lrv.nassaucountyny.gov/info/36366++00150/](https://lrv.nassaucountyny.gov/info/36366++00150/)
  - Fair Market Value **$741,000 — identical in all four displayed roll years** (frozen roll).
  - Effective Market Value (= AV ÷ 0.1%): 2025 $675K · 2026 $659K · 2027 $610K · 2028-tentative $739K — EMV lags FMV because Class-1 AV can't rise >6%/yr or >20%/5yr (RPTL §1805; Taxpayer Protection Plan notices on the same page).
  - 2025-26 school year, taxable AV 653: **school $2,247.867/​$100 → $14,678.57 · library $84.459/$100 → $551.52 · combined $15,230.09**.
  - 2026 general, in-village district #401: county lines 2.187 + 2.59 + .294 + 20.648 + 95.75 + 2.896 + 64.937 (sewer) + town general 17.095 = **$206.397/$100 → $1,347.77**. No county police-district line (13), no town highway/park/refuse, no fire/sanitary special districts — the village levy funds RVC's own police, sanitation, and roads.
- **413 Rose Ln (SBL 36/503/9, RVC UFSD but OUTSIDE the village)** — [lrv.nassaucountyny.gov/info/36503++00090/](https://lrv.nassaucountyny.gov/info/36503++00090/): same school/library rates; general total **$886.816/$100** (incl. county police 202.017, town lines, S. Hempstead fire 141.794, Sanitary 2 167.897) and no village tax. The calculator's old "county 12% / town 2% / special 1.5%" split resembles this out-of-village profile, not a village resident's.

**Village roll (village tax).**
The Village of RVC assesses its **own roll**: FY26 AV $59,732,924, rate **$69.89**; FY27 AV
$59,388,849, rate **$74.91** per $100 of *village* AV (adopted FY27 budget PDF, p. "Adopted Budget
Summary"; rate = levy ÷ AV × 100 checks exactly: 44,488,056 ÷ 59,388,849 × 100 = 74.91). The
village's level of assessment is its **NYS equalization rate**: **0.87 (2025)**, 0.96 (2024),
0.99 (2023) — NYS ORPTS via [data.ny.gov e6pv-77bh](https://data.ny.gov/resource/e6pv-77bh.json?%24q=ROCKVILLE),
SWIS 282029. So a $900K-market home carries roughly $7,800 of village AV → ≈$5,470/yr village tax
at FY26's rate. Implied village-wide full value: $59.7M ÷ 0.87% ≈ $6.9B.

**STAR.** Post-2015 owners get a **credit check** (2025 final, RVC Class 1: Basic $1,089 /
Enhanced $3,147.01) — the *bill* is unchanged. Pre-2015 exemption holders get an on-bill school
reduction (max $1,068 / $2,856). "Total bill" therefore means bill-before-credit for most buyers
since 2015. (DTF tables, already in `_SOURCES.md`.)

## 3. The diagnosis, proven

The model's only per-household formula is `tax = MV × 2.073%`, where 2.073% = $15,230 ÷ $735,000
(June validation's own finding: "circular"). This audit adds the missing fact: **$15,230.09 is the
actual 2025-26 school+library bill of a $741K-FMV in-village parcel** — a school-only figure, not
a total. The March model labeled it "school tax" (right); the June validation re-labeled it "the
total" (wrong) and the 2.073% "total effective rate" inherited that error.

Real total for the same verified parcel (FY26 village rate, village AV estimated at eq-rate):

| Line | Amount |
|---|---|
| School (AV 653 × 2247.867/100) | $14,678.57 ✓ bill-verified |
| Library (653 × 84.459/100) | $551.52 ✓ bill-verified |
| General county+town (653 × 206.397/100) | $1,347.77 ✓ bill-verified |
| Village (741,000 × 0.87% × 69.89/100) | ≈ $4,505.60 (estimated) |
| **Total** | **≈ $21,083** |

That is **2.85% of its frozen county Fair Market Value** ($741K), **3.23% of its bill-era
taxable EMV** ($653K), or ~2.6% of a current-market estimate — versus the model's flat 2.073%.

**Jeff's numbers.** Back-solving his reported reconciliation: $1.1M × 2.073% ⇒ actual total
≈ **$22,800**. Feed that into the real mechanics (reconcile.html reverse mode, market estimate
$1.05M): village ≈ $6,384; county-roll remainder $16,416 ÷ $25.38723-per-AV ⇒ implied taxable AV
≈ **647**, i.e. bill-era county EMV ≈ **$647K**. So:

- **$647K** — what his 2025 bills were actually computed on (2025/2025-26 county roll EMV, frozen-roll vintage, TPP-capped);
- **~$900K** — the county's newer number (2026/27 final or 2027/28 tentative roll, published Jan 2, 2026 — the same tentative roll where the verified parcel jumped $610K → $739K, +21%, as the county moves values back toward FMV);
- **~$1.1M** — an artifact: his real total divided by a rate that was never a total-bill rate. It lands near a plausible true market value only by coincidence (the fake 2.073% happens to sit near a real total-bill-to-true-market ratio).

**Answer to "which is right":** his bill is right, both county numbers are real but from different
roll years, and the model's 2.073% was the only wrong number in the room. If his AV moves to ~900
when the 2027/28 tentative roll becomes taxable, the same rates would imply a school+library+
general bill of ≈$22.8K *before* the village line — a ~30% jump absent rate compression (rates
recompute downward when the base rises; levies, not rates, are what districts actually set).

## 4. What Jeff should paste to confirm to the penny

From his bills (all appear on two bills + the village bill, or at lrv.nassaucountyny.gov → his
parcel → "General and School Taxes"):

1. 2025-26 **school bill**: taxable value + school and library line amounts;
2. 2026 **general bill**: taxable value + total;
3. 2025-26 **village bill**: village assessed value + amount;
4. the **$900K notice**: which roll year it names (2026/27 final vs 2027/28 tentative) and whether it says Fair Market Value or Effective/Tentative Assessed Value.

Enter (1)–(3) in `site/reconcile.html`; the forward mode should match each line to the penny
(village line exactly, once his real village AV is entered). Any residual ⇒ an exemption line we
haven't modeled — visible on the same LRV tax tab.

## 5. Fixes shipped with this audit

- `site/reconcile.html` — new reconciliation calculator (forward + back-solve modes, 2 built-in verification cases asserted on load).
- `site/calculator.html` — `EFF_RATE` 0.02073 → **0.0257** (= verified $21,083 total ÷ current-market $819K ACS/Zillow median; comment explains basis + pointer to reconcile.html); `COMPONENTS` → verified in-village split (school .696 / village .214 / county .059 / library .026 / town .005); `avgPropTax.rvc` 15230 → 21100 (labeled estimate); prose "2.07%" → "≈2.6%"; comparison-chart RVC point updated; link to reconcile.html added.
- `site/index.html` §467 card: ≈$4,700/yr → **≈$7,300/yr** (50% tier on the verified ≈$14.7K school bill; range ≈$730–$9,500); source note now cites the verified parcel instead of "(assumption)".
- `site/fiscal-math.html`: same correction in body + pull-number + summary list.
- `tools/build_deck_pptx.py` + regenerated `site/RVC_Legislator_Deck.pptx`: deck card ≈$4,700 → ≈$7,300.
- `site/validation.html`: addendum row correcting the June pass's own $15,230 re-label (correction-of-the-correction, dated).
- `docs/_SOURCES.md`: new receipts (LRV parcel tax tables, ORPTS equalization rates, FY27 budget AV line).
- `DEPLOY.md`: reconcile.html added to the served-paths table.

**Unchanged because unaffected:** `brief-2026-08` (md + html) — all levy/rate aggregates,
re-checked line by line; breakeven (assumption already ⚠-flagged, now bounded); governance,
redraw-evidence, voices pages (no valuation math).

**Reproducibility scope note.** The Nassau LRV parcel tax tables are reCaptcha-gated (address/SBL
search) and render via JavaScript; the primary rates cited here ($2,247.867 / $84.459 / $206.397
in-village / $886.816 out-of-village per $100 AV) were verified in-session via a real browser on
2026-07-18 but could not be independently re-fetched by the PR reviewer through plain HTTP. The
direct parcel URLs above load in any normal browser. **Jeff pasting his own bill components (§4)
remains the to-the-penny confirmation.**

*Prepared 2026-07-18 · branch `fix/math-audit-2026-07` · all rates fetched same-day.*
