"""Load and validate the data-hub backbone: sources, releases, caveats.

Every figure on a data page should trace to a source (source_registry.json)
and the release it came from (data/<dataset>/dataset_release.json). This module
reads those files, checks the required fields are present, and offers small
lookups so page builders never hard-code a source name or caveat string.

Run directly for a self-check over every registered dataset:

    python scripts/datahub/registry.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
META_DIR = ROOT / "data" / "_meta"
DATA_DIR = ROOT / "data"

SOURCE_REQUIRED = (
    "source_id", "source_name", "publisher", "source_type", "source_url",
    "format", "update_frequency", "licence", "authority_level", "status",
)
RELEASE_REQUIRED = (
    "release_id", "source_id", "dataset_name", "period_start", "period_end",
    "publication_date", "source_files", "is_provisional", "status",
)
VALID_STATUS = {"implemented", "planned", "current", "superseded", "revised", "archived"}


class RegistryError(ValueError):
    """Raised when the backbone JSON is missing required fields or is inconsistent."""


def _load(path: Path) -> dict:
    if not path.exists():
        raise RegistryError(f"Missing backbone file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_sources() -> dict[str, dict]:
    """Return {source_id: source_record} from data/_meta/source_registry.json."""
    raw = _load(META_DIR / "source_registry.json")
    out: dict[str, dict] = {}
    for rec in raw.get("sources", []):
        missing = [f for f in SOURCE_REQUIRED if f not in rec]
        if missing:
            raise RegistryError(f"Source {rec.get('source_id', '?')} missing fields: {missing}")
        out[rec["source_id"]] = rec
    return out


def load_caveats() -> dict[str, str]:
    """Return {caveat_id: text} from data/_meta/caveats.json."""
    return _load(META_DIR / "caveats.json").get("caveats", {})


def load_releases(dataset_dir: str) -> list[dict]:
    """Return the release list from data/<dataset_dir>/dataset_release.json."""
    raw = _load(DATA_DIR / dataset_dir / "dataset_release.json")
    releases = raw.get("releases", [])
    for rec in releases:
        missing = [f for f in RELEASE_REQUIRED if f not in rec]
        if missing:
            raise RegistryError(f"Release {rec.get('release_id', '?')} missing fields: {missing}")
        if rec["status"] not in VALID_STATUS:
            raise RegistryError(f"Release {rec['release_id']} has unknown status '{rec['status']}'")
    return releases


def current_release(dataset_dir: str) -> dict:
    """Return the single release marked status == 'current' for a dataset."""
    current = [r for r in load_releases(dataset_dir) if r["status"] == "current"]
    if len(current) != 1:
        raise RegistryError(
            f"Expected exactly one 'current' release in {dataset_dir}; found {len(current)}."
        )
    return current[0]


def caveat(caveat_id: str) -> str:
    """Resolve a caveat id to its canonical text, or raise if unknown."""
    caveats = load_caveats()
    if caveat_id not in caveats:
        raise RegistryError(f"Unknown caveat id: {caveat_id}")
    return caveats[caveat_id]


def validate_release_sources(dataset_dir: str, sources: dict[str, dict]) -> list[str]:
    """Return a list of problems where a release points at an unregistered source."""
    problems = []
    for rel in load_releases(dataset_dir):
        if rel["source_id"] not in sources:
            problems.append(
                f"Release {rel['release_id']} cites unregistered source '{rel['source_id']}'"
            )
    return problems


# Datasets with a release ledger to check. Add new dataset dirs here.
KNOWN_DATASETS = ("insolvency-statistics", "companies-house", "the-gazette", "ons-business", "payment-practices")


def _self_check() -> int:
    sources = load_sources()
    caveats = load_caveats()
    print(f"Sources:  {len(sources)} registered")
    for sid, rec in sources.items():
        print(f"  - {sid:28} [{rec['authority_level']:14}] {rec['status']}")
    print(f"Caveats:  {len(caveats)} in library")

    problems: list[str] = []
    for dataset in KNOWN_DATASETS:
        releases = load_releases(dataset)
        print(f"Releases ({dataset}): {len(releases)}")
        for rel in releases:
            prov = "provisional" if rel["is_provisional"] else "final"
            print(f"  - {rel['release_id']:24} {rel['status']:10} {prov}")
        problems += validate_release_sources(dataset, sources)

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(f"  ! {p}")
        return 1
    print("\nBackbone OK: every release traces to a registered source.")
    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(_self_check())
    except RegistryError as exc:
        print(f"REGISTRY ERROR: {exc}")
        sys.exit(2)
