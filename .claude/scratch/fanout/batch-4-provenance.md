# districts.json provenance — Batch 4 fan-out (verified 2026-07-20)

Per-field fetch log for the 13 districts in `.claude/scratch/fanout/batch-4.json`. Every
value below was read from a live fetch on 2026-07-20, replicating the L1 pilot method in
`.claude/scratch/districts-provenance.md`. No figure exists here without a row below.
STAR fields are carried unchanged from the existing verified stub rows in
`site/assets/districts.json` (DTF, 2026-07-20) and are not re-logged.

## Method deltas from the pilot (what this batch confirmed / added)

- **Census school-district geography, preferred over place proxy.** Unified districts
  resolve directly at `https://data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=9700000US<geoid>`
  (summary level 970). No place proxy was needed for any unified district in this batch.
- **Elementary districts need summary level 950, prefix `9500000US`, NOT 970 or 960.**
  Floral Park-Bellerose (3611160) and Valley Stream 24 (3629460) return nothing under
  `9700000US`/`9600000US`; `9500000US<geoid>` returns the district row cleanly.
  (960 is the *secondary* level; 950 is *elementary*.)
- **NYSED instid lookup endpoint = `https://data.nysed.gov/search_schools.php?term=<name>`**
  (JSON autocomplete used by the site's search box; found in the homepage JS as
  `source: "/search_schools.php"`). Filter `type=="16"` for the district entity. The
  search is fuzzy: "Westbury" returns East Meadow and East Williston UFSD before Westbury
  UFSD, so match on the returned `value` name, not position.
- **OSC levy field name is `school_district_tax_levy`** (per-segment). Multi-municipality
  districts are summed across `municipality` rows.
- **GIS parcel discovery: a 60 m radius often returns zero features; use 300-500 m.**
  Layer 1 = Parcels; `PARID` (space-padded) is the key; `PARCEL_ADDRESS` gives the hamlet.
- **gstaxes school section parse:** the Net School Tax row cells are `[taxable_value,
  rate_per_$100, tax_$]`; Net Library Tax follows with its own `[value, rate, $]` if a
  library district applies (else the label is immediately followed by Net Recreation Tax /
  Combined). The parcel's `/info/` page shows "School District: <NAME> - <n>" and the
  property Class, used to confirm the parcel is Class 1 AND actually inside the target
  district. **Hamlet name != school district** (see Malverne below).
- **Independent cross-check:** any parcel carrying a STAR Savings line reproduces the DTF
  exempt-savings figure to the dollar, which pins both the district identity and the rate.

## Per-district log

Columns: median (Census B25077 district geo) · instid (NYSED) · enrollment cur/base
(NYSED enrollment.php year=2025 / year=2016) · levy (OSC iq85-sdzs FY2025) · school/library
rate per $100 AV (LRV gstaxes, tax yr 2026 = school 2025-26) · sampled parcel · board_url.

### Bethpage UFSD (3604740, unified, Oyster Bay)
- median **$630,900** — `…&g=9700000US3604740`
- instid **800000048758** ("BETHPAGE UFSD"); enrollment **2,957 / 2,880** (note: up +2.7%, not a decline)
- levy **$71,513,844** — single Oyster Bay segment
- schoolRate **1845.861** / libraryRate **70.722** — parcel `46108  00030` (23 Sheridan Ave, Class 1); AV 477 -> School $8,804.76 + Library $337.34 = Combined $9,142.10 (reproduces to the penny)
- board_url https://www.bethpagecommunity.com/ (bethpagecsd.org and bethpage.ws do NOT resolve / are not the district; confirmed official via search)

### East Rockaway UFSD (3609960, unified, Hempstead)
- median **$567,200** — `…&g=9700000US3609960`
- instid **800000049403**; enrollment **1,126 / 1,172**
- levy **$33,401,742** — single Hempstead segment
- schoolRate **2144.262** / libraryRate **omitted** — parcel `42003  00160` (77 Lawson Ave, Class 1, "EAST ROCKAWAY UFSD - 19"); AV 317 -> School $6,797.31 = Combined $6,797.31 (reproduces). No separate Net Library Tax line on the sampled parcel's school bill.
- board_url https://www.eastrockawayschools.org/ (200)

