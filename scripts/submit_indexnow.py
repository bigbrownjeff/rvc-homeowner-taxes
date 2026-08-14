#!/usr/bin/env python3
"""Manually submit the released RVC sitemap to IndexNow.

IndexNow ownership uses a public verification key file. This script intentionally
does not load application credentials, visitor data, or caller-supplied URLs. It is
dry-run by default and is not scheduled: a release owner must explicitly pass
``--submit``.

Before the one POST, ``--submit`` verifies that production serves both the exact
local sitemap and the root key file. That makes it safe to run only after Pages
has deployed the same release represented by this checkout.

Usage:
    python3 scripts/submit_indexnow.py
    python3 scripts/submit_indexnow.py --submit
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

from site_routes import CANONICAL_ORIGIN, CANONICAL_URLS


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SITEMAP = SITE / "sitemap.xml"
ORIGIN = CANONICAL_ORIGIN
HOST = urlsplit(ORIGIN).netloc
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
EXPECTED_URL_COUNT = len(CANONICAL_URLS)
KEY_PATTERN = re.compile(r"^[a-f0-9]{64}$")
RFC3986_URL_PATTERN = re.compile(
    rf"^{re.escape(ORIGIN)}/(?:[A-Za-z0-9._~!$&'()*+,;=:@/-]|%[0-9A-Fa-f]{{2}})*$"
)
TIMEOUT_SECONDS = 20
USER_AGENT = "rvc-taxes-indexnow/1.0"


class SafetyError(ValueError):
    """The release artifact is not safe to submit."""


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Make every redirect a hard failure for release verification and submission."""

    def reject_redirect(self, request, response, code, message, headers):
        raise urllib.error.HTTPError(request.full_url, code, message, headers, response)

    http_error_301 = reject_redirect
    http_error_302 = reject_redirect
    http_error_303 = reject_redirect
    http_error_307 = reject_redirect
    http_error_308 = reject_redirect


NO_REDIRECT_OPENER = urllib.request.build_opener(NoRedirectHandler())


def load_public_key() -> tuple[str, Path]:
    """Return the single 64-hex key deliberately published at the site root."""
    matches = [path for path in SITE.glob("*.txt") if KEY_PATTERN.fullmatch(path.stem)]
    if len(matches) != 1:
        raise SafetyError(
            "expected exactly one 64-hex IndexNow key file at site root; found "
            f"{len(matches)}"
        )
    key_file = matches[0]
    key = key_file.stem
    if key_file.read_text(encoding="utf-8") != f"{key}\n":
        raise SafetyError(f"{key_file.relative_to(ROOT)} must contain only its public key plus a newline")
    return key, key_file


def urls_from_sitemap(raw: bytes, source: str) -> list[str]:
    """Read only the exact ordered canonical route allowlist from a sitemap."""
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise SafetyError(f"{source} is not valid XML: {exc}") from exc

    urls = [node.text or "" for node in root.findall("{*}url/{*}loc")]
    if len(urls) != EXPECTED_URL_COUNT:
        raise SafetyError(f"{source} must contain {EXPECTED_URL_COUNT} canonical URLs, found {len(urls)}")

    for value in urls:
        if not value:
            raise SafetyError(f"{source} has an empty <loc>")
        if not value.isascii() or any(char.isspace() for char in value):
            raise SafetyError(f"{source} has a raw whitespace or non-ASCII URL: {value!r}")
        if not RFC3986_URL_PATTERN.fullmatch(value):
            raise SafetyError(f"{source} has a non-RFC3986 canonical URL: {value!r}")
    if len(set(urls)) != len(urls):
        raise SafetyError(f"{source} contains duplicate URLs")
    unknown = [value for value in urls if value not in CANONICAL_URLS]
    if unknown:
        raise SafetyError(f"{source} has an unknown canonical route: {unknown[0]!r}")
    if tuple(urls) != CANONICAL_URLS:
        raise SafetyError(f"{source} routes are reordered; canonical sitemap order is required")
    return urls


def load_local_urls() -> list[str]:
    try:
        return urls_from_sitemap(SITEMAP.read_bytes(), str(SITEMAP.relative_to(ROOT)))
    except OSError as exc:
        raise SafetyError(f"could not read {SITEMAP.relative_to(ROOT)}: {exc}") from exc


