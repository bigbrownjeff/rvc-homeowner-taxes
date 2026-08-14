#!/usr/bin/env python3
"""Offline regression tests for the one-off IndexNow release submitter."""

from __future__ import annotations

import contextlib
import html
import io
import sys
import unittest
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import submit_indexnow as indexnow  # noqa: E402
from site_routes import CANONICAL_URLS  # noqa: E402


REDIRECT_CODES = (301, 302, 303, 307, 308)


def sitemap_for(urls: list[str]) -> bytes:
    rows = "".join(f"<url><loc>{html.escape(url)}</loc></url>" for url in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{rows}</urlset>"
    ).encode("utf-8")


class RedirectRefusalTests(unittest.TestCase):
    @staticmethod
    def redirect_error(code: int) -> HTTPError:
        return HTTPError("https://example.invalid/redirect", code, "redirect", Message(), io.BytesIO())

    def test_no_redirect_handler_raises_for_every_redirect_status(self):
        redirect_handlers = [
            handler
            for handler in indexnow.NO_REDIRECT_OPENER.handlers
            if isinstance(handler, HTTPRedirectHandler)
        ]
        self.assertEqual(len(redirect_handlers), 1)
        self.assertIsInstance(redirect_handlers[0], indexnow.NoRedirectHandler)
        request = Request("https://example.invalid/redirect")
        for code in REDIRECT_CODES:
            with self.subTest(code=code):
                headers = Message()
                headers["Location"] = "https://example.invalid/final"
                with self.assertRaisesRegex(HTTPError, "redirect") as caught:
                    indexnow.NO_REDIRECT_OPENER.error(
                        "http", request, io.BytesIO(), code, "redirect", headers
                    )
                self.assertEqual(caught.exception.code, code)
                caught.exception.close()

    def test_get_refuses_all_redirects(self):
        for code in REDIRECT_CODES:
            with self.subTest(code=code), patch.object(
                indexnow.NO_REDIRECT_OPENER, "open", side_effect=self.redirect_error(code)
            ):
                with self.assertRaisesRegex(indexnow.SafetyError, rf"HTTP {code}"):
                    indexnow.fetch_public("https://example.invalid/redirect")

    def test_post_refuses_all_redirects(self):
        payload = {
            "host": indexnow.HOST,
            "key": "0" * 64,
            "keyLocation": f"{indexnow.ORIGIN}/{'0' * 64}.txt",
            "urlList": list(CANONICAL_URLS),
        }
        for code in REDIRECT_CODES:
            with self.subTest(code=code), patch.object(
                indexnow.NO_REDIRECT_OPENER, "open", side_effect=self.redirect_error(code)
            ):
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(indexnow.post_payload(payload), 1)

    def test_timeout_and_oserror_are_clean_failures(self):
        with patch.object(indexnow.NO_REDIRECT_OPENER, "open", side_effect=TimeoutError("slow")):
            with self.assertRaisesRegex(indexnow.SafetyError, "timed out"):
                indexnow.fetch_public("https://example.invalid/final")
        with patch.object(indexnow.NO_REDIRECT_OPENER, "open", side_effect=OSError("closed")):
            with self.assertRaisesRegex(indexnow.SafetyError, "could not read"):
                indexnow.fetch_public("https://example.invalid/final")


class SitemapAllowlistTests(unittest.TestCase):
    def assert_rejected(self, urls: list[str]):
        with self.assertRaises(indexnow.SafetyError):
            indexnow.urls_from_sitemap(sitemap_for(urls), "offline test sitemap")

    def test_current_sitemap_matches_the_shared_ordered_allowlist(self):
        urls = indexnow.urls_from_sitemap(indexnow.SITEMAP.read_bytes(), "current sitemap")
        self.assertEqual(tuple(urls), CANONICAL_URLS)

    def test_rejects_unknown_raw_space_unicode_and_non_rfc3986_routes(self):
        cases = {
            "unknown": (4, f"{indexnow.ORIGIN}/not-a-canonical-route"),
            "raw-space": (4, f"{indexnow.ORIGIN}/raw space"),
            "unicode": (4, f"{indexnow.ORIGIN}/voicés"),
            "bad-percent": (4, f"{indexnow.ORIGIN}/validation%ZZ"),
        }
        for name, (position, replacement) in cases.items():
            with self.subTest(case=name):
                urls = list(CANONICAL_URLS)
                urls[position] = replacement
                self.assert_rejected(urls)

    def test_rejects_duplicate_and_reordered_routes(self):
        duplicate = list(CANONICAL_URLS)
        duplicate[4] = duplicate[3]
        self.assert_rejected(duplicate)

        reordered = list(CANONICAL_URLS)
        reordered[2], reordered[3] = reordered[3], reordered[2]
        self.assert_rejected(reordered)


if __name__ == "__main__":
    unittest.main()
