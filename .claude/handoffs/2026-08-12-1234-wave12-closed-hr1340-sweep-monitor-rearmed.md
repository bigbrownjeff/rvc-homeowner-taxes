# Handoff — outreach closure and source-monitor maintenance (privacy-redacted)

**Date:** 2026-08-12 · **Project:** rvc-homeowner-taxes

## Goal

Close a historical outreach phase while keeping the public facts ledger and
accuracy monitoring current.

## Retained outcomes

- A prior outreach phase was completed. Recipient identities, contact routes,
  message copy, timestamps, mailbox state, and reply details are intentionally
  absent from source control.
- A historical legislative-count correction was made using the primary-source
  workflow. Do not reuse a count from this handoff; the current
  [facts and sources page](https://rvc-taxes.jeffpinto.com/validation) is the
  public source of truth.
- The daily source monitor reads its expected value from the facts ledger rather
  than embedding a stale number. It must continue after a public launch and
  fail loudly when the ledger cannot be read.
- Public-facing artifacts were checked for ledger drift before release. The
  current release process remains the authoritative procedure.

## Durable working method

1. Verify the live, primary source before making a factual assertion.
2. Treat time-sensitive facts and public routes as day-of-use checks.
3. Keep public copy voluntary, nonpartisan, and independent; never imply
   support or consent.
4. Use an owner-authorized operational system for direct outreach and check it
   before acting. Do not recreate recipient data or campaign status from git.
5. Preserve monitoring and release checks after launch; a public site requires
   ongoing accuracy review.

## Current references

- Public evidence: [RVC facts and sources](https://rvc-taxes.jeffpinto.com/validation)
- Primary-source count workflow: `scripts/count_hr1340_cosponsors.py`
- Side-effect-free monitor rehearsal: `SWEEP_DRY=1 scripts/daily_posture_sweep.sh`
- Artifact drift check: `scripts/check_pdf_drift.sh`

## Open work

Any new public communication must use approved current copy and verified links.
Any direct contact requires owner approval and an authorized operational record;
no recipient-specific material belongs in this repository.

## Historical engineering notes retained

- The source monitor was changed to read its baseline from the ledger at run
  time, with an explicit failure when that value cannot be parsed. This avoids
  silently carrying a stale literal in automation.
- Generated public artifacts must be re-rendered and checked whenever a
  ledger-backed claim changes. Live verification needs cache-aware requests and
  a real-browser pass.
- A local worktree can make a merge command report a cleanup error after the
  remote merge already succeeded. Verify the remote state before retrying a
  publication action.
- Fresh pull requests may briefly report an indeterminate mergeability state.
  Poll the provider rather than treating the first result as final.
- An unrelated content-only site update occurred in the same session. It did
  not alter this project's public facts, release process, or outreach boundary.
