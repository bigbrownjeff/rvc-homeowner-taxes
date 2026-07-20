# districts.json fan-out — BATCH 2 provenance (verified 2026-07-20)

Per-field fetch log for `.claude/scratch/fanout/batch-2.json` (13 districts). Method
mirrors the L1 pilot (`.claude/scratch/districts-provenance.md`). Every value below was
read from a LIVE fetch on 2026-07-20. STAR fields + geoid + sdType were already present
in the `site/assets/districts.json` stub rows (L1) and are carried through unchanged; this
batch adds medianValue, enrollment, levy, schoolRate/libraryRate, town, board_url.
`county_leg` intentionally SKIPPED (officials lane).

## Method notes (batch-2 additions to the pilot recipe)

- **NYSED instid lookup** (the pilot left this manual): `data.nysed.gov/lists.php?type=district`
  paginates by `start=<ASCII letter code>` (A=65, B=66, …). Each district row is
  `instid=NNN">DISTRICT NAME`. Fetch the letter page, grep `instid=[0-9]+">NAME`.
- **Census median**: keyless `data.census.gov/api/access/data/table?id=ACSDT5Y2024.B25077&g=<geo>`.
  School-district geography prefixes: **unified = `9700000US`**, **elementary = `9500000US`**
  (Elmont, North Bellmore), secondary = `9600000US`. Response is JSON `{response:{data:[hdr,row]}}`;
  value is column `B25077_001E`, and `NAME` confirms the district. All 13 resolved on the
  district geography (no place proxy needed).
- **Per-parcel district validation (new hard gate)**: the LRV `/info/<PARID>/` page exposes
  the school district SERVER-SIDE — grep for `School District` → e.g. `FREEPORT - 9`, and
  `NYS SWIS Code`. This lets you confirm a GIS-discovered parcel is actually in the target
  district before trusting its rate (GIS layer 1 carries no district field). Substrings as
  LRV prints them differ from Census names: North Bellmore = **`N BELLMORE UFSD`** (abbreviated).
- **STAR cross-check**: where a parcel carries Basic/Enhanced STAR, the parcel's `STAR Savings`
  line equals the district's `starExemptSavings` in districts.json (Baldwin −$1,086 = basic;
  Freeport −$897 = basic; Levittown −$3,304.08 = enhanced) — an independent confirm the parcel
  sits in the right district.
- **Levy**: OSC `iq85-sdzs` filtered `school_name=<name>&fiscal_year_ending=2025`. Query WITHOUT
  a county filter for Cold Spring Harbor (Suffolk-home). Multi-segment districts summed.

## Per-district field log

