"""The ordered, canonical public routes for RVC Housing and Schools.

This is the single source of truth for the sitemap integrity gate and the IndexNow
submission payload. Keep the insertion order aligned with ``site/sitemap.xml``.
"""

CANONICAL_ORIGIN = "https://rvc-taxes.jeffpinto.com"

PAGE_ROUTES = {
    "/": "index.html",
    "/fiscal-math": "fiscal-math.html",
    "/validation": "validation.html",
    "/voices": "voices.html",
    "/voices-library": "voices-library.html",
    "/calculator": "calculator.html",
    "/reconcile": "reconcile.html",
    "/breakeven": "breakeven.html",
    "/governance": "governance.html",
    "/governance-options": "governance-options.html",
    "/redraw-evidence": "redraw-evidence.html",
    "/coverage": "coverage.html",
    "/deck": "deck.html",
    "/privacy": "privacy.html",
}

CANONICAL_PATHS = tuple(PAGE_ROUTES)
CANONICAL_URLS = tuple(f"{CANONICAL_ORIGIN}{path}" for path in CANONICAL_PATHS)
