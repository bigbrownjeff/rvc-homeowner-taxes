#!/bin/zsh
# Daily accuracy sweep for the RVC Housing x Schools campaign (rvc-taxes.jeffpinto.com).
# LOCAL replaces cloud: the prior cloud routine ran in a sandbox with no outbound
# network, so it never fetched congress.gov / nysenate.gov / the live site and never
# delivered a single report. Running here on Jeff's Mac guarantees egress + freshness,
# mirroring the estate precedent (outbound_with_jeff_and_marv/scripts/run_daily_sweep.sh).
#
# What it does daily (07:00 America/New_York, via com.jeffpinto.rvc-posture-sweep):
#   1. H.R. 1340 cosponsor count + Rep. Gillen (NY-4) status.
#   2. NY S3309 / A5288 posture + Sen. Palumbo (SD-1) prime-sponsor / no-cosponsor.
#   3. Officeholders still hold their seats (Bynoe SD-6, Canzoneri-Fitzpatrick SD-9,
#      Palumbo SD-1, Griffin AD-21, Davis LD-1).
#   4. Deploy drift: LIVE /validation + /deck figures match the repo copies.
#   5. PDF drift (shell, pre-deploy gate): the downloadable handout still renders
#      from the current deck. See scripts/check_pdf_drift.sh.
# It DETECTS and REPORTS only. It NEVER edits site figures; validation.html is the
# facts ledger and the single source of truth.
#
# Delivery: a dated report lands in reports/posture-sweep-YYYY-MM-DD.md every run.
# On ANY discrepancy or a failed run it files a board card via failtask (that replaces
# the cloud routine's email). ALL-GREEN days: report file only, no card.
#
# Dry check (no tokens burned): SWEEP_DRY=1 scripts/daily_posture_sweep.sh
# zsh-safe: null-glob (N) on any glob; no use of the reserved $status.
set -o pipefail

REPO="${RVC_REPO:-/Users/jeffpinto/Projects/rvc-homeowner-taxes}"   # overridable so a worktree can test the gates
CLAUDE_BIN="/Users/jeffpinto/.local/bin/claude"      # absolute: launchd PATH lacks it (lantern PR #19)
FAILTASK="$(command -v failtask || echo "$HOME/.claude/bin/failtask")"
export PATH="/Users/jeffpinto/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

TODAY="$(date +%Y-%m-%d)"
TODAY_NUM="$(date +%Y%m%d)"
REPORT="reports/posture-sweep-${TODAY}.md"
LOG="/Users/jeffpinto/Library/Logs/rvc-posture-sweep.log"

# --- Auto-retire: the site goes public Aug 1, 2026; the campaign value of this
# sweep ends then, so it retires 2026-08-02. (It was briefly extended to 08-10 as a
# persona-graph shadow-cutover pilot; that migration is NOT being pursued -- the
# rvc sweep needs browser-grade fetch for nysenate.gov, which persona-graph's
# no-evasion design can't provide -- so the campaign-driven date is restored.) ----
if [[ "$TODAY_NUM" -gt 20260802 ]]; then
  "$FAILTASK" rvc-taxes "Retire the RVC posture sweep (past 2026-08-02 sunset)" \
    --dedupe-key rvc-posture-retire --severity warn \
    --detail "The daily posture sweep passed its 2026-08-02 sunset (site went public Aug 1). Unload + remove: launchctl bootout gui/\$UID/com.jeffpinto.rvc-posture-sweep; rm ~/Library/LaunchAgents/com.jeffpinto.rvc-posture-sweep.plist; delete scripts/daily_posture_sweep.sh. See $LOG"
  echo "retired: past 2026-08-02 sunset ($TODAY)"
  exit 0
fi

cd "$REPO" || { "$FAILTASK" rvc-taxes "RVC posture sweep: repo cd failed" --dedupe-key rvc-posture-run-failed --severity error --detail "Could not cd to $REPO. See $LOG"; exit 1; }

# git pull is best-effort: a stale checkout still sweeps live sources, but a persistent
# pull failure means the deploy-drift baseline is stale, so warn-file it.
git pull --ff-only 2>/dev/null || {
  echo "WARN: git pull failed; sweeping on the local checkout" >&2
  "$FAILTASK" rvc-taxes "RVC posture sweep: git pull failed (stale drift baseline)" \
    --dedupe-key rvc-posture-git-pull --severity warn \
    --detail "git pull --ff-only failed in daily_posture_sweep.sh; deploy-drift compared live vs a possibly-stale repo copy. See $LOG"
}

