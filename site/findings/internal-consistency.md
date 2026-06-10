# Internal Consistency Audit — RVC Homeowner Taxes Project
_Cross-checks among the three artifacts only (Action Plan .docx, Financial Model .xlsx, Tax Calculator .html). No external sources used here; external verdicts live in the sibling findings files._

## A. Cross-document numeric contradictions

| # | Item | Plan (.docx) | Model (.xlsx) | Calculator (.html) | Note |
|---|------|--------------|---------------|--------------------|------|
| A1 | Senior exempt parcels | 1,404 (scenarios: 140/281/421/562/702) | 1,405 = ROUND(7,808×.18) (141/281/422/562/703) | — | Sensitivity sheet base case says **1,342** — a third number |
| A2 | District budget | "~$135M" (exec summary) AND $139.89M | $139.89M | $139.89M | $135M appears only in exec summary/key table; all math uses $139.89M |
| A3 | Per-pupil | $42,050 | **$42,060** = 139.89M/3,326 | $42,050 shown, chart=42050; metric caption says "=139.89M÷3,326" which is $42,059.53 | Transcription drift |
| A4 | Enhanced STAR savings | $2,680 | B40=$2,680 but B43 note says "STAR **$2,856**"; Deep Dive uses $2,856 | STAR const = 2,680 | Two values used in same workbook |
| A5 | Basic STAR savings | $1,220 | B41=$1,220; Deep Dive uses **$1,068** | 1,220 | Same conflict |
| A6 | Avg combined savings/parcel | $4,900 ($2,680+~$2,200) | B43=$4,900, but its own note "$2,856+$2,600" sums to **$5,456** | — | Note ≠ value; sensitivity base case says **$5,500** |
| A7 | Effective senior school tax | **~$4,563** (9,443−2,680−2,200) | **$10,330** (B44=15,230−4,900) | — | 2.3× apart. Root cause: model B42 labels the **total** tax ($15,230) as "Avg School Tax" |
| A8 | §467 max-tier savings | "~$2,200 school + ~$2,700 other" | Deep Dive: **$7,750 total** at 50% | — | Three irreconcilable §467 quantifications; see C3 |
| A9 | Transfer tax @10% | $412K (implies $735K avg price) | $394.8K (uses $700K×0.4%) | — | Exec summary says "$410K–$2.1M"; sensitivity base = $700K |
| A10 | New total enrollment @10% | 3,456 (base 3,260 = 2026-27 proj.) | 3,523 (base 3,326 = 2025-26) | — | Different enrollment bases for the same scenario |
| A11 | New school-tax revenue @10% | $688K exec summary / $686K implied (140×4,900) | $690.9K (141×4,900) | — | Three near-values for one number |
| A12 | Reserves arithmetic | "$8M (8% of budget)" | same | "~$8M"; separately "$4.8M unappropriated (3.5%) + ~$4.2M retirement reserves" | $8M is **5.7%** of $139.89M, not 8%. $4.8M+$4.2M=$9.0M≠$8M. Also ERS/TRS reserves are *restricted* — calling the bundle "unrestricted" is wrong |
| A13 | "1% growth" | "total revenues may grow only ~1% ($1.4M)" | — | "only 1% growth **in state aid**" | Different denominators; $1.4M≈1% of total budget, so the calculator's "state aid" phrasing is wrong |
| A14 | Capacity cost timing | "Up to ~20% (~393 students) near-zero marginal cost" | charges $525K already at 20% (B36: >288 students × $5,000) | — | Plan and model disagree at the margin |
| A15 | Marginal cost per student | "near $0" up to capacity | $5,000 **one-time** (A36) vs $12,000/yr in ratio row (B41) vs $8–18K in sensitivity | — | Three different marginal-cost concepts, never reconciled |
| A16 | Levy-cap 2026-27 | "2.1% (MaryBeth Joyce)" | $111,911,163 = "**2.45%** increase (LI Herald)" | "~2.1%" | 109.24M→111.91M is +2.445%; one of the two is wrong |

## B. Formula/label defects in the .xlsx (cosmetic but should be fixed)
- D11 note "Calc: B11*B10" → should read B9×B10.
- D36 note "Calc: B35+8400" → should read B34+8400 (B35 is a text cell).
- **B42 label "Avg School Tax on Median Home (no exemptions)" holds $15,230 — the TOTAL tax.** School-only is ~$9,443 (62%). Every downstream "effective senior school tax" figure inherits this error.
- D44 note "Calc: B43-B44" is self-referential; should be B42−B43. B45 note "Calc: B44" should be "=B43".
- B42's own note bases $15,230 on "$109M levy / ~7,000 parcels" = $15.6K — close to $15,230 only by coincidence; levy÷parcels would be a *school* tax estimate, yet the number equals the claimed *total* bill. Confused provenance.
- Deep Dive "Est. Assessed Value Reduction" column ($362,500 at 50%) treats AV ≈ ½ market value. Nassau Class 1 level of assessment is 0.1% — AV of a $735K home is ≈ $735, not $362,500-of-$725,000. The dollar-savings column only works if the % is applied to the *tax*, not to any real AV; the AV column is fiction either way.
- Deep Dive tier labels "Option 1/2/3 tier" are invented; RPTL §467 sliding-scale options are not structured that way.

