"""
Editorial Quality Checker for cc_builder pages
================================================
Runs mechanical (Tier 1) checks from the Editorial OS governance files:
- Pre-publish gate checks (16-pre-publish-gate.md)
- Human-authorship self-audit (human-authorship-voice-engine.md)
- SEO signal checklist S1-S12 (18-seo-signal-governance.md)
- AI prose fingerprint detection (14-failure-modes-and-recovery.md §16)

Usage:
    python scripts/quality_check.py                    # Check all pages
    python scripts/quality_check.py --page travel      # Check one page
    python scripts/quality_check.py --verbose          # Show all details
"""

import importlib
import os
import re
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

PAGES_DIR = PROJECT_ROOT / "scripts" / "cc_builder" / "data" / "pages"


def load_page_config(slug: str) -> dict:
    """Load a page config by slug."""
    module_name = slug.replace("-", "_")
    module_path = PAGES_DIR / f"{module_name}.py"
    if not module_path.exists():
        raise FileNotFoundError(f"No page config: {module_path}")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PAGE_CONFIG


def extract_all_prose(config: dict) -> str:
    """Extract all prose/text content from a page config."""
    texts = []
    texts.append(config.get("title", ""))
    texts.append(config.get("meta_description", ""))

    for section in config.get("sections", []):
        stype = section.get("type", "")
        if stype == "prose":
            for p in section.get("paragraphs", []):
                texts.append(p)
        elif stype == "verdict_box":
            texts.append(section.get("verdict", ""))
            texts.append(section.get("best_for", ""))
            texts.append(section.get("watch_out", ""))
        elif stype == "heading":
            texts.append(section.get("text", ""))
        elif stype in ("tip", "warning", "info"):
            texts.append(section.get("content", ""))
        elif stype == "methodology":
            texts.append(section.get("content", ""))
        elif stype == "bottom_line":
            texts.append(section.get("content", ""))
        elif stype == "pros_cons":
            for p in section.get("pros", []):
                texts.append(p)
            for c in section.get("cons", []):
                texts.append(c)
        elif stype == "comparison_table":
            for row in section.get("rows", []):
                for cell in row:
                    texts.append(str(cell))
        elif stype == "table":
            texts.append(section.get("html", ""))

    # Also check card overrides
    for card_id, overrides in config.get("card_overrides", {}).items():
        for key in ("verdict", "best_for", "watch_out", "not_ideal", "fit_label", "eligibility"):
            if key in overrides:
                texts.append(str(overrides[key]))

    return "\n".join(texts)