| District | medianValue (geo) | enroll cur/base (instid) | levy FY2025 | school/lib rate · parcel · LRV district |
|---|---|---|---|---|
| Baldwin | $595,100 · 9700000US3603840 | 4,309 / 4,730 · 800000049578 | $106,372,709 (Hempstead) | 2279.106 / 126.199 · 54022 03390 (2146 Grove St) · BALDWIN UFSD - 10 |
| Cold Spring Harbor | $1,625,500 · 9700000US3608010 | 1,528 / 1,804 · 800000037394 | $70,685,552 = Nassau/OysterBay $15,388,245 + Suffolk/Huntington $55,297,307 | 1625.624 / 71.301 · 26 C 17090 (1328 Ridge Rd, Laurel Hollow) · COLD SPRING HARBOR CSD - 11 |
| Elmont (elem) | $606,600 · 9500000US3610620 | 3,170 / 3,601 · 800000049455 | $118,054,467 (Hempstead; elem-only) | 1737.658 / 35.984 · 32490 00100 (1511 Estelle Ave) · ELMONT UFSD - 16 |
| Freeport | $502,900 · 9700000US3611550 | 6,125 / 6,874 · 800000049608 | $87,162,040.72 (Hempstead) | 1819.195 / 141.172 · 62076 01160 (7 East Ave) · FREEPORT - 9 |
| Hempstead | $451,700 · 9700000US3614130 | 5,071 / 7,488 · 800000049875 | $75,934,370 (Hempstead) | 2267.491 / — · 34396 01120 (6 Duryea Pl) · HEMPSTEAD - 1 |
| Island Park | $635,200 · 9700000US3615480 | 655 / 704 · 800000049252 | $25,737,543 (Hempstead) | 1686.568 / 109.598 · 43006 03500 (78 Ostend Rd) · ISLAND PARK UFSD - 31 |
| Levittown | $600,700 · 9700000US3617160 | 7,061 / 7,085 · 800000049713 | $158,813,038 (Hempstead) | 2360.054 / 123.455 · 45229 00130 (28 Carriage Ln) · LEVITTOWN UFSD - 5 |
| Massapequa | $678,300 · 9700000US3618630 | 6,460 / 7,124 · 800000048704 | $178,753,644 (Oyster Bay) | 1993.324 / 76.739 · 52160 00270 (99 Michigan Ave) · MASSAPEQUA UFSD - 23 |
| North Bellmore (elem) | $653,000 · 9500000US3620940 | 2,128 / 2,100 · 800000049730 | $84,696,129 (Hempstead; elem-only) | 2055.727 / 96.431 · 51331 00180 (2542 Iris Ln) · N BELLMORE UFSD - 4 |
| Oyster Bay-East Norwich | $871,000 · 9700000US3622290 | 1,310 / 1,569 · 800000048868 | $58,195,044 (Oyster Bay) | 1362.757 / 48.927 · 27042 00110 (10 Audrey Ave) · O BAY/OYSTER BAY - E NORWICH CSD #6 - 9 |
| Roosevelt | $476,700 · 9700000US3624990 | 3,020 / 3,170 · 800000049648 | $24,278,096 (Hempstead) | 1619.46 / — · 55333 01020 (23 Harts Ave) · ROOSEVELT UFSD - 8 |
| Uniondale | $516,100 · 9700000US3629280 | 5,768 / 6,736 · 800000049792 | $134,565,503 (Hempstead) | 1531.163 / — · 34079 00160 (550 Duryea Ave) · UNIONDALE UFSD - 2 |
| Wantagh | $711,700 · 9700000US3629850 | 2,710 / 3,012 · 800000049334 | $67,051,549 (Hempstead) | 2100.824 / 90.897 · 56233 00130 (2134 Jones Ave) · WANTAGH UFSD - 23 |

board_url: all 13 probed HTTP 200 (Island Park = https://www.ips.k12.ny.us/ — found via
web search after two guessed domains 000'd; Massapequa = https://www.msd.k12.ny.us/, title
"Massapequa School District" confirmed).

## Gaps & structure notes (honest omissions, never estimated)

1. **Cold Spring Harbor — Suffolk-side rate out of scope.** CSH is a Suffolk-home district
   with a Nassau sliver (Laurel Hollow / Town of Oyster Bay). The verified parcel is Nassau-side,
   so schoolRate/libraryRate are the **Nassau-roll rate only**; the Suffolk (Huntington) roll is a
   different assessing system, not verified. medianValue is the full district geography (both
   counties). Levy is the segment sum across both counties (breakdown logged).
2. **Elmont & North Bellmore — elementary districts, combined school line.** Both are elementary
   districts inside a CHSD (Sewanhaka; Bellmore-Merrick). The LRV parcel shows a **single
   `Net School Tax` line** = combined elementary + CHSD; Nassau bills them as one school line and
   the CHSD portion is **not separable at the parcel level**. schoolRate is therefore the combined
   rate. Their `levy` (OSC) is the **elementary district's own levy** and excludes the CHSD levy,
   which rides separately as a component district. `sdType: elementary` retained from the stub.
3. **libraryRate omitted for Hempstead, Roosevelt, Uniondale.** These three parcels have **no
   `Net Library Tax` line** on the school bill (verified: the label is followed by no tax cells).
   A structural absence (library funded outside the school tax), not a fetch failure — field
   omitted per the no-estimate rule.
4. **county_leg** — SKIPPED for all 13 (officials lane; must be re-verified same-day on
   nassaucountyny.gov before any politician-facing use).
5. **No §467 / exemption-gap figures** — FOIL-gated, per the standing rule. None added.