### Floral Park-Bellerose UFSD (3611160, ELEMENTARY, Hempstead) — Sewanhaka CHSD component
- median **$777,300** — `…&g=9500000US3611160` (elementary sumlevel 950)
- instid **800000049337**; enrollment **1,448 / 1,458**
- levy **$59,382,912.56** — Hempstead $50,147,190.88 + North Hempstead $9,235,721.68
- schoolRate **1560.415** / libraryRate **omitted** — parcel `32074  13480` (89 Plainfield Ave, Class 1, "FLORAL PARK-BELLEROSE UFSD - 22"); AV 782 -> School $12,202.45 = Combined $12,202.45 (reproduces); **STAR Savings -$752.00 == DTF Basic exempt savings $752** exactly.
- **STRUCTURE:** LRV bills the elementary district and the Sewanhaka CHSD as ONE combined Net School Tax line — no separate elementary/CHSD lines exist on the parcel. 1560.415 is the combined rate as billed.
- board_url https://www.fpbsd.org/ (200)

### Glen Cove City SD (3612180, unified/city, City of Glen Cove) — RATE GAP
- median **$698,900** — `…&g=9700000US3612180`
- instid **800000049886**; enrollment **3,063 / 3,179**
- levy **$77,336,931** — single Glen Cove (city) segment
- schoolRate / libraryRate **OMITTED**. gstaxes for parcel `21006  00120` (8 Johnson St) returns: "This property is located within the City of Glen Cove. Tax information for this property can be obtained by calling the City of Glen Cove (516)-676-2000" and shows NO school/general tax lines (only county/town). City assesses its own roll — same archetype as the Long Beach pilot gap. Resolving the rate needs a City of Glen Cove tax bill / city assessor source.
- board_url https://www.glencoveschools.org/ (200)

### Hewlett-Woodmere UFSD (3631710, unified, Hempstead)
- median **$829,100** — `…&g=9700000US3631710`
- instid **800000049523**; enrollment **2,650 / 2,938**
- levy **$108,577,501** — single Hempstead segment
- schoolRate **2357.17** / libraryRate **139.853** — parcel `41024  00420` (1019 Walsh Ave, Woodmere, Class 1); AV 429 -> School $10,112.26 + Library $599.97 = Combined $10,712.23 (reproduces)
- board_url https://www.hewlett-woodmere.net/ (200)

### Jericho UFSD (3615810, unified, Oyster Bay)
- median **$1,057,200** — `…&g=9700000US3615810` (highest in the batch)
- instid **800000048822**; enrollment **3,230 / 2,999** (up +7.7%)
- levy **$115,460,400** — North Hempstead $6,751,320 + Oyster Bay $108,709,080
- schoolRate **1932.341** / libraryRate **90.916** — parcel `11354  00020` (135 Seaman Rd, Class 1); AV 713 -> School $13,777.59 + Library $648.23 = Combined $14,425.82 (reproduces)
- board_url https://www.jerichoschools.org/ (200)

### Malverne UFSD (3618210, unified, Hempstead)
- median **$618,200** — `…&g=9700000US3618210`
- instid **800000049551**; enrollment **1,801 / 1,659**
- levy **$48,660,033** — single Hempstead segment
- schoolRate **2058.618** / libraryRate **omitted** — parcel `37345  00240` (46 Nottingham Rd, Class 1); AV 443 -> School $9,119.68 = Combined $9,119.68 (reproduces); **STAR Savings -$983.00 == DTF Basic $983** exactly.
- **CAUTION logged:** a nearby Malverne-*addressed* parcel `37511  00410` (57 West Ave) showed a DIFFERENT rate (1640.379) and STAR -$781 — i.e. it sits in a different school district. Hamlet name != school district. Confirmed 37345 00240 as Malverne UFSD via the STAR match + "MALVERNE UFSD - 12" info label.
- board_url https://www.malverneschools.org/ (200)

### Mineola UFSD (3619500, unified, North Hempstead)
- median **$674,000** — `…&g=9700000US3619500`
- instid **800000049007**; enrollment **2,794 / 2,695**
- levy **$87,217,536** — single North Hempstead segment
- schoolRate **1449.641** / libraryRate **omitted** — parcel `09336  03900` (346 Nassau Blvd, Class 1, "MINEOLA UFSD - 10"); AV 508 -> School $7,364.18 = Combined $7,364.18 (reproduces). No separate library line on the sampled parcel.
- board_url https://www.mineola.k12.ny.us/ (200; mineolaufsd.org does not resolve)

