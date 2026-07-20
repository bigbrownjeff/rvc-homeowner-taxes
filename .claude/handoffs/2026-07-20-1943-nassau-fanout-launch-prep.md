# Handoff — Nassau-wide address feature, coverage instruments, Aug 1 launch prep
**Date:** 2026-07-20 · **Project:** rvc-homeowner-taxes

## Goal
Turn the RVC-only site into an any-Nassau-address tool ("See my details"), reframe the
validation page as a facts ledger (no progress-report sausage), build the coverage/instruments
page, and stage the Aug 1 public launch (legislator/quoted-people/public email waves + daily
accuracy sweeps). Main session orchestrated; rvc-advocate agents built; every PR got an
adversarial review before merge; merges+deploys session-approved by Jeff.

## What got done (12 PRs, all merged + deployed + live-verified)
- **#8** validation.html → facts ledger: cut the four progress-report sections, new hero
  ("Every number on this site, traced to its source"), inline TOC, 4 callout stats linked to
  ledger rows; nav label → "Facts & sources" site-wide.
- **#9** governance-options process-narration redaction (agent missed 9 spots on page 1;
  fixed in review) + deck.html full redraft to Modernist/RVC synced to ledger figures.
- **#10** PPTX deck RETIRED (Jeff's call): artifact + tools/build_deck_pptx.py + orphaned
  liherald png removed; deck card points at print-ready deck.html.
- **#11** districts.json pilot (RVC / Long Beach / Locust Valley full rows + 52 STAR stubs).
- **#12** index.html: geocoder extended (county/town/village + **elementary/secondary school
  layers** — Nassau's 11 elementary + 3 CHSDs are NOT in the Census unified layer), action kit
  moved to bottom of Section 01, "Build my letters"→"See my details", flash refresh with
  reserved slots, honest Suffolk/out-of-Nassau fallback.
- **#13** **S3309 sponsor correction**: ledger had credited Canzoneri-Fitzpatrick; the bill
  page shows **Palumbo (R, SD-1)**, no co-sponsors. Fixed ledger/deck/REPS-note, withdrew the
  wrong outreach email, drafted Palumbo replacement, updated the daily sweep.
- **#14** coverage.html: 55-row harvey-ball matrix (pattern lifted from mattel-engagement
  coverage.html, RVC tokens), campaign instruments band + honest-expectations block, count-only
  engagement counters (`POST/GET /api/count` in _worker.js, KV, zero PII), validation section 13
  (7 f-nassau-* provenance rows).
- **#15/#16/#18/#19** 4-batch data fan-out (13 districts each, fragment files only).
- **#17** address-entry copy softened: WIP caution + coverage-page link + report-an-error mailto.
- **#20** integration: **55 rows, 53 with verified rates**; enhStarExemptParcels 55/55 from
  data.ny.gov `aa3i-eamx`; coverage **28% → 81%**.
- **Outreach**: 16 Gmail drafts staged (search `[WAVE-`): W1 legislators (Bynoe, Palumbo,
  Griffin, Davis, RVC BOE) + 4 orgs (AARP NY, NSSBA, LIHP, Vision LI); W2 quoted people
  (Zublionis, Gaven, Messier/Joyce/Dorrego via boe@); W3 community email. Files + MANIFEST at
  `.claude/scratch/outreach-aug1/`. Send plan: W1 ~Jul 29 · W2 ~Jul 31 · W3 Aug 1.
- **Daily sweep**: cloud routine `trig_01EFwQ6CxqL4hUMFSWMxGtxc`, 7am ET daily through Aug 1,
  Opus + repo + Gmail; emails ALL GREEN/DISCREPANCY on H.R.1340 count, S3309/A5288 posture,
  officeholders, deploy drift. Manage: claude.ai/code/routines.

## What worked (and why)
- **Pilot → method notes → fan-out.** 3-district pilot (one per jurisdiction archetype) wrote
  reusable recipes into `.claude/scratch/districts-provenance.md`; 4 parallel batch agents then
  ran 13 districts each with zero merge conflicts (fragment files only, integrator folds).
