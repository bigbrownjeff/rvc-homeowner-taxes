#!/usr/bin/env python3
"""Static release gate for RVC Housing and Schools.

Checks the crawl and conversion surfaces that a browser cannot reliably prove from
file://: canonical routes, social image references, internal links, shared chrome,
and the privacy boundary between the address tool and the update list.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

from site_routes import CANONICAL_ORIGIN, CANONICAL_URLS, PAGE_ROUTES


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
HTML_FILES = sorted(SITE.glob("*.html"))
MAILTO_PREFIX = "mailto:jeff@bluecamelconsulting.com?subject=%5Brvc-taxes%5D%20"
OG_IMAGE = "/assets/rvc-housing-schools-social-1200x630.png"
INDEXNOW_KEY_PATTERN = re.compile(r"^[a-f0-9]{64}$")
TRACKED_ROUTES = {
    "/go/email": ("email", "email"),
    "/go/linkedin": ("linkedin", "social"),
    "/go/bsky": ("bsky", "social"),
    "/go/threads": ("threads", "social"),
    "/go/x": ("x", "social"),
    "/go/facebook": ("facebook", "social"),
}


def attrs(html: str, attr: str) -> list[str]:
    return re.findall(rf"\b{attr}=['\"]([^'\"]+)['\"]", html, flags=re.I)


def main() -> int:
    failures: list[str] = []
    sitemap_list: list[str] = []
    sitemap_locs: set[str] = set()
    try:
        root = ET.parse(SITE / "sitemap.xml").getroot()
        sitemap_list = [node.text or "" for node in root.findall("{*}url/{*}loc")]
        sitemap_locs = set(sitemap_list)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"sitemap.xml is not valid XML: {exc}")

    robots = (SITE / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {CANONICAL_ORIGIN}/sitemap.xml" not in robots:
        failures.append("robots.txt does not name the canonical sitemap")

    indexnow_files = [path for path in SITE.glob("*.txt") if INDEXNOW_KEY_PATTERN.fullmatch(path.stem)]
    if len(indexnow_files) != 1:
        failures.append(f"expected exactly one public IndexNow key file, found {len(indexnow_files)}")
    elif indexnow_files[0].read_text(encoding="utf-8") != f"{indexnow_files[0].stem}\n":
        failures.append("public IndexNow key file must contain only its filename key plus a newline")
    if tuple(sitemap_list) != CANONICAL_URLS:
        failures.append("sitemap must match the ordered canonical route allowlist")

    for route, filename in PAGE_ROUTES.items():
        canonical = f"{CANONICAL_ORIGIN}{route}"
        if canonical not in sitemap_locs:
            failures.append(f"sitemap missing {canonical}")
        if not (SITE / filename).is_file():
            failures.append(f"route {route} has no static source {filename}")

    for path in HTML_FILES:
        html = path.read_text(encoding="utf-8")
        name = path.name
        expected_route = next((route for route, filename in PAGE_ROUTES.items() if filename == name), None)
        if expected_route:
            canonical = f'<link rel="canonical" href="{CANONICAL_ORIGIN}{expected_route}">'
            if canonical not in html:
                failures.append(f"{name}: missing canonical {canonical}")
        if name != "404.html" and OG_IMAGE not in html:
            failures.append(f"{name}: missing final social image metadata")
        if name != "deck.html" and "assets/nav.js" not in html:
            failures.append(f"{name}: missing shared nav")

        for href in attrs(html, "href"):
            parsed = urlparse(href)
            if href.startswith("mailto:") and not href.startswith(MAILTO_PREFIX):
                failures.append(f"{name}: noncanonical mailto {href}")
            if parsed.scheme in {"http", "https"}:
                if parsed.netloc == "rvc-taxes.jeffpinto.com" and parsed.path.endswith(".html"):
                    failures.append(f"{name}: old .html canonical link {href}")
                continue
            if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
                continue
            clean = href.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            if clean.startswith("/"):
                if clean in PAGE_ROUTES:
                    continue
                if not (SITE / clean.lstrip("/")).is_file():
                    failures.append(f"{name}: missing internal target {href}")
            elif not (path.parent / clean).is_file():
                failures.append(f"{name}: missing relative target {href}")

    nav = (SITE / "assets" / "nav.js").read_text(encoding="utf-8")
    if "utm_source=rvc-housing-schools" not in nav or "independence-note" not in nav:
        failures.append("shared footer lacks the Blue Camel transparency link")

    index = (SITE / "index.html").read_text(encoding="utf-8")
    for forbidden in ("kitEmail", "rvc-action-signups", "function signup(", "address:matched"):
        if forbidden in index:
            failures.append(f"index.html still couples action-kit data to signup: {forbidden}")
    if '<form id="kitForm"' not in index or 'id="kitBuild" type="submit"' not in index:
        failures.append("index.html action kit is not a semantic keyboard-submittable form")
    if 'og:image:width" content="1200"' not in index or 'og:image:height" content="630"' not in index:
        failures.append("index.html social metadata does not match the 1200x630 image")
    for route in TRACKED_ROUTES:
        if f'data-share-url="{CANONICAL_ORIGIN}{route}"' not in index:
            failures.append(f"index.html does not expose copyable campaign route {route}")

    worker = (SITE / "_worker.js").read_text(encoding="utf-8")
    for required in ("/api/unsubscribe", "body.consent !== true", "signupKey(email)", "serveNotFound"):
        if required not in worker:
            failures.append(f"worker missing required privacy or SEO behavior: {required}")
    if 'CAMPAIGN_NAME = "wave-3-2026"' not in worker:
        failures.append("worker missing the Wave 3 campaign name")

    # An action-kit card whose key is not in the worker allowlist gets a 400 that
    # the client's ping swallows, so the card goes uncounted in silence. That has
    # happened twice. Make the two lists prove they agree.
    card_keys = set(re.findall(r'\{key:"([A-Za-z0-9_]+)"', index))
    allow_match = re.search(r"const ACTION_KEYS = new Set\(\[(.*?)\]\)", worker, re.S)
    if not card_keys:
        failures.append("index.html exposes no action-kit card keys to check")
    elif not allow_match:
        failures.append("worker ACTION_KEYS allowlist not found")
    else:
        allowed = set(re.findall(r'"([A-Za-z0-9_]*)"', allow_match.group(1)))
        expected = card_keys | {""}
        if allowed != expected:
            missing = sorted(expected - allowed)
            extra = sorted(allowed - expected)
            failures.append(
                "worker ACTION_KEYS is out of sync with the index.html cards array: "
                f"missing {missing or 'none'}, unused {extra or 'none'}"
            )
    for route, (source, medium) in TRACKED_ROUTES.items():
        if f'"{route}": {{ source: "{source}", medium: "{medium}" }}' not in worker:
            failures.append(f"worker missing campaign redirect mapping for {route}")
    if 'url.pathname.startsWith("/go/")' not in worker:
        failures.append("worker does not protect unknown /go/* paths with a 404")
    deck = (SITE / "deck.html").read_text(encoding="utf-8")
    if "utm_source=rvc-housing-schools" not in deck:
        failures.append("print deck lacks the Blue Camel transparency link")

    if failures:
        print("SITE INTEGRITY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"SITE INTEGRITY: PASS ({len(HTML_FILES)} HTML pages, {len(PAGE_ROUTES)} canonical routes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
