# Deploying rvc-taxes.jeffpinto.com

Everything in `site/` is static — no build step. Hosting: Cloudflare Pages; DNS stays at Hover.

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

3. **Custom domain (Cloudflare side):**
   Cloudflare dashboard → Workers & Pages → `rvc-taxes` → Custom domains → Add `rvc-taxes.jeffpinto.com`. Because jeffpinto.com's DNS is *not* on Cloudflare, it will ask you to validate via CNAME.

4. **DNS (Hover side):**
   Hover → jeffpinto.com → DNS → Add record:
   ```
   Type: CNAME   Hostname: rvc-taxes   Target: rvc-taxes.pages.dev   TTL: default
   ```
   Subdomain CNAME to Pages works with third-party DNS; only apex domains require moving nameservers to Cloudflare. TLS cert is issued automatically once the CNAME resolves (usually < 15 min, up to a few hours).

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

## Notes

- Design system: Editorial DS (jeffpinto.com) with the ink-blue policy accent (`#1E3A8A`); pages load Source Serif 4 / Inter / IBM Plex Mono from Google Fonts (system fallbacks included). The PPTX maps to Georgia/Arial/Courier New so it renders identically in PowerPoint, Keynote, and Google Slides without font installs. The calculator keeps its original styling and depends only on Chart.js from cdnjs.
- A real-browser pass (fonts, print layout, chart rendering) is part of done — `curl` is not sufficient. Open both the pages.dev URL and the custom domain after DNS cutover.
