---
name: outreach-copy-surface
description: Politician-facing figures live in .claude/scratch/outreach-aug1/ as well as site/; every figure change must sweep those drafts too
metadata:
  type: project
---

The ledger's "used on" column covers **deployed pages only**. Campaign figures also sit in
tracked, publicly-visible outreach drafts under `.claude/scratch/outreach-aug1/` — Wave-1
letters to named officials, the LinkedIn/Bluesky drafts, and `MANIFEST.md` with its
figure->ledger-row crosswalk and pre-send checklist.

**Why:** on 2026-07-24, moving the H.R. 1340 count 146 -> 147 across the site left the stale
146 in `w1-01-gillen-cd4.md`, the letter addressed to Rep. Gillen — the exact member the
federal ask targets, sending ~2026-07-29, in a **public** repo her staff can read. The
adversarial review pass caught it; the ledger's used-on column never would have, because
that file is not a deployed page. `MANIFEST.md` was worse: its "re-verify before sending"
step had *encoded* the stale number ("146 as of 7/20, still 146 on BillTrack50"), so the
safeguard itself was the thing going stale.

**How to apply:** on any figure change, `grep -rn "<old value>" .claude/scratch/outreach-aug1/`
in addition to `site/` and `docs/`. And keep checklists **pointing at** the ledger row rather
than restating a number — a checklist that quotes a volatile figure rots into
misinformation. MANIFEST step 2 now points at `site/validation.html#f-hr1340` plus the counter
script.

Dated historical docs are the deliberate exception: `docs/REFRESH_2026-07.md` keeps 146 in its
"July 18 state" column (rewriting it would destroy the delta the doc exists to record) and
carries a "Superseded since this refresh" pointer instead. Same for `.claude/handoffs/` notes.
