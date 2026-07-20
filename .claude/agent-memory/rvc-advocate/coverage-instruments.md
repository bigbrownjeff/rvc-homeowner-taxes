---
name: coverage-instruments
description: coverage.html matrix + campaign instruments + count-only endpoint (PR #14, 2026-07-20); north-star Enhanced-STAR parcel-count sourcing finding
metadata:
  type: project
---

Built `site/coverage.html` (live Harvey-ball matrix over districts.json), the
campaign-instruments band, and a count-only engagement endpoint. Shipped as PR #14
(`feature/coverage-instruments`), NOT merged.

**Why:** coverage layer for the Nassau address feature; §8/§9 of
`.claude/scratch/nassau-address-feature-plan.md`. **How to apply:**

- **North-star sourcing finding (the key verification):** DTF publishes Enhanced-STAR
  **exemption-program** recipient counts by school district at `data.ny.gov` resource
  **`aa3i-eamx`** (col `number_of_enhanced_exemptions`, filter `school_district_name`;
  RVC = 395 for levy_year 2025, 416/2024, 428/2023 — a visibly shrinking legacy pool).
  This is NOT the full Enhanced-STAR parcel count: post-2016 enrollees get a CREDIT
  check, not an exemption, and credit-recipient counts by district are NOT cleanly
  published (dataset `jajz-mu5n` has credit AMOUNTS/tax-class, not per-district counts).
  So the true north-star per-district parcel count needs the credit portion added =
  derivation or FOIL, still pending. Also distinct from the §467 count (different
  program, FOIL-gated, Ask #3). Coverage north-star column stays EMPTY/pending for all
  districts until districts.json gains a sourced `enhStarParcels` field; the finding is
  documented in ledger row `#f-nassau-parcels`, not fabricated into a complete cell.
- **Matrix design:** cells DERIVE state from field presence + `hasRef()` (source_ref
  url resolves). 8 dims: resolution, star (3-part → Amityville/Cold Spring Harbor score
  0.67 partial, their 2026-27 max lives on the Suffolk DTF page), starParcels★, levy,
  rate, value, enrollment, officials (county_leg + board_url /2). Verified live: 55
  rows, overall 28%, RVC 88%, pilots ~81-88% (north-star pending caps everyone < 100%).
  `window.COVERAGE_SUMMARY` exports for a later sourcing agent.
- **Count-only endpoint (`_worker.js`):** `POST /api/count {event:lookup|letter}` +
  `GET /api/count` → `{lookup,letter,signup}`. Reuses SIGNUPS KV with `count:<event>`
  integer keys, read-modify-write (no atomic incr; a lost race under-counts by one,
  never leaks). `/api/signup` bumps `count:signup` only on a NEW email. Aggregate ints
  only, no addresses/PII/IP. index.html fires `pingCount()` (fire-and-forget, keepalive)
  on resolve + on letter copy. On a plain http.server the POST 501s / GET 404s and the
  band shows "—" gracefully — expected in static preview.
- **instruments-manual.json** (`site/assets/`): hand-maintained pillar-(b) counters Jeff
  edits (hr1340 cosponsors 146, committee posture, office_replies/walkthroughs at 0).
- Worker unit-tested with a mock KV Map via `node /tmp/worker_test.mjs` (import the
  `export default`, fake `env.SIGNUPS.get/put`). Good pattern for testing the worker
  without wrangler dev.
