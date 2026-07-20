# Deploying rvc-taxes.jeffpinto.com

Everything in `site/` is static — no build step. Hosting: Cloudflare Pages; DNS in the Cloudflare jeffpinto.com zone (moved from Hover 2026-07).

## One-time setup

1. **Create the Pages project** (from repo root):
   ```bash
   npx wrangler login
   npx wrangler pages project create rvc-taxes --production-branch main
   ```

2. **Deploy:**
   ```bash
   npx wrangler pages deploy site --project-name rvc-taxes
   ```
   First deploy gives you `https://rvc-taxes.pages.dev`. Verify it renders before touching DNS.

3. **Custom domain** (done 2026-07-20):
   Cloudflare dashboard → Workers & Pages → `rvc-taxes` → Custom domains → Add `rvc-taxes.jeffpinto.com`. The jeffpinto.com zone lives in the same Cloudflare account, so the proxied CNAME is created automatically — no manual DNS record, no registrar step. TLS is issued on activation (usually < 1 min).

## Redeploys

```bash
npx wrangler pages deploy site --project-name rvc-taxes
```
Pages invalidates its own cache on deploy. Hard-refresh to bypass browser cache.

## What's served

| Path | Content |
|------|---------|
| `/` | 8-page legislator briefing (`site/index.html`, Editorial DS) — print-to-PDF friendly (⌘P → Save as PDF gives the 8-page handout) |
| `/fiscal-math.html` | Long-form write-up of the honest fiscal mechanics (companion to briefing p. 5) |
| `/RVC_Legislator_Deck.pptx` | 26-slide deck (15 live + appendix) — opens in PowerPoint / Keynote / Google Slides; regenerate with `tools/build_deck_pptx.py` |
| `/calculator.html` | RVC Tax & Outcomes Calculator (corrected fork of the original) |
| `/validation.html` | Fact-check & methodology page backing every number in the deck |
| `/brief-2026-08.html` | August 2026 refresh brief (2-page print handout; source `docs/BRIEF_2026-08.md`, receipts `docs/_SOURCES.md`) |
| `/reconcile.html` | Bill reconciliation calculator — real county/village roll mechanics, forward + back-solve modes (July 2026 math audit, `docs/MATH-AUDIT-2026-07.md`) |

## Notes

- Design system: Editorial DS (jeffpinto.com) with the ink-blue policy accent (`#1E3A8A`); pages load Source Serif 4 / Inter / IBM Plex Mono from Google Fonts (system fallbacks included). The PPTX maps to Georgia/Arial/Courier New so it renders identically in PowerPoint, Keynote, and Google Slides without font installs. The calculator keeps its original styling and depends only on Chart.js from cdnjs.
- A real-browser pass (fonts, print layout, chart rendering) is part of done — `curl` is not sufficient. Open both the pages.dev URL and the custom domain after DNS cutover.
