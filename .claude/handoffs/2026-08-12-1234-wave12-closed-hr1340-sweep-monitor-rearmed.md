# Handoff — Waves 1 and 2 closed, H.R. 1340 147 to 150, daily monitor re-armed
**Date:** 2026-08-12 · **Project:** rvc-homeowner-taxes (session started from `~`; a small
jeffpinto-site change rode along at the top, see the last section)

## Goal
Jeff had sent Wave-1 emails that morning and asked for three things: log the work, draft a
Gmail note to Rep. Laura Gillen, and draft one to a Nassau legislator he knows personally.
Mid-session he added: fix the ledger and the site, and re-arm the daily monitor. It ended
with Waves 1 and 2 fully closed.

## What got done

**Sixteen sends across four batches, all confirmed off the Gmail sent box.**
- 14:53-15:03 UTC (Jeff, before the session): Palumbo SD-1, NSSBA, Davis LD-1, Griffin AD-21,
  Canzoneri-Fitzpatrick SD-9, Bynoe SD-6, RVC BOE.
- 15:29-15:32: Gillen NY-4 (`replauragillen@mail.house.gov`, address Jeff supplied) and Nassau
  Leg. **Olena Nicks** LD-5 (`onicks@nassaucountyny.gov`).
- 16:17-16:19: AARP NY, LIBOR, LIHP, Vision LI, LWV Nassau, RVC Chamber, plus the Village of
  RVC via its resident-feedback webform.
- 16:23 and 16:32: the Vision LI resend after a bounce, then Zublionis and Gaven.

**The send log now exists** at `.claude/scratch/outreach-aug1/SENDLOG.md`. It is
**machine-local and NOT in git** (see dead ends). MANIFEST.md now states that up front so a
fresh clone does not read its absence as "nothing sent."

