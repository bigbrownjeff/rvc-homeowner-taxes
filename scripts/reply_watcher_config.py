"""Local-only configuration for the reply watcher.

The tracked source intentionally contains no mailbox, recipient, domain, or
campaign-routing identities. Put those only in the ignored local configuration
file created from ``reply_watcher_config.example.json``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


CONFIG_NAME = "reply_watcher.local.json"
TEMPLATE_NAME = "reply_watcher_config.example.json"
SCHEMA_VERSION = 1


class ConfigError(ValueError):
    """A local watcher configuration is missing or unsafe to use."""


@dataclass(frozen=True)
class WatcherConfig:
    campaign_addresses: tuple[str, ...]
    campaign_domains: tuple[str, ...]
    our_addresses: tuple[str, ...]
    expected_account: str


def config_path(root: Path) -> Path:
    return root / "scripts" / CONFIG_NAME


def template_path(root: Path) -> Path:
    return root / "scripts" / TEMPLATE_NAME


def _clean_list(data: dict, key: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ConfigError(f"{key} must be a JSON list")
    items = tuple(item.strip() for item in value if isinstance(item, str) and item.strip())
    if len(items) != len(value):
        raise ConfigError(f"{key} may contain only non-empty strings")
    if not allow_empty and not items:
        raise ConfigError(f"{key} must not be empty")
    if len(set(item.lower() for item in items)) != len(items):
        raise ConfigError(f"{key} contains duplicate values")
    if any(any(char.isspace() for char in item) for item in items):
        raise ConfigError(f"{key} values may not contain whitespace")
    return items


def load_config(root: Path) -> WatcherConfig:
    path = config_path(root)
    if not path.exists():
        raise ConfigError(
            f"missing local config: {path}. Copy {template_path(root)} to the ignored local path."
        )
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot read local watcher config: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError("local watcher config must be a JSON object")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ConfigError(f"schema_version must equal {SCHEMA_VERSION}")

    campaign_addresses = _clean_list(data, "campaign_addresses")
    campaign_domains = _clean_list(data, "campaign_domains", allow_empty=True)
    our_addresses = _clean_list(data, "our_addresses")
    expected_account = data.get("expected_account")
    if not isinstance(expected_account, str) or not expected_account.strip() or "@" not in expected_account:
        raise ConfigError("expected_account must be a non-empty email address")
    expected_account = expected_account.strip()
    if expected_account.lower() not in {address.lower() for address in our_addresses}:
        raise ConfigError("expected_account must also appear in our_addresses")

    return WatcherConfig(
        campaign_addresses=campaign_addresses,
        campaign_domains=campaign_domains,
        our_addresses=our_addresses,
        expected_account=expected_account,
    )
