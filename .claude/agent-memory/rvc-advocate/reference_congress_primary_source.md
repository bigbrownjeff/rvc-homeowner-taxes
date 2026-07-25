---
name: congress-primary-source
description: Congress.gov HTML is unreachable to all automation; the GPO GovInfo BILLSTATUS bulk XML is the citable primary for federal bill facts
metadata:
  type: reference
---

**Congress.gov HTML cannot be fetched by anything**, verified 2026-07-24 across three
methods: 403 to `curl` (even with a browser User-Agent), 403 to WebFetch, and a
Cloudflare interstitial (`<title>Just a moment...</title>`) to headless Chrome
`--dump-dom`. `api.congress.gov` is 403 without a key, and no key is on this machine.

**The citable primary instead** is GPO's bill-status bulk feed, the same Legislative
Branch source data Congress.gov presents:

    https://www.govinfo.gov/bulkdata/BILLSTATUS/119/hr/BILLSTATUS-119hr1340.xml

It carries the full `<cosponsors><item>` list with `bioguideId`, `state`, `district`,
`sponsorshipDate`, and `sponsorshipWithdrawnDate`, plus `<sponsors>` and `updateDate`.
Vintage comes from the HTTP `Last-Modified` header. GPO republishes roughly a day after
a new cosponsorship, so a feed 2-3 days old is normal and is **not** drift by itself.

In-repo counter (rvc-homeowner-taxes): `scripts/count_hr1340_cosponsors.py`, plain
stdlib, `--json` flag, exit 2 if the feed is unreachable. It also prints
`sponsors_inclusive` for tracker reconciliation and tests for an NY-4 cosponsor by
**district, not surname** (there is a `Rep. Gill, Brandon [R-TX-26]` on H.R. 1340, so a
"Gillen" substring match is fragile).

**Fetchable corroborating secondary:** GovTrack (`https://www.govtrack.us/congress/bills/119/hr1340`)
is plain HTML, returns 200, and rendered `147 Cosponsors` on 2026-07-24. Prefer it over
BillTrack50 in citations: BillTrack50's count is client-rendered, so its static HTML
contains no number at all and a reader following the citation cannot verify it.

Related: [[cosponsor-count-definition]]