**H.R. 1340 corrected 147 to 150 (PR #41, #42), ledger first.** The repo's own
`scripts/count_hr1340_cosponsors.py` read 150 records, 150 unique bioguide IDs, 0 withdrawn,
no NY-4 cosponsor; GPO feed published 2026-08-04, latest cosponsorship 2026-08-03; GovTrack
corroborated 150. Row `f-hr1340` changed first, then every page in its used-on column: brief
fact strip, the prewritten federal letter in the action kit, deck body + roster + endnote 11,
`assets/instruments-manual.json` (how coverage.html gets the number), and the two outreach
drafts carrying it. Tracker note moved 148 to 151. PDF re-rendered, drift gate passed,
deployed, verified cache-busted on `/validation`, `/`, `/deck`, the JSON and the PDF
(byte-identical to the repo copy). #42 caught the vintage labels still saying July 24.

**The daily monitor is re-armed (PR #41)** and proven with a real `launchctl kickstart` run
that returned `OVERALL: GREEN` on all four checks
(`reports/posture-sweep-2026-08-12.md`). Two fixes:
1. The 2026-08-02 auto-retire is **gone**. It killed the sweep on 08-09 and the count drifted
   unwatched.
2. CHECK 1 no longer hard-codes the expected count. It reads `LEDGER_HR1340` out of
   `site/validation.html` row `f-hr1340` at run time and fails loudly (SWEEP_DRY-guarded) if
   the row cannot be parsed. Negative-tested by rewording the row.

**Street address removed from the system (PR #43).** All eight Wave-1 signatures end at
`Rockville Centre, NY 11570`; MANIFEST pre-send step 1 now forbids a placeholder instead of
demanding one. Global memory `no-street-address-in-drafts`.

**Seven unsent Wave-1 drafts and two Wave-2 drafts re-tensed (PR #44, #47)** before being
staged as Gmail drafts. BOE duplicates (Messier, Joyce, Dorrego) dropped by Jeff's call and
tagged DO NOT SEND.

## What worked (and why)

**Asking three decision-shaped questions before doing anything.** CRM target, Gillen routing,
Olena's identity. All three had answers only Jeff had, and guessing any of them would have
wasted the whole session's output.

**Reading the sent box instead of trusting the drafts.** It surfaced that Jeff rewrites
subjects and openers by hand at send time, that the Davis note got personalized, and that
`[street address]` had shipped unfilled. None of that is knowable from the draft files.

**Running the repo's own counter rather than eyeballing a tracker.** The definitional trap
(cosponsors excludes the lead sponsor) is already encoded in the script and the ledger row.

**Verifying before asserting, twice, both times with a payoff.** Confirming both quotes were
actually live on `/voices` before telling two superintendents they were quoted in full; and
re-fetching both district addresses the same day.

## What didn't / dead ends

**`git add -A` silently dropped SENDLOG.md.** `~/.gitignore_global` excludes
`**/.claude/scratch/`, so PR #40 merged carrying only the MANIFEST edits while the file it was
named for was never committed. The 38 files already in that directory are tracked only because
they were force-added before the policy. **Do not `git add -f` past it** (memory
`scratch-stays-local`); machine-local is right anyway, since this repo is public and the log
carries candid operating detail. The file was rescued out of the worktree before removal.

**A "VERIFIED" address stamp is only as good as its date.** `outreach@visionli.org` was
verified 07-20 off Vision Long Island's own contact page, which still lists it. It bounced
`550 5.1.1` fourteen seconds after send. The two addresses re-checked that morning both
delivered. Rerouted to `ea@visionli.org` (same domain, live Google MX, so the mailbox died not
the domain), which delivered. PR #46 records the bounce, fallback
`outreach@visionlongisland.org`, and the phone.

**Gmail-API drafts lag the iOS Mail drafts list by minutes.** Cost a round trip when Jeff
screenshotted an empty-looking Drafts folder three minutes after creation. They exist
server-side immediately; check Gmail on the web.

**`gh pr merge --squash --delete-branch` fails from a worktree** with "'main' is already used
by worktree". The merge itself succeeds; only the local branch-delete step dies. Verify with
`gh pr view N --json state` before re-running anything.

**Fresh PRs report `mergeable: UNKNOWN`** for a few seconds. Poll before merging.

## Key decisions

- **Send log in the repo, not the business CRM** (Jeff). `outbound_with_jeff_and_marv/crm.db`
  has zero RVC rows and its account/tier/wave machinery is built for consulting sales;
  officeholders in it would pollute the Scenario B metrics.
- **BOE duplicates dropped, not deferred** (Jeff). Three trustees share `boe@rvcschools.org`,
  which got the Wave-1 Board note the same morning.
- **No sunset on the monitor.** Retiring it when the site went public was backwards: Aug 1 is
  when legislative staff started reading the figures.
- **Cited 150 in the Gillen letter while the site still said 147**, then swept the site the
  same hour. The ledger states its own verified date, so the gap was self-explaining, but the
  sweep closed it before anything else went out.
- **Nicks accepted on Jeff's say-so.** No public record of an "Olena Douglass" exists;
  `onicks@nassaucountyny.gov` is secondary-sourced. Her letter states outright that Jeff is
  not her constituent (LD-5 is Uniondale/Westbury) and hooks the ask to her Finance and
  Veteran & Senior Affairs seats.

## How to reproduce / pick up

```bash
cd ~/Projects/rvc-homeowner-taxes
cat .claude/scratch/outreach-aug1/SENDLOG.md        # source of record, local only
python3 scripts/count_hr1340_cosponsors.py          # the primary-source counter
SWEEP_DRY=1 scripts/daily_posture_sweep.sh          # side-effect-free rehearsal
launchctl print gui/$UID/com.jeffpinto.rvc-posture-sweep
scripts/check_pdf_drift.sh                          # pre-deploy gate; --fix to re-render
npx wrangler pages deploy --project-name rvc-taxes  # direct-upload: merge is NOT deploy
```
Deploy verification is always cache-busted: `curl -s "<url>?cb=$RANDOM"`.

## Open threads / next steps

1. **Wave 3, the public lane, is the only thing left.** `w3-01-community-email` has no
   recipients prefilled; `w3-02-linkedin` is re-grounded to 150; **`w3-03-bluesky` is untouched
   and still carries pre-launch framing** (295 chars, re-tense before posting).
2. **Zero replies so far**, across sixteen sends. The first one is the real test.
3. **Watch for late bounces**, especially the four org addresses verified 07-20 and not
   re-fetched (`nyaarp@aarp.org`, `pr@lirealtor.com`, `info@lihp.org`) plus
   `info@lwvofnassaucounty.org`, which is corroborated rather than primary-verified.
4. **The monitor fires 07:00 daily.** First unattended run is 2026-08-13. If a card lands via
   `failtask`, the report is in `reports/posture-sweep-YYYY-MM-DD.md`.
5. **LIBOR optics** stay Jeff's call: a realtor board benefits from more transactions, so
   listing them publicly as a backer could read as self-interested. Sending was harmless.
6. **rvc-advocate persona not yet evolved.** This session's durable lessons live in
   `.claude/agent-memory/rvc-advocate/wave1-sent-and-sendlog.md` and global memory
   `no-street-address-in-drafts`. Promoting the VERIFIED-has-a-date rule and the
   no-sunset-on-monitors rule into `persona.md` via `/persona-author` is the outstanding step.
7. **Beacon retrofit** landed as PR #45 from a parallel lane (memory `beacon-from-day-one`);
   not this session's work but it is in the same commit range.

## Rode along: jeffpinto.com

Before the RVC work, one unrelated change: `/notes/the-list/` retitled to "The List - aka an
old school homage" with the dek opening "Welcome to my mailing list... in the style of Raymond
Chandler:" after feedback that the noir voice read as opaque. jeffpinto-site PR #228, merged
and live on both the note page and the notes wall. Body, dates and update stamps untouched.