## C. Conceptual errors (the load-bearing ones)

**C1. Levy mechanics — the central framing error.** NY school districts levy a fixed dollar amount; the rate is levy ÷ taxable AV. Exemptions (§467) remove AV from the base and therefore *shift* tax onto non-exempt taxpayers — the district still collects 100% of its levy. The headline "$6.9M annual revenue gap … nearly double the deficit" and all "recaptured school tax revenue" rows describe **taxpayer burden relief, not new district revenue**. Senior turnover does not add a dollar to the levy (which is capped); it lowers everyone else's rate. The deficit-coverage row (18%–91%) is therefore category-confused: this money cannot close a budget gap.

**C2. STAR is state-funded.** The STAR exemption is reimbursed to districts by NYS; post-2015 buyers get a state-paid credit check. Enhanced STAR savings ($2,680) belong in *no* district-revenue calculation. When a senior (Enhanced) sells to a family (Basic credit), the saver is **New York State** (~$1,400/parcel), not RVC UFSD. Likewise "STAR Credit Modernization … shifts $2,680/parcel from local burden to state" is wrong — the exemption is already state-funded; conversion changes plumbing (and lets the benefit grow 2%/yr), not local burden.

**C3. §467 participation overcount / double counting.** 1,404 = 18% × owner-occupied units = an estimate of *senior-owned* parcels, not §467-*exempt* parcels. §467 is income-tested (ceiling ≈ $58.4K under the max sliding scale — see exemptions findings) while the project's own senior median income is **$82,000** — i.e., the median senior homeowner doesn't qualify at all. Yet the model multiplies all 1,404 parcels by a $4,900 average that embeds mid-tier §467 + full Enhanced STAR. Model note #2 concedes "~75% receive some level" but the math never applies that haircut, and 75% is itself unsupported. Actual counts are knowable (assessment-roll exemption data; the plan's own FOIL request) — until then $6.9M is an extrapolation stacked on two unverified assumptions, and it is near-certainly overstated by 2–4×.

**C4. "Prop 19-style portability" does not map onto NY.** California needs portability because Prop 13 taxes acquisition value; selling re-bases you upward. New York taxes current assessed value with **no acquisition basis** — a Nassau buyer inherits the parcel's existing AV (sales do not trigger reassessment; the county roll has been frozen for years). A NY senior who downsizes to a cheaper home automatically pays less; there is no "tax base" to port. The Level-2 centerpiece ask is therefore a solution to a problem NY doesn't have. The *real* NY-native levers: §467/Enhanced STAR continuity across moves (they already largely port), senior school-tax **deferral** enabling law (pay at sale), transfer-tax relief for downsizers, capital-gains relief (federal), and downsizing housing supply. Related plan claim "loss of §467/STAR benefits upon moving" is mostly false — Enhanced STAR follows the owner to any NY primary residence; §467 persists where the destination jurisdiction adopted it.

**C5. Marginal-cost story is self-contradicting.** The model's own "Revenue-to-Marginal-Cost Ratio" row says recaptured revenue is **0.3×** the cost of the new students it adds ($3,500 vs $12,000) — flatly contradicting the plan's "nearly pure upside" framing. Meanwhile "288 seats of spare capacity" equates a decade's enrollment decline with building capacity (no capacity study cited), and per-pupil-spending improvements in the model come purely from denominator growth while costs are held flat — i.e., the model quietly assumes ~$0 marginal cost in one row and $12K in another. The defensible argument is utilization + enrollment-linked aid + vote sustainability, not per-student profit.

**C6. Misc.** (a) "61% enrollment decline" phrasing in one spot reads as a 61% drop rather than 61% of districts declining. (b) "Each tier reduction removes ~20–40 parcels" — no source, pure guess. (c) "$15K+ annual local retail spending per family" — assumption presented as Chamber-ready fact. (d) Calculator lets any income select Enhanced STAR (no $110,750 gate) and applies flat max savings at every home value. (e) Calculator hardcodes the 2025 OBBBA SALT cap ($40K) for all years — 2026 cap is $40,400 and the page is being shipped in 2026. (f) NYS per-pupil card says "$36,293 … 91% above national avg" and two lines later "132% premium vs $15,633" — mixed vintages, both can't be true.

## D. Where the artifacts AGREE and are internally coherent
- $15,230 total tax on $735K = 2.072% ✓; 62% school share → $9,443 ✓; village/county recapture rows ($1,800/$900) ≈ 50% of the village (18%) and county (12%) bill shares ✓ arithmetic.
- Deficit-coverage percentages match the model's own outputs ✓ (the inputs, not the arithmetic, are the problem).
- 10-parcel pilot math (10×$4,900 + 10×$2,700 = $76K) consistent with model constants ✓.
- Plan's lock-in total ($2,680+$2,200+$2,700 = $7,580; $15,230−$7,580 = $7,650 effective) is internally consistent ✓ — but inherits the unsupported $2,200 §467-school figure.
