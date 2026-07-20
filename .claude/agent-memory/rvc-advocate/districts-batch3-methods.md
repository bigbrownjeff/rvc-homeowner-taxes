---
name: districts-batch3-methods
description: Reusable live-fetch recipes for Nassau per-district data (Census/NYSED/OSC/LRV) confirmed in batch-3 fan-out
metadata:
  type: reference
---

Batch-3 of the district fan-out (PR #19, 2026-07-20) confirmed/extended these keyless
live-fetch recipes for `districts.json`-style per-district rows. See
[[districts-data-sourcing]] for the pilot L1 notes.

- **Census B25077 median** — `data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=<PRE><geoid>`.
  Prefix is type-dependent: `9700000US` for UNIFIED, **`9500000US` for ELEMENTARY**
  districts. Wrong prefix returns empty/non-JSON (silent null). Secondary districts use `9600000US`.
- **NYSED instid** — reliable lookup is the autocomplete `data.nysed.gov/search_schools.php?term=<name>`
  (JSON; district row is `"type":"16"`). The paginated `lists.php?type=district&start=N`
  is unreliable: `start` is not a clean page index for small ints. Enrollment string is
  `K-12 Enrollment: N,NNN` even for K-6 elementary districts.
- **LRV rate HARD GATE** (batch-2 method, essential): GIS layer 1 has no school-district
  field, so parse the LRV `/info/<PARID>/` page's server-side `School District <NAME> - <n>`
  label and require it to equal the target after normalizing LRV abbreviations
  (`N MERRICK UFSD`, `W HEMPSTEAD UFSD`, `VALLEY STREAM UFSD 13`). Then confirm with a
  STAR-verified single-family parcel whose STAR Savings matches the DTF exemption to the cent.
- **Record the STAR parcel's OWN rate, not a modal rate.** Village-center geocodes surface
  co-op/condo (Class 2) and commercial (Class 4) parcels with different, lower per-$100
  rates on the same roll (Garden City 273.712, Lynbrook 515.558 were Class-4 traps; the
  Class-1 residential rates are 1411.338 and 2174.389).
- **Elementary districts (Bellmore-Merrick CHSD, Valley Stream CHSD):** LRV consolidates
  elementary + CHSD into ONE `Net School Tax` line, not separable at parcel level →
  schoolRate is the combined rate; OSC levy is elementary-only.
- **Missing `Net Library Tax` line = structural absence, not a fetch miss** (Garden City,
  Herricks, Lynbrook, Valley Stream 13) → libraryRate null + note.
- **Nominatim rate-limits/403s** after ~12 calls; fall back to the Census onelineaddress
  geocoder for seed points.
- **Honest finding:** enrollment is NOT uniformly declining across Nassau — East Meadow
  +10.7%, Herricks +9.4%, Merrick +8.6% grew 2015-16→2024-25; state direction per district.
