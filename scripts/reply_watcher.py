#!/usr/bin/env python3
"""Watch jeff@jeffpinto.com for replies to the RVC Housing x Schools outreach.

Why this exists: on 2026-08-12 the campaign's first two substantive replies (Asm. Griffin
offering a meeting, N-SSBA's executive director taking the site to his Executive Committee)
sat unnoticed because every check that day searched the SENT box. Delivery and response are
different questions and nothing was watching the second one. A reply from a legislative
office is the whole point of the campaign and is also the most perishable: an offer to
schedule goes cold.

What it does: lists inbox threads involving any campaign recipient, keeps only messages NOT
from Jeff, skips vacation/auto-responders, and files a board card for each genuinely new one.
Detect-and-report only; it never replies, never labels, never sends.

Credentials: GMAIL_JP_CLIENT_ID / GMAIL_JP_CLIENT_SECRET / GMAIL_JP_REFRESH_TOKEN, from the
environment or scripts/.env (gitignored). Mint them with the outbound repo's
scripts/gmail_auth_setup.py while signed in as jeff@jeffpinto.com, then rename the three
GMAIL_BCC_* keys it prints to GMAIL_JP_*. Without them this exits 0 after filing exactly one
deduped card, so an unarmed watcher announces itself once instead of erroring daily.

Usage:
  python3 scripts/reply_watcher.py            # normal run
  python3 scripts/reply_watcher.py --dry-run  # print findings, file nothing, touch no ledger

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

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / ".claude" / "scratch" / "outreach-aug1" / ".reply-watcher-seen.json"
ENV_FILE = ROOT / "scripts" / ".env"
FAILTASK = os.path.expanduser("~/.claude/bin/failtask")
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://gmail.googleapis.com/gmail/v1/users/me"

# Everyone the campaign wrote to. A reply from any of them is what we are watching for.
# Keep in sync with .claude/scratch/outreach-aug1/SENDLOG.md.
RECIPIENTS = [
    "palumbo@nysenate.gov",
    "info@nssba.org",
    "nssba.org",
    "SDavis@nassaucountyny.gov",
    "griffinj@nyassembly.gov",
    "nyassembly.gov",
    "canzoneri@nysenate.gov",
    "Bynoe@nysenate.gov",
    "boe@rvcschools.org",
    "replauragillen@mail.house.gov",
    "mail.house.gov",
    "onicks@nassaucountyny.gov",
    "nyaarp@aarp.org",
    "pr@lirealtor.com",
    "info@lihp.org",
    "ea@visionli.org",
    "visionli.org",
    "info@lwvofnassaucounty.org",
    "ChamberRVC@gmail.com",
    "zublionisc@northshoreschools.org",
    "northshoreschools.org",
    "mgaven@rvcschools.org",
]

# Substrings that mark a message as machine-generated. Auto-replies are still worth seeing
# once (Zublionis's revealed an unmonitored mailbox), so they are reported at warn severity
# rather than dropped, but they never look like a human reply.
AUTO_MARKERS = (
    "automatic reply",
    "auto-reply",
    "autoreply",
    "out of office",
    "this will acknowledge receipt",
    "delivery status notification",
    "mail delivery subsystem",
    "undeliverable",
)

OURS = ("jeff@jeffpinto.com", "bigbrownjeff@gmail.com", "jeff@bluecamelconsulting.com")


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

    def get(k):
        return os.environ.get(k) or env.get(k)

    vals = (get("GMAIL_JP_CLIENT_ID"), get("GMAIL_JP_CLIENT_SECRET"), get("GMAIL_JP_REFRESH_TOKEN"))
    return vals if all(vals) else None


def failtask(title: str, detail: str, key: str, severity: str = "warn") -> None:
    if not os.path.exists(FAILTASK):
        print(f"failtask missing; would have filed: {title}", file=sys.stderr)
        return
    subprocess.run(
        [FAILTASK, "rvc-taxes", title, "--detail", detail, "--dedupe-key", key, "--severity", severity],
        check=False,
    )


def access_token(cid: str, secret: str, refresh: str) -> str:
    body = urllib.parse.urlencode(
        {"client_id": cid, "client_secret": secret, "refresh_token": refresh, "grant_type": "refresh_token"}
    ).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=30) as r:
        return json.load(r)["access_token"]


def api_get(path: str, token: str, **params) -> dict:
    url = f"{API}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def header(msg: dict, name: str) -> str:
    for h in msg.get("payload", {}).get("headers", []):
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def main() -> int:
    dry = "--dry-run" in sys.argv

    c = creds()
    if not c:
        msg = (
            "scripts/reply_watcher.py has no Gmail credentials, so nothing is watching for replies "
            "to the RVC outreach. One-time fix: run the outbound repo's scripts/gmail_auth_setup.py "
            "while signed in as jeff@jeffpinto.com, then write the three values into "
            f"{ENV_FILE} as GMAIL_JP_CLIENT_ID / GMAIL_JP_CLIENT_SECRET / GMAIL_JP_REFRESH_TOKEN. "
            "The watcher arms itself on the next run. Until then, check replies by hand at "
            "mail.google.com/mail/u/3 with an in:inbox search."
        )
        print(msg, file=sys.stderr)
        if not dry:
            failtask("RVC reply watcher is not armed (no Gmail credentials)", msg, "rvc-reply-watcher-unarmed", "warn")
        return 0

    token = access_token(*c)
    query = "in:inbox newer_than:30d {" + " ".join(f"from:{r}" for r in RECIPIENTS) + "}"
    listing = api_get("messages", token, q=query, maxResults=50)

    seen = set()
    if LEDGER.exists():
        seen = set(json.loads(LEDGER.read_text()).get("seen", []))

    fresh = []
    for stub in listing.get("messages", []) or []:
        mid = stub["id"]
        if mid in seen:
            continue
        msg = api_get(f"messages/{mid}", token, format="metadata",
                      metadataHeaders=["From", "Subject", "Date"])
        sender = header(msg, "From")
        if any(o.lower() in sender.lower() for o in OURS):
            continue  # our own message in the thread
        subject = header(msg, "Subject")
        blob = f"{subject} {msg.get('snippet','')}".lower()
        auto = any(m in blob for m in AUTO_MARKERS)
        fresh.append({"id": mid, "from": sender, "subject": subject,
                      "date": header(msg, "Date"), "auto": auto,
                      "snippet": msg.get("snippet", "")[:300]})

    if not fresh:
        print("no new replies")
        return 0

    for r in fresh:
        kind = "auto-reply" if r["auto"] else "REPLY"
        line = f"{kind} from {r['from']}: {r['subject']}"
        print(line)
        print(f"    {r['snippet']}")
        if dry:
            continue
        failtask(
            f"RVC {kind}: {r['from']}",
            f"{r['subject']}\n\n{r['snippet']}\n\nReceived {r['date']}. "
            f"Open at https://mail.google.com/mail/u/3/#inbox/{r['id']} . "
            "A human reply from a legislative office is perishable; an offer to schedule goes cold.",
            f"rvc-reply-{r['id']}",
            "warn" if r["auto"] else "error",
        )

    if not dry:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        LEDGER.write_text(json.dumps({"seen": sorted(seen | {r["id"] for r in fresh})}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except urllib.error.HTTPError as e:
        detail = f"{e.code} {e.read().decode('utf-8', 'replace')[:400]}"
        print(f"gmail api error: {detail}", file=sys.stderr)
        if "--dry-run" not in sys.argv:
            failtask("RVC reply watcher: Gmail API error",
                     f"reply_watcher.py failed: {detail}. A watcher that cannot check is not green.",
                     "rvc-reply-watcher-broken", "error")
        sys.exit(1)
