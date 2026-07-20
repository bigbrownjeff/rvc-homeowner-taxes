---
name: districts-data-sourcing
description: Working keyless endpoints + gotchas for per-district Nassau data (verified 2026-07-20, L1 pilot PR #11); full recipe in .claude/scratch/districts-provenance.md on the pilot branch
metadata:
  type: project
---

L1 pilot (PR #11) proved every per-district datum is fetchable keyless. The full
per-field recipe lives in `.claude/scratch/districts-provenance.md` (committed on
`feature/districts-data-pilot`); these are the gotchas worth never re-deriving:

**Why:** the fan-out across ~52 remaining districts reuses these exact paths; each
was nontrivial to find. **How to apply:** follow the provenance file's method notes;
below are the traps.

- **api.census.gov now requires an API key** (rejected 2026-07-20). Keyless
  primary-issuer path: `https://data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=<geo>`
  — geo `160XX00US<placeFIPS>` or `9700000US<USD geoid>`. ACS 2020-24 is current.
- **Nassau LRV without reCaptcha:** parcel page 303s to itself to set a cookie
  (`curl -L -c jar -b jar`); the tax table comes from `POST /gstaxes.php` with
  space-padded `PARID` + `TOWN_NAME`. Default year 2026 = school 2025-26. Discover
  parcel SBLs via county GIS REST `gis.nassaucountyny.gov/server/rest/services/Layers/MapServer/1/query`
  (point+distance, inSR=4326, outFields=PARID,PARCEL_ADDRESS). Pick class 210.01
  single-family parcels as representatives.
- **Levy:** OSC Socrata `data.ny.gov/resource/iq85-sdzs.json` (keyless),
  `fiscal_year_ending=2025` = 2024-25. Multi-municipality districts: sum DISTINCT
  segments — the city-roll segment can appear twice under two labels (Long Beach:
  $84.06M city + $25.02M Hempstead = $109.08M, matches the adopted $109.1M).
- **NYSED enrollment is server-rendered:** grep `K-12 Enrollment: N,NNN` at
  `data.nysed.gov/enrollment.php?year=YYYY&instid=NNN`. instids: LB 800000049221,
  LV 800000048920 (RVC 800000049383 in ledger).
- **DTF STAR quirks:** Glen Cove uses Homestead/`H` class codes, not `1`; the
  max-savings page has typo "Floral Park-Bellrose"; Amityville + Cold Spring Harbor
  max savings live on the SUFFOLK page (sd52) — omitted by scope decision.
- **District keying trap:** Nassau has 3 secondary CHSDs (Bellmore-Merrick,
  Sewanhaka, Valley Stream CHSD) + 11 elementary districts in TIGER layers 1/2, NOT
  the unified layer. The geocoder's "unified school" pick() will not resolve those
  addresses — L2 must also read elementary/secondary layers. TIGERweb
  `School/MapServer` layers 0/2/1 give NAME+GEOID; all 55 DTF names matched.
- **Long Beach city-roll rate is the open archetype gap:** the city assesses its
  own roll; LRV only covers the county-roll (Lido Beach/Point Lookout) portion.

**Batch-2 additions (PR #15, 13 districts, 2026-07-20 — all completed, none gapped):**
- **NYSED instid lookup (was manual):** `data.nysed.gov/lists.php?type=district`
  paginates by `start=<ASCII letter>` (A=65, B=66 …); rows are `instid=NNN">NAME`.
- **Per-parcel district gate (new, use always):** the LRV `/info/<PARID>/` page
  exposes the school district SERVER-SIDE — grep `School District` → e.g.
  `FREEPORT - 9` + `NYS SWIS Code`. GIS layer 1 has NO district field, so validate
  every GIS-found parcel this way before trusting its rate. LRV names differ from
  Census: North Bellmore prints **`N BELLMORE UFSD`** (abbreviated).
- **STAR cross-check:** a parcel's `STAR Savings` line == the district's
  `starExemptSavings` in districts.json (independent confirm of correct district).
- **Elementary districts bill ONE combined school line:** Elmont (Sewanhaka) &
  North Bellmore (Bellmore-Merrick) show a single `Net School Tax` = elementary +
  CHSD combined, NOT separable at parcel level; their OSC levy is elementary-only.
  Census median for elementary districts uses geo prefix `9500000US` (not 9700000US).
- **Some districts have NO library line** on the school bill (Hempstead, Roosevelt,
  Uniondale) — omit libraryRate, it's a structural absence not a fetch miss.
- **Cold Spring Harbor** (Suffolk-home): a Nassau-side parcel exists in Laurel
  Hollow (Town of Oyster Bay) = valid Nassau-roll rate; Suffolk roll out of scope;
  levy is both-county segment sum. Query OSC WITHOUT a county filter for it.
