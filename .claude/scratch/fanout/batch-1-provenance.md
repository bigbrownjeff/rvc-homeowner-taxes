# districts.json provenance — batch-1 fan-out (verified 2026-07-20)

Per-field fetch log for the 13 batch-1 Nassau school districts. Mirrors the L1 pilot
method in `.claude/scratch/districts-provenance.md`. Every value was read from a LIVE
fetch on 2026-07-20. Fields sourced: **medianValue** (ACS B25077, school-district geography),
**enrollment** cur/base (NYSED per instid), **levy** (OSC iq85-sdzs FY2025), **schoolRate +
libraryRate** (Nassau GIS REST parcel -> LRV /info -> gstaxes POST, tax year 2026 = school
2025-26), **board_url** (probed 200). STAR fields are unchanged from the existing stub rows
(not re-verified today). county_leg skipped (officials lane).

## Method upgrades applied (from the batch-2 lessons + pilot)

- **In-district HARD GATE on every rate.** Before trusting any parcel rate, the LRV
  `/info/<PARID>` page's *School District* label was confirmed to name the target district.
  This caught two errors: a Valley Stream 30 seed that landed in **Elmont UFSD**, and East
  Williston parcels labeled **`E WILLISTON UFSD - 2`** (LRV abbreviates; an exact-name match
  would have wrongly gapped the district). Syosset's label is `SYOSSET/SYOSSET CSD # 2 - 12`
  (contains `/` and `#`, so the gate parses the value cell, not a regex).
- **Census summary level 950 for elementary districts.** Franklin Square, New Hyde
  Park-Garden City Park, and Valley Stream 30 resolve under `9500000US<geoid>`, not the
  unified `9700000US` prefix (which 404s the table for them).