- **Cross-batch learning mid-flight**: batch 2's discoveries (LRV `/info/<PARID>/` district
  label = the in-district HARD GATE; NYSED `search_schools.php?term=`; `9500000US` elementary
  Census prefix) were relayed by SendMessage to in-flight batches — batch 3/4 then caught
  wrong-district parcels (Malverne 57 West Ave, VS30→Elmont seed) and the **modal-rate trap**
  (commercial parcels share the roll with different rates; only the STAR-verified Class-1
  parcel's own rate is authoritative).
- **Adversarial review caught real regressions**: #9's incomplete redaction; #11 and #16 stale
  branch bases that would have deleted sibling files on squash-merge; the S3309 sponsor error
  (found because the org-research agent read the bill page for support memos).
- **Coverage page as self-softening disclaimer**: the WIP caution links the gap map, which
  improves itself as data lands.
- **GIS REST SBL discovery bypasses LRV's reCaptcha** → the 52-district rate grind cost hours,
  not days.

## What didn't / dead ends
- **Ledger row f-office carried an unverified sponsor claim** that today's deck redraft then
  propagated (overwriting the deck's original correct "(Palumbo)"). Lesson: an agent following
  ledger discipline faithfully amplifies a poisoned ledger row — officials/sponsor claims need
  bill-page verification at write time, and the daily sweep now checks it.
- **3 of 5 fan-out agents violated worktree discipline** (worked in the primary checkout,
  left HEAD on their branch). Coordinator symptom: `git pull --ff-only` "diverging" while the
  real cause is HEAD ≠ main. See agent-memory `fanout-checkout-discipline.md`; the fix that
  stuck was making `git worktree add` the agent's literal FIRST command (integrator complied).
- **Cloudflare custom-domain propagation lags ~20–60s** after `wrangler pages deploy` —
  looks like a stale page; poll with an until-loop, don't diagnose. Missing assets 200 as
  index.html (SPA fallback), so a deleted file "still responds".
- **Persona subagents have NO Gmail MCP/ToolSearch** — outreach agents write files; the main
  session creates drafts. Also `gh pr create` from agents worked via `gh api` only.
- **Batch-1's background-waiter pattern stalled its finish** — resumed with "no more background
  waiters, finish inline"; that worked.

## Key decisions
- Suffolk = out of scope, honest fallback (option a). Northport/Three Village/Brentwood quotes
  stay as narrative only.
- PPTX retired rather than rebuilt; deck.html prints clean (8pp).
- North-star metric = Enhanced-STAR parcel turnover; DTF publishes only the exemption-program
  legacy count (`aa3i-eamx`; RVC 395, shrinking) — credit-side counts unpublished, so the
  coverage north-star column stays EMPTY by design (`enhStarParcels` ≠ `enhStarExemptParcels`,
  protective comment in coverage.html). No cash-back promises anywhere: stabilization +
  burden-shift framing (honest-expectations block on /coverage).
- Org outreach: AARP/NSSBA/LIHP/Vision drafted; LIBOR drafted but HELD (optics — Jeff's call);
  LIBI excluded (developer-lobby read), NYSUT held, RPA better cited than solicited.
- Officials `county_leg` column deliberately deferred (multi-LD spans); coverage shows 51%.

## How to reproduce / pick up
- Repo `~/Projects/rvc-homeowner-taxes`, deploy = `npx wrangler pages deploy` from repo root
  (direct-upload project; merge ≠ deploy), then poll the live URL.
- Data: `site/assets/districts.json` (schema in `_meta`); provenance per batch in
  `.claude/scratch/fanout/batch-N-provenance.md`; pilot recipes in
  `.claude/scratch/districts-provenance.md`.
- Plan of record: `.claude/scratch/nassau-address-feature-plan.md` (§7 acceptance suite,
  §8 coverage, §9 instruments).
- Counters: `curl https://rvc-taxes.jeffpinto.com/api/count` → `{lookup,letter,signup}`.
- Instruments manual entries: `site/assets/instruments-manual.json` (Jeff hand-edits replies/
  walkthroughs).
- Agent memories: `.claude/agent-memory/rvc-advocate/` (method files, checkout discipline,
  org outreach, deploy gotchas).

## Open threads / next steps
**Jeff:**
1. Trash stale Gmail draft (search `[WAVE-1]` "Your bill S3309" to canzoneri@ — replaced by
   Palumbo draft). 2. Fill `[street address]` in W1 drafts. 3. LIBOR call (list/brief/skip).
4. Hover→? n/a; but pre-send: strip `[WAVE-n]` prefixes.
**Agent lanes:**
- Wave-1 send prep (Jul 29): same-day re-verify H.R.1340 count + S3309/A5288 posture +
  officials (sweep emails cover this daily); webform sends for Gillen / Village RVC / Turnow
  are manual. LWV Nassau + RVC Chamber contact routes need re-confirmation before drafting.
- L5 calculator flow-back (phase 2 of plan): district selector reading districts.json; federal/
  NYS math `<script>` must stay byte-identical.
- Playwright e2e gate: install playwright, repoint hardcoded ROOT in `scripts/e2e-acceptance.py`,
  make it the standing regression (10-case suite in plan §7).
- Officials/county_leg lane (coverage 51% column) when wanted.
- "Backed by" strip ships only on written permission (f-endorse-* ledger rows); watch org replies.
- Coverage gaps: Glen Cove + Long Beach city-roll school rates (city assessor sources);
  Amityville/CSH Suffolk-side omissions are permanent by scope.
- Daily sweep: disable routine after Aug 1 (it will email a reminder).
