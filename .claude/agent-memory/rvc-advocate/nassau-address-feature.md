---
name: nassau-address-feature
description: Scoping findings for the "any Nassau address → geo-specific follow-one-home-sale" feature (verified 2026-07-20); plan at .claude/scratch/nassau-address-feature-plan.md
metadata:
  type: project
---

Feature: move the index.html action kit to bottom of Section 01, relabel "Build my
letters" → "See my details", make it serve any Nassau address with geo-specific
"follow one home sale" figures + a per-geo Harvey-ball coverage page.

**Why:** Jeff directive 2026-07-20. Full BUILD PLAN (8 sections + acceptance suite +
coverage page) at `.claude/scratch/nassau-address-feature-plan.md`.

**How to apply / verified feasibility (2026-07-20):**
- **District resolution already exists** in index.html — the Census geocoder JSONP
  call already `pick()`s the "Unified School Districts" layer (`c.school`). Confirmed
  it returns the correct NY UFSD/City district Nassau-wide (Long Beach City SD,
  Levittown/Great Neck/Hewlett-Woodmere UFSD) + full CD/SD/AD stack. No new API.
- **Per-district STAR is the anchor datum, fully sourceable:** DTF `comparison/
  28-nassau.htm` (credits) and `max-savings/school-district/sd28.htm` (exemption) both
  enumerate every Nassau district. The $2,058 downsizing dividend = Enhanced−Basic per
  district. Log to a new `assets/districts.json` + ledger.
- **Binding data gap:** no clean county-wide school-tax-RATE table; rates come
  one-parcel-at-a-time from reCaptcha-gated Nassau LRV (direct parcel URLs load). One
  representative parcel URL per district = the labor-intensive fan-out lane.
- **Architecture = static-first precomputed `districts.json`** (Option A), NOT runtime
  lookups. Only the geocoder stays runtime. Every field carries a `source_ref`.
- **Pages:** index.html (primary) + validation.html (ledger) + new districts.json +
  new coverage.html; calculator flow-back is phase-2 optional. Confirms Jeff's guess.
  No per-district detail pages needed.
- **Suffolk gap (must-fix):** our own content quotes **Northport (14×), Three Village,
  Brentwood** — all Suffolk County, unservable by a Nassau data plan. Tool must detect
  non-Nassau resolution and degrade honestly. Acceptance suite = 10 Nassau geos we
  quote (RVC/Long Beach/Locust Valley pilot first) as pilot+regression.
- Coverage page lifts PATTERN ONLY from `~/Projects/mattel-engagement/coverage.html`
  (Harvey-ball SVG, live-computed cells, least-complete-first, COVERAGE_SUMMARY export);
  retune to RVC tokens; cells derive state from districts.json + ledger source status.

**L2+L3 SHIPPED as PR #12 (2026-07-20, feature/nassau-address-entry, NOT merged).**
- Confirmed Census geocoder layer→field map (curl-verified, all 4 pilot addresses):
  Counties: NAME "Nassau County" / GEOID "36059" (Suffolk "36103"); County Subdivisions:
  NAME "Hempstead town" etc; Incorporated Places: NAME "Rockville Centre village" (absent
  for unincorporated parcels); Unified School Districts: NAME is the districts.json key,
  GEOID present as fallback. Nassau detection = GEOID==="36059".
- Pilot district NAMEs (the districts.json keys L1 must use EXACTLY): "Rockville Centre
  Union Free School District", "Long Beach City School District", "Locust Valley Central
  School District". Note 235 Lido Blvd resolves place=NONE (barrier island, Hempstead town)
  yet school=Long Beach City SD — fine, we key on school NAME not place.
- ACTUAL shipped districts.json schema (PR #11, merged): `{_meta:{...}, districts:{
  "<Census NAME>":{dtfName, censusName, geoid, sdType, starCredit:{basic,enhanced},
  medianValue, schoolRate, levy, enrollment:{cur,base}, jurisdiction, town, county_leg,
  board_url, source_refs:{<field>:{url,vintage,verified}}}}}`. NOT a flat map, and
  source_refs are OBJECTS not strings. index.html reads data.districts + refs.<f>.url.
  Money refresh uses ONLY starCredit (Enhanced-Basic = STAR dividend) + medianValue
  (transfer=0.004×, sale=/1000, label=dtfName). A field renders ONLY if its source_ref
  url is present; Elmont/VS13 have starCredit but no medianValue → STAR-only, honest.
- Playwright on python3.12 (`/Library/Frameworks/.../python3.12`, browsers cached) is the
  working browser-driver here; plain headless Chrome HANGS on the live Google-Fonts page
  (screenshots must go through Playwright over an http.server, not file://).
- **Nassau school-district layering (critical):** the geocoder "Unified School Districts"
  layer is EMPTY for Nassau's elementary + CHSD districts (Elmont, Valley Stream 13/24/30,
  Bellmore, Franklin Square...). Those return an "Elementary School Districts" entry (the
  local district, where school tax + STAR sit) plus a "Secondary School Districts" entry
  (the Central High School District it pairs with). pick() must read unified, elementary,
  AND secondary; resolved school = unified||elementary; CHSD = secondary. Verified NAMEs:
  Elmont UFSD within Sewanhaka CHSD; Valley Stream UFSD 13 within Valley Stream CHSD;
  Bellmore UFSD within Bellmore-Merrick CHSD. districts.json MUST key elementary rows by
  the Census elementary NAME (or carry geoid/chsd) or the lookup misses to honest baseline.
  Landed in PR #12 commit 45590a3.
