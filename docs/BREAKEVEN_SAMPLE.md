# Break-even sample calculation — what "no more cuts" requires
_Worked example behind `site/breakeven.html` and deck slide 12. Illustrative: assumption-flagged inputs are marked ⚠; everything else is validated (see VALIDATION_REPORT.md)._

## The identity

Holding services constant, the budget balances without cuts or overrides iff revenue growth ≥ cost growth:

```
cost_growth ≤ w_levy × (cap + δ) + w_aid × aid_growth + w_other × other_growth
```

where **δ** is the tax-base growth factor — the DTF "quantity change": physical additions to taxable full value (construction, renovations, new units), never price appreciation. δ is the only lawful way the levy grows faster than the cap without a 60% override.

## Validated inputs (2025-26 / 2026-27)

| Input | Value | Source |
|---|---|---|
| Budget base | $141.32M (2026-27 adopted) | LI Herald Apr 2026 |
| Revenue mix | levy 78% ($109.24M/$139.89M) · aid ~15% · other ~7% | district budget / LI Herald |
| Cap | 2.0% (2026-27 final ≈2.1%) | OSC / LI Herald |
| Aid growth | ~1%/yr | district, Mar 2026 |
| Other growth | ~0 (held flat) | assumption ⚠ |

## Worked example at 3% cost growth

Cost growth of 3%/yr is the conservative shape of the documented drivers (health insurance +10% on ~$20M ≈ +$2M ≈ +1.4% of budget by itself; out-of-district special-ed placements +71% to $6.38M).

- **Autopilot revenue growth** (δ = 0): 0.78×2% + 0.15×1% = **1.71%/yr**
- **Structural gap**: (3% − 1.71%) × $141.3M ≈ **$1.8M/yr** — consistent with lived history: the 2025-26 and 2026-27 budgets grew just +1.63% and +1.03%, balancing the identity with ~62 position cuts.
- **δ required to close in-cap**: 1.29% ÷ 0.78 ≈ **1.65%/yr of physical base growth**
- **Construction that implies**: 1.65% × district full value. Full value is not yet pulled from DTF ⚠ — at an assumed **$7B**, δ requires ≈ **$115M/yr** of renovations + new construction.

## What the housing dials deliver against that

| Dial | Setting (⚠ assumptions) | Physical value added /yr |
|---|---|---|
| Senior→family transitions | 100/yr × $150K renovation | ~$15M (≈13% of requirement) |
| New units (ADU/condo) | 20/yr × $600K | ~$12M (≈10%) |
| **Housing dials combined** | | **~$27M ≈ 23%** |

**Conclusion the numbers force:** turnover is necessary and meaningfully helpful — and nowhere near sufficient alone. The remaining ~77% balances only through some mix of (a) more new units, (b) enrollment-linked aid growth (turnover helps here too — students drive aid), (c) cost-line discipline, or (d) the overrides/cuts the village is currently living. It is a **four-dial problem by construction**, which is the argument for pulling all four levers at once rather than litigating any one of them.

Sensitivity worth knowing: every 0.5pt of cost growth moves the gap by ~$0.7M/yr; every $1B of actual full value moves the required-construction figure by ~$16.5M/yr at 3% cost growth.

## Data that converts this from illustration to instrument

1. **DTF school-district full value** for RVC UFSD (replaces the $7B ⚠).
2. **§467 / Enhanced STAR counts + exempted AV by district** (Nassau Assessment; FOIL drafted) — sizes the eligible-senior pool and the burden shift.
3. **District facilities/capacity study** — converts the ~7% enrollment decline into absorbable seats and a marginal-cost curve.
4. Renovation-at-resale evidence (permits pulled within 24 months of arm's-length Class 1 sales, Nassau) — replaces the $150K ⚠.
