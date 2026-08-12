#!/usr/bin/env python3
"""Mint READ-ONLY Gmail credentials for the RVC reply watcher, on jeff@jeffpinto.com.

Deliberately separate from the outbound repo's gmail_auth_setup.py, which is right for its
own job and wrong for this one in three ways:
  1. Its scope is gmail.compose. This watcher only ever reads, so it takes gmail.readonly.
     A watcher that cannot send cannot mis-send.
  2. Its login_hint is jeff@bluecamelconsulting.com. The campaign mailbox is
     jeff@jeffpinto.com, and Google's account chooser defaults to whoever is already signed
     in. That default connected the wrong mailbox twice on 2026-08-11. The hint here is
     jeffpinto, and the script prints the granted address back at you so a wrong pick is
     caught at mint time rather than by silence weeks later.
  3. It writes GMAIL_BCC_* into the outbound repo's .env. This writes GMAIL_JP_* into this
     repo's gitignored scripts/.env.

RUN THIS IN A REAL TERMINAL, not through Claude Code's `!` prefix: the prompts need a TTY,
and the client secret should not land in a transcript. `!` gives you EOFError on the first
prompt.

One-time prerequisites, in a GCP project tied to jeff@jeffpinto.com:
  1. Enable the Gmail API:  https://console.cloud.google.com/apis/library/gmail.googleapis.com
  2. Configure the OAuth consent screen as External, and add jeff@jeffpinto.com as a test
     user:                  https://console.cloud.google.com/apis/credentials/consent
  3. Create an OAuth client ID of type "Desktop app":
                            https://console.cloud.google.com/apis/credentials
     Copy its client id and client secret; that is what this script asks for.

Then:
  python3 scripts/gmail_auth_setup.py
  python3 scripts/reply_watcher.py --dry-run

If Google omits the refresh token (it does that on repeat consent), revoke prior access at
https://myaccount.google.com/permissions and run this again.
"""
from __future__ import annotations

import argparse
import getpass
import http.server
import json
import os
import stat
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / "scripts" / ".env"

# 8913, one above the outbound repo's 8912, so both flows can exist without colliding.
REDIRECT_PORT = 8913
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
ACCOUNT = "jeff@jeffpinto.com"


class _CodeCatcher(http.server.BaseHTTPRequestHandler):
    code = None
    error = None

    def do_GET(self):  # noqa: N802
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _CodeCatcher.code = (q.get("code") or [None])[0]
        _CodeCatcher.error = (q.get("error") or [None])[0]
        body = b"Authorized. You can close this tab and return to the terminal."
        if _CodeCatcher.error:
            body = f"OAuth failed: {_CodeCatcher.error}".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):  # silence the default request logging
        pass


def wait_for_code() -> str:
    server = http.server.HTTPServer(("localhost", REDIRECT_PORT), _CodeCatcher)
    print(f"Waiting for the redirect on {REDIRECT_URI} ...")
    server.handle_request()  # blocks for exactly one request
    server.server_close()
    if _CodeCatcher.error:
        raise SystemExit(f"OAuth consent failed: {_CodeCatcher.error}")
    if not _CodeCatcher.code:
        raise SystemExit("no authorization code received")
    return _CodeCatcher.code


def exchange_code(client_id: str, client_secret: str, code: str) -> str:
    body = urllib.parse.urlencode({
        "client_id": client_id, "client_secret": client_secret, "code": code,
        "grant_type": "authorization_code", "redirect_uri": REDIRECT_URI,
    }).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=30) as r:
            payload = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"token exchange failed: {e.code} {e.read().decode('utf-8', 'replace')}")
    refresh = payload.get("refresh_token")
    if not refresh:
        raise SystemExit(
            "Google returned no refresh_token (this happens on repeat consent). Revoke prior "
            "access at https://myaccount.google.com/permissions and run this again."
        )
    return refresh, payload.get("access_token")


def granted_address(access_token: str) -> str | None:
    """Read back which mailbox actually granted consent. The whole point of item 2 above."""
    req = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get("emailAddress")
    except Exception:
        return None


def write_env(client_id: str, client_secret: str, refresh: str) -> None:
    updates = {
        "GMAIL_JP_CLIENT_ID": client_id,
        "GMAIL_JP_CLIENT_SECRET": client_secret,
        "GMAIL_JP_REFRESH_TOKEN": refresh,
    }
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    out, seen = [], set()
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line else None
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
        else:
            out.append(line)
    for k, v in updates.items():
        if k not in seen:
            out.append(f"{k}={v}")
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENV_PATH.write_text("\n".join(out) + "\n")
    os.chmod(ENV_PATH, stat.S_IRUSR | stat.S_IWUSR)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client-id")
    ap.add_argument("--client-secret", help="avoid: it lands in shell history. Prefer the prompt.")
    args = ap.parse_args()

    if not sys.stdin.isatty() and not (args.client_id and args.client_secret):
        raise SystemExit(
            "No TTY. Run this in a real terminal (Terminal.app), not through Claude Code's `!` "
            "prefix, which gives EOFError on the first prompt and would put your client secret "
            "in the transcript."
        )

    client_id = args.client_id or input("OAuth Client ID: ").strip()
    client_secret = args.client_secret or getpass.getpass("OAuth Client Secret (hidden): ").strip()
    if not client_id or not client_secret:
        raise SystemExit("client id and secret are both required")

    auth_url = AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": client_id, "redirect_uri": REDIRECT_URI, "response_type": "code",
        "scope": SCOPE, "access_type": "offline", "prompt": "consent",
        "login_hint": ACCOUNT,
    })
    print(f"\nOpen this URL and sign in as {ACCOUNT} (check the account chooser, it defaults to")
    print("whoever is already signed in):\n")
    print(auth_url + "\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    code = wait_for_code()
    print("Authorization code received. Exchanging for tokens...")
    refresh, access = exchange_code(client_id, client_secret, code)

    who = granted_address(access) if access else None
    if who and who.lower() != ACCOUNT.lower():
        raise SystemExit(
            f"WRONG MAILBOX: consent was granted by {who}, not {ACCOUNT}. Nothing was written. "
            f"Revoke at https://myaccount.google.com/permissions and rerun, picking {ACCOUNT} "
            "in the account chooser."
        )

    write_env(client_id, client_secret, refresh)
    print(f"\nGranted by: {who or 'unknown (profile read failed; verify by hand)'}")
    print(f"Wrote GMAIL_JP_CLIENT_ID / GMAIL_JP_CLIENT_SECRET / GMAIL_JP_REFRESH_TOKEN to "
          f"{ENV_PATH} (chmod 600, gitignored).")
    print("Next: python3 scripts/reply_watcher.py --dry-run")


if __name__ == "__main__":
    main()
