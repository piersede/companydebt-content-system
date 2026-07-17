#!/usr/bin/env python3
"""Validate a Google Ads account config YAML file.

Usage: python scripts/validate-config.py accounts/company-debt.yml
"""

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import available_timezones

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REQUIRED_TOP_LEVEL = [
    "account_name",
    "customer_id",
    "currency",
    "timezone",
    "primary_conversion_actions",
    "targets",
    "comparison_periods",
    "reporting",
]

REQUIRED_TARGETS = [
    "minimum_clicks_before_judgement",
    "minimum_impressions_before_ad_judgement",
    "zero_conversion_spend_threshold",
    "low_conversion_volume_threshold",
    "conversion_lag_days",
]

PLACEHOLDER_MARKERS = ("REPLACE_WITH", "REPLACE")


def is_placeholder(value):
    if not isinstance(value, str):
        return False
    return any(marker in value for marker in PLACEHOLDER_MARKERS)


def find_placeholders(obj, path=""):
    found = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            found.extend(find_placeholders(value, f"{path}.{key}" if path else key))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            found.extend(find_placeholders(value, f"{path}[{i}]"))
    elif is_placeholder(obj):
        found.append(path)
    return found


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate-config.py <path-to-account-yaml>", file=sys.stderr)
        sys.exit(2)

    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"ERROR: file not found: {config_path}", file=sys.stderr)
        sys.exit(2)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    errors = []
    warnings = []

    for field in REQUIRED_TOP_LEVEL:
        if field not in config:
            errors.append(f"missing required top-level field: {field}")

    if "customer_id" in config and not isinstance(config["customer_id"], str):
        errors.append("customer_id must be a string (leading zeros / dashes would be lost otherwise)")

    if "login_customer_id" in config and not isinstance(config["login_customer_id"], str):
        errors.append("login_customer_id must be a string")

    if "timezone" in config:
        if config["timezone"] not in available_timezones():
            errors.append(f"invalid IANA timezone: {config['timezone']}")

    if "currency" in config:
        currency = config["currency"]
        if not (isinstance(currency, str) and len(currency) == 3 and currency.isupper()):
            errors.append(f"currency should be a 3-letter ISO code, got: {currency!r}")

    targets = config.get("targets", {})
    for field in REQUIRED_TARGETS:
        if field not in targets:
            errors.append(f"missing required targets field: targets.{field}")
    for field in ("target_cpa", "minimum_roas"):
        if field in targets:
            value = targets[field]
            if value is not None and not isinstance(value, (int, float)):
                errors.append(f"targets.{field} must be numeric or null, got: {value!r}")

    primary = set(config.get("primary_conversion_actions") or [])
    secondary = set(config.get("secondary_conversion_actions") or [])
    ignored = set(config.get("ignore_as_success_metrics") or [])

    overlap_primary_ignored = primary & ignored
    if overlap_primary_ignored:
        errors.append(f"conversion action(s) in both primary and ignored lists: {sorted(overlap_primary_ignored)}")

    overlap_secondary_ignored = secondary & ignored
    if overlap_secondary_ignored:
        warnings.append(f"conversion action(s) in both secondary and ignored lists: {sorted(overlap_secondary_ignored)}")

    overlap_primary_secondary = primary & secondary
    if overlap_primary_secondary:
        errors.append(f"conversion action(s) listed as both primary and secondary: {sorted(overlap_primary_secondary)}")

    protected = set(t.lower() for t in (config.get("protected_terms") or []))
    irrelevant = set(t.lower() for t in (config.get("irrelevant_topics") or []))
    overlap_protected_irrelevant = protected & irrelevant
    if overlap_protected_irrelevant:
        errors.append(f"term(s) listed as both protected and irrelevant: {sorted(overlap_protected_irrelevant)}")

    placeholders = find_placeholders(config)
    if placeholders:
        warnings.append(f"unfilled placeholder values (must be replaced before a live audit): {placeholders}")

    print(f"Validating {config_path}")
    print(f"  checked at: {datetime.now().isoformat(timespec='seconds')}")
    print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print()
        print("FAIL")
        sys.exit(1)

    print("PASS (structurally valid — check WARNINGS above before running a live audit)")


if __name__ == "__main__":
    main()
