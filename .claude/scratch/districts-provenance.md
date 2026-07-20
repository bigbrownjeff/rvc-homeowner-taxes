# districts.json provenance — L1 pilot (verified 2026-07-20)

Per-field fetch log for `site/assets/districts.json`. Every value below was read from
a live fetch on 2026-07-20 by the L1 data-sourcing lane. This file feeds the L4
validation.html "Per-district figures" section. No figure in the JSON exists without a
row here or in the county-wide STAR section at the bottom.

Method notes (reusable for the fan-out):

- **DTF STAR tables** parse cleanly from raw HTML. Comparison page rows are
  Municipality × District × Tax class; keep class `1` plus `Homestead` (Glen Cove).
  Max-savings page uses class codes `1/2/4` and `H/N` for Glen Cove; keep `1` and `H`.
  Districts repeating across municipalities were asserted identical (zero conflicts,
  55 districts).
- **Census median values**: `api.census.gov` now requires an API key; the keyless
  primary-issuer path is `https://data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=<geo>`
  with geo `160XX00US<place>` (place) or `9700000US<geoid>` (unified school district).
- **NYSED enrollment**: `data.nysed.gov/enrollment.php?year=YYYY&instid=NNN` is
  server-rendered; the figure is the literal string `K-12 Enrollment: N,NNN`.
  `year=2025` = 2024-25 school year.
- **Nassau LRV**: parcel page `https://lrv.nassaucountyny.gov/info/<PARID with spaces→+>/`
  303-redirects to itself once to set a session cookie (curl needs `-L -c jar -b jar`).
  The tax table is NOT in the page; it comes from `POST /gstaxes.php` with form fields
  `PARID` (space-padded) and `TOWN_NAME`, using the session cookie. Default response
  year is 2026 = school 2025-26 ("2026 - School ('25-26) and County/Town '26'").
  Parcel SBLs are discoverable without the reCaptcha search via the county GIS REST:
  `https://gis.nassaucountyny.gov/server/rest/services/Layers/MapServer/1/query`
  (point + distance, `outFields=PARID,PARCEL_ADDRESS`, `inSR=4326`).
- **Levy**: NYS OSC "Real Property Tax Rates Levy Data By Municipality" Socrata
  dataset `iq85-sdzs` on data.ny.gov (keyless). `fiscal_year_ending=2025` = 2024-25
  school year. Multi-municipality districts appear as one row per segment; sum the
  distinct segments (the city-roll segment can appear twice under two municipality
  labels — dedupe before summing).
- **TIGER district keys**: TIGERweb `School/MapServer` layers 0 (unified),
  1 (secondary), 2 (elementary) give NAME + GEOID. All 55 DTF districts matched a
  TIGER name after stripping the "…School District" suffix (one DTF truncation:
  "New Hyde Park-Garden City" = "New Hyde Park-Garden City Park UFSD"; one DTF typo:
  max-savings "Floral Park-Bellrose").

---

## Pilot 1 — Rockville Centre UFSD (geoid 3624780, unified, village-in-town)