### North Shore CSD (3626370, unified, Oyster Bay)
- median **$954,400** — `…&g=9700000US3626370`
- instid **800000048966**; enrollment **2,541 / 2,687**
- levy **$92,540,475.27** — North Hempstead $4,212,476.28 + Oyster Bay $88,327,998.99
- schoolRate **1716.315** / libraryRate **omitted** — parcel `21057  00020` (36 Hillcrest Dr, Glen Head, Class 1, "GLEN HEAD/NORTH SHORE CSD # 1 - 2"); AV 663 -> School $11,379.17 = Combined $11,379.17 (reproduces); **STAR Savings -$829.00 == DTF Basic $829** exactly.
- District spans Sea Cliff / Roslyn Harbor villages plus Glen Head / Glenwood Landing unincorporated; sampled parcel is unincorporated Glen Head. No separate library line on the sampled parcel.
- board_url https://www.northshoreschools.org/ (200)

### Plainview-Old Bethpage CSD (3623220, unified, Oyster Bay)
- median **$819,500** — `…&g=9700000US3623220`
- instid **800000048891**; enrollment **5,406 / 4,865** (largest in the batch, up +11.1%)
- levy **$143,232,660** — single Oyster Bay segment
- schoolRate **2076.266** / libraryRate **101.352** — parcel `12477  00140` (73 Victor St, Plainview, Class 1); AV 479 -> School $9,945.31 + Library $485.48 = Combined $10,430.79 (reproduces)
- board_url https://www.pobschools.org/ (200)

### Seaford UFSD (3626400, unified, Hempstead)
- median **$656,700** — `…&g=9700000US3626400`
- instid **800000049690**; enrollment **2,184 / 2,283**
- levy **$59,930,530** — single Hempstead segment
- schoolRate **2177.895** / libraryRate **85.485** — parcel `57148  01590` (38 Estella St, Class 1); AV 401 -> School $8,733.36 + Library $342.79 = Combined $9,076.15 (reproduces); **STAR Savings -$3,019.00 == DTF Enhanced $3,019** exactly.
- board_url https://www.seaford.k12.ny.us/ (200)

### Valley Stream UFSD 24 (3629460, ELEMENTARY, Hempstead) — Valley Stream CHSD component
- median **$614,500** — `…&g=9500000US3629460` (elementary sumlevel 950)
- instid **800000049326**; enrollment **1,036 / 1,100**
- levy **$47,641,480** — single Hempstead segment
- schoolRate **1719.061** / libraryRate **omitted** — parcel `37343  01120` (22 Hamilton Pl, Class 1, "VALLEY STREAM UFSD 24 - 24"); AV 447 -> School $7,684.20 = Combined $7,684.20 (reproduces); **STAR Savings -$831.00 == DTF Basic $831** exactly.
- **STRUCTURE:** LRV bills the elementary district and the Valley Stream CHSD as ONE combined Net School Tax line. 1719.061 is the combined rate as billed. Confirmed district 24 (not VS 13/30) via the info label + STAR match.
- board_url https://valleystreamschooldistrict24.org/ (200; the SharpSchool host and vs24.org are dead)

### Westbury UFSD (3630960, unified, North Hempstead)
- median **$570,000** — `…&g=9700000US3630960`
- instid **800000049217** (NOT 800000049753 = East Meadow, the fuzzy-search first hit); enrollment **4,328 / 4,934** (down -12.3%)
- levy **$78,218,042** — Hempstead $1,847,372 + North Hempstead $76,370,670
- schoolRate **2315.833** / libraryRate **78.587** — parcel `10184  02320` (256 Lewis Ave, Class 1, "WESTBURY UFSD - 1"); AV 398 -> School $9,217.02 + Library $312.78 = Combined $9,529.80 (reproduces)
- board_url https://www.westburyschools.org/ (200)

## Gaps (honest omissions, not estimates)

1. **Glen Cove schoolRate + libraryRate** — city-roll archetype; county LRV declines to bill.
2. **Elementary elem-vs-CHSD rate split** (Floral Park-Bellerose, Valley Stream 24) — LRV
   bills a single combined line; the split is not separable from this source.
3. **libraryRate for East Rockaway, Malverne, Mineola, North Shore** — no separate Net
   Library Tax line on the sampled Class-1 parcel (library funded off the school bill).
4. **county_leg** — officials lane, omitted (re-verify same-day before politician-facing use).
5. **No section-467 / exemption-gap figures** — FOIL-gated, per standing rule.
