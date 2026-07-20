# Handoff — facts ledger, full redesign, action kit, persona (2026-07-20)

## What we set out to do
Pivot session: (1) rewrite the useless fact-check page as the site's single fact source, (2) implement the Claude Design handoff package (design + voice + interactions) across every page, (3) make contact buttons + the address lookup accurate and working, (4) create a project persona.

## What shipped (PRs #5, #6, both merged + deployed + live-verified)
- **PR #5 — the facts ledger.** `site/validation.html` = every figure → primary source → verified date → used-on pages, with `#f-*` row anchors, a maintenance rule (change the ledger first, propagate via used-on), a vintage watch, and a known-unknowns list. The old corrections narrative lives on only in `docs/` + git.
- **PR #6 — the redesign.** Modernist/RVC system (`#f3f2f2`/`#201e1d`/green `#1e6b3d`/gold `#c5a44e`, Archivo, zero radius, flush-left buttons) across all 12 pages. New landing `/` = the brief + **action kit**: Census-geocoder JSONP lookup → five official cards → prewritten letters → prefilled mailtos + Copy letter. Old print deck → `/deck.html`; `/brief-2026-08` 301s home. Signup backend is real: `site/_worker.js` → KV `SIGNUPS` (id `55371b2ca075430faeeae249f9b036cc`), bound via repo-root `wrangler.toml`; deploy is now just `npx wrangler pages deploy`.
- **Persona:** `rvc-advocate` authored from this session, compiled, installed (`~/.claude/agents/rvc-advocate.md`), committed to the personas repo (default branch renamed master→primary per standing rule). Memory `rvc-taxes-project` updated to point at it.

## Fact corrections (do not regress; receipts in the ledger)
- **RVC's state senator is Siela Bynoe (SD-6)** — nysenate.gov/senators/siela-bynoe/district lists Rockville Centre. Canzoneri-Fitzpatrick (SD-9) is the S3309 sponsor + RVC resident, NOT the senator. The pre-redesign site had this wrong.
- Nassau LD-1 (Scott Davis, `SDavis@nassaucountyny.gov`) covers all of RVC on the 2026 court-settlement map.
- Freddie Mac "Silver Tsunami" pinned to the Dec 19, 2024 release; ledger row `f-downsize-intent` carries the 68% age-in-place counter-stat so nobody overreads the downsize claim.
- Griffin (AD-21): her contact page has NO form but lists `griffinj@nyassembly.gov` → her card is a direct mailto (documented deviation from the handoff's "form only").

## What worked / gotchas for next time
- **Page-agent fan-out** (5 agents, disjoint files, one worktree, `DESIGN_CONVENTIONS.md` as the contract, `reports/<page>.md` back) shipped 10 pages in parallel with zero conflicts. Pilot one page yourself first to set the conventions.
- **Copy-letter "returned nothing" in the design preview** was the claude.ai iframe blocking the async clipboard API. On the live site it works: verified with a MutationObserver watching the label flip to "Copied" after a real click. Do NOT `navigator.clipboard.readText()` in a driven browser — the permission prompt freezes CDP for 45s.
- **`wrangler kv key get` defaults to LOCAL storage** — pass `--remote` or you'll conclude your writes vanished (DEPLOY.md now says so).
- **Headless Chrome clamps `--window-size=390` to ~485-500px** — mobile verification needs Playwright real viewports; three agents independently hit this.
- Census geocoder needs JSONP (`format=jsonp`) — no CORS headers. congress.gov + housingwire 403 automated fetches.
- Re-skin proof pattern: diff `<script>` blocks vs `git show HEAD:` — byte-identical or it doesn't merge.

## Open threads
1. **2026 final STAR credits** still unpublished (DTF page checked 07-20, still 2025-labeled) → when they land, update ledger `f-star-credit` + the $2,058 dividend + brief/calculator/mechanics per used-on.
2. **Nassau FOIL** for §467/Enhanced-STAR parcel counts still open — the exemption-gap number stays unpublished until then.
3. **Politician push (Aug 2026):** before any office sees material, same-day re-verify H.R. 1340 cosponsors + Gillen status; run ground-claims.
4. localStorage signup entries from pre-backend visitors are not migrated (nothing meaningful was live before today).
5. Legacy em dashes remain in preserved memo prose (governance/redraw/voices-library) by design; new copy is dash-free.