| Field | Value | Exact URL fetched | Read on | Vintage |
|---|---|---|---|---|
| starCredit basic / enhanced | $1,089.00 / $3,147.01 | https://www.tax.ny.gov/pit/property/star/comparison/28-nassau.htm | 2026-07-20 | 2025 final (2026 unpublished) |
| starExemptSavings basic / enh | $1,068.00 / $2,856.00 | same page | 2026-07-20 | 2025 final |
| starMaxExemptSavings2026_27 | $1,068 / $2,856 | https://www.tax.ny.gov/pit/property/star/max-savings/school-district/sd28.htm | 2026-07-20 | 2026-27 |
| medianValue | $818,700 | https://data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=160XX00US3663264 | 2026-07-20 | ACS 2020-24 |
| medianValue cross-check (district geo) | $811,100 | …&g=9700000US3624780 | 2026-07-20 | ACS 2020-24 |
| schoolRate / libraryRate | 2247.867 / 84.459 per $100 AV | https://lrv.nassaucountyny.gov/info/36366++00150/ → POST /gstaxes.php PARID=`36366  00150` TOWN_NAME=Hempstead | 2026-07-20 | tax yr 2026 (school 2025-26) |
| — bill reproduction | AV 653 → Combined School Taxes $15,230.09 | same response | 2026-07-20 | matches ledger #f-rates and #f-15230 to the penny |
| levy | $106,470,000 | https://data.ny.gov/resource/iq85-sdzs.json?county=Nassau&school_name=Rockville%20Centre (fiscal_year_ending 2025, Hempstead row) | 2026-07-20 | 2024-25 |
| — levy cross-check | ledger #f-budget26: 2025-26 levy $109.24M = 106.47M × 1.026 exactly | site/validation.html | 2026-07-20 | — |
| enrollment cur | 3,276 | https://data.nysed.gov/enrollment.php?year=2025&instid=800000049383 ("K-12 Enrollment: 3,276") | 2026-07-20 | 2024-25 |
| enrollment base | 3,533 | https://data.nysed.gov/enrollment.php?year=2016&instid=800000049383 | 2026-07-20 | 2015-16 |
| county_leg | Leg. Scott Davis, LD-1 | https://www.nassaucountyny.gov/505/District-1---Scott-Davis (repo officials table, verified 2026-07-20) | 2026-07-20 | 2026 map |
| board_url | https://www.rvcschools.org/ | probed 200 | 2026-07-20 | — |

## Pilot 2 — Long Beach City SD (geoid 3617730, unified, city archetype)

| Field | Value | Exact URL fetched | Read on | Vintage |
|---|---|---|---|---|
| starCredit basic / enhanced | $619.13 / $1,733.57 | DTF comparison page (above) | 2026-07-20 | 2025 final |
| starExemptSavings basic / enh | $613.00 / $1,733.57 | same | 2026-07-20 | 2025 final |
| starMaxExemptSavings2026_27 | $613 / $1,734 | DTF max-savings sd28 (above) | 2026-07-20 | 2026-27 |
| medianValue | $696,400 | https://data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=160XX00US3643335 | 2026-07-20 | ACS 2020-24; city-place proxy |
| medianValue cross-check (district geo) | $724,600 | …&g=9700000US3617730 | 2026-07-20 | district incl. Lido Beach / Point Lookout |
| schoolRate / libraryRate | 1238.265 / 44.782 per $100 AV | https://lrv.nassaucountyny.gov/info/60016++00250/ → POST /gstaxes.php PARID=`60016  00250` TOWN_NAME=Hempstead | 2026-07-20 | tax yr 2026 (school 2025-26) |
| — parcel | 16 Harrogate St, Lido Beach; class 210.01 single-family; AV 580 | parcel page | 2026-07-20 | — |
| — STAR cross-check | parcel's "STAR Savings −$613.00" = DTF Basic exemption savings exactly | gstaxes response | 2026-07-20 | independent source agreement |
| — SCOPE | county-roll rate (Town of Hempstead portion only); City of Long Beach assesses its own roll; city-parcel rate NOT verified, omitted | — | — | the city-archetype gap |
| levy | $109,080,539 = $84,062,477 (city roll) + $25,018,062 (Town of Hempstead) | https://data.ny.gov/resource/iq85-sdzs.json?county=Nassau&school_name=Long%20Beach (FY 2025 rows) | 2026-07-20 | 2024-25 |
| — levy cross-check | LI Herald: adopted 2024-25 levy "$109.1 million" (liherald.com …,208000; page 403s automated fetch — figure from search-result text, not a fetched page) | search 2026-07-20 | — | corroborates segment-sum reading |
| enrollment cur | 3,265 | https://data.nysed.gov/enrollment.php?year=2025&instid=800000049221 | 2026-07-20 | 2024-25 |
| enrollment base | 3,673 | https://data.nysed.gov/enrollment.php?year=2016&instid=800000049221 | 2026-07-20 | 2015-16 |
| board_url | https://www.lbeach.org/ | probed 200 | 2026-07-20 | — |

## Pilot 3 — Locust Valley CSD (geoid 3617700, unified, town-unincorporated)

