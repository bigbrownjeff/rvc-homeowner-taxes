# batch-3.json provenance — Nassau districts fan-out, Batch 3 (verified 2026-07-20)

13 districts: Bellmore, East Meadow, Farmingdale, Garden City, Herricks, Island Trees,
Lynbrook, Merrick, North Merrick, Plainedge, Roslyn, Valley Stream 13, West Hempstead.

Every value below was read from a LIVE fetch this session. No figure is estimated; any
field that could not be verified is omitted and logged as a gap. Output mirrors the pilot
full-row schema in `site/assets/districts.json`; this file is the L1-pilot-style per-field
fetch log. `starCredit` / `starExemptSavings` / `starMaxExemptSavings2026_27` are carried
over unchanged from the existing verified stub rows in `districts.json` (DTF, 2026-07-20).

## Method (reusable, confirms + extends pilot notes)

- **Census median (B25077)** — district geography, keyless:
  `https://data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=<PRE><geoid>`.
  **Prefix depends on district type:** `9700000US` for unified districts, **`9500000US`
  for the four ELEMENTARY districts** (Bellmore, Merrick, North Merrick, Valley Stream 13).
  Using 9700000US on an elementary geoid returns an empty/non-JSON body — that was the
  initial cause of four null medians until the prefix was switched.
- **NYSED instid** — the reliable lookup is the site's own autocomplete:
  `https://data.nysed.gov/search_schools.php?term=<name>` returns JSON; the district row is
  `"type":"16"`. (The paginated `lists.php?type=district&start=N` list works too but `start`
  is not a clean page index and repeats the A–E slice for small integers.) Enrollment then:
  `https://data.nysed.gov/enrollment.php?year=2025|2016&instid=<id>`, literal
  `K-12 Enrollment: N,NNN`. NYSED prints the "K-12 Enrollment" label even for the K-6
  elementary districts; the number is the district's total enrolled.
- **Levy** — OSC `data.ny.gov/resource/iq85-sdzs.json?county=Nassau&fiscal_year_ending=2025`
  filtered `starts_with(school_name,'<dtfName>')`, then kept only exact `school_name`
  matches and summed distinct `swis_code` segments. Roslyn is the only multi-segment
  district in this batch (North Hempstead + a small Oyster Bay segment).
- **schoolRate / libraryRate** — GIS point query (keyless, no reCaptcha)
  `gis.nassaucountyny.gov/server/rest/services/Layers/MapServer/1/query` (point + distance,
  `outFields=PARID,PARCEL_ADDRESS`, `inSR=4326`) to discover parcels, then the LRV
  `/info/<PARID+with+plusses>/` page (sets session cookie) → `POST /gstaxes.php`
  (`PARID` space-padded + `TOWN_NAME`). `Net School Tax` and `Net Library Tax` give the
  per-$100 rates.
  - **HARD GATE (batch-2 method, applied):** GIS layer 1 has NO school-district field, so
    before logging any rate the LRV `/info/` page is parsed for its server-side
    `School District <NAME> - <n>` label and normalized (LRV abbreviates: `N MERRICK UFSD`,
    `W HEMPSTEAD UFSD`, `VALLEY STREAM UFSD 13`). The parcel is used only if the normalized
    label EQUALS the target district (this distinguishes Bellmore vs North Bellmore, Merrick
    vs North Merrick).
  - **SECOND check:** the chosen parcel is a STAR-verified single-family homeowner parcel
    whose `STAR Savings` equals this district's DTF exemption savings to the cent (see each
    row). Its own rate is recorded — not a modal rate over nearby parcels, because
    village-center geocodes surface co-op/condo (Class 2) and commercial (Class 4) parcels
    that carry DIFFERENT, lower per-$100 rates on the same roll. This bit Garden City
    (a Class-4 parcel at 888 Franklin Ave showed 273.712) and Lynbrook (a commercial parcel
    at 37-45 Atlantic Ave showed 515.558) before the STAR-parcel rule corrected them to the
    Class-1 residential rates 1411.338 and 2174.389.
- **Elementary parcel structure** — on the LRV bill the elementary + CHSD school taxes are
  CONSOLIDATED into one `Net School Tax` line and are not separable at the parcel level.
  `schoolRate` for Bellmore, Merrick, North Merrick, Valley Stream 13 is therefore the
  COMBINED elementary + CHSD Class-1 rate; the `levy` is the elementary district's own levy
  (the CHSD levy is separate). Recorded in each row's `sdStructure`.
- **Missing `Net Library Tax` line** — Garden City, Herricks, Lynbrook and Valley Stream 13
  parcels carry NO Net Library Tax line. This is a structural absence (library not billed as
  a separate line on those districts' LRV school-tax bills), not a fetch miss;
  `libraryRate` is null with a `libraryRateNote`.
- **board_url** — HTTP-200 probed. Garden City (`gardencity.k12.ny.us`) and Merrick
  (`merrick.k12.ny.us`) resolve on the k12.ny.us domain, not a `*schools.org` guess;
  Valley Stream 13 resolves at `valleystream13.com` (no `www`).

## Per-district fetch log

Rate parcels are all Class-1 single-family, tax year 2026 (school 2025-26). "STAR ✓" =
parcel STAR Savings matches this district's DTF exemption savings exactly (in-district proof
on top of the /info/ label gate).