- **Combined school line for component districts.** On the Nassau county bill the elementary
  district and its central high school district (CHSD) are billed as ONE `Net School Tax`
  line. The logged schoolRate for the 3 elementary districts is therefore the *combined
  elementary + CHSD* rate (the homeowner's actual school burden); it is NOT itemized. Their
  OSC `levy`, by contrast, is the elementary district's own levy only (CHSD levy separate).
- **libraryRate 0.0 = verified structural absence.** Several districts (Carle Place, East
  Williston, Lawrence*, Valley Stream 30) show no `Net Library Tax` line on the Class-1 bill,
  confirmed on two parcels each. That is a real omission, not a fetch miss. (*Lawrence DOES
  have a library line 36.015; listed here are the genuinely absent ones.)
- **NYSED instid discovery:** `data.nysed.gov/search_schools.php?term=<name>` returns JSON;
  the district row is `type==16`. All 13 resolved to a single unambiguous match.

## Per-district figures

| District | median (geo) | enroll cur/base | levy FY25 | schoolRate | libraryRate | board_url |
|---|---|---|---|---|---|---|
| Amityville (unif) | $514,100 `9700000US36` | 2,678/2,986 | GAP | GAP | GAP | https://www.amityvilleschools.org/ |
| Carle Place (unif) | $727,700 `9700000US36` | 1,306/1,370 | $46,850,434 | 1765.269 | absent(0) | https://www.cps.k12.ny.us/ |
| East Williston (unif) | $1,187,000 `9700000US36` | 1,571/1,711 | $61,374,159 | 1838.915 | absent(0) | https://www.ewsdonline.org/ |
| Franklin Square (elem) | $675,500 `9500000US36` | 1,738/1,857 | $64,139,154 | 1133.01 | 50.021 | https://www.franklinsquare.k12.ny.us/ |
| Great Neck (unif) | $1,001,500 `9700000US36` | 6,600/6,394 | $236,985,206 | 1355.724 | 58.151 | https://www.greatneck.k12.ny.us/ |
| Hicksville (unif) | $624,600 `9700000US36` | 5,286/5,230 | $115,533,074 | 1406.8 | 62.657 | https://www.hicksvillepublicschools.org/ |
| Lawrence (unif) | $933,200 `9700000US36` | 2,155/2,645 | $85,954,300 | 887.273 | 36.015 | https://www.lawrence.org/ |
| Manhasset (unif) | $1,781,100 `9700000US36` | 3,007/3,329 | $99,748,822 | 1083.777 | 62.92 | https://www.manhassetschools.org/ |
| New Hyde Park-Garden City (elem) | $757,800 `9500000US36` | 1,419/1,678 | $76,279,549 | 1549.988 | 59.028 | https://www.nhp-gcp.org/ |
| Oceanside (unif) | $641,500 `9700000US36` | 5,179/5,578 | $130,349,860 | 1877.382 | 115.483 | https://www.oceansideschools.org/ |
| Port Washington (unif) | $1,053,000 `9700000US36` | 5,231/5,283 | $161,546,663 | 1621.518 | 72.866 | https://www.portnet.org/ |
| Syosset (unif) | $934,600 `9700000US36` | 6,980/6,247 | $226,511,537 | 2296.55 | 82.423 | https://www.syossetschools.org/ |
| Valley Stream 30 (elem) | $617,500 `9500000US36` | 1,348/1,537 | $52,023,322 | 1704.851 | absent(0) | https://www.valleystream30.com/ |

All figures carry a full `source_ref {url, vintage, verified}` in batch-1.json.

## Representative rate parcels (all Class-1 210.x, in-district gate-confirmed, tax yr 2026)

- **Amityville**: rate GAP (see below)
- **Carle Place**: tax year 2026 (school 2025-26); parcel 316 GLEN COVE AVE CARLE PLACE 11514 (10012  00010), Class 1 code 210.01, LRV school district 'CARLE PLACE UFSD - 11'; Net School Tax rate 1765.269, no Net Library Tax line (structural absence, verified) per $100 AV; rate-consistency cross-check: parcel 315 ROSLYN AVE CARLE PLACE 11514 (10012  00070) shows identical school rate
- **East Williston**: tax year 2026 (school 2025-26); parcel 206 GLENMORE ST EAST WILLISTON 11596 (09214  02560), Class 1 code 210.01, LRV school district 'E WILLISTON UFSD - 2'; Net School Tax rate 1838.915, no Net Library Tax line (structural absence, verified) per $100 AV; rate-consistency cross-check: parcel 214 GLENMORE ST EAST WILLISTON 11596 (09214  02650) shows identical school rate
- **Franklin Square**: tax year 2026 (school 2025-26); parcel 246 JEFFERSON ST FRANKLIN SQUARE 11010 (35126  01510), Class 1 code 210.01, LRV school district 'FRANKLIN SQUARE UFSD - 17'; Net School Tax rate 1133.01, Net Library 50.021 per $100 AV | single combined Net School Tax line = elementary + CHSD combined (not itemized on the county bill); rate-consistency cross-check: parcel 218 JEFFERSON ST FRANKLIN SQUARE 11010 (35126  01650) shows identical school rate
- **Great Neck**: tax year 2026 (school 2025-26); parcel 43 MAPLE DR GREAT NECK 11021 (02038  01640), Class 1 code 210.01, LRV school district 'GREAT NECK UFSD - 7'; Net School Tax rate 1355.724, Net Library 58.151 per $100 AV; rate-consistency cross-check: parcel 41 MAPLE DR GREAT NECK 11021 (02038  01670) shows identical school rate
- **Hicksville**: tax year 2026 (school 2025-26); parcel 90 KRAEMER ST HICKSVILLE 11801 (12247  01190), Class 1 code 210.01, LRV school district 'HICKSVILLE UFSD - 17'; Net School Tax rate 1406.8, Net Library 62.657 per $100 AV; rate-consistency cross-check: parcel 107 BAY AVE HICKSVILLE 11801 (12182  00330) shows identical school rate
- **Lawrence**: tax year 2026 (school 2025-26); parcel 274 CARYL DR LAWRENCE 11559 (40185  00100), Class 1 code 210.01, LRV school district 'LAWRENCE UFSD - 15'; Net School Tax rate 887.273, Net Library 36.015 per $100 AV; rate-consistency cross-check: parcel 56 WASHINGTON AVE CEDARHURST 11516 (39419  00250) shows identical school rate
- **Manhasset**: tax year 2026 (school 2025-26); parcel 174 RYDER RD MANHASSET 11030 (03099  00060), Class 1 code 210.01, LRV school district 'MANHASSET UFSD - 6'; Net School Tax rate 1083.777, Net Library 62.92 per $100 AV; rate-consistency cross-check: parcel 162 LINDBERG ST MANHASSET 11030 (03  F0500190) shows identical school rate
- **New Hyde Park-Garden City**: tax year 2026 (school 2025-26); parcel 3 SOUTH EIGHTH ST NEW HYDE PARK 11040 (33104  03340), Class 1 code 210.01, LRV school district 'NEW HYDE PARK-GARDEN CITY PARK - 5'; Net School Tax rate 1549.988, Net Library 59.028 per $100 AV | single combined Net School Tax line = elementary + CHSD combined (not itemized on the county bill); rate-consistency cross-check: parcel 3 S 10TH ST NEW HYDE PARK 11040 (33106  02060) shows identical school rate
- **Oceanside**: tax year 2026 (school 2025-26); parcel 3097 TRINITY ST OCEANSIDE 11572 (38372  00750), Class 1 code 210.01, LRV school district 'OCEANSIDE UFSD - 11'; Net School Tax rate 1877.382, Net Library 115.483 per $100 AV; rate-consistency cross-check: parcel 3156 FOURTH ST OCEANSIDE 11572 (43368  01470) shows identical school rate
- **Port Washington**: tax year 2026 (school 2025-26); parcel 41 CARLTON AVE PORT WASHINGTON 11050 (05055  00030), Class 1 code 210.01, LRV school district 'PORT WASHINGTON UFSD - 4'; Net School Tax rate 1621.518, Net Library 72.866 per $100 AV; rate-consistency cross-check: parcel 32 SOUTH WASHINGTON ST PORT WASHINGTON 11050 (05055  01340) shows identical school rate
- **Syosset**: tax year 2026 (school 2025-26); parcel 3 ROBERT CIR SYOSSET 11791 (15087  00100), Class 1 code 210.01, LRV school district 'SYOSSET/SYOSSET CSD # 2 - 12'; Net School Tax rate 2296.55, Net Library 82.423 per $100 AV; rate-consistency cross-check: parcel 6 TEIBROOK AVE SYOSSET 11791 (15087  00020) shows identical school rate
- **Valley Stream 30**: tax year 2026 (school 2025-26); parcel 143 CASPER ST VALLEY STREAM 11580 (37288  02200), Class 1 code 210.01, LRV school district 'VALLEY STREAM UFSD 30 - 30'; Net School Tax rate 1704.851, no Net Library Tax line (structural absence, verified) per $100 AV | single combined Net School Tax line = elementary + CHSD combined (not itemized on the county bill); rate-consistency cross-check: parcel 151 CASPER ST VALLEY STREAM 11580 (37288  02240) shows identical school rate

## Gaps (honest omissions, not estimates)

- **Amityville**:
    - levy: OSC lists a Nassau/Oyster Bay row ($19,648,866) but Census TIGER places Amityville UFSD entirely in Suffolk (bbox lon -73.43..-73.40); the district's true levy is on the Suffolk OSC dataset (out of scope). Omitted rather than record a conflicting Nassau-county figure.
    - schoolRate/libraryRate: no Nassau Class-1 parcel resolves to Amityville school district (probed the SW county-line area); LRV covers Nassau parcels only and this district's territory is in Suffolk. Omitted.

## Method surprises

1. **LRV abbreviates district names** in the parcel `School District` label
   (`E WILLISTON`, `SYOSSET/SYOSSET CSD # 2`). A gate keyed to the full census name would
   have false-negatived them. Fixed by matching the LRV's own token.
2. **Elementary districts share a seed-boundary hazard.** Adjacent K-6 districts feed the
   same CHSD, so a nominal town-center seed can land in the wrong one (Valley Stream 30 ->
   Elmont). Resolved by seeding from the TIGERweb district centroid + the LRV label gate.
3. **Amityville is effectively un-sourceable on the Nassau side.** Census TIGER places the
   whole district in Suffolk; no Nassau parcel resolves to Amityville school district, yet OSC
   carries a $19.6M 'Nassau/Oyster Bay' Amityville levy row that conflicts with the geography.
   Recorded only the district-wide ACS median + NYSED enrollment; levy and rate are gaps.
4. **`api.census.gov` needs a key; `data.census.gov/api/access/data/table` does not** —
   the keyless path from the pilot still works and returns `B25077_001E` cleanly.