| Field | Value | Exact URL fetched | Read on | Vintage |
|---|---|---|---|---|
| starCredit basic / enhanced | $809.00 / $2,257.00 | DTF comparison page (above) | 2026-07-20 | 2025 final |
| starExemptSavings basic / enh | $793.00 / $1,965.00 | same | 2026-07-20 | 2025 final |
| starMaxExemptSavings2026_27 | $793 / $1,965 | DTF max-savings sd28 (above) | 2026-07-20 | 2026-27 |
| medianValue | $846,500 | https://data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=160XX00US3643192 | 2026-07-20 | ACS 2020-24; CDP proxy (district also covers Bayville, Lattingtown, Matinecock, Mill Neck) |
| medianValue cross-check (district geo) | $884,400 | …&g=9700000US3617700 | 2026-07-20 | ACS 2020-24 |
| schoolRate / libraryRate | 1626.547 / 68.394 per $100 AV | https://lrv.nassaucountyny.gov/info/30066++04760/ → POST /gstaxes.php PARID=`30066  04760` TOWN_NAME=Oyster Bay | 2026-07-20 | tax yr 2026 (school 2025-26) |
| — parcel | 35 Weir Ln, Locust Valley; class 210.01 single-family; AV 758 | parcel page | 2026-07-20 | — |
| — rate consistency check | second parcel 30021++00170 (18 Locust Pl): identical 1626.547 | https://lrv.nassaucountyny.gov/info/30021++00170/ | 2026-07-20 | — |
| levy | $88,081,852 | https://data.ny.gov/resource/iq85-sdzs.json?county=Nassau&school_name=Locust%20Valley (FY 2025, single Oyster Bay segment) | 2026-07-20 | 2024-25 |
| enrollment cur | 1,754 | https://data.nysed.gov/enrollment.php?year=2025&instid=800000048920 | 2026-07-20 | 2024-25 |
| enrollment base | 2,087 | https://data.nysed.gov/enrollment.php?year=2016&instid=800000048920 | 2026-07-20 | 2015-16; −16.0%, consistent with the site's "15% drop" claim |
| board_url | https://www.locustvalleyschools.org/ | probed 200 (lvcsd.k12.ny.us is http-only) | 2026-07-20 | — |

## County-wide STAR (all 55 DTF-listed Nassau districts, stub rows)

Both DTF tables fetched raw and parsed 2026-07-20:

- **2025 final credit + exemption savings** (Class 1 / Homestead):
  https://www.tax.ny.gov/pit/property/star/comparison/28-nassau.htm — 55 districts,
  zero cross-municipality conflicts. Page still 2025-labeled (2026 finals
  unpublished as of 2026-07-20; ledger #watch item applies to every row).
- **Max 2026-27 exemption savings** (Class 1 / H):
  https://www.tax.ny.gov/pit/property/star/max-savings/school-district/sd28.htm —
  53 districts (Amityville and Cold Spring Harbor absent: DTF publishes their max
  savings on the Suffolk page sd52, out of scope; field omitted for them).

Spot-verifications against previously-cited figures: RVC $3,147.01/$1,089 (ledger
#f-star-credit, exact), Levittown Enh $3,304.08 / Basic $1,162, Hempstead
$3,174.49/$1,133.75, Glen Cove $2,056/$800.44 (plan §2B examples, exact).

## Known gaps (honest omissions, not estimates)

1. **Long Beach city-roll school rate** — the city assesses its own roll; the JSON
   carries only the county-roll rate with an explicit `schoolRateScope`. Resolving
   the city-side rate needs a City of Long Beach tax bill or city assessor source.
2. **county_leg for Long Beach and Locust Valley** — officials lane; must be
   verified same-day on nassaucountyny.gov before any politician-facing use.
3. **Amityville / Cold Spring Harbor starMaxExemptSavings2026_27** — Suffolk page,
   out of scope by decision (option a).
4. **Secondary CHSDs (Bellmore-Merrick, Sewanhaka, Valley Stream CHSD)** — no DTF
   STAR rows of their own; their levy rides component elementary districts. The
   geocoder resolves those addresses via elementary+secondary layers, not unified —
   L2 must handle this (documented in `_meta.notes`).
5. **No §467 / exemption-gap figures anywhere** — FOIL-gated, per standing rule.