| District (type) | median (geo) | enroll cur→base (instid) | levy FY25 | schoolRate / libraryRate | rate parcel · AV · combined · STAR ✓ |
|---|---|---|---|---|---|
| Bellmore (elem) | $720,100 (9500000US3604410) | 1,027 ← 993 (…49672) | $57,319,798 | 2195.124 / 124.398 | 63026 00110, 2530 Horace Ct · AV 461 · $10,692.99 · Basic −$1,065.00 = DTF 1065 ✓ |
| East Meadow (unified) | $638,900 (9700000US3609840) | 7,783 ← 7,028 (…49753) | $156,374,337 | 1504.739 / 80.23 | 50172 00010, 1826 McKinley Ave · AV 569 · $9,018.47 · Basic −$752.37 = DTF 752.37 ✓ |
| Farmingdale (unified) | $599,500 (9700000US3610980) | 5,180 ← 5,762 (…48748) | $105,322,980 | 2051.035 / 59.329 | 49068 00140, 56 Columbia St · AV 365 · $7,733.78 · Enh −$2,871.45 = DTF 2871.45 ✓ |
| Garden City (unified) | $1,075,900 (9700000US3611760) | 3,931 ← 3,848 (…49449) | $111,991,970 | 1411.338 / — (no lib line) | 34059 00300, 105 Arthur St · AV 990 · $13,972.25 · Basic −$690.00 = DTF 690 ✓ |
| Herricks (unified) | $922,600 (9700000US3614280) | 4,258 ← 3,891 (…49018) | $107,258,592 | 1642.032 / — (no lib line) | 09577 00100, 36 East St, New Hyde Park · AV 532 · $8,735.61 · Enh −$2,298.84 = DTF 2298.84 ✓ |
| Island Trees (unified) | $591,200 (9700000US3615510) | 2,261 ← 2,231 (…49285) | $49,577,566 | 1469.648 / 39.323 | 51462 00160, 97 Longfellow Ave, Levittown · AV 335 · $5,055.05 · Enh −$2,057.51 = DTF 2057.51 ✓ |
| Lynbrook (unified) | $644,100 (9700000US3617910) | 2,725 ← 2,768 (…49385) | $74,989,523 | 2174.389 / — (no lib line) | 38498 00080, 27 Doxsey Pl · AV 649 · $14,111.78 · Basic −$1,048.00 = DTF 1048 ✓ |
| Merrick (elem) | $783,300 (9500000US3619110) | 1,596 ← 1,470 (…49333) | $87,867,592 | 2264.12 / 101.558 | 62190 00130, 1866 Charles St · AV 364 · $8,611.07 · Enh −$3,169.77 = DTF 3169.77 ✓ |
| North Merrick (elem) | $682,100 (9500000US3621120) | 1,237 ← 1,188 (…49270) | $47,027,973 | 2044.009 / 132.671 | 55515 00010, 1 Cliff Rd · AV 508 · $11,057.54 · Basic −$986.00 = DTF 986 ✓ ("N MERRICK UFSD") |
| Plainedge (unified) | $626,300 (9700000US3623190) | 2,802 ← 3,035 (…48780) | $70,035,559 | 2241.07 / 90.918 | 52105 00340, 236 N Hickory St, Massapequa · AV 492 · $11,473.38 · Enh −$3,137.50 = DTF 3137.5 ✓ |
| Roslyn (unified) | $1,119,600 (9700000US3625050) | 3,329 ← 3,138 (…49164) | $106,644,040 | 1790.885 / 86.543 | 07 F 07030, 72 Main St · AV 688 · $12,916.71 · Basic −$864.00 = DTF 864 ✓ |
| Valley Stream 13 (elem) | $640,400 (9500000US3629430) | 1,904 ← 2,048 (…49526) | $74,097,448 | 1640.379 / — (no lib line) | 37625 00040, 979 Dana Ave · AV 448 · $7,348.90 · Basic −$781.00 = DTF 781 ✓ ("VALLEY STREAM UFSD 13") |
| West Hempstead (unified) | $646,900 (9700000US3630660) | 1,596 ← 2,033 (…49293) | $50,647,344 | 1817.282 / 160.649 | 35375 00210, 216 Spruce St · AV 434 · $8,584.22 · Basic −$879.00 = DTF 879 ✓ |

Levy segments: all single Town-of-Hempstead segments except Farmingdale and Plainedge
(single Oyster Bay), Herricks (single North Hempstead) and **Roslyn** (North Hempstead
$106,083,295 + Oyster Bay $560,745 = $106,644,040).

## Observations (report honestly, not for the site)

- **Enrollment is NOT uniformly declining in this batch.** Up since 2015-16: East Meadow
  (+10.7%), Herricks (+9.4%), Roslyn (+6.1%), Merrick (+8.6%), North Merrick (+4.1%),
  Island Trees (+1.3%), Garden City (+2.2%), Bellmore (+3.4%). Down: West Hempstead
  (−21.5%), Plainedge (−7.7%), Farmingdale (−10.1%), Valley Stream 13 (−7.0%), Lynbrook
  (−1.6%). Any site use of these must state the direction per district, not assume decline.
- **Median home value spread is wide:** Roslyn $1.12M and Garden City $1.08M at the top,
  Island Trees $591K and Farmingdale $600K at the bottom — a ~1.9× range across the batch.

## Gaps / honest omissions

1. **libraryRate for Garden City, Herricks, Lynbrook, Valley Stream 13** — omitted (null):
   no Net Library Tax line on those districts' parcel bills. Structural, not a fetch miss.
2. **CHSD-portion split for the four elementary districts** — not separable at the parcel
   level (single consolidated Net School Tax line); `schoolRate` is the combined rate and
   `levy` is elementary-only. Not an estimate — the underlying components are simply not
   published at parcel granularity by Nassau LRV.
3. **county_leg** — intentionally skipped (officials lane; re-verify same-day before any
   politician-facing use), per task.
4. No §467 / exemption-gap figures anywhere (FOIL-gated, standing rule).
