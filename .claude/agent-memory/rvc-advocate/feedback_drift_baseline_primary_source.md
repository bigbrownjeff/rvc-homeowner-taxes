---
name: drift-baseline-primary-source
description: A monitor's expected value must be pinned to a primary source, never to a third-party tracker, or it generates recurring false drift
metadata:
  type: feedback
---

When a monitoring sweep compares a site figure against a **third-party tracker**, it will
fire repeatedly and spuriously. Pin the baseline to the primary source and have the sweep
recompute the number itself.

**Why:** `scripts/daily_posture_sweep.sh` CHECK 1 told the sweep agent to "cross-check at
least two of BillTrack50 / GovInfo / GovTrack" and to flag drift "if the count moved off
146". Trackers lag the official feed and label totals differently, so the check fired
DISCREPANCY on both 2026-07-23 and 2026-07-24. Jeff's standing rule: a bug class seen
twice gets a root-cause fix plus a convention, never a second spot fix.

**How to apply:** three properties make a drift check durable, all now in CHECK 1:
1. **Compute, don't eyeball.** Ship an executable counter (`scripts/count_hr1340_cosponsors.py`)
   and have the check RUN it. A prose instruction to "go look at two trackers" invites the
   agent to average secondary sources.
2. **Relational rules over hard-coded numbers** (see [[cosponsor-count-definition]]).
3. **Name the non-signals explicitly.** Source vintage lag and a tracker's `+1` are both
   stated as NOT drift, or the next agent re-derives them as findings.

Corollary learned the same day: **an executable snippet embedded as copy-paste prose is a
liability.** The first version of this fix pasted a Python heredoc into the sweep prompt with
4-space indentation, so the `PY` terminator was not flush-left and the block died on
`IndentationError` — an agent hitting that traceback would fall back to a tracker and file
the exact false discrepancy the fix was meant to kill. A real script file removes the whole
failure class.