def fetch_public(url: str) -> bytes:
    """Fetch a public release artifact and reject redirects or non-200 responses."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with NO_REDIRECT_OPENER.open(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status != 200 or response.geturl() != url:
                raise SafetyError(
                    f"production artifact is not a direct 200 at {url} "
                    f"(status {response.status}, final URL {response.geturl()})"
                )
            return response.read()
    except urllib.error.HTTPError as exc:
        try:
            if 300 <= exc.code < 400:
                raise SafetyError(f"production artifact redirected at {url}: HTTP {exc.code}") from exc
            raise SafetyError(f"production artifact unavailable at {url}: HTTP {exc.code}") from exc
        finally:
            exc.close()
    except urllib.error.URLError as exc:
        raise SafetyError(f"could not reach production artifact at {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise SafetyError(f"timed out reaching production artifact at {url}") from exc
    except OSError as exc:
        raise SafetyError(f"could not read production artifact at {url}: {exc}") from exc


def payload_for_current_release() -> dict[str, object]:
    key, key_file = load_public_key()
    urls = load_local_urls()
    return {
        "host": HOST,
        "key": key,
        "keyLocation": f"{ORIGIN}/{key_file.name}",
        "urlList": urls,
    }


def verify_live_release(payload: dict[str, object]) -> None:
    """Refuse submission unless the released public artifacts match this checkout."""
    live_urls = urls_from_sitemap(fetch_public(f"{ORIGIN}/sitemap.xml"), "production sitemap")
    local_urls = payload["urlList"]
    if live_urls != local_urls:
        raise SafetyError("production sitemap differs from this checkout; deploy or refresh before submitting")

    key_location = str(payload["keyLocation"])
    key = str(payload["key"])
    if fetch_public(key_location) != f"{key}\n".encode("utf-8"):
        raise SafetyError("production IndexNow key file does not exactly match this checkout")


def post_payload(payload: dict[str, object]) -> int:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with NO_REDIRECT_OPENER.open(request, timeout=TIMEOUT_SECONDS) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        try:
            if 300 <= exc.code < 400:
                print(f"IndexNow endpoint redirected the POST: HTTP {exc.code}; submission stopped.", file=sys.stderr)
                return 1
            print(f"IndexNow submission was not accepted: HTTP {exc.code}", file=sys.stderr)
            return 1
        finally:
            exc.close()
    except urllib.error.URLError as exc:
        print(f"IndexNow submission could not reach the endpoint: {exc.reason}", file=sys.stderr)
        return 1
    except TimeoutError:
        print("IndexNow submission timed out; no automatic retry was attempted.", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"IndexNow submission failed before a response: {exc}", file=sys.stderr)
        return 1

    if status == 200:
        print(f"IndexNow accepted {len(payload['urlList'])} canonical URLs (HTTP 200).")
        return 0
    if status == 202:
        print(
            f"IndexNow received {len(payload['urlList'])} canonical URLs; key validation is pending (HTTP 202)."
        )
        return 0
    print(f"IndexNow returned unexpected HTTP {status}; do not retry blindly.", file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--submit",
        action="store_true",
        help="verify the deployed release, then make one POST to api.indexnow.org",
    )
    args = parser.parse_args(argv)

    try:
        payload = payload_for_current_release()
    except SafetyError as exc:
        print(f"IndexNow safety check failed: {exc}", file=sys.stderr)
        return 1

    print(
        f"IndexNow {'submission' if args.submit else 'dry run'}: "
        f"{len(payload['urlList'])} canonical URLs from {SITEMAP.relative_to(ROOT)}"
    )
    print(f"Public verification key: {payload['keyLocation']}")
    for url in payload["urlList"]:
        print(f"- {url}")

    if not args.submit:
        print("Dry run only. No network request was made. Re-run with --submit after deploy.")
        return 0

    try:
        verify_live_release(payload)
    except SafetyError as exc:
        print(f"IndexNow release verification failed: {exc}", file=sys.stderr)
        return 1
    return post_payload(payload)


if __name__ == "__main__":
    sys.exit(main())
