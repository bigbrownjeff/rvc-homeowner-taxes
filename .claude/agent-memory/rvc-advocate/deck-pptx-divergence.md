---
name: deck-pptx-divergence
description: deck.html and RVC_Legislator_Deck.pptx are separate artifacts on different design systems and drift apart; the PPTX generator carries its own stale figures
metadata:
  type: project
---

As of 2026-07-20 (PR #9), `site/deck.html` was rebuilt into the Modernist/RVC
system and its figures synced to the validation ledger. The **PPTX is NOT in sync**:
`tools/build_deck_pptx.py` (~55KB) still emits the old Editorial DS (Georgia/Arial/
Courier, #1E3A8A, cream) and hardcodes stale figures independently (117+ cosponsors,
"Palumbo" as S3309 sponsor, Blakeman as County Executive/data-ask target, no Bynoe,
~$3,300 transfer tax).

**Why:** the PPTX is a standalone python-generated file, not derived from deck.html;
editing the HTML does nothing to it. In PR #9 the PPTX download links were removed
from deck.html, but **index.html still links `RVC_Legislator_Deck.pptx`** (left for
Jeff's call).

**How to apply:** never treat the deck HTML and the PPTX as one artifact. Before any
office receives the PPTX, either rewrite `build_deck_pptx.py` to the Modernist system
+ current ledger figures and regenerate, or drop the index.html link. When the deck's
figures change, the PPTX does not follow automatically. See [[rvc-taxes-project]].