# --- PDF drift, pure shell, no tokens. The downloadable handout linked from / and
# /deck is a rendered snapshot of deck.html; edit the deck without re-rendering and
# legislators download corrected-on-the-page figures that are stale in the PDF.
# Exit 1 = drift, exit 2 = the check could not run (both file a card; a check that
# cannot verify is not green, same rule as the legislative checks below). Never
# aborts the sweep: the accuracy checks matter more than the artifact. ------------
"$REPO/scripts/check_pdf_drift.sh"
PDF_RC=$?
if [[ "${SWEEP_DRY:-0}" = "1" ]]; then
  echo "DRY: PDF drift check exited $PDF_RC; no card filed"
elif [[ $PDF_RC -eq 1 ]]; then
  "$FAILTASK" rvc-taxes "RVC: downloadable PDF is stale vs deck.html" \
    --dedupe-key rvc-pdf-drift --severity warn \
    --detail "site/deck.html changed without re-rendering site/RVC_Briefing_8pager.pdf, so /RVC_Briefing_8pager.pdf serves figures the live deck no longer shows. Fix: scripts/check_pdf_drift.sh --fix, then commit and deploy. See $LOG"
elif [[ $PDF_RC -ne 0 ]]; then
  "$FAILTASK" rvc-taxes "RVC: PDF drift check could not run" \
    --dedupe-key rvc-pdf-drift-broken --severity warn \
    --detail "scripts/check_pdf_drift.sh exited $PDF_RC (missing html2pdf, missing pdftotext, or a failed render), so PDF staleness went unverified for ${TODAY}. See $LOG"
fi

# ---------------------------------------------------------------------------------
# The headless prompt. Judgment-heavy legislative checks against LIVE primary sources.
# Claude writes the dated report and ends it with exactly one machine-readable line:
#   OVERALL: GREEN     (everything matches expectations)
#   OVERALL: DISCREPANCY  (something drifted, or a source could not be reached)
# The shell reads that verdict and does the loud delivery (below). Claude does not
# file board cards; it detects and reports only.
# ---------------------------------------------------------------------------------
read -r -d '' PROMPT <<PROMPT_EOF
Adopt the rvc-advocate persona (installed at ~/.claude/agents/rvc-advocate.md; read
and become it before anything else). Within it, you are the daily accuracy sweep
for the RVC Housing x Schools campaign
(rvc-taxes.jeffpinto.com). Today is ${TODAY}. Verify four things against LIVE
primary sources, then write ONE report file. You DETECT and REPORT only. You must
NOT edit any site file or any figure; validation.html is the facts ledger.

Ground every claim: fetch the actual source (WebFetch/WebSearch). Never assert a
count or a seat from memory. If a source cannot be reached after a real attempt,
that check is a DISCREPANCY (a sweep that cannot verify is not green).

