---
name: wave1-sent-and-sendlog
description: Wave 1 went out 2026-08-12 (7 sends from jeff@jeffpinto.com); SENDLOG.md is the source of record for sends, MANIFEST.md only stages drafts
metadata:
  type: project
---

Wave 1 of the Aug-1 launch outreach was sent **2026-08-12**, 11 days after the manifest's
~Jul 29 target and 11 days after the site went public. Seven recipients: Palumbo SD-1,
NSSBA, Davis LD-1, Griffin AD-21, Canzoneri-Fitzpatrick SD-9, Bynoe SD-6, RVC BOE. All from
`jeff@jeffpinto.com`. Per-recipient timestamps and subjects are in
`.claude/scratch/outreach-aug1/SENDLOG.md`.

**Why the send log exists:** `MANIFEST.md` stages drafts and has no send state, so a later
session reading it cannot tell a contacted official from an untouched one, and would re-draft
or double-send. The business CRM (`outbound_with_jeff_and_marv/crm.db`) is deliberately NOT
the home for this: it carries zero RVC rows and its account/tier/wave machinery is built for
consulting sales, so officeholders in it would pollute the Scenario B metrics. Jeff chose the
repo send log on 2026-08-12.

**How to apply:**
- Any send, for any wave, gets a row in `SENDLOG.md` read off the Gmail sent box, not off the
  drafts. Subjects and bodies get edited by hand at send time and the drafts do not record that.
- Two defects shipped in Wave 1 and will recur unless drafts change: the `[street address]`
  placeholder went out **unfilled** (the constituency line and signature both), and pre-launch
  tense survived into an 11-days-post-launch send ("goes public on August 1"). Fill the address
  in the draft file at authoring time; never leave a placeholder for send time. Re-tense any
  staged draft against the actual send date before it goes.
- Drafts created 2026-08-12 and not yet sent: Rep. Gillen NY-4 (`replauragillen@mail.house.gov`,
  address supplied by Jeff, since the House contact page still publishes no email) and Nassau
  Legislator **Olena Nicks** LD-5 (`onicks@nassaucountyny.gov`, secondary-sourced, not primary
  verified; the verified route is her county contact form). Jeff calls Nicks "Olena Douglass";
  no public record of that surname exists and he confirmed the identity anyway.
- Nicks is LD-5 (Uniondale/Westbury), so Jeff is not her constituent. Her draft says so outright
  and hooks the county data ask to her Finance and Veteran & Senior Affairs assignments instead.
  Never let a letter to her imply constituency; that is the one credibility asset the campaign has.
