---
name: districts-batch1-method
description: Batch-1 districts fan-out (PR #18) — reusable fetch recipes and the gotchas that broke naive versions
metadata:
  type: project
---

Batch-1 of the districts fan-out (13 Nassau districts) shipped as PR #18 (2026-07-20),
files under `.claude/scratch/fanout/batch-1.{json,provenance.md}`. 12/13 fully sourced;
Amityville partial (Suffolk-home, levy+rate are gaps).

**Why:** proves the 5-field per-district recipe end-to-end and records the traps so batch-N
and any districts.json expansion reuse them instead of re-deriving.

**How to apply — the recipes that worked (all keyless, live):**
- **NYSED instid:** `data.nysed.gov/search_schools.php?term=<name>` → JSON; the district row
  is `type==16`. Enrollment: `enrollment.php?year=2025&instid=<id>` (2024-25), `year=2016`
  (2015-16); scrape `K-12 Enrollment: N,NNN`.
- **Census median (B25077):** `data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=<geo>`.
  `api.census.gov` now needs a key; this data.census.gov path does not. **Geo prefix by type:
  unified = `9700000US<geoid>`, ELEMENTARY = `9500000US<geoid>`, secondary = `9600000US`.**
  Using 9700000US on an elementary district returns empty/404.
- **Levy:** OSC `data.ny.gov/resource/iq85-sdzs.json?county=Nassau&school_name=<n>&fiscal_year_ending=2025`.
  Values are strings incl. decimals — parse as float. Sum distinct `swis_code` segments.
- **Parcel rate:** Nassau GIS REST point/buffer query (layer 1) → PARID → LRV `/info/<PARID>`
  (curl `-L -c jar -b jar`, urllib loops on the 303) → POST `/gstaxes.php` {PARID (space-padded),
  TOWN_NAME}. Default response year 2026 = school 2025-26. Class-1 residential = code `210.x`.

**How to apply — the traps (each one broke a naive pass):**
- **ALWAYS district-gate a rate parcel.** Read the LRV `/info` page's *School District* label
  and confirm it names the target BEFORE trusting the rate. A Valley Stream 30 town-center
  seed landed in Elmont UFSD; adjacent elementary districts feed the same CHSD so seeds drift.
  Seed from the TIGERweb district centroid (`tigerweb.geo.census.gov/.../School/MapServer/{0 unified,1 secondary,2 elementary}`, `outSR=4326`).
- **LRV abbreviates district names** and uses `/`,`#` in the label (`E WILLISTON UFSD - 2`,
  `SYOSSET/SYOSSET CSD # 2 - 12`). Match the LRV's own token, and parse the label as the cell
  AFTER "School District" (a `[A-Z...]` regex chokes on `/#`).
- **Component (elementary) districts bill ONE combined `Net School Tax` line** = elementary +
  CHSD, not itemized. So schoolRate = combined burden, but the OSC `levy` is elementary-only
  (CHSD levy is a separate OSC row). Document the scope asymmetry.
- **`libraryRate: 0.0` can be a verified structural absence** (no Net Library Tax line on the
  Class-1 bill; Carle Place, East Williston, Valley Stream 30). Confirm on 2 parcels; it is not
  a fetch miss.
- **Suffolk-home districts (Amityville) are un-sourceable on the Nassau side:** Census TIGER
  puts the whole district in Suffolk, no Nassau parcel resolves to it, yet OSC carries a
  conflicting Nassau levy row. Record only ACS median + NYSED enrollment; gap the rest.

See also [[deploy-verify-gotchas]], [[districts-data-sourcing]], [[districts-batch4-method]].