Repo copies of record to read for the deploy-drift comparison:
  site/validation.html  (the ledger; rows #f-hr1340, #f-s3309, #f-office)
  site/deck.html
  site/index.html

CHECK 1 - H.R. 1340 (federal Section 121 fix).
  Expected: 147 cosponsors; Rep. Laura Gillen still holds NY-4 and is NOT a cosponsor.

  THE BASELINE IS THE PRIMARY SOURCE, NOT A TRACKER. Third-party trackers lag the
  official feed and label their totals inconsistently, so a tracker mismatch alone
  is NOT a discrepancy. Do not eyeball a tracker; count the primary feed by running
  the repo's counter, which reads the GPO BILLSTATUS bulk feed (the same Legislative
  Branch source data Congress.gov presents):

    python3 scripts/count_hr1340_cosponsors.py

  Report its 'cosponsors (live)' number, its withdrawn count, its NY-4 line, and
  its feed vintage. Exit code 2 means the feed could not be reached or parsed:
  that IS a discrepancy (a sweep that cannot verify is not green).

  DEFINITIONAL TRAP (this produced two days of false drift, 2026-07-23 and 07-24):
  "cosponsors" EXCLUDES the lead sponsor (Panetta, CA-19); "sponsors" INCLUDES him,
  so a tracker's "Sponsors (N)" total runs exactly ONE HIGHER than the cosponsor
  count this site cites. The rule is relational, never a hard-coded number:
  tracker total == the script's 'sponsors-inclusive' value is AGREEMENT; only some
  other relationship is drift. Do not read the expected count off a tracker, and do
  not treat a tracker that is one higher as movement.

  VINTAGE IS NOT DRIFT. GPO republishes within about a day of a new cosponsorship,
  so a feed published before today is normal. A feed older than the ledger's
  verified date is NOT a discrepancy by itself - report the dates and say so plainly.

  DISCREPANCY only if: the counter yields a live cosponsor count other than 147, or
  its withdrawn count is not 0, or a NY-4 cosponsor appears (Rep. Gillen is the
  federal ask's target and must stay off the bill), or she no longer holds NY-4
  (verify on her own House member page, https://gillen.house.gov/ , not news), or
  the counter exits non-zero.

CHECK 2 - NY S3309 and A5288 (exemption continuity in a move year).
  Expected posture (nysenate.gov / nyassembly.gov): S3309 cleared Senate Aging 7-0
  (Apr 21 2026) and died in Finance; A5288 never left Assembly Real Property
  Taxation; both to be re-advanced in 2027. S3309 prime sponsor is Sen. Anthony
  Palumbo (SD-1) with NO co-sponsors. DISCREPANCY on any NEW action on either bill,
  a changed sponsor, or any co-sponsor now listed on S3309.

CHECK 3 - Officeholders each still hold the stated seat (verify on the chamber's
  own site, not news): Sen. Siela Bynoe (SD-6), Sen. Patricia Canzoneri-Fitzpatrick
  (SD-9), Sen. Anthony Palumbo (SD-1), Assembly AD-21 = Judy Griffin, Nassau County
  Legislator Scott Davis (LD-1). DISCREPANCY if any seat has changed hands.

CHECK 4 - Deploy drift. WebFetch https://rvc-taxes.jeffpinto.com/validation and
  https://rvc-taxes.jeffpinto.com/deck and confirm the deployed figures (the
  cosponsor count, the officials roster, the S3309/A5288 posture) match the repo copies you
  read above. DISCREPANCY if the live site shows a figure the repo does not, or
  vice versa. (Prose/markdown formatting differences are fine; compare the numbers
  and names, not the exact HTML.)

Then WRITE the report to this exact path (overwrite if it exists):
  ${REPORT}
Format: a markdown heading '# RVC Posture Sweep - ${TODAY}', then one section per
check with Expected / Observed / Sources (the URLs you fetched) / Verdict
(GREEN or DISCREPANCY with a one-line reason). Then a '## Discrepancies' section
(the word 'none' if all green). The FINAL line of the file must be exactly one of:
  OVERALL: GREEN
  OVERALL: DISCREPANCY
Keep it factual and terse. No em dashes or en dashes anywhere in the report.
PROMPT_EOF

if [[ "${SWEEP_DRY:-0}" = "1" ]]; then
  echo "DRY: prompt built for ${TODAY} ($(print -r -- "$PROMPT" | wc -l | tr -d ' ') lines); report would land at $REPORT; skipping the run"
  exit 0
fi

# Headless run. Read-only research tools plus Write for the single report file.
"$CLAUDE_BIN" -p "$PROMPT" \
  --model sonnet \
  --allowedTools "WebSearch" "WebFetch" "Read" "Grep" "Glob" "Write" \
  --max-turns 60 || {
  "$FAILTASK" rvc-taxes "RVC posture sweep: headless run failed" \
    --dedupe-key rvc-posture-run-failed --severity error \
    --detail "The headless Claude run exited nonzero; no verified report for ${TODAY}. Egress or the claude CLI path under launchd is the first suspect. See $LOG"
  exit 1
}

# --- Delivery gate. The report is the artifact; a discrepancy or a missing/verdictless
# report is the loud signal. -------------------------------------------------------
if [[ ! -f "$REPORT" ]]; then
  "$FAILTASK" rvc-taxes "RVC posture sweep: no report written for ${TODAY}" \
    --dedupe-key rvc-posture-run-failed --severity error \
    --detail "The headless run exited 0 but $REPORT was not written; the sweep did not complete its checks. See $LOG"
  exit 1
fi

VERDICT="$(grep -E '^OVERALL: (GREEN|DISCREPANCY)$' "$REPORT" | tail -1)"
if [[ -z "$VERDICT" ]]; then
  "$FAILTASK" rvc-taxes "RVC posture sweep: report has no OVERALL verdict (${TODAY})" \
    --dedupe-key rvc-posture-run-failed --severity error \
    --detail "$REPORT exists but has no 'OVERALL: GREEN|DISCREPANCY' line; treat as an incomplete run. See $REPORT"
  exit 1
fi

if [[ "$VERDICT" == "OVERALL: DISCREPANCY" ]]; then
  DISC="$(awk '/^## Discrepancies/{f=1;next} f' "$REPORT" | grep -v '^$' | head -20)"
  "$FAILTASK" rvc-taxes "RVC posture sweep: DISCREPANCY found (${TODAY})" \
    --dedupe-key rvc-posture-discrepancy --severity error \
    --detail "The ${TODAY} sweep flagged a drift in campaign facts vs the ledger/live site. Re-verify same-day before anything politician-facing goes out. Details: ${DISC} -- full report: $REPORT"
  echo "DISCREPANCY filed for ${TODAY}: $REPORT"
  exit 0
fi

echo "sweep GREEN for ${TODAY}: $REPORT"
