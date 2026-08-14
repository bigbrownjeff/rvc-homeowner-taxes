#!/usr/bin/env python3
"""Mint read-only Gmail credentials for the reply watcher.

The expected mailbox is read only from the ignored
scripts/reply_watcher.local.json configuration. This tracked helper contains no
mailbox or campaign identities.

Run this in a real terminal, not through an agent shell: the prompts require a
TTY and client secrets must not enter a transcript.

One-time prerequisites:
  1. Enable the Gmail API: https://console.cloud.google.com/apis/library/gmail.googleapis.com
  2. Configure an appropriate OAuth consent screen:
     https://console.cloud.google.com/apis/credentials/consent
  3. Create or reuse a Desktop OAuth client:
     https://console.cloud.google.com/apis/credentials

The helper requests gmail.readonly, verifies the granted mailbox against the
ignored local config, and writes credentials only to ignored scripts/.env.
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

from reply_watcher_config import ConfigError, load_config


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / "scripts" / ".env"
REDIRECT_PORT = 8913
REDIRECT_URI = f"http://localhost:{REDIRECT_PORT}"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/gmail.readonly"


class _CodeCatcher(http.server.BaseHTTPRequestHandler):
    code = None
    error = None

    def do_GET(self):  # noqa: N802
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _CodeCatcher.code = (query.get("code") or [None])[0]
        _CodeCatcher.error = (query.get("error") or [None])[0]
        body = b"Authorized. You can close this tab and return to the terminal."
        if _CodeCatcher.error:
            body = f"OAuth failed: {_CodeCatcher.error}".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # noqa: D401
        """Silence the default request log."""


def wait_for_code() -> str:
    server = http.server.HTTPServer(("localhost", REDIRECT_PORT), _CodeCatcher)
    print(f"Waiting for the redirect on {REDIRECT_URI} ...")
    server.handle_request()
    server.server_close()
    if _CodeCatcher.error:
        raise SystemExit(f"OAuth consent failed: {_CodeCatcher.error}")
    if not _CodeCatcher.code:
        raise SystemExit("no authorization code received")
    return _CodeCatcher.code


def exchange_code(client_id: str, client_secret: str, code: str) -> tuple[str, str | None]:
    body = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }
    ).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"token exchange failed: {exc.code} {exc.read().decode('utf-8', 'replace')}")
    refresh = payload.get("refresh_token")
    if not refresh:
        raise SystemExit(
            "Google returned no refresh token. Revoke prior access at "
            "https://myaccount.google.com/permissions and run this again."
        )
    return refresh, payload.get("access_token")


def granted_address(access_token: str) -> str | None:
    """Read which mailbox granted consent so the local expected account can be checked."""

    request = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response).get("emailAddress")
    except Exception:
        return None


def write_env(client_id: str, client_secret: str, refresh: str) -> None:
    updates = {
        "GMAIL_JP_CLIENT_ID": client_id,
        "GMAIL_JP_CLIENT_SECRET": client_secret,
        "GMAIL_JP_REFRESH_TOKEN": refresh,
    }
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    output, seen = [], set()
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line else None
        if key in updates:
            output.append(f"{key}={updates[key]}")
            seen.add(key)
        else:
            output.append(line)
    for key, value in updates.items():
        if key not in seen:
            output.append(f"{key}={value}")
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENV_PATH.write_text("\n".join(output) + "\n")
    os.chmod(ENV_PATH, stat.S_IRUSR | stat.S_IWUSR)


def main() -> None:
    try:
        config = load_config(ROOT)
    except ConfigError as exc:
        raise SystemExit(f"reply watcher local configuration is invalid: {exc}") from exc

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--client-id")
    parser.add_argument("--client-secret", help="Avoid shell history; prefer the prompt.")
    args = parser.parse_args()

    if not sys.stdin.isatty() and not (args.client_id and args.client_secret):
        raise SystemExit(
            "No TTY. Run this in a real terminal, not through an agent shell, so client secrets "
            "do not enter a transcript."
        )

    client_id = args.client_id or input("OAuth Client ID: ").strip()
    client_secret = args.client_secret or getpass.getpass("OAuth Client Secret (hidden): ").strip()
    if not client_id or not client_secret:
        raise SystemExit("client id and secret are both required")

    auth_url = AUTH_URL + "?" + urllib.parse.urlencode(
        {
            "client_id": client_id,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent",
            "login_hint": config.expected_account,
        }
    )
    print("\nOpen this URL and sign in to the account configured locally:\n")
    print(auth_url + "\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    code = wait_for_code()
    print("Authorization code received. Exchanging for tokens...")
    refresh, access = exchange_code(client_id, client_secret, code)

    granted = granted_address(access) if access else None
    if granted and granted.lower() != config.expected_account.lower():
        raise SystemExit(
            "WRONG MAILBOX: consent did not match the locally configured expected account. "
            "Nothing was written. Revoke access and rerun with the correct account."
        )

    write_env(client_id, client_secret, refresh)
    print(f"\nGranted by: {granted or 'unknown (profile read failed; verify by hand)'}")
    print(
        "Wrote GMAIL_JP_CLIENT_ID / GMAIL_JP_CLIENT_SECRET / GMAIL_JP_REFRESH_TOKEN to "
        f"{ENV_PATH} (chmod 600, gitignored)."
    )
    print("Next: python3 scripts/reply_watcher.py --check-config")


if __name__ == "__main__":
    main()
