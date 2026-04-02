"""Resolve compact runtime-pack stacks for common Company Debt tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIR = ROOT / "runtime-packs"
EDITORIAL_DIR = ROOT / "editorial-os"


STAGE_PACKS = {
    "brief": "stages/brief.md",
    "source-grounding": "stages/source-grounding.md",
    "outline": "stages/outline.md",
    "draft": "stages/draft.md",
    "trust-pass": "stages/trust-pass.md",
    "adversarial-review": "stages/adversarial-review.md",
    "final-polish": "stages/final-polish.md",
}

TASK_BASE_PACKS = {
    "brief": ["writer-core.md"],
    "research": ["research-core.md"],
    "source-grounding": ["research-core.md", "writer-core.md"],
    "outline": ["writer-core.md"],
    "draft": ["writer-core.md"],
    "rewrite": ["writer-core.md", "review-core.md"],
    "trust-pass": ["review-core.md"],
    "review": ["review-core.md"],
    "adversarial-review": ["review-core.md"],
    "final-polish": ["writer-core.md", "review-core.md"],
    "build": ["build-core.md"],
    "deploy": ["deploy-core.md"],
}

TASK_CANONICAL = {
    "brief": ["01-master-methodology.md", "03-workflow-playbook.md", "17-audience-and-persona.md", "24-content-registry.md", "27-article-type-structure.md"],
    "research": ["10-evidence-governance.md", "19-editorial-image-evidence.md"],
    "source-grounding": ["10-evidence-governance.md", "04-trust-architecture.md", "25-update-logic.md", "26-call-out-box-governance.md"],
    "outline": ["12-structure-governance.md", "27-article-type-structure.md"],
    "draft": ["09-voice-governance.md", "12-structure-governance.md", "13-readability-governance.md", "17-audience-and-persona.md", "24-content-registry.md", "26-call-out-box-governance.md", "27-article-type-structure.md"],
    "rewrite": ["09-voice-governance.md", "12-structure-governance.md", "23-prose-quality-gates.md", "24-content-registry.md", "26-call-out-box-governance.md", "27-article-type-structure.md"],
    "trust-pass": ["10-evidence-governance.md", "16-pre-publish-gate.md", "23-prose-quality-gates.md", "24-content-registry.md", "25-update-logic.md", "26-call-out-box-governance.md"],
    "review": ["05-scoring-rubric.md", "14-failure-modes-and-recovery.md", "16-pre-publish-gate.md"],
    "adversarial-review": ["11-comparison-governance.md", "14-failure-modes-and-recovery.md", "16-pre-publish-gate.md", "24-content-registry.md", "26-call-out-box-governance.md"],
    "final-polish": ["13-readability-governance.md", "16-pre-publish-gate.md", "25-update-logic.md"],
    "build": ["20-build-time-quality-gate.md", "21-wordpress-technical-build-quality.md", "24-content-registry.md"],
    "deploy": ["16-pre-publish-gate.md", "20-build-time-quality-gate.md", "24-content-registry.md", "25-update-logic.md", "26-call-out-box-governance.md"],
}

ARTICLE_TYPE_CANONICAL = {
    "review": ["docs/article-types/review.md"],
    "roundup": ["docs/article-types/roundup.md"],
    "guide": ["docs/article-types/guide.md"],
    "comparison": ["docs/article-types/comparison.md"],
    "brand_compare": ["docs/article-types/comparison.md"],
    "brand_comparison": ["docs/article-types/comparison.md"],
}

PAGE_CLASS_OVERLAYS = {
    "entity_owner": "overlays/entity-owner.md",
    "entity_modifier": "overlays/entity-modifier.md",
    "trigger": "overlays/trigger.md",
    "enforcement": "overlays/enforcement.md",
    "director_risk": "overlays/director-risk.md",
    "pricing_cost": "overlays/pricing-cost.md",
    "process_guide": "overlays/process-guide.md",
    "recovery_strategy": "overlays/recovery-strategy.md",
    "debt_solution_comparison": "overlays/debt-solution-comparison.md",
    "legal_compliance": "overlays/legal-compliance.md",
    "case_insight": "overlays/case-insight.md",
}

PAGE_CLASS_CANONICAL = {
    "entity_owner": ["27-article-type-structure.md", "24-content-registry.md"],
    "entity_modifier": ["27-article-type-structure.md", "24-content-registry.md"],
    "trigger": ["27-article-type-structure.md", "24-content-registry.md"],
    "enforcement": ["27-article-type-structure.md", "24-content-registry.md"],
    "director_risk": ["27-article-type-structure.md", "24-content-registry.md"],
    "pricing_cost": ["27-article-type-structure.md", "24-content-registry.md"],
    "process_guide": ["27-article-type-structure.md", "24-content-registry.md"],
    "recovery_strategy": ["27-article-type-structure.md", "24-content-registry.md"],
    "debt_solution_comparison": ["27-article-type-structure.md", "24-content-registry.md"],
    "legal_compliance": ["27-article-type-structure.md", "24-content-registry.md"],
    "case_insight": ["27-article-type-structure.md", "24-content-registry.md"],
}


def normalize_page_type(page_type: str | None) -> str | None:
    if not page_type:
        return None
    lowered = page_type.strip().lower()
    if lowered in {"brand_compare", "brand-comparison", "brand_comparison"}:
        return "brand_compare"
    return lowered


def normalize_page_class(page_class: str | None) -> str | None:
    if not page_class:
        return None
    lowered = page_class.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "entityowner": "entity_owner",
        "entitymodifier": "entity_modifier",
        "directorrisk": "director_risk",
        "pricingcost": "pricing_cost",
        "processguide": "process_guide",
        "recoverystrategy": "recovery_strategy",
        "debtsolutioncomparison": "debt_solution_comparison",
        "legalcompliance": "legal_compliance",
        "caseinsight": "case_insight",
    }
    return aliases.get(lowered, lowered)


def infer_overlay_paths(page_type: str | None, slug: str | None = None, page_class: str | None = None) -> list[str]:
    normalized = normalize_page_type(page_type)
    normalized_page_class = normalize_page_class(page_class)
    slug = (slug or "").strip().lower()
    overlays: list[str] = []

    if normalized == "review":
        overlays.append("overlays/review.md")
    elif normalized == "roundup":
        overlays.append("overlays/roundup.md")
    elif normalized == "guide":
        overlays.append("overlays/guide.md")
    elif normalized in {"brand_compare", "comparison"}:
        overlays.append("overlays/comparison.md")
        if "-alternative" in slug or "alternative" in slug or slug.startswith("compare-"):
            overlays.append("overlays/alternatives.md")

    if normalized_page_class in PAGE_CLASS_OVERLAYS:
        overlay = PAGE_CLASS_OVERLAYS[normalized_page_class]
        if overlay not in overlays:
            overlays.append(overlay)

    return overlays


def resolve_runtime_context(task: str, *, page_type: str | None = None, slug: str | None = None, page_class: str | None = None) -> dict:
    normalized_task = task.strip().lower()
    if normalized_task not in TASK_BASE_PACKS:
        valid = ", ".join(sorted(TASK_BASE_PACKS))
        raise ValueError(f"Unknown task '{task}'. Valid tasks: {valid}")

    packs = list(TASK_BASE_PACKS[normalized_task])
    stage_pack = STAGE_PACKS.get(normalized_task)
    if stage_pack:
        packs.append(stage_pack)

    for overlay in infer_overlay_paths(page_type, slug, page_class):
        if overlay not in packs:
            packs.append(overlay)

    canonical = [str(EDITORIAL_DIR / rel) for rel in TASK_CANONICAL.get(normalized_task, [])]
    normalized_page_type = normalize_page_type(page_type)
    normalized_page_class = normalize_page_class(page_class)
    for rel in ARTICLE_TYPE_CANONICAL.get(normalized_page_type, []):
        canonical.append(str(EDITORIAL_DIR / rel))
    for rel in PAGE_CLASS_CANONICAL.get(normalized_page_class, []):
        path = str(EDITORIAL_DIR / rel)
        if path not in canonical:
            canonical.append(path)

    return {
        "task": normalized_task,
        "page_type": normalized_page_type,
        "page_class": normalized_page_class,
        "slug": slug,
        "runtime_packs": [str(RUNTIME_DIR / rel) for rel in packs],
        "canonical_refs": canonical,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect system-decided runtime pack stacks")
    parser.add_argument("--task", required=True, help="Task or workflow stage")
    parser.add_argument("--page-type", default=None, help="Page type, if known")
    parser.add_argument("--page-class", default=None, help="Company Debt page class, if known")
    parser.add_argument("--slug", default=None, help="Page slug, if known")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    recommendation = resolve_runtime_context(args.task, page_type=args.page_type, page_class=args.page_class, slug=args.slug)
    if args.json:
        print(json.dumps(recommendation, indent=2))
        return

    print(f"Task: {recommendation['task']}")
    if recommendation["page_type"]:
        print(f"Page type: {recommendation['page_type']}")
    if recommendation["page_class"]:
        print(f"Page class: {recommendation['page_class']}")
    if recommendation["slug"]:
        print(f"Slug: {recommendation['slug']}")

    print("\nRuntime packs:")
    for path in recommendation["runtime_packs"]:
        print(f"  - {path}")

    print("\nCanonical references to consult only if needed:")
    for path in recommendation["canonical_refs"]:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
