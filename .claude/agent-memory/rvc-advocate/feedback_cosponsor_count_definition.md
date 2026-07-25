---
name: cosponsor-count-definition
description: A bill tracker's "Sponsors (N)" total is exactly one higher than the cosponsor count, because it counts the lead sponsor; never treat that +1 as drift
metadata:
  type: feedback
---

When reconciling a federal bill's cosponsor count, "cosponsors" EXCLUDES the lead
sponsor and "sponsors" INCLUDES them. A tracker showing `N+1` where the primary feed
shows `N` is **agreement, not drift**. Cite the cosponsor count.

**Why:** on 2026-07-23 and again on 2026-07-24 the daily posture sweep filed a
"DISCREPANCY: H.R. 1340 cosponsors moved from 146 to 147-148" against the ledger.
The real state was 147 cosponsors, and BillTrack50's "Sponsors (148)" was those same
147 plus lead sponsor Panetta (CA-19). The count HAD genuinely moved 146 -> 147, but
the "148" half of the reported range was pure definitional artifact. Two days were
lost partly to chasing a phantom.

**How to apply:** state the rule *relationally*, never as a hard-coded number, or it
inverts the moment the real count reaches the old tracker value. `scripts/count_hr1340_cosponsors.py`
prints both `cosponsors` and `sponsors_inclusive` so a tracker gets reconciled instead
of trusted. When writing a monitor's expectations, "tracker == primary + 1 is agreement,
any other relationship is drift" stays true forever; "an observed 148 is agreement" goes
false on the very next cosponsorship.

Related: [[congress-primary-source]], [[drift-baseline-primary-source]]
