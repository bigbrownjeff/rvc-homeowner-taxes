# Handoff: action-kit instrumentation + public-zero suppression — 2026-08-22

Question that started it (Jeff): can we tell how many people used the action-kit links to
contact reps, deduped, per official, on the insights page? Answer at the time: essentially
nobody — 10 lookups, 0 press-throughs, and the counting had two live bugs.

## What shipped (PRs #67, #68, both merged + deployed; insights repo PR #12 merged + deployed)

1. **Governor card fixed**: `gov` was missing from ACTION_KEYS, so every Hochul/A6032 ping
   400'd silently since the card shipped. Now accepted. `scripts/check_site_integrity.py`
   derives card keys from index.html and FAILS THE BUILD on drift vs ACTION_KEYS — the two
   lists are one source of truth now, negative-tested.
2. **Per-official grain**: pings write three places — the legacy `count:<event>` scalars
   (untouched, back-compat), `count:grid` (one lifetime JSON blob `{event:{official:n}}`),
   and `count:day:<YYYY-MM-DD>` (one blob per America/New_York day; Intl verified in
   production workerd, fixed-offset fallback logs if ever hit). One-blob-per-day because
   the insights reader shells a wrangler subprocess PER KEY — key-per-cell would be a
   10k-key subprocess storm.
3. **Dedupe**: IP-hash per event+official+ET-day (25h TTL), count events only. A floor,
   not a census (shared NAT collapses; no CF-Connecting-IP = no throttle). Deliberately NO
   localStorage device ID — privacy.html promises count-only telemetry and the promise was
   updated truthfully for what we do store.
4. **Insights page** (site-insights repo): action-kit funnel 10 → 1 → 0 → 0, 6×3
   per-official grid, "unmeasured is not zero" treatment for pre-instrumentation history.
   Bug fixed there: reader hardcoded the retired `count:letter` key and dropped
   letter_copied/contact_opened/sent_confirmed entirely. Also pull.py wrote raw signup
   JSON bypassing strip_pii — fixed before the first real signup could leak.
5. **Public zeros suppressed** (Jeff's ruling): `/coverage` hides the press-through strip
   until EVERY figure >= 1; `grid` removed from public GET /api/count (still written to KV;
   gated insights reads KV directly). The withholding sentence keeps the page honest.

## The bug only production could produce (the day's lesson)

First deploy used "show strip if ANY figure >= 1". Production carries legacy
`count:letter`=1, so the strip published "1 letters copied · 0 contact routes opened ·
0 self-confirmed sends" — the exact sentence suppression existed to prevent. Local KV never
carries production's legacy keys, and all-zero is the one state where any/every agree.
**Test reveal logic against production key state.** Fixed same session (#68, gate = every).

## Baselines for reading the numbers later

- Counters at instrumentation start: lookup 10, letter_copied 1 (legacy), contact_opened 0,
  sent_confirmed 0, signup 0. Everything before 2026-08-22 is UNMEASURED, not zero.
- Deploy-verification pinged exactly one event (contact_opened/gov) and restored KV to
  baseline byte-exactly, rate: key included. First real contact_opened is a real person.
- sent_confirmed is self-reported and gates the /coverage reveal; it will lag. If Jeff
  wants the strip sooner: gate on contact_opened && sent_confirmed, or publish figures
  independently — flagged as an open choice, current state is the safe one.

## Open threads

1. The strip's VISIBLE state has never rendered on production (needs three non-zero
   counters; agent correctly refused to manufacture them). Eyeball it when real numbers
   arrive.
2. The funnel is four independent daily-unique counts, NOT monotonic — a later step can
   exceed an earlier one (confirm Tuesday what you opened Monday). Insights renders
   "N more than the step before"; never rebuild it as a strict funnel.
3. Politician push (late Aug): the finding stands — people reach the kit and stop. That is
   a copy/UX problem, not a measurement one; the instrumentation now shows WHERE they stop
   and per which official.
