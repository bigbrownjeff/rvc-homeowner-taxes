# Deploying rvc-taxes.jeffpinto.com

Everything in site/ is static (no build step) plus one advanced-mode worker
(site/_worker.js) for consent-only update-list APIs, clean-URL redirects, and
real 404 behavior. Hosting is Cloudflare Pages; configuration lives in
repo-root wrangler.toml.

## Deploy

~~~bash
python3 scripts/check_site_integrity.py
scripts/check_pdf_drift.sh       # gate: is the downloadable PDF still current?
npx wrangler pages deploy        # reads wrangler.toml: project rvc-taxes, output site/
~~~

Run the gate first. /RVC_Briefing_8pager.pdf is a rendered snapshot of
/deck.html, so a deck edit that skips the re-render can ship a handout whose
figures no longer match the live page. Exit 0 is clean, 1 is drift, and 2 could
not check. On drift, run scripts/check_pdf_drift.sh --fix, then commit the
PDF. The daily posture sweep runs the same check and files a board card.

Pages invalidates its own cache on deploy. Hard-refresh to bypass browser cache.
Cloudflare can cache a miss too, so verify new assets with a cache-busting query
before concluding that a deploy failed.

**After any deploy touching site/_worker.js signup/count logic, run the live
smoke test:**

~~~bash
scripts/smoke-signup.sh
~~~

The test posts a uniquely named consented signup to the deployed site, asserts
the KV row contains only email and consent metadata, verifies the count changes
once, then verifies the self-service deletion endpoint removes the row and
restores the counter. Cloudflare KV reads are eventually consistent, so the
script polls remote key state and /api/count for up to 120 seconds at a
3-second cadence by default. It retries reads only, never either POST. Set
SMOKE_POLL_MAX_SECONDS, SMOKE_POLL_INTERVAL_SECONDS, and
SMOKE_WRANGLER_MAX_TIME to tune those bounds.

The trap first uses the same single unsubscribe request if it has not yet been
attempted. Its direct-KV emergency fallback removes only the uniquely named
smoke row and never writes count:signup; a divergent or unreadable tally is
reported for manual remediation rather than clobbered.

## Privacy-release cleanup

The pre-2026-08-14 signup flow allowed address and name fields in KV and did not
record affirmative consent. After the privacy release is live, run this sequence
once from the release checkout:

~~~bash
python3 scripts/purge_legacy_signup_pii.py
python3 scripts/purge_legacy_signup_pii.py --apply
scripts/smoke-signup.sh
~~~

The first command is a read-only inventory. The apply command deletes legacy
rows that lack an explicit consent timestamp rather than silently treating them
as newly consented. It migrates any explicitly consented row to a SHA-256 key
and removes name and address fields. It prints counts only, never subscriber
data. Do not skip the dry run.

If wrangler.toml is ever absent, the explicit form is
npx wrangler pages deploy site --project-name rvc-taxes -- but that skips the
KV binding; /api/signup will 503 until the binding is attached in the
dashboard.

## One-time setup (done)

- The Pages project and custom domain are attached to the existing Cloudflare
  zone.
- The consent-only KV namespace is bound through wrangler.toml. Signup keys
  are SHA-256 hashes of lowercased email addresses, not raw email addresses.
  Inspect it with:

  ~~~bash
  npx wrangler kv key list --namespace-id 55371b2ca075430faeeae249f9b036cc --remote
  npx wrangler kv key get "signup:<sha256-lowercase-email>" --namespace-id 55371b2ca075430faeeae249f9b036cc --remote
  ~~~

## What's served

