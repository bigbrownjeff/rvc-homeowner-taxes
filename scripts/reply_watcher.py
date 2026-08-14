#!/usr/bin/env python3
"""Watch a configured inbox for replies to an independent outreach program.

The tracked source deliberately contains no campaign-recipient, domain, or
mailbox identities. Those values live only in the ignored local configuration.

What it does: lists configured inbox threads, skips messages from the configured
owner addresses and obvious automated mail, then files one deduplicated alert
for each genuinely new message. Detect-and-report only: it never replies,
labels, or sends.

Credentials: GMAIL_JP_CLIENT_ID / GMAIL_JP_CLIENT_SECRET /
GMAIL_JP_REFRESH_TOKEN, from the environment or ignored scripts/.env.

Usage:
  python3 scripts/reply_watcher.py                 # normal run
  python3 scripts/reply_watcher.py --dry-run       # findings only, no cards or state write
  python3 scripts/reply_watcher.py --check-config  # no network; validates local config only

stdlib only, to match the rest of this repo.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from reply_watcher_config import ConfigError, load_config


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / ".claude" / "scratch" / "outreach-aug1" / ".reply-watcher-seen.json"
ENV_FILE = ROOT / "scripts" / ".env"
FAILTASK = os.path.expanduser("~/.claude/bin/failtask")
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://gmail.googleapis.com/gmail/v1/users/me"

# Substrings that mark a message as machine-generated. Auto-replies remain
# visible once, but never look like a human reply.
AUTO_MARKERS = (
    "automatic reply",
    "auto-reply",
    "out of office",
    "out-of-office",
    "vacation",
    "unattended",
    "do not reply",
    "noreply",
)

# Headers that mark mass mail. A newsletter is not a reply.
BULK_HEADERS = ("List-Unsubscribe", "List-Id", "Precedence")


def load_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    return env


def creds() -> tuple[str, str, str] | None:
    env = load_env()

    def get(key: str) -> str | None:
        return os.environ.get(key) or env.get(key)

    values = (
        get("GMAIL_JP_CLIENT_ID"),
        get("GMAIL_JP_CLIENT_SECRET"),
        get("GMAIL_JP_REFRESH_TOKEN"),
    )
    return values if all(values) else None


def failtask(title: str, detail: str, key: str, severity: str = "warn") -> None:
    if not os.path.exists(FAILTASK):
        print(f"failtask missing; would have filed: {title}", file=sys.stderr)
        return
    subprocess.run(
        [FAILTASK, "rvc-taxes", title, "--detail", detail, "--dedupe-key", key, "--severity", severity],
        check=False,
    )


def access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    body = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=30) as response:
        return json.load(response)["access_token"]


def api_get(path: str, token: str, **params) -> dict:
    url = f"{API}/{path}"
    if params:
        # doseq=True preserves repeated metadataHeaders query parameters.
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def header(message: dict, name: str) -> str:
    for item in message.get("payload", {}).get("headers", []):
        if item.get("name", "").lower() == name.lower():
            return item.get("value", "")
    return ""


def main() -> int:
    allowed = {"--dry-run", "--check-config"}
    unknown = [argument for argument in sys.argv[1:] if argument not in allowed]
    if unknown:
        print(f"unknown argument(s): {' '.join(unknown)}", file=sys.stderr)
        return 2
    dry_run = "--dry-run" in sys.argv
    check_config = "--check-config" in sys.argv

    try:
        config = load_config(ROOT)
    except ConfigError as exc:
        detail = f"RVC reply watcher local configuration is unavailable: {exc}"
        print(detail, file=sys.stderr)
        if not dry_run and not check_config:
            failtask(
                "RVC reply watcher is not configured",
                detail,
                "rvc-reply-watcher-config-missing",
                "warn",
            )
        return 2

    if check_config:
        print(
            "reply watcher config valid: "
            f"campaign_addresses={len(config.campaign_addresses)}, "
            f"campaign_domains={len(config.campaign_domains)}, "
            f"our_addresses={len(config.our_addresses)}"
        )
        return 0

    credentials = creds()
    if not credentials:
        detail = (
            "scripts/reply_watcher.py has no Gmail credentials, so nothing is watching for replies. "
            "Run scripts/gmail_auth_setup.py in a real terminal, then keep the generated values in "
            f"{ENV_FILE}. Until then, check replies manually."
        )
        print(detail, file=sys.stderr)
        if not dry_run:
            failtask(
                "RVC reply watcher is not armed (no Gmail credentials)",
                detail,
                "rvc-reply-watcher-unarmed",
                "warn",
            )
        return 0

    token = access_token(*credentials)

    # A message in a thread we started is a reply by definition. Domain-level
    # matches broaden discovery for a new thread from a colleague, but remain
    # lower-confidence until thread membership proves the relationship.
    sent_query = "in:sent newer_than:60d {" + " ".join(
        f"to:{address}" for address in config.campaign_addresses
    ) + "}"
    our_threads = {
        message["threadId"]
        for message in api_get("messages", token, q=sent_query, maxResults=100).get("messages", []) or []
    }

    recipient_terms = config.campaign_addresses + config.campaign_domains
    inbox_query = "in:inbox newer_than:30d {" + " ".join(
        f"from:{recipient}" for recipient in recipient_terms
    ) + "}"
    listing = api_get("messages", token, q=inbox_query, maxResults=50)

    seen = set()
    if LEDGER.exists():
        seen = set(json.loads(LEDGER.read_text()).get("seen", []))

    fresh = []
    for stub in listing.get("messages", []) or []:
        message_id = stub["id"]
        if message_id in seen:
            continue
        message = api_get(
            f"messages/{message_id}",
            token,
            format="metadata",
            metadataHeaders=["From", "Subject", "Date", "List-Unsubscribe", "List-Id", "Precedence"],
        )
        sender = header(message, "From")
        if not sender:
            print(f"    WARN: message {message_id} returned no From header; skipping", file=sys.stderr)
            continue
        if any(address.lower() in sender.lower() for address in config.our_addresses):
            continue

        if any(header(message, name) for name in BULK_HEADERS):
            print(f"    bulk mail, skipped: {sender}")
            continue

        subject = header(message, "Subject")
        blob = f"{subject} {message.get('snippet', '')}".lower()
        in_thread = message.get("threadId") in our_threads
        if any(marker in blob for marker in AUTO_MARKERS):
            kind = "auto-reply"
        elif in_thread:
            kind = "REPLY"
        else:
            kind = "unsolicited"
        fresh.append(
            {
                "id": message_id,
                "from": sender,
                "subject": subject,
                "date": header(message, "Date"),
                "kind": kind,
                "snippet": message.get("snippet", "")[:300],
            }
        )

    if not fresh:
        print("no new replies")
        return 0

    for reply in fresh:
        kind = reply["kind"]
        print(f"{kind} from {reply['from']}: {reply['subject']}")
        print(f"    {reply['snippet']}")
        if dry_run:
            continue
        failtask(
            f"RVC {kind}: {reply['from']}",
            f"{reply['subject']}\n\n{reply['snippet']}\n\nReceived {reply['date']}. "
            f"Open at https://mail.google.com/mail/u/3/#inbox/{reply['id']} . "
            "A human reply from a public office can be time-sensitive.",
            f"rvc-reply-{reply['id']}",
            "error" if kind == "REPLY" else "warn",
        )

    if not dry_run:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps({"seen": sorted(seen | {reply["id"] for reply in fresh})}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except urllib.error.HTTPError as exc:
        detail = f"{exc.code} {exc.read().decode('utf-8', 'replace')[:400]}"
        print(f"gmail api error: {detail}", file=sys.stderr)
        if "--dry-run" not in sys.argv and "--check-config" not in sys.argv:
            failtask(
                "RVC reply watcher: Gmail API error",
                f"reply_watcher.py failed: {detail}. A watcher that cannot check is not green.",
                "rvc-reply-watcher-broken",
                "error",
            )
        sys.exit(1)
