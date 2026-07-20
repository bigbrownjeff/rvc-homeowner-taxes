---
name: districts-integration
description: districts.json is now a full 55-row table (PR #20); enhStar field-naming discipline; the north-star column stays empty by design
metadata:
  type: project
---

The 4-batch Nassau district fan-out was integrated into `site/assets/districts.json` (PR #20, 2026-07-20). The file is no longer stub-heavy: all 55 DTF-listed districts carry full rows except two documented rate/levy scope-gaps.

**Fact:** every DTF-named row now has median/levy/schoolRate/enrollment/board_url + STAR trio + `enhStarExemptParcels`, each with a `source_ref`. Coverage.html computes 81% overall.

**Why (field-naming trap):** coverage.html's north-star scorer keys on `r.enhStarParcels` — a field NO row carries. The rows carry `enhStarExemptParcels` (the aa3i-eamx Enhanced-STAR EXEMPTION-program count, 2025 levy year, legacy path only). These names MUST stay distinct: the exemption count is not the §467 parcel count Ask #3 seeks, so it must not light the north-star column. A protective code comment now guards the scorer.

**How to apply:** if a future task asks to "light the north-star column" or "fix the enhStar field name," STOP — that column is intentionally empty until credit-recipient counts land (FOIL/derivation pending). The 395-for-RVC figure is the exemption-program subset, never an exemption-gap total.

**Two scope-gap rows** (not stubs, deliberately partial): Amityville (Suffolk home county — no Nassau parcel rate, conflicting levy omitted) and Glen Cove (city assessment roll — county LRV returns no school lines, same as Long Beach pilot). Both documented in `_meta.notes`.

**Structural library absence:** 16 districts show no Net Library Tax line on the sampled parcel; numeric `libraryRate` omitted, `libraryRateNote` records it. This is verified absence (library funded off the school bill), not a fetch miss.

**Tooling gap:** `scripts/e2e-acceptance.py` needs playwright (not installed anywhere) and has a hardcoded ROOT to a sibling worktree. Verified Elmont geo-swap in node against the real `lookupDistrict` instead. See [[deploy-verify-gotchas]] (headless Chrome hangs on live Google-Fonts pages).
