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
| `/` | 8-page legislator deck (`site/index.html`) — print-to-PDF friendly (⌘P → Save as PDF gives the 8-page handout) |
| `/calculator.html` | RVC Tax & Outcomes Calculator (corrected fork of the original) |
| `/validation.html` | Fact-check & methodology page backing every number in the deck |

## Notes

- Keep the deck self-contained (inline CSS, no external fonts) so the PDF export and offline copies match the web version. The calculator's only external dependency is Chart.js from cdnjs.
- A real-browser pass (fonts, print layout, chart rendering) is part of done — `curl` is not sufficient. Open both the pages.dev URL and the custom domain after DNS cutover.
