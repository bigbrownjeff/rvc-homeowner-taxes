# Handoff: Griffin meeting, A6032 Governor card, sweep auth — 2026-08-21

Session ran as **rvc-advocate**. Started ~09:00 with 90 minutes before an in-person meeting
Jeff did not yet have prep for, and ended with three PRs merged, a deploy, and the campaign's
first legislator commitment.

## What we set out to do

Jeff asked for: adopt the persona, read his jeff@ mail, draft replies to Judy Griffin's aide
JT, and build a mobile meeting prep. Mid-session it expanded into shipping what Griffin
accepted in the room, and then into a monitor outage he spotted.

## What actually got done

1. **Meeting prep** (artifact `b45c2b56-193b-4c0b-8e12-a0f02bde4ffd`) built and delivered with
   ~45 minutes to spare. Meeting was **today 10:30am, 74 N. Village Ave**, discovered by
   reading the inbox: Andrea Wilkins had scheduled it the previous afternoon.
2. **The meeting went ~1 hour.** Outcomes in
   `.claude/agent-memory/rvc-advocate/griffin-meeting-2026-08-21.md` (read that first).
   Short version: she is personally digging into the A5288 stall, she accepted the A6032
   letter-card offer, the parcel-data ask landed flat, and she talked at length about an
   energy bill she thought was badly written and backed anyway.
3. **PR #62** — Governor card asking Hochul to sign A6032, plus ledger row `#f-a6032` and a
   `#watch` retirement entry. Merged and **deployed**; live and verified.
4. **PR #63** — sweep survives headless auth loss (token from `scripts/.env` + auth preflight).
5. **PR #64** — corrected the remedy text #63 put in the preflight card, which was wrong.
6. **Follow-up notes** drafted for JT and Judy (artifact
   `0eb737c0-030a-4024-991b-37a98c86e85f`). **Neither has been sent yet.**

## What worked, and why

- **Verify-before-asserting paid off four times.** Every one of these would have been an error
  in front of legislative staff: the fiscal-note theory for A5288 (the sponsor memo says
  "FISCAL IMPLICATIONS: None"); the assumption A6032 had reached the Governor (it has not);
  the STAR credit/exemption argument (needed the 2015 cutoff to be exact); and the `gh` scope
  (already present, refresh was a dead end).
- **The winning frame was structural, not rhetorical.** A6032 and A5288 amend the *same
  statute* (RPTL §425) and went to the *same committee*; she moved hers out, A5288 never got a
  vote. Pairing "her bill fixes the front door, A5288 fixes the exit" did more work than any
  argument about housing.
- **Lead with a give.** The A6032 letter-card offer went first and was accepted; every ask
  after it was easier. JT had already flagged it to Andrea and Griffin before Jeff walked in.
- **Answering her own open question was the highest-value artifact.** She had asked JT nine
  days earlier why A5288 had not passed. The lineage back to **S.3246 (1999-2000)**, not 2019,
  was work her office owed her.

## Dead ends and things I got wrong

- **The coordination theory.** Jeff noticed §121 froze in 1997 and the NY bill starts in 1999
  and asked whether something locked it down. It does not hold: TRA97 was a *liberalization*
  (repealed §1034 rollover, killed the age-55 one-time $125K cap), and the 1999 NY bill is
  explained entirely by STAR's own 1997 enactment. The two signings are **two days apart**
  (Aug 5 and Aug 7, 1997) and unrelated — two budget calendars. Use the frozen-threshold frame
  instead; it needs no villain and is bipartisan.
- **`claude /login` and `gh auth refresh -s read:project`** were both wrong advice, handed to
  Jeff stacked in one block. `/login` is an in-session slash command; the gh token already had
  `project`. New standing rule from this: **one copy-paste command per block, verified first.**
- **Refuted hypotheses for the sweep outage** (do not re-inherit): reboot/cold keychain
  (uptime 25 days), keychain auto-lock (`no-timeout`), missing gh scope (present and working).
- **Browser verification burned ~10 rounds.** Three separate harness traps, all now written up
  in the agent-memory note: `clipboard.readText()` freezes CDP on the live https origin but
  *not* on localhost; an unfocused tab makes `writeText` reject and look like a broken button;
  and `computer` click coordinates are in **scaled screenshot space**, not CSS pixels
  (1918x1195 viewport vs 1204x984 screenshot), so rect-derived clicks miss by hundreds of px.
  The decisive cheap check was `git show <sha> -- site/index.html` to prove the copy path was
  untouched.

## Key decisions

- **The A6032 letter asks her to sign it "when it reaches your desk"**, not to beat a deadline.
  The bill has not been delivered, so the 10-day/30-day clock has not started. Undelivered by
  year end = dead with the session.
- **The card is explicitly time-bound.** `#watch` says retire it the day A6032 is signed or
  vetoed. Per the 08-12 no-sunset lesson, that is a decision someone makes, not a date baked in.
- **JT's "seniors wait up to two years" gloss stays off the site.** It is not in the bill text.
  The ledger row says so; the letter states the statutory mechanism only. Note 1 raises it with
  him gently rather than correcting him publicly.
- **The token goes in `scripts/.env`** (already gitignored, already holds the reply watcher's
  creds), never in the checked-in plist.

## Repro / commands

```
# read jeff@ mail (OAuth creds already in scripts/.env)
python3 <scratch>/gmail_read.py "<gmail query>" 15 --full

# sweep, manually, correct syntax (--tag is a FLAG, not positional)
~/.claude/bin/runlog --tag rvc-posture-manual /bin/zsh scripts/daily_posture_sweep.sh

# sweep failure path, testable now
RVC_REPO=$PWD RVC_CLAUDE_BIN=/tmp/failing-stub SWEEP_DRY=1 zsh scripts/daily_posture_sweep.sh

# deploy (direct-upload project: merge != deploy)
npx wrangler pages deploy
```

Verification gate used for #62: `scripts/check_site_integrity.py` PASS, `node --check` on the
kit script, local serve + real-browser action-kit run, then cache-busted live checks and a
browser run on the custom domain.

## Open threads

1. **Send the two notes** in artifact `0eb737c0-030a-4024-991b-37a98c86e85f`. JT is waiting on
   the first; he said he would circle back with the district team after the meeting.
2. **`claude setup-token`** then append `CLAUDE_CODE_OAUTH_TOKEN=` to `scripts/.env`. Optional
   hardening; auth works today, this protects against the next self-update.
3. **Ask JT which energy bill** Judy kept returning to. Possible opening to become the office's
   outside analyst rather than a one-issue constituent.
4. **Why `gh` failed inside the 08-17 launchd run** is still unexplained and not reproducible.
5. **STAR restriction history** (2011 growth cap, 2016 credit conversion, income ceilings)
   could not be re-verified — `tax.ny.gov/pit/property/star/star-changes.htm` 404s. Do not cite
   those years until sourced.
6. **Retire the Governor card** when A6032 is signed or vetoed, and update `#f-a6032`.
7. **The token hardening probably belongs in the other launchd jobs** that shell out to
   `claude`, since they inherit the same self-update exposure.