def strip_html(text: str) -> str:
    """Remove HTML tags and entities for word counting."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def word_count(text: str) -> int:
    """Count words in cleaned text."""
    cleaned = strip_html(text)
    return len(cleaned.split()) if cleaned else 0


# ── CHECK FUNCTIONS ──────────────────────────────────────────────

def check_placeholders(prose: str) -> list[dict]:
    """Check for remaining [VERIFY], [NEEDS_IMAGE], [HUMAN CONFIRMATION] placeholders."""
    issues = []
    verify_count = len(re.findall(r"\[VERIFY[^\]]*\]", prose))
    image_count = len(re.findall(r"\[NEEDS_IMAGE\]", prose))
    human_count = len(re.findall(r"\[HUMAN CONFIRMATION[^\]]*\]", prose))

    if verify_count:
        issues.append({"check": "Placeholders", "severity": "warn",
                        "detail": f"{verify_count} [VERIFY] placeholder(s) remaining"})
    if image_count:
        issues.append({"check": "Placeholders", "severity": "warn",
                        "detail": f"{image_count} [NEEDS_IMAGE] placeholder(s) remaining"})
    if human_count:
        issues.append({"check": "Placeholders", "severity": "info",
                        "detail": f"{human_count} [HUMAN CONFIRMATION] flag(s)"})
    return issues


def check_voice_credibility(prose: str) -> list[dict]:
    """Check 1: Voice credibility — first person, padded evaluation, AI fingerprints."""
    issues = []
    cleaned = strip_html(prose)
    wc = word_count(prose)
    if wc == 0:
        return issues

    # First person count
    first_person_patterns = [
        r"\bI think\b", r"\bI believe\b", r"\bin my view\b",
        r"\bI would say\b", r"\bI find\b", r"\bfrom what I have seen\b",
        r"\bI should be clear\b", r"\bI would\b", r"\bI have\b",
    ]
    fp_count = 0
    for pat in first_person_patterns:
        fp_count += len(re.findall(pat, cleaned, re.IGNORECASE))

    fp_per_1k = (fp_count / wc) * 1000 if wc else 0
    if fp_per_1k > 5:
        issues.append({"check": "Voice: first person", "severity": "HARD_FAIL",
                        "detail": f"{fp_count} first-person instances ({fp_per_1k:.1f}/1k words, limit 5)"})

    # "I think" opening multiple sentences
    i_think_opens = len(re.findall(r"(?:^|\. )I think\b", cleaned, re.IGNORECASE))
    if i_think_opens > 1:
        issues.append({"check": "Voice: 'I think' opens", "severity": "HARD_FAIL",
                        "detail": f"'I think' opens {i_think_opens} sentences (limit 1)"})

    # Padded evaluation
    padded_phrases = [
        "genuinely good", "well-executed", "robust solution", "strong reputation",
        "strong option", "strong platform", "strong fit", "powerful tool",
        "comprehensive solution", "industry-leading", "best-in-class",
        "game-changer", "cutting-edge", "seamless experience",
    ]
    found_padded = []
    for phrase in padded_phrases:
        if phrase.lower() in cleaned.lower():
            found_padded.append(phrase)
    if len(found_padded) >= 2:
        issues.append({"check": "Voice: padded evaluation", "severity": "HARD_FAIL",
                        "detail": f"Padded phrases: {', '.join(found_padded)}"})
    elif found_padded:
        issues.append({"check": "Voice: padded evaluation", "severity": "warn",
                        "detail": f"Padded phrase: {found_padded[0]}"})

    return issues


def check_ai_fingerprints(prose: str) -> list[dict]:
    """Check for AI prose fingerprints (14-failure-modes-and-recovery.md §16)."""
    issues = []
    cleaned = strip_html(prose)

    fingerprints = {
        "synthetic transition": r"\b(that said|that being said|with that in mind|having said that|it['']s worth noting)\b",
        "hedge stack": r"\b(tend to|often|typically|generally|in many cases|for the most part)\b.*\b(tend to|often|typically|generally|in many cases|for the most part)\b",
        "list preamble": r"(?:here['']s|here is|let['']s (?:take a look|explore|dive|break down|walk through))",
        "false balance": r"\b(on the one hand|on the other hand|while.*there are also|pros and cons)\b",
        "empty intensifier": r"\b(very|really|extremely|incredibly|absolutely|truly) (important|useful|powerful|effective|valuable)\b",
        "filler transition": r"(?:^|\. )(now that we['']ve|moving on to|let['']s now|turning to|next up)\b",
        "AI summary opener": r"(?:^|\. )(in summary|to summarize|in conclusion|to wrap up|all in all)\b",
        "colon-list pattern": r":\s*\n",
        "rhetorical question": r"\?(?:\s|$).*\?(?:\s|$)",
        "breathless praise": r"\b(stands out|shines|excels|impressive|remarkable)\b",
    }

    found = []
    for name, pattern in fingerprints.items():
        matches = re.findall(pattern, cleaned, re.IGNORECASE | re.MULTILINE)
        if matches:
            found.append(name)

    if len(found) >= 3:
        issues.append({"check": "AI fingerprints", "severity": "HARD_FAIL",
                        "detail": f"{len(found)} distinct fingerprints: {', '.join(found)}"})
    elif len(found) >= 2:
        issues.append({"check": "AI fingerprints", "severity": "warn",
                        "detail": f"{len(found)} fingerprints: {', '.join(found)}"})

    return issues


def check_human_authorship(prose: str) -> list[dict]:
    """Check 1a: Human-authorship hard fails."""
    issues = []
    cleaned = strip_html(prose)
    wc = word_count(prose)
    if wc < 200:
        return issues

    # "you" density
    you_count = len(re.findall(r"\byou(?:r|['']re|['']ll|['']ve)?\b", cleaned, re.IGNORECASE))
    you_per_1k = (you_count / wc) * 1000
    if you_per_1k < 8:
        issues.append({"check": "Authorship: 'you' density", "severity": "HARD_FAIL",
                        "detail": f"{you_count} 'you' instances ({you_per_1k:.1f}/1k, need ≥8)"})

    # "we" density (editorial context)
    we_count = len(re.findall(r"\bwe(?:['']ve|['']re)?\b", cleaned, re.IGNORECASE))
    we_per_1k = (we_count / wc) * 1000
    if we_per_1k < 5:
        issues.append({"check": "Authorship: 'we' density", "severity": "HARD_FAIL",
                        "detail": f"{we_count} 'we' instances ({we_per_1k:.1f}/1k, need ≥5)"})

    # Sections >200 words with zero "you"
    paragraphs = re.split(r"\n\s*\n", cleaned)
    long_no_you = 0
    for para in paragraphs:
        para_wc = len(para.split())
        if para_wc > 200 and not re.search(r"\byou", para, re.IGNORECASE):
            long_no_you += 1
    if long_no_you:
        issues.append({"check": "Authorship: section without 'you'", "severity": "HARD_FAIL",
                        "detail": f"{long_no_you} section(s) >200 words with zero 'you'"})

    return issues


def check_seo_signals(config: dict, prose: str) -> list[dict]:
    """SEO signal checks S1-S12."""
    issues = []
    cleaned = strip_html(prose)
    title = config.get("title", "")
    meta = config.get("meta_description", "")

    # S1: Title-content match (basic check: title words appear in content)
    title_words = set(re.findall(r"\b\w{4,}\b", title.lower()))
    content_words = set(re.findall(r"\b\w{4,}\b", cleaned.lower()))
    missing_title_words = title_words - content_words
    if len(missing_title_words) > len(title_words) * 0.3:
        issues.append({"check": "S1: Title-content match", "severity": "warn",
                        "detail": f"Title words not in content: {missing_title_words}"})

    # S2: Generic anchor text
    generic_anchors = re.findall(
        r'<a[^>]*>(?:click here|read more|find out more|here|learn more|this guide|more information)</a>',
        prose, re.IGNORECASE
    )
    if generic_anchors:
        issues.append({"check": "S2: Generic anchor text", "severity": "HARD_FAIL",
                        "detail": f"{len(generic_anchors)} generic anchor(s) found"})

    # S3: Banned authenticity phrases
    banned = ["powerful tool", "industry-leading", "best-in-class",
              "game-changer", "cutting-edge", "seamless experience",
              "one-stop shop", "comprehensive solution"]
    found_banned = [b for b in banned if b.lower() in cleaned.lower()]
    if found_banned:
        issues.append({"check": "S3: Banned authenticity phrases", "severity": "warn",
                        "detail": f"Found: {', '.join(found_banned)}"})

    # S7: Author byline — check if methodology section exists (proxy)
    has_methodology = any(s.get("type") == "methodology" for s in config.get("sections", []))
    if not has_methodology:
        issues.append({"check": "S7: Methodology/author", "severity": "warn",
                        "detail": "No methodology section found"})

    # S8: Internal links out
    internal_links = re.findall(r'/business-credit-cards/[a-z-]+/', prose)
    unique_internal = set(internal_links)
    if len(unique_internal) < 2:
        issues.append({"check": "S8: Internal links out", "severity": "warn",
                        "detail": f"Only {len(unique_internal)} internal link(s), need ≥2"})

    # S11: Freshness date
    has_date = bool(config.get("verification_date"))
    if not has_date:
        issues.append({"check": "S11: Freshness date", "severity": "warn",
                        "detail": "No verification_date set"})

    # S12: Meta description
    if not meta or len(meta) < 50:
        issues.append({"check": "S12: Meta description", "severity": "warn",
                        "detail": f"Meta description too short ({len(meta)} chars)"})
    elif len(meta) > 160:
        issues.append({"check": "S12: Meta description length", "severity": "warn",
                        "detail": f"Meta description too long ({len(meta)} chars, limit 160)"})

    return issues


def check_comparison_trust(config: dict) -> list[dict]:
    """Comparison-specific trust architecture checks."""
    issues = []
    page_type = config.get("page_type", "")

    if page_type not in ("brand_compare", "roundup"):
        return issues

    # Check for verification_date on card overrides
    overrides = config.get("card_overrides", {})
    missing_verdicts = []
    for card_id, ov in overrides.items():
        if "verdict" not in ov or not ov["verdict"]:
            missing_verdicts.append(card_id)
    if missing_verdicts:
        issues.append({"check": "Trust: card verdicts", "severity": "warn",
                        "detail": f"Cards missing verdict overrides: {', '.join(missing_verdicts)}"})

    return issues


# ── RUNNER ────────────────────────────────────────────────────────

def run_checks(config: dict) -> dict:
    """Run all checks on a page config. Returns results dict."""
    prose = extract_all_prose(config)
    wc = word_count(prose)

    all_issues = []
    all_issues.extend(check_placeholders(prose))
    all_issues.extend(check_voice_credibility(prose))
    all_issues.extend(check_ai_fingerprints(prose))
    all_issues.extend(check_human_authorship(prose))
    all_issues.extend(check_seo_signals(config, prose))
    all_issues.extend(check_comparison_trust(config))

    hard_fails = [i for i in all_issues if i["severity"] == "HARD_FAIL"]
    warns = [i for i in all_issues if i["severity"] == "warn"]
    infos = [i for i in all_issues if i["severity"] == "info"]

    return {
        "word_count": wc,
        "hard_fails": hard_fails,
        "warnings": warns,
        "infos": infos,
        "pass": len(hard_fails) == 0,
    }


def main():
    import argparse
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(description="Editorial quality checker")
    parser.add_argument("--page", help="Check a single page by slug")
    parser.add_argument("--verbose", action="store_true", help="Show all details")
    args = parser.parse_args()

    # Discover pages
    if args.page:
        slugs = [args.page]
    else:
        slugs = []
        for f in sorted(PAGES_DIR.glob("*.py")):
            if f.name == "__init__.py":
                continue
            slugs.append(f.stem.replace("_", "-"))

    total_pass = 0
    total_fail = 0
    total_warns = 0

    print("=" * 70)
    print("EDITORIAL QUALITY CHECK — BusinessExpert Credit Cards")
    print("=" * 70)

    for slug in slugs:
        try:
            config = load_page_config(slug)
        except Exception as e:
            print(f"\n❌ {slug}: LOAD ERROR — {e}")
            total_fail += 1
            continue

        result = run_checks(config)
        status = "✅ PASS" if result["pass"] else "❌ FAIL"
        warn_count = len(result["warnings"])
        total_warns += warn_count

        print(f"\n{status}  {slug}  ({result['word_count']} words, {warn_count} warnings)")

        if result["hard_fails"]:
            total_fail += 1
            for issue in result["hard_fails"]:
                print(f"  ❌ HARD FAIL: {issue['check']} — {issue['detail']}")
        else:
            total_pass += 1

        if args.verbose or result["hard_fails"]:
            for issue in result["warnings"]:
                print(f"  ⚠️  {issue['check']} — {issue['detail']}")
            for issue in result["infos"]:
                print(f"  ℹ️  {issue['check']} — {issue['detail']}")

    print("\n" + "=" * 70)
    print(f"SUMMARY: {total_pass} pass, {total_fail} fail, {total_warns} total warnings")
    print("=" * 70)


if __name__ == "__main__":
    main()
