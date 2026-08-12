# Deploying rvc-taxes.jeffpinto.com

Everything in `site/` is static (no build step) plus one advanced-mode worker (`site/_worker.js`) for `/api/signup` and legacy redirects. Hosting: Cloudflare Pages; DNS in the Cloudflare jeffpinto.com zone (moved from Hover 2026-07). Config lives in repo-root `wrangler.toml` (project name, output dir, KV binding).

## Deploy

```bash
scripts/check_pdf_drift.sh       # gate: is the downloadable PDF still current?
npx wrangler pages deploy        # reads wrangler.toml: project rvc-taxes, output site/
```
Run the gate first. `/RVC_Briefing_8pager.pdf` is a rendered snapshot of `/deck.html`, so a deck edit that skips the re-render ships a handout whose figures the live page has already corrected. Exit 0 clean, 1 drift, 2 could not check. On drift: `scripts/check_pdf_drift.sh --fix`, then commit the PDF. The daily posture sweep runs the same check and files a board card.

Pages invalidates its own cache on deploy. Hard-refresh to bypass browser cache. Cloudflare's edge caches a miss too: a path requested before the file existed can keep serving the 404 body for up to 4 hours (`max-age=14400`), so verify new assets with a cache-busting query (`?cb=1`) before concluding a deploy failed.

If wrangler.toml is ever absent, the explicit form is `npx wrangler pages deploy site --project-name rvc-taxes` — but that skips the KV binding; `/api/signup` will 503 until the binding is attached (dashboard → rvc-taxes → Settings → Bindings, KV `SIGNUPS` → namespace id `55371b2ca075430faeeae249f9b036cc`).

## One-time setup (done)

- Pages project `rvc-taxes` created; custom domain `rvc-taxes.jeffpinto.com` attached 2026-07-20 (same-account zone: proxied CNAME auto-created).
- KV namespace `SIGNUPS` (`55371b2ca075430faeeae249f9b036cc`) created 2026-07-20 for the action-kit mailing list. Read signups with:
  ```bash
  npx wrangler kv key list --namespace-id 55371b2ca075430faeeae249f9b036cc --remote
  npx wrangler kv key get "signup:<email>" --namespace-id 55371b2ca075430faeeae249f9b036cc --remote
  ```

## What's served (July 2026 redesign — "Modernist" system, RVC green/gold, Archivo)

| Path | Content |
|------|---------|
| `/` | The brief: main landing + action kit (Census-geocoder letter builder, five cards, prefilled mailtos, copy-letter) |
| `/fiscal-math.html` | Mechanics: long-form fiscal write-up for aides |
| `/validation.html` | Facts & sources: the ledger backing every number on the site |
| `/voices.html` | Curated quote library (condensed); `/voices-library.html` = full archive |
| `/calculator.html` | Tax & outcomes calculator (July 2026 audited constants; no chart libs) |
| `/reconcile.html` | Bill reconciler — real county/village roll mechanics (math untouched by redesign) |
| `/breakeven.html` | Break-even instrument (math untouched by redesign) |
| `/deck.html` | The 8-page print briefing (old landing; print-first layout kept; ⌘P → PDF handout). Pages are white so it prints clean. |
| `/RVC_Briefing_8pager.pdf` | Rendered PDF of `/deck.html`, linked as "Downloadable copy" from `/` and the deck banner. Re-render after any deck edit: `scripts/check_pdf_drift.sh --fix` |
| `/governance.html`, `/governance-options.html`, `/redraw-evidence.html` | Governance memos (re-skinned) |
| ~~`/RVC_Legislator_Deck.pptx`~~ | **Not served.** Neither `site/RVC_Legislator_Deck.pptx` nor `tools/build_deck_pptx.py` is in the repo (verified 2026-08-02); this row documented a file that never shipped. The PDF above is the handout. |
| `/api/signup` | POST {name,email,address} → KV `SIGNUPS` (email required) |
| `/brief-2026-08(.html)` | 301 → `/` (both `_redirects` and `_worker.js` handle it) |

## Notes

- Design source of truth: `design_handoff_rvc_site_redesign/` (checked into the repo) — tokens, copy rules (no em dashes), component patterns. Shared chrome: `site/assets/site.css` + `site/assets/nav.js`.
- Contact routing: every contact link is `mailto:jeff@bluecamelconsulting.com?subject=[rvc-taxes] …` — never any other email.
- Officials table in `/` (action kit): fetch-verified 2026-07-20 — Gillen CD-4, Suozzi CD-3, Bynoe SD-6 (RVC's senator under current lines), Canzoneri-Fitzpatrick SD-9 (S3309 sponsor), Griffin AD-21 (direct email griffinj@nyassembly.gov), Davis LD-1 (SDavis@nassaucountyny.gov). Re-verify before each politician-facing push.
- A real-browser pass is part of done — `curl` is not sufficient. After deploy: check the custom domain, run the action kit with a real address, and click one Copy letter + one mailto.

## Reply watcher (`com.jeffpinto.rvc-reply-watcher`)

`scripts/reply_watcher.py`, every two hours via launchd, no sunset. Lists inbox threads from
any campaign recipient, drops our own messages, flags auto-responders separately from human
replies, and files one `failtask` card per genuinely new message (deduped by Gmail message id
in `.claude/scratch/outreach-aug1/.reply-watcher-seen.json`, gitignored). Detect and report
only: it never replies, labels, or sends.

**It is not armed until Gmail credentials exist.** One-time, and it must run in a REAL
TERMINAL (the prompts need a TTY; Claude Code's `!` prefix gives EOFError and would put the
client secret in a transcript):

```bash
cd ~/Projects/rvc-homeowner-taxes && python3 scripts/gmail_auth_setup.py
```

That is this repo's own auth helper, not the outbound repo's. Three deliberate differences:
**read-only scope** (`gmail.readonly`, so a watcher that cannot send cannot mis-send),
**login_hint jeff@jeffpinto.com** plus a post-consent profile read that ABORTS if a different
mailbox granted it (Google's chooser defaults to whoever is signed in; that default connected
the wrong mailbox twice on 2026-08-11), and it writes `GMAIL_JP_*` into this repo's gitignored
`scripts/.env` at chmod 600. Prereqs: use the existing `jeffpinto-site` GCP project (it already runs the site's contact
form through the Gmail API), set the [OAuth consent
screen](https://console.cloud.google.com/apis/credentials/consent) to **Internal** (available
because jeffpinto.com is a Workspace org), and create or reuse a **Desktop app** [OAuth
client](https://console.cloud.google.com/apis/credentials). **Internal, not External:** an
External app left in "Testing" issues refresh tokens that expire after 7 days, so the watcher
would die silently every week and the failure would look like "no replies" rather than like a
broken credential.

Until the credentials exist, each run files exactly one deduped `rvc-reply-watcher-unarmed`
card and exits 0, so an unarmed watcher announces itself once instead of erroring every two
hours or pretending to work.

```bash
python3 scripts/reply_watcher.py --dry-run     # findings only, no cards, no ledger write
cp scripts/com.jeffpinto.rvc-reply-watcher.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.jeffpinto.rvc-reply-watcher.plist
tail -f ~/Library/Logs/rvc-reply-watcher.log
```

Why it exists: on 2026-08-12 the campaign's first two substantive replies sat unnoticed
because every check that day searched the SENT box. Delivery and response are different
questions, and only the first one had anything watching it.
