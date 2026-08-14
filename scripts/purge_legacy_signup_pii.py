#!/usr/bin/env python3
"""Remove legacy signup PII after the consent-only signup release.

Default mode is read-only. Pass --apply only after the privacy release is live.
Legacy raw-email keys without an explicit consent timestamp are deleted instead of
being silently re-consented. Records that already carry explicit consent are
migrated to a SHA-256 key and rewritten without name or address fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import UTC, datetime


NAMESPACE = "55371b2ca075430faeeae249f9b036cc"
HASH_RE = re.compile(r"^signup:[a-f0-9]{64}$")
SOURCE_RE = re.compile(r"^[a-z0-9:/. _-]*$", re.I)


def wrangler(*args: str) -> str:
    result = subprocess.run(
        ["npx", "wrangler", "kv", "key", *args, "--namespace-id", NAMESPACE, "--remote"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def email_key(email: str) -> str:
    digest = hashlib.sha256(email.encode("utf-8")).hexdigest()
    return f"signup:{digest}"


def normalized_email(value: object) -> str:
    return value.strip().lower() if isinstance(value, str) else ""


def clean_source(value: object) -> str:
    source = value.strip()[:120] if isinstance(value, str) else ""
    return source if SOURCE_RE.fullmatch(source) else ""


def load_record(key: str) -> dict[str, object] | None:
    raw = wrangler("get", key).strip()
    if not raw:
        return None
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def put(key: str, record: dict[str, object]) -> None:
    wrangler("put", key, json.dumps(record, separators=(",", ":")))


def delete(key: str) -> None:
    wrangler("delete", key)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="perform the irreversible remote cleanup")
    args = parser.parse_args()

    try:
        rows = json.loads(wrangler("list", "--prefix", "signup:"))
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"Could not list remote signup records: {exc}", file=sys.stderr)
        return 2

    summary = {"migrate": 0, "sanitize": 0, "delete_unconsented": 0, "skip": 0}
    operations: list[tuple[str, str, dict[str, object] | None]] = []
    now = datetime.now(UTC).isoformat().replace("+00:00", "Z")

    for row in rows:
        key = row.get("name") if isinstance(row, dict) else None
        if not isinstance(key, str) or not key.startswith("signup:"):
            continue
        try:
            record = load_record(key)
        except subprocess.CalledProcessError:
            summary["skip"] += 1
            continue
        if record is None:
            summary["skip"] += 1
            continue
        email = normalized_email(record.get("email"))
        if not email or "@" not in email:
            summary["skip"] += 1
            continue

        consent_at = record.get("consentAt")
        if not isinstance(consent_at, str) or not consent_at:
            operations.append(("delete_unconsented", key, None))
            summary["delete_unconsented"] += 1
            continue

        cleaned = {
            "email": email,
            "source": clean_source(record.get("source")),
            "consentAt": consent_at,
            "first": record.get("first") if isinstance(record.get("first"), str) else now,
            "last": record.get("last") if isinstance(record.get("last"), str) else now,
        }
        target = email_key(email)
        if key == target:
            if record != cleaned:
                operations.append(("sanitize", key, cleaned))
                summary["sanitize"] += 1
            continue
        operations.append(("migrate", key, cleaned))
        summary["migrate"] += 1

    print("Legacy signup privacy cleanup")
    print("  explicit-consent records to migrate:", summary["migrate"])
    print("  hashed records to sanitize:", summary["sanitize"])
    print("  legacy records to delete and re-consent:", summary["delete_unconsented"])
    print("  records skipped for manual review:", summary["skip"])
    if not args.apply:
        print("Dry run only. Re-run with --apply after the privacy release is live.")
        return 0

    if summary["skip"]:
        print("Refusing to apply while records need manual review.", file=sys.stderr)
        return 2

    removed = 0
    try:
        for action, key, record in operations:
            if action == "delete_unconsented":
                delete(key)
                removed += 1
            elif action == "sanitize":
                assert record is not None
                put(key, record)
            elif action == "migrate":
                assert record is not None
                put(email_key(str(record["email"])), record)
                delete(key)
        if removed:
            current = int(wrangler("get", "count:signup").strip() or "0")
            wrangler("put", "count:signup", str(max(0, current - removed)))
    except subprocess.CalledProcessError as exc:
        print(f"Remote cleanup stopped: {exc}", file=sys.stderr)
        return 2

    print("Cleanup applied. No name or address fields were retained.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
