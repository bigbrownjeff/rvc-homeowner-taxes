#!/usr/bin/env python3
"""Count H.R. 1340 cosponsors from the GPO BILLSTATUS primary feed.

This exists because the daily posture sweep kept firing false "cosponsor drift"
discrepancies (2026-07-23 and 2026-07-24) by comparing the ledger against
third-party trackers. Trackers lag the official feed and label their totals
inconsistently: a "sponsors" total counts the lead sponsor and therefore runs
exactly one HIGHER than the cosponsor count the site cites. The fix is to stop
reading trackers for the baseline and count the primary feed directly.

The feed is GPO's bill-status bulk data over the same Legislative Branch source
data Congress.gov presents. Congress.gov's own HTML bot-blocks automated fetches
(403 to curl and to WebFetch, Cloudflare challenge to headless Chrome), so this
feed is the citable primary.

Usage:
    python3 scripts/count_hr1340_cosponsors.py            # human-readable
    python3 scripts/count_hr1340_cosponsors.py --json      # machine-readable

Exit codes: 0 = counted, 2 = feed unreachable or unparseable (a sweep that
cannot verify is not green; treat as a DISCREPANCY, not a pass).
"""

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://www.govinfo.gov/bulkdata/BILLSTATUS/119/hr/BILLSTATUS-119hr1340.xml"

# The federal ask targets RVC's own member. Test by district, not by surname:
# there is already a "Rep. Gill, Brandon [R-TX-26]" on this bill, so a substring
# match on "Gillen" is fragile in both directions.
RVC_STATE, RVC_DISTRICT = "NY", "4"


def fetch(url=FEED, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "rvc-taxes-posture-sweep"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Last-Modified")


def main():
    try:
        raw, last_modified = fetch()
        bill = ET.fromstring(raw).find("bill")
    except Exception as exc:  # noqa: BLE001 - any failure to reach/parse is a discrepancy
        print("UNREACHABLE: could not fetch or parse %s: %s" % (FEED, exc), file=sys.stderr)
        return 2

    def txt(node, path):
        return (node.findtext(path) or "").strip()

    items = bill.find("cosponsors")
    items = items.findall("item") if items is not None else []
    withdrawn = [i for i in items if txt(i, "sponsorshipWithdrawnDate")]
    live = [i for i in items if not txt(i, "sponsorshipWithdrawnDate")]

    sponsors = bill.find("sponsors")
    sponsors = sponsors.findall("item") if sponsors is not None else []
    lead = sponsors[0] if sponsors else None
    lead_id = txt(lead, "bioguideId") if lead is not None else None

    rvc_member = [
        txt(i, "fullName")
        for i in live
        if txt(i, "state") == RVC_STATE and txt(i, "district") == RVC_DISTRICT
    ]

    result = {
        "feed": FEED,
        "cosponsors": len(live),
        "cosponsor_records": len(items),
        "unique_bioguide_ids": len({txt(i, "bioguideId") for i in live}),
        "withdrawn": len(withdrawn),
        "lead_sponsor": txt(lead, "fullName") if lead is not None else None,
        "lead_sponsor_also_cosponsor": lead_id in {txt(i, "bioguideId") for i in live},
        # What a tracker showing a "sponsors" total should read. Relational, not
        # hard-coded: tracker == sponsors_inclusive is agreement, never drift.
        "sponsors_inclusive": len(live) + (0 if lead is None else 1),
        "ny_cosponsors": sorted(
            txt(i, "fullName") for i in live if txt(i, "state") == RVC_STATE
        ),
        "rvc_district_cosponsor": rvc_member[0] if rvc_member else None,
        "latest_cosponsorship": max(
            (txt(i, "sponsorshipDate") for i in live), default=None
        ),
        "feed_update_date": txt(bill, "updateDate"),
        "feed_last_modified": last_modified,
    }

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
        return 0

    print("H.R. 1340 (119th) cosponsors, counted from the GPO BILLSTATUS primary feed")
    print("  cosponsors (live):      %d" % result["cosponsors"])
    print("  cosponsor records:      %d" % result["cosponsor_records"])
    print("  unique bioguide IDs:    %d" % result["unique_bioguide_ids"])
    print("  withdrawn:              %d" % result["withdrawn"])
    print("  lead sponsor:           %s" % result["lead_sponsor"])
    print("  also a cosponsor:       %s" % result["lead_sponsor_also_cosponsor"])
    print("  sponsors-inclusive:     %d  <- what a tracker's 'Sponsors (N)' should read"
          % result["sponsors_inclusive"])
    print("  NY-%s cosponsor:         %s"
          % (RVC_DISTRICT, result["rvc_district_cosponsor"] or "none (expected)"))
    print("  NY cosponsors:          %s" % ", ".join(result["ny_cosponsors"]))
    print("  latest cosponsorship:   %s" % result["latest_cosponsorship"])
    print("  feed updateDate:        %s" % result["feed_update_date"])
    print("  feed last-modified:     %s" % result["feed_last_modified"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