| Path | Content |
|------|---------|
| / | The brief: main landing plus an address-based public action kit |
| /fiscal-math | Mechanics: long-form fiscal write-up |
| /validation | Facts & sources: the ledger backing every number on the site |
| /voices | Curated quote library; /voices-library is the full archive |
| /calculator | Tax and outcomes calculator |
| /reconcile | Bill reconciler and county/village roll mechanics |
| /breakeven | Break-even instrument |
| /deck | The 8-page print briefing |
| /RVC_Briefing_8pager.pdf | Rendered PDF of /deck.html; re-render after a deck edit with scripts/check_pdf_drift.sh --fix |
| /governance, /governance-options, /redraw-evidence | Governance memos |
| /coverage | District coverage matrix and honestly labeled aggregate campaign counts |
| /privacy | Privacy, independence, funding disclosures, and self-service update-list deletion |
| /robots.txt, /sitemap.xml | Crawl directives and canonical clean-URL sitemap |
| missing route | Custom 404 page with a true 404 status |
| /api/signup | Same-origin consented update-list POST |
| /api/unsubscribe | Same-origin self-service deletion POST |
| /api/count | Aggregate engagement counter API |
| /go/{email,linkedin,bsky,threads,x,facebook} | Fixed privacy-safe campaign redirects with channel UTM labels |
| /*.html and /brief-2026-08(.html) | 301 to the clean canonical route |

## Notes

- Design source of truth: design_handoff_rvc_site_redesign/ (checked into the
  repo). Shared chrome is site/assets/site.css plus site/assets/nav.js.
- Public-action routes are defined in the live source and must be verified
  against current first-party information at time of use. Do not store
  recipient-specific routing in deployment notes.
- The address action tool and update list are deliberately separate. The browser
  sends an address to the U.S. Census geocoder to find districts, but this site
  does not receive or retain that address or the optional name. The signup strip
  collects email only after explicit checkbox consent.
- Every non-print page includes a disclosure linking to Blue Camel Consulting's
  mission-driven work. Project supporters must never be moved into consulting
  outreach without a separate opt-in.
- Public representation metadata is re-verified against first-party sources
  before action-oriented public communications. Historical deployment notes are
  not a source of contact or recipient truth.
- A real-browser pass is part of done. After deploy: check the custom domain,
  run the action kit with a test address, confirm a copy control, verify a
  public-action route, and confirm the separate signup checkbox is required.

## Post-deploy crawl and SEO verification

Use cache-busting query strings and verify these outcomes before announcing a
release:

~~~bash
curl -sI "https://rvc-taxes.jeffpinto.com/?cb=$RANDOM"
curl -sI "https://rvc-taxes.jeffpinto.com/robots.txt?cb=$RANDOM"
curl -sI "https://rvc-taxes.jeffpinto.com/sitemap.xml?cb=$RANDOM"
curl -sI "https://rvc-taxes.jeffpinto.com/this-page-does-not-exist?cb=$RANDOM"
curl -sI "https://rvc-taxes.jeffpinto.com/index.html?cb=$RANDOM"
curl -sI "https://rvc-taxes.jeffpinto.com/assets/rvc-housing-schools-social-1200x630.png?cb=$RANDOM"
curl -sI "https://rvc-taxes.jeffpinto.com/go/linkedin?cb=$RANDOM"
~~~

Expect 200 for the landing page, robots, sitemap, and social image; a 404 for
the missing route; a 301 from /index.html to /; and a 302 from the channel
redirect to the landing page with the expected UTM labels. Inspect the landing
HTML for its canonical URL, Open Graph title/description/image, and JSON-LD.
Then submit https://rvc-taxes.jeffpinto.com/sitemap.xml through verified Google
Search Console and Bing Webmaster Tools. Keep confirmation receipts with the
release notes.

### One-off IndexNow notification

IndexNow supplements, rather than replaces, the sitemap submissions above. Its 64-hex
verification key is intentionally public: the root `site/<key>.txt` file is the
[ownership proof the protocol requires](https://www.indexnow.org/documentation). It is not an API secret, does not identify a
visitor, and must stay in version control so the deployed file and release script
remain reviewable together.

After the Pages deploy and the crawl checks above are clean, run the script once from
the exact release checkout:

```bash
python3 scripts/submit_indexnow.py
python3 scripts/submit_indexnow.py --submit
```

The first command is a no-network dry run. The second accepts only the exact ordered
14-route canonical allowlist from the local sitemap, verifies production serves that
same sitemap and the exact root key file without a redirect, then makes one JSON POST
to `api.indexnow.org`.
It has no scheduling, retry loop, caller-supplied URLs, analytics, or user data. A
`200` means accepted; `202` means received while key validation is pending. Any other
result is a stop-and-investigate signal, not a cue to retry blindly. Record the
command output in the release notes.

The Pages worker needs no special IndexNow route: a `/<64-hex>.txt` request is a
static asset path (it has a file extension and is not an `.html` route), so it falls
through to `env.ASSETS.fetch`. Do not add it to the worker's clean-page map or API
surface. If the key is ever rotated, replace the root file with one new 64-hex file;
both the integrity gate and the submitter deliberately refuse zero or multiple keys.

## Reply watcher (`com.jeffpinto.rvc-reply-watcher`)

scripts/reply_watcher.py runs every two hours via launchd and has no sunset. It
detects configured reply candidates and files one deduplicated alert per new
message. It never replies, labels, or sends. Recipient, domain, and mailbox
identities are stored only in ignored local configuration.

Before installing or reloading the launch agent, create the local configuration
from its tracked empty template, populate it only on the target machine, and
validate without network access:

~~~bash
cp scripts/reply_watcher_config.example.json scripts/reply_watcher.local.json
chmod 600 scripts/reply_watcher.local.json
# Populate the local file with authorized values. Never commit it.
python3 scripts/reply_watcher.py --check-config
~~~

The watcher is not armed until read-only Gmail credentials exist. Run the auth
helper in a real terminal; it reads the expected mailbox only from the local
configuration and writes credentials only to ignored scripts/.env:

~~~bash
python3 scripts/gmail_auth_setup.py
python3 scripts/reply_watcher.py --dry-run  # networked findings only; no cards or state write
~~~

After the no-network config check and an approved dry-run, the existing launchd
definition can be installed or reloaded separately:

~~~bash
cp scripts/com.jeffpinto.rvc-reply-watcher.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.jeffpinto.rvc-reply-watcher.plist
tail -f ~/Library/Logs/rvc-reply-watcher.log
~~~

The local configuration, credentials, and dedupe state are ignored by git.
Keep direct-outreach records and message details in authorized operational
systems, never in source control.
