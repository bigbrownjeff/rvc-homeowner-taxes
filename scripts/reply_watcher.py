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

# Everyone the campaign wrote to. Keep in sync with
# .claude/scratch/outreach-aug1/SENDLOG.md.
#
# ADDRESSES are exact. DOMAINS are deliberately broader, because the reply we most want may
# come from a colleague rather than the person written to: Griffin's Chief of Staff Andrea
# Wilkins is supposed to reach out about scheduling, and she will not be writing from
# griffinj@. The cost of that breadth is newsletters. A run on 2026-08-12 surfaced a
# legislator's constituent mailing and a political blast alongside the real replies, so
# domain hits are scoped: a message counts as a REPLY only if it lands in a thread we
# started, bulk mail is dropped outright, and anything else from a campaign domain is
# reported at lower severity rather than either trusted or silently discarded.
ADDRESSES = [
    "palumbo@nysenate.gov",
    "info@nssba.org",
    "SDavis@nassaucountyny.gov",
    "griffinj@nyassembly.gov",
    "canzoneri@nysenate.gov",
    "Bynoe@nysenate.gov",
    "boe@rvcschools.org",
    "replauragillen@mail.house.gov",
    "onicks@nassaucountyny.gov",
    "nyaarp@aarp.org",
    "pr@lirealtor.com",
    "info@lihp.org",
    "ea@visionli.org",
    "info@lwvofnassaucounty.org",
    "ChamberRVC@gmail.com",
    "zublionisc@northshoreschools.org",
    "mgaven@rvcschools.org",
]

DOMAINS = [
    "nssba.org",
    "nyassembly.gov",
    "nysenate.gov",
    "mail.house.gov",
    "nassaucountyny.gov",
    "visionli.org",
    "northshoreschools.org",
    "rvcschools.org",
]

RECIPIENTS = ADDRESSES + DOMAINS

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

# Headers that mark mass mail. A constituent newsletter from an office we wrote to is not a
# reply, and two of them showed up in the first live run.
BULK_HEADERS = ("list-unsubscribe", "list-id", "precedence")


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
        # doseq=True is load-bearing: metadataHeaders is a repeated query param, and without
        # it urlencode serializes the LIST ITSELF ("metadataHeaders=['From', 'Subject']"), so
        # Gmail returns a message with no headers at all. Every From and Subject came back
        # empty on 2026-08-12, which also silently broke the auto-responder classifier and the
        # is-it-from-us check, because both test strings that were always "".
        url += "?" + urllib.parse.urlencode(params, doseq=True)
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

    # Threads we started. A message landing in one of these IS a reply, by definition, and
    # that is the only claim this watcher gets to make with confidence.
    sent_q = "in:sent newer_than:60d {" + " ".join(f"to:{a}" for a in ADDRESSES) + "}"
    our_threads = {m["threadId"] for m in api_get("messages", token, q=sent_q,
                                                  maxResults=100).get("messages", []) or []}

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
                      metadataHeaders=["From", "Subject", "Date", "List-Unsubscribe",
                                       "List-Id", "Precedence"])
        sender = header(msg, "From")
        if not sender:
            # Never classify on empty headers again: that is how the 08-12 run reported five
            # senderless "REPLY from :" lines and misfiled two auto-responders as human.
            print(f"    WARN: message {mid} returned no From header; skipping", file=sys.stderr)
            continue
        if any(o.lower() in sender.lower() for o in OURS):
            continue  # our own message in the thread

        if any(header(msg, h) for h in BULK_HEADERS):
            print(f"    bulk mail, skipped: {sender}")
            continue

        subject = header(msg, "Subject")
        blob = f"{subject} {msg.get('snippet','')}".lower()
        in_thread = msg.get("threadId") in our_threads
        if any(m in blob for m in AUTO_MARKERS):
            kind = "auto-reply"
        elif in_thread:
            kind = "REPLY"
        else:
            # Right domain, but not in a thread we started and not obviously bulk. Could be
            # Griffin's Chief of Staff opening a fresh scheduling thread; could be noise.
            kind = "unsolicited"
        fresh.append({"id": mid, "from": sender, "subject": subject,
                      "date": header(msg, "Date"), "kind": kind,
                      "snippet": msg.get("snippet", "")[:300]})

    if not fresh:
        print("no new replies")
        return 0

    for r in fresh:
        kind = r["kind"]
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
            "error" if kind == "REPLY" else "warn",
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
