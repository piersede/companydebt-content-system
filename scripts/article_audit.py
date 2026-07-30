"""
Article Audit — Canonical Pre-Publish Gate for /drafts article HTML
===================================================================

Runs the Tier 1 (mechanical) and mechanical Tier 2 (structural) checks from
the Editorial OS canonical governance files against the HTML articles stored
in `/drafts/` (the rewrite worktree pattern).

Source of truth:
  - editorial-os/16-pre-publish-gate.md   (gate structure and hard-fail list)
  - editorial-os/13-readability-governance.md  (em dashes, paragraphs, emphasis)
  - editorial-os/09-voice-governance.md   (first-person, padded evaluation)
  - editorial-os/14-failure-modes-and-recovery.md §16  (AI fingerprints)

Emits per article:
  - Detailed pass/fail on each of the 25 scorable items
  - A binary GATE verdict (PASS / FAIL) driven by the canonical hard-fail list
  - A /25 score suitable for the Monday "Post Score" column

Tier 3 editorial checks (information gain per section, authored authority,
evaluative bite, concrete scenes) are NOT automated here — the script prints
a reminder that they remain a human or model-driven review step.

Usage:
    python scripts/article_audit.py --drafts drafts/ [--slug some-slug] [--json out.json]

Expected header in each draft HTML file (first three lines):
    <!-- TITLE: ... -->
    <!-- POST ID: 12345 / TYPE: pages / AUTHOR: 34 / FM: 70562 / TEMPLATE: templates/take-the-test-template.php -->
    <!-- LINK: https://... -->
"""

from __future__ import annotations
import argparse
import io
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

# Force UTF-8 stdout on Windows so emoji squares render without a charmap crash.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ---------------------------------------------------------------------------
# Constants drawn directly from the canonical files.
# ---------------------------------------------------------------------------

# editorial-os/09-voice-governance.md §4
FIRST_PERSON_SCAFFOLDING = [
    r"\bI think\b", r"\bI believe\b", r"\bin my view\b",
    r"\bI would say\b", r"\bI find\b", r"\bfrom what I have seen\b",
    r"\bI should be clear\b", r"\bI want to help you understand\b",
    r"\bI would not call this a dealbreaker\b", r"\bI would recommend\b",
    r"\bI want to be upfront\b", r"\bif I am being honest\b",
]

# editorial-os/09-voice-governance.md §5 — padded evaluation that must not stand alone.
PADDED_EVALUATION = [
    "genuinely good", "well-executed", "robust solution", "strong offering",
    "compelling platform", "solid choice", "capable tool",
    "impressive feature set", "thoughtfully designed", "comprehensive solution",
    "industry-leading", "best-in-class", "game-changer", "cutting-edge",
    "seamless experience", "one-stop shop", "powerful tool",
]

# editorial-os/14-failure-modes-and-recovery.md §16 — AI prose fingerprints.
AI_FINGERPRINTS = {
    "synthetic transition": r"\b(that said|that being said|with that in mind|having said that|it['\u2019]s worth noting)\b",
    "list preamble": r"(?:here['\u2019]s|here is|let['\u2019]s (?:take a look|explore|dive|break down|walk through))",
    "false balance": r"\b(on the one hand|on the other hand|while .* there are also|pros and cons)\b",
    "empty intensifier": r"\b(very|really|extremely|incredibly|absolutely|truly) (important|useful|powerful|effective|valuable)\b",
    "filler transition": r"(?:^|\. )(now that we['\u2019]ve|moving on to|let['\u2019]s now|turning to|next up)\b",
    "AI summary opener": r"(?:^|\. )(in summary|to summarize|in conclusion|to wrap up|all in all)\b",
    "breathless praise": r"\b(stands out|shines|excels|remarkable)\b",
}

# editorial-os/16-pre-publish-gate.md Check 14 — generic anchor text.
GENERIC_ANCHOR_RE = re.compile(
    r'<a[^>]*>\s*(click here|read more|find out more|here|learn more|this guide|more information)\s*</a>',
    re.IGNORECASE,
)

# editorial-os/16-pre-publish-gate.md Check 10 + feedback memory — banned opening patterns.
BAD_OPENING_PATTERNS = [
    r"this (page|article|guide) (explains|covers|tells|shows|will)",
    r"this (page|article|guide) break.?s? down",
    r"in this (page|article|guide)",
    r"welcome to",
    r"let['\u2019]s look at",
    r"this (page|article) is (for|about)",
]

# Company Debt internal link hosts (staging or production).
INTERNAL_HOSTS = ("companydebt.com", "comdebstage.wpengine.com")

# Author ID for Chris Andersen per repo convention (feedback memory).
CHRIS_ANDERSEN_AUTHOR_ID = "34"

# Recognised page-template filename fragments. The take-the-test template is
# the default for insolvency guide pages; sector posts (/sectors/*) use the
# post-sectors.php page-builder template instead. Either is acceptable.
TAKE_THE_TEST_TEMPLATE = "take-the-test"
SECTOR_TEMPLATE = "post-sectors"
RECOGNISED_TEMPLATES = (TAKE_THE_TEST_TEMPLATE, SECTOR_TEMPLATE)


# ---------------------------------------------------------------------------
# Core data structures.
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    id: str
    name: str
    tier: str           # "T1", "T2"
    passed: bool
    detail: str = ""
    hard_fail: bool = True  # canonical gate treats all named checks as hard fails

@dataclass
class ArticleAudit:
    path: str
    title: str
    post_id: str
    author: str
    featured_media: str
    template: str
    word_count: int
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(1 for c in self.checks if c.passed)

    @property
    def max_score(self) -> int:
        return len(self.checks)

    @property
    def gate_passed(self) -> bool:
        return all(c.passed for c in self.checks if c.hard_fail)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["score"] = self.score
        d["max_score"] = self.max_score
        d["gate_passed"] = self.gate_passed
        return d


# ---------------------------------------------------------------------------
# Utility helpers.
# ---------------------------------------------------------------------------

def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


def _strip_wp_comments(html: str) -> str:
    """Remove WordPress block comments but preserve the text inside blocks."""
    return re.sub(r"<!--[^-]*(?:-[^-]+)*-->", "", html)


def _extract_metadata(raw: str) -> dict[str, str]:
    meta = {"title": "", "post_id": "", "author": "", "featured_media": "", "template": ""}
    t = re.search(r"<!--\s*TITLE:\s*(.*?)\s*-->", raw)
    if t:
        meta["title"] = t.group(1)
    p = re.search(
        r"POST ID:\s*(\d+)\s*/\s*TYPE:\s*\S+\s*/\s*AUTHOR:\s*(\w+)\s*/\s*FM:\s*(\S+?)\s*/\s*TEMPLATE:\s*(\S+)",
        raw,
    )
    if p:
        meta["post_id"], meta["author"], meta["featured_media"], meta["template"] = p.groups()
    return meta


def _body_after_metadata(raw: str) -> str:
    """Return the article body with the three header comment lines removed."""
    body = re.sub(r"^<!--\s*(TITLE:|POST ID:|LINK:)[^\n]*\n", "", raw, flags=re.M)
    return body.strip()


def _strip_sources_section(body: str) -> str:
    """
    Em dashes are acceptable inside the Sources & References list (citation
    format). Strip that section before counting em dashes elsewhere so the
    mechanical check reflects the canonical rule.

    Recognises both the legacy `<h2>Sources & References</h2>` form and the
    canonical `<aside class="cd-sources">` / `<aside class="sources-block">` form.
    """
    # Canonical aside form
    for cls in ("cd-sources", "sources-block"):
        m = re.search(
            rf'<aside\s+class=["\']{cls}["\']', body, re.I,
        )
        if m:
            return body[: m.start()]
    # Legacy H2 form
    m = re.search(r"<h2[^>]*>\s*Sources\s*&amp;\s*References\s*</h2>", body, re.I)
    if not m:
        m = re.search(r"<h2[^>]*>\s*Sources\s*&\s*References\s*</h2>", body, re.I)
    return body[: m.start()] if m else body


def _h2_texts(body: str) -> list[str]:
    return [
        _strip_tags(h).strip()
        for h in re.findall(r"<h2[^>]*>(.*?)</h2>", body, re.I | re.S)
    ]


def _first_paragraphs(body: str, n: int = 3) -> list[str]:
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.I | re.S)[:n]
    return [_strip_tags(p).strip() for p in paras]


def _prose_text(body: str) -> str:
    text = _strip_wp_comments(body)
    text = _strip_tags(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Individual checks.
# ---------------------------------------------------------------------------

def check_em_dashes(body_excl_sources: str) -> CheckResult:
    """
    editorial-os/13-readability-governance.md §2:
    'Maximum 1 per article. Zero is preferred.' (Sources citation format exempt.)
    """
    count = body_excl_sources.count("\u2014")
    return CheckResult(
        id="01", tier="T1",
        name="Em dashes \u2264 1 in body (excluding Sources)",
        passed=count <= 1,
        detail=f"{count} em dash(es) in body",
    )


def check_first_person_density(prose: str, wc: int) -> CheckResult:
    """
    editorial-os/16-pre-publish-gate.md Check 1: 'More than 5 first-person
    instances per 1,000 words' is a hard fail. We count I / me / my / we-as-
    personal-scaffolding phrases.
    """
    count = 0
    for pat in FIRST_PERSON_SCAFFOLDING:
        count += len(re.findall(pat, prose, re.I))
    # raw "I" pronouns as well
    count += len(re.findall(r"\bI\b", prose))
    per_1k = (count / wc * 1000) if wc else 0
    return CheckResult(
        id="02", tier="T1",
        name="First-person I/me/my density < 5 / 1k (ceiling)",
        passed=per_1k < 5,
        detail=f"{count} instance(s), {per_1k:.1f}/1k",
    )


def check_you_density(prose: str, wc: int) -> CheckResult:
    """
    editorial-os/16-pre-publish-gate.md Check 1a hard fail:
    '"you" density below 8 per 1,000 words'.
    """
    count = len(re.findall(r"\byou(?:r|[\u2019']re|[\u2019']ll|[\u2019']ve|[\u2019']d)?\b|\byours?\b", prose, re.I))
    per_1k = (count / wc * 1000) if wc else 0
    return CheckResult(
        id="03", tier="T1",
        name="'you' density \u2265 8 / 1k",
        passed=per_1k >= 8,
        detail=f"{count} instance(s), {per_1k:.1f}/1k",
    )


def check_we_density(prose: str, wc: int) -> CheckResult:
    """
    editorial-os/16-pre-publish-gate.md Check 1a hard fail:
    '"we" density below 5 per 1,000 words where editorial judgement is present'.
    """
    count = len(re.findall(r"\bwe(?:[\u2019']ve|[\u2019']re|[\u2019']ll|[\u2019']d)?\b|\bour\b|\bus\b", prose, re.I))
    per_1k = (count / wc * 1000) if wc else 0
    return CheckResult(
        id="04", tier="T1",
        name="'we/our/us' density \u2265 5 / 1k",
        passed=per_1k >= 5,
        detail=f"{count} instance(s), {per_1k:.1f}/1k",
    )


def check_i_think_opens(prose: str) -> CheckResult:
    """
    editorial-os/09-voice-governance.md §4: "'I think' must not appear as the
    opening phrase of more than one sentence in any article."
    """
    count = len(re.findall(r"(?:^|\.\s+)I think\b", prose))
    return CheckResult(
        id="05", tier="T1",
        name="'I think' opens \u2264 1 sentence",
        passed=count <= 1,
        detail=f"{count} 'I think' sentence-opens",
    )


def check_ai_fingerprints(prose: str) -> CheckResult:
    """
    editorial-os/14-failure-modes-and-recovery.md §16: 3+ distinct fingerprints
    is a hard fail.
    """
    found = []
    for name, pattern in AI_FINGERPRINTS.items():
        if re.search(pattern, prose, re.I | re.M):
            found.append(name)
    return CheckResult(
        id="06", tier="T1",
        name="AI fingerprints < 3 distinct",
        passed=len(found) < 3,
        detail=f"{len(found)} fingerprint(s): {', '.join(found) if found else 'none'}",
    )


def check_padded_evaluation(prose: str) -> CheckResult:
    """
    editorial-os/09-voice-governance.md §5: listed padded phrases must not
    appear as stand-alone evaluation. We fail on 2+ occurrences as a proxy
    for the gate's 'multiple instances' hard fail.
    """
    found = [p for p in PADDED_EVALUATION if p.lower() in prose.lower()]
    return CheckResult(
        id="07", tier="T1",
        name="Padded evaluation phrases \u2264 1",
        passed=len(found) <= 1,
        detail=f"{len(found)} found: {', '.join(found) if found else 'none'}",
    )


def check_generic_anchors(raw_html: str) -> CheckResult:
    """
    editorial-os/16-pre-publish-gate.md Check 14 hard fail:
    any generic anchor text ('click here', 'read more', etc.) blocks publish.
    """
    hits = GENERIC_ANCHOR_RE.findall(raw_html)
    return CheckResult(
        id="08", tier="T1",
        name="No generic anchor text",
        passed=len(hits) == 0,
        detail=f"{len(hits)} generic anchor(s)" if hits else "clean",
    )


def check_banned_openings(body: str) -> CheckResult:
    """
    editorial-os/16-pre-publish-gate.md Check 10 hard fail:
    'Opening is generic, delayed, or uses a banned pattern.' Plus the
    feedback_no_this_page_explains.md memory rule.
    """
    paras = _first_paragraphs(body, n=3)
    matches = []
    for i, t in enumerate(paras):
        for pat in BAD_OPENING_PATTERNS:
            if re.search(pat, t, re.I):
                matches.append(f"P{i+1}: {pat}")
                break
    return CheckResult(
        id="09", tier="T1",
        name="Opening P1\u2013P3 clear of banned patterns",
        passed=len(matches) == 0,
        detail=f"{len(matches)} match(es): {'; '.join(matches) if matches else 'clean'}",
    )


def check_word_count(wc: int) -> CheckResult:
    return CheckResult(
        id="10", tier="T2",
        name="Word count \u2265 800",
        passed=wc >= 800,
        detail=f"{wc} words",
        hard_fail=False,  # the gate has no explicit floor; flag as advisory.
    )


def check_featured_image(fm: str) -> CheckResult:
    return CheckResult(
        id="11", tier="T2",
        name="Featured image set",
        passed=fm not in ("", "0", "None", "?"),
        detail=f"FM={fm}",
    )


def check_no_body_hero(body: str) -> CheckResult:
    """
    Repo convention (feedback_no_hero_image_in_body.md): the featured image is
    theme-level only. No <img> injected near the top of body content.
    We scan the first ~2000 chars of body prose for a wp-block-image figure.
    """
    head = body[:2000]
    has_hero = bool(re.search(r'<figure[^>]+wp-block-image|<img\b', head, re.I))
    return CheckResult(
        id="12", tier="T2",
        name="No hero image in body (within first 2k chars)",
        passed=not has_hero,
        detail="hero image present in body head" if has_hero else "clean",
    )


def check_template(template: str) -> CheckResult:
    return CheckResult(
        id="13", tier="T2",
        name="Template is take-the-test or post-sectors",
        passed=any(frag in template for frag in RECOGNISED_TEMPLATES),
        detail=f"template={template}",
    )


def check_author(author: str) -> CheckResult:
    return CheckResult(
        id="14", tier="T2",
        name="Author = Chris Andersen (ID 34)",
        passed=author == CHRIS_ANDERSEN_AUTHOR_ID,
        detail=f"author_id={author}",
    )


def check_internal_links(body: str) -> CheckResult:
    """
    editorial-os/16-pre-publish-gate.md Check 14:
    'Article links to at least 2 other site pages with descriptive anchors.'
    Repo memory (feedback_internal_links_minimum.md) tightens this to \u22653.
    """
    hrefs = re.findall(r'href=["\\\']([^"\\\']+)["\\\']', body)
    internal = [h for h in hrefs if any(host in h for host in INTERNAL_HOSTS) or (h.startswith("/") and not h.startswith("//"))]
    return CheckResult(
        id="15", tier="T2",
        name="Internal links \u2265 3",
        passed=len(internal) >= 3,
        detail=f"{len(internal)} internal link(s)",
    )


def check_faq_accordion(raw_html: str, body: str) -> CheckResult:
    """
    Repo memory (feedback_faqs_accordion.md): FAQs must be in accordion format.
    The Ultimate Blocks wp:ub/content-toggle-block emits FAQPage schema on the
    front end, so its presence satisfies both the accordion and schema rules.

    Per editorial-os/28-htag-semantic-framework.md (changed 2026-07-08),
    Related Guides must be the FINAL H2 in the main article flow, immediately
    after FAQ. Methodology and Sources blocks must sit OUTSIDE the H2
    hierarchy (as styled labels in a footer/aside/div, not as h2). Any H2
    other than Related Guides appearing AFTER the FAQ H2 is a hierarchy
    violation.
    """
    name = "FAQ accordion present + Related Guides is final H2"
    has_ub = bool(re.search(r"wp:ub/content-toggle", raw_html, re.I))
    if not has_ub:
        return CheckResult(
            id="16", tier="T2", name=name, passed=False,
            detail="no accordion block found",
        )
    # Find the FAQ H2 position
    faq_re = re.compile(r"<h2[^>]*>\s*(?:Frequently\s+Asked\s+Questions|FAQs?\b)", re.I)
    m = faq_re.search(body)
    if not m:
        return CheckResult(
            id="16", tier="T2", name=name, passed=False,
            detail="accordion present but no FAQ H2 found",
        )
    # Everything after the FAQ H2 must be exactly one Related Guides H2, and
    # nothing else.
    tail = body[m.end():]
    later_h2s = re.findall(r"<h2[^>]*>([^<]{0,80})", tail)
    if not later_h2s:
        return CheckResult(
            id="16", tier="T2", name=name, passed=False,
            detail="FAQ found but no Related Guides H2 follows it",
        )
    if len(later_h2s) > 1:
        extra = later_h2s[1].strip()
        return CheckResult(
            id="16", tier="T2", name=name, passed=False,
            detail=f"H2 follows Related Guides: '{extra[:60]}'",
        )
    related_text = later_h2s[0].strip()
    if not re.search(r"Related\s+Guides?", related_text, re.I):
        return CheckResult(
            id="16", tier="T2", name=name, passed=False,
            detail=f"H2 after FAQ is not Related Guides: '{related_text[:60]}'",
        )
    return CheckResult(
        id="16", tier="T2", name=name, passed=True,
        detail="wp:ub/content-toggle present, Related Guides is final H2 after FAQ",
    )


def check_methodology(body: str) -> CheckResult:
    """
    editorial-os/16-pre-publish-gate.md Check 3 + Check 10:
    decision-stage pages require a Methodology block.

    Per editorial-os/28-htag-semantic-framework.md (April 2026 update),
    Methodology/Disclosure should NOT sit in the main H-tag flow as an H2 —
    that promotes it into the article hierarchy and pushes editorial H2s
    out of the FAQs-as-final-H2 discipline. Detection is heading-agnostic:
    we look for the Methodology/Disclosure label as a heading (h2/h3/h4/h5/h6)
    OR as a styled label inside a div/section/aside (typically <strong> or
    <p class="...">), provided it is followed by editorial-process or
    disclosure content within ~2,000 chars.
    """
    # Heading match (any level) OR styled label match
    label_re = re.compile(
        r"(?:<h[2-6][^>]*>|<(?:strong|b|p|div|span|aside|footer)[^>]*>)\s*"
        r"Methodology(?:\s*(?:&amp;|&|and)\s*Disclosure)?",
        re.I,
    )
    m = label_re.search(body)
    if not m:
        return CheckResult(id="17", tier="T2",
                           name="Methodology & Disclosure block present",
                           passed=False)
    # Must be followed by some editorial-process content within 2k chars
    tail = body[m.end():m.end() + 2000].lower()
    has_substance = (
        "editorial team" in tail or "reviewed" in tail or "written by" in tail
        or "company debt" in tail or "insolvency practitioner" in tail
    )
    return CheckResult(
        id="17", tier="T2",
        name="Methodology & Disclosure block present",
        passed=has_substance,
        detail="block found" if has_substance else "label found but no substance within 2k chars",
    )


def check_sources(body: str) -> CheckResult:
    """
    editorial-os/10-evidence-governance.md §7 + §7b — Sources & References required,
    every entry must carry a clickable URL when one exists publicly.

    Per editorial-os/28-htag-semantic-framework.md (April 2026 update),
    Sources/References should NOT sit in the main H-tag flow as an H2.
    Detection is heading-agnostic (any heading level OR styled label).

    Pass criteria:
      - Block label present (h2-h6 OR styled label)
      - At least one gov.uk / legislation.gov.uk link nearby (substance check)
      - Every <li> within the Sources block contains either
          (a) an <a href="..."> link, OR
          (b) an explicit opt-out marker: <!-- no-url: <reason> -->
        per editorial-os/10-evidence-governance.md §7b "Source link requirement".
      - The anchor on each <li> must NOT be a suffix-only domain link.
        Anti-pattern: '<li>Citation title plain text - <a>legislation.gov.uk</a></li>'
        where the descriptive citation is unclickable and only the trailing
        domain is the link. Citation titles must be the clickable element
        (or the entire <li> contents must be wrapped in the anchor).
    """
    label_re = re.compile(
        r"(?:<h[2-6][^>]*>|<(?:strong|b|p|div|span|aside|footer)[^>]*>)\s*"
        r"Sources\s*(?:&amp;|&|and)?\s*References",
        re.I,
    )
    m = label_re.search(body)
    if not m:
        return CheckResult(id="18", tier="T2",
                           name="Sources & References block present",
                           passed=False)

    # Region of interest: from label to end of next </ul> (or 6k chars fallback)
    region_end = body.find("</ul>", m.end())
    if region_end == -1:
        region_end = m.end() + 6000
    else:
        region_end += len("</ul>")
    region = body[m.end():region_end]
    region_lower = region.lower()

    has_substance = "legislation.gov.uk" in region_lower or "gov.uk" in region_lower
    if not has_substance:
        return CheckResult(
            id="18", tier="T2",
            name="Sources & References block present",
            passed=False,
            detail="label found but no gov.uk/legislation.gov.uk link nearby",
        )

    # Source link requirement: every <li> must carry an <a href> OR an explicit no-url opt-out.
    li_blocks = re.findall(r"<li[^>]*>(.*?)</li>", region, re.DOTALL | re.I)
    if not li_blocks:
        # No <li> structure — fall through to substance-only pass (some sources blocks
        # are paragraph-style; we don't enforce <li> structure here).
        return CheckResult(
            id="18", tier="T2",
            name="Sources & References block present",
            passed=True,
            detail="block found (no <li> structure)",
        )

    no_link: list[str] = []
    for li in li_blocks:
        has_link = bool(re.search(r"<a\s[^>]*href=[\"'][^\"']+[\"']", li, re.I))
        has_opt_out = bool(re.search(r"<!--\s*no-url\b[^>]*-->", li, re.I))
        if not has_link and not has_opt_out:
            # Capture first 60 chars of bullet text for the failure message
            text = re.sub(r"<[^>]+>", "", li).strip()
            no_link.append(text[:60])

    if no_link:
        sample = "; ".join(no_link[:3])
        return CheckResult(
            id="18", tier="T2",
            name="Sources & References block present",
            passed=False,
            detail=f"{len(no_link)} source bullet(s) without a link or no-url opt-out: {sample}",
        )

    # Anti-pattern: suffix-only anchor.
    # Form: '<li>Citation title plain text - <a href="...">legislation.gov.uk</a></li>'
    # The descriptive citation is unclickable; only the trailing domain is the link.
    # Detect: substantial plain text outside anchors AND every anchor text matches a
    # bare-hostname pattern (no spaces, dot-separated).
    domain_only_re = re.compile(r"^(www\.)?[a-z0-9-]+(\.[a-z0-9-]+){1,3}$", re.I)
    suffix_only: list[str] = []
    for li in li_blocks:
        # Extract anchor texts
        anchor_texts = [
            re.sub(r"<[^>]+>", "", a).strip()
            for a in re.findall(r"<a\s[^>]*>(.*?)</a>", li, re.DOTALL | re.I)
        ]
        if not anchor_texts:
            continue  # no-anchor case already failed above
        # Skip opt-outs
        if re.search(r"<!--\s*no-url\b[^>]*-->", li, re.I):
            continue
        # Plain text outside any anchor
        masked = re.sub(r"<a\s[^>]*>.*?</a>", "", li, flags=re.DOTALL | re.I)
        plain_outside = re.sub(r"<[^>]+>", "", masked).strip()
        # Strip cosmetic separators ("- ", " : ", ".") from the count
        plain_compact = re.sub(r"[-:.\s]+", "", plain_outside)
        if (
            len(plain_compact) > 20
            and all(domain_only_re.match(at) for at in anchor_texts)
        ):
            text = re.sub(r"<[^>]+>", "", li).strip()
            suffix_only.append(text[:70])

    if suffix_only:
        sample = "; ".join(suffix_only[:3])
        return CheckResult(
            id="18", tier="T2",
            name="Sources & References block present",
            passed=False,
            detail=(
                f"{len(suffix_only)} source bullet(s) use suffix-only anchor "
                f"(citation title is plain text, only domain is linked): {sample}"
            ),
        )

    return CheckResult(
        id="18", tier="T2",
        name="Sources & References block present",
        passed=True,
        detail=f"{len(li_blocks)} sources, all linked",
    )


def check_keyword_h2s(title: str, body: str) -> CheckResult:
    """
    Repo memory (feedback_keyword_rich_htags.md): H2s must be keyword-rich.
    We require at least one meaningful title word to appear in \u2265 30% of H2s.
    """
    h2s = [t.lower() for t in _h2_texts(body)]
    stop = {"what", "when", "where", "how", "why", "does", "the", "and",
            "that", "for", "with", "your", "this", "into", "about"}
    # Only consider words with >3 chars and not in stop list, take first 3.
    title_words = [w.lower() for w in re.findall(r"\w+", title)
                   if len(w) > 3 and w.lower() not in stop and not w.isdigit()][:3]
    if not h2s or not title_words:
        return CheckResult(id="19", tier="T2", name="Keyword-rich H2s", passed=False,
                           detail="no H2s or no title keywords to check")
    hits = sum(1 for h in h2s if any(w in h for w in title_words))
    ratio = hits / len(h2s)
    return CheckResult(
        id="19", tier="T2",
        name="Keyword-rich H2s (\u2265 30% contain title keyword)",
        passed=ratio >= 0.30,
        detail=f"{hits}/{len(h2s)} H2s contain a title keyword ({ratio:.0%})",
    )


def check_table_cell_brevity(body: str) -> CheckResult:
    """
    editorial-os/13-readability-governance.md §3c — Table cell brevity (HARD RULE).

    Table cells are scan units, not paragraphs. Long cells stack badly on
    mobile, defeat the table's job (reader scans, doesn't read), and usually
    indicate the H2 should be paragraph form instead.

    Thresholds:
      <th> column header: 50 chars hard ceiling (target 30)
      <td> body cell:     200 chars hard ceiling (target 120)

    Soft fail (paragraph-length sibling): the gate still passes, but the
    flag should be treated as a real signal during review.
    """
    th_offenders: list[str] = []
    td_offenders: list[str] = []

    for tm in re.finditer(r"<table\b[^>]*>(.*?)</table>", body, re.DOTALL | re.I):
        table = tm.group(1)
        for th in re.findall(r"<th\b[^>]*>(.*?)</th>", table, re.DOTALL | re.I):
            text = re.sub(r"<[^>]+>", "", th).strip()
            if len(text) > 50:
                th_offenders.append(f"{len(text)}ch: {text[:60]}")
        for td in re.findall(r"<td\b[^>]*>(.*?)</td>", table, re.DOTALL | re.I):
            text = re.sub(r"<[^>]+>", "", td).strip()
            if len(text) > 200:
                td_offenders.append(f"{len(text)}ch: {text[:60]}")

    total = len(th_offenders) + len(td_offenders)
    if total == 0:
        return CheckResult(
            id="24", tier="T2",
            name="Table cells concise (<th> ≤50ch, <td> ≤200ch)",
            passed=True,
            hard_fail=False,
        )

    parts: list[str] = []
    if th_offenders:
        parts.append(f"{len(th_offenders)} <th> over 50ch")
    if td_offenders:
        parts.append(f"{len(td_offenders)} <td> over 200ch")
    sample = (th_offenders[:2] + td_offenders[:2])[:3]
    return CheckResult(
        id="24", tier="T2",
        name="Table cells concise (<th> ≤50ch, <td> ≤200ch)",
        passed=False,
        detail=f"{', '.join(parts)} — {'; '.join(sample)}",
        hard_fail=False,  # soft, like paragraph-length
    )


def check_no_strong_in_auto_bolded_table_cells(body: str) -> CheckResult:
    """
    editorial-os/13-readability-governance.md §3b — Auto-bolded contexts (HARD RULE).

    Theme CSS auto-bolds two table contexts:
        .main-content table thead th { font-weight: 700; }
        .main-content table tbody tr td:first-child { font-weight: 600; }

    Wrapping <th> header text or first-column <td> cells in <strong> or <b>
    is redundant and was the cause of double-bold table-cell rendering on
    /liquidation/ before the bolder→700 theme fix landed (May 2026). The
    theme fix prevents the visual compounding, but the writing rule still
    applies as defence in depth: a future theme change or a different theme
    family could reintroduce the cascade.

    Pass criteria: no <strong>/<b> inside <th> elements anywhere in <thead>,
    and no <strong>/<b> inside the first <td> of each <tr> within <tbody>.
    """
    # Iterate every <table>...</table> in the body
    offenders: list[str] = []
    for tm in re.finditer(r"<table\b[^>]*>(.*?)</table>", body, re.DOTALL | re.I):
        table = tm.group(1)
        # Check thead <th> cells
        thead_match = re.search(r"<thead\b[^>]*>(.*?)</thead>", table, re.DOTALL | re.I)
        if thead_match:
            for th in re.findall(r"<th\b[^>]*>(.*?)</th>", thead_match.group(1), re.DOTALL | re.I):
                if re.search(r"<(?:strong|b)\b", th, re.I):
                    text = re.sub(r"<[^>]+>", "", th).strip()
                    offenders.append(f"<th>: {text[:50]}")
        # Check tbody first-<td> per row
        tbody_match = re.search(r"<tbody\b[^>]*>(.*?)</tbody>", table, re.DOTALL | re.I)
        rows_source = tbody_match.group(1) if tbody_match else table
        # Skip thead rows if no <tbody> wrapper
        if not tbody_match and thead_match:
            rows_source = rows_source.replace(thead_match.group(0), "")
        for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", rows_source, re.DOTALL | re.I):
            first_td = re.search(r"<td\b[^>]*>(.*?)</td>", tr, re.DOTALL | re.I)
            if first_td and re.search(r"<(?:strong|b)\b", first_td.group(1), re.I):
                text = re.sub(r"<[^>]+>", "", first_td.group(1)).strip()
                offenders.append(f"<td:first>: {text[:50]}")

    if offenders:
        sample = "; ".join(offenders[:3])
        return CheckResult(
            id="23", tier="T2",
            name="No <strong>/<b> in <th> or first-column <td> (theme auto-bolds)",
            passed=False,
            detail=f"{len(offenders)} cell(s) with redundant emphasis: {sample}",
        )
    return CheckResult(
        id="23", tier="T2",
        name="No <strong>/<b> in <th> or first-column <td> (theme auto-bolds)",
        passed=True,
    )


def check_block_comment_json_no_raw_html(raw_html: str) -> CheckResult:
    """
    Gutenberg block markers carry attribute values as inline JSON inside
    HTML comments, e.g.:
        <!-- wp:ub/content-toggle-panel-block {"panelTitle":"\\u003cstrong\\u003e..."} -->

    If a writer puts raw HTML in a JSON string value (e.g. panelTitle:"<strong>..."),
    WordPress's content_save_pre filters HTML-escape the inner block-comment
    marker on save, which breaks the Gutenberg block parser and the inner
    blocks never render (Ultimate Blocks accordion panels collapse to escaped
    text). The fix is to JSON-unicode-escape the < and > characters in
    attribute values:
        "panelTitle":"\\u003cstrong\\u003e..."  ✓
        "panelTitle":"<strong>..."              ✗ (this check fails)

    This check scans every <!-- wp:... {...} --> marker and flags any JSON
    attribute string that contains raw < or > characters. The fix is
    automated by tools/escape_block_attrs.py once that exists; for now,
    writers manually replace <X> with \\u003cX\\u003e in panelTitle and
    similar attributes.
    """
    # Match block-comment markers with JSON attributes.
    #
    # This pattern used to be r"<!--\s*wp:[\w/-]+\s+(\{[^}]*\})\s*-->", which silently
    # skipped the blocks most likely to break, and so reported a green pass on them:
    #   1. [^}]* stops at the FIRST closing brace, so any block with nested JSON
    #      (e.g. "padding":{"top":"0"...},"margin":{...} — i.e. most CTA blocks)
    #      never matched at all.
    #   2. It required "-->" and did not allow the self-closing "/-->" form that
    #      void blocks like ub/call-to-action-block use.
    # A raw <strong> in a CTA block's JSON therefore sailed through this T1 check and
    # dumped the whole block comment onto the page as literal text (23698, 2026-07-14).
    # Non-greedy to the last brace before the closing marker handles nesting correctly.
    block_re = re.compile(r"<!--\s*wp:[\w/-]+\s+(\{.*?\})\s*/?-->", re.DOTALL)
    offenders: list[str] = []
    # Detect malformed Unicode escapes — common breakage pattern is a writer dropping
    # the leading backslash, leaving "u003cstrong" instead of "<strong". The literal
    # text then renders on the page as "u003c..." in the FAQ panel title.
    malformed_escape_re = re.compile(r"(?<!\\)u003[ce]", re.I)
    # Detect HTML-entity-encoded block markers: `&lt;!-- wp:... --&gt;` or
    # `&lt;!-- wp:... /--&gt;`. WordPress never sees these as Gutenberg blocks because
    # the parser only recognises raw `<!--` delimiters; the JSON renders as literal
    # text on the page (seen 2026-05-11 on directors-duties-to-creditors CTA).
    encoded_marker_re = re.compile(r"&lt;!--\s*wp:[\w/-]+", re.IGNORECASE)
    encoded_count = len(encoded_marker_re.findall(raw_html))
    if encoded_count:
        offenders.append(
            f"{encoded_count} HTML-entity-encoded block marker(s) found (&lt;!-- wp:... --&gt;) — "
            "Gutenberg parser will not recognise these; JSON will render as literal text"
        )
    for m in block_re.finditer(raw_html):
        json_blob = m.group(1)
        # Find string values: "key":"value"  -- look for raw < or > inside the value
        # Skip values where < is already <-escaped
        for sm in re.finditer(r'"([^"]+)"\s*:\s*"((?:\\.|[^"\\])*)"', json_blob):
            key = sm.group(1)
            value = sm.group(2)
            if "<" in value or ">" in value:
                offenders.append(f"{key}: raw HTML — {value[:60]}")
            elif malformed_escape_re.search(value):
                offenders.append(f"{key}: malformed unicode escape (literal 'u003c'/'u003e' without leading backslash) — {value[:60]}")
    if offenders:
        sample = "; ".join(offenders[:3])
        return CheckResult(
            id="22", tier="T1",
            name="Block-comment JSON attrs use \\u003c-escapes for HTML",
            passed=False,
            detail=f"{len(offenders)} attr(s) malformed: {sample}",
        )
    return CheckResult(
        id="22", tier="T1",
        name="Block-comment JSON attrs use \\u003c-escapes for HTML",
        passed=True,
    )


def check_lead_paragraph_no_strong(body: str) -> CheckResult:
    """
    editorial-os/13-readability-governance.md §3b — Lead paragraph emphasis (HARD RULE).

    Theme CSS auto-bolds the first paragraph of every article:
        .site-main .main-content > p:first-of-type { font-weight: 700; }
        .content > p:first-of-type                 { font-weight: 700; }

    Combined with the global rule `b, strong { font-weight: bolder; }`, any
    <strong> or <b> inside the first <p> escalates to weight 800/900 because
    `bolder` resolves relative to the parent's weight. The visible effect is
    a heavier sub-string inside the already-bold lead — the "double-bold"
    reviewers flag.

    Rule: the first <p> in the body must contain no <strong> or <b> tag.
    The active bold pass applies to body sections only, never the lead.
    """
    first_p = re.search(r"<p[^>]*>(.*?)</p>", body, re.DOTALL | re.I)
    if not first_p:
        return CheckResult(
            id="21", tier="T1",
            name="Lead paragraph: no <strong> or <b> (theme auto-bolds)",
            passed=True,
            detail="no <p> found",
        )
    inner = first_p.group(1)
    if re.search(r"<(?:strong|b)\b", inner, re.I):
        snippet = re.sub(r"<[^>]+>", "", inner).strip()
        return CheckResult(
            id="21", tier="T1",
            name="Lead paragraph: no <strong> or <b> (theme auto-bolds)",
            passed=False,
            detail=f"first paragraph contains <strong> or <b> (theme already bolds it): \"{snippet[:80]}...\"",
        )
    return CheckResult(
        id="21", tier="T1",
        name="Lead paragraph: no <strong> or <b> (theme auto-bolds)",
        passed=True,
    )


def check_paragraph_length(body: str) -> CheckResult:
    """
    editorial-os/13-readability-governance.md: no paragraph exceeds ~4 rendered
    lines. We proxy this by character count: >400 chars in a single <p> element
    is a hard ceiling violation.
    """
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.I | re.S)
    long_count = 0
    for p in paras:
        text = _strip_tags(p).strip()
        if len(text) > 400:
            long_count += 1
    return CheckResult(
        id="20", tier="T2",
        name="No paragraph > 400 chars (\u22484 rendered lines)",
        passed=long_count == 0,
        detail=f"{long_count} over-long paragraph(s)",
        hard_fail=False,  # soft gate — surfaces as warning.
    )


def check_h3_density_per_h2(body: str) -> CheckResult:
    """
    editorial-os/28-htag-semantic-framework.md + runtime-packs/writer-core.md
    (Heading discipline) — soft backstop to the writing-time judgement.

    H3s are earned by semantic coherence, not count. Keep them when they are
    clear, logical subheadings that each genuinely subdivide the parent H2
    (parallel parts of one coherent topic). Demote to bold labels / bullets /
    a table when they are merely a list, or drift onto a subject separate from
    the H2's core.

    3+ H3s under one H2 is only a TRIGGER to apply that test, not a verdict.
    SOFT signal only — it does not block the gate; it flags the sections where
    the judgement (and file 28's Heading Promotion test) should be applied.
    """
    heads = re.findall(r"<(h2|h3)\b[^>]*>(.*?)</\1>", body, re.I | re.S)
    offenders: list[str] = []
    current_h2: str | None = None
    h3_count = 0
    for tag, inner in heads:
        if tag.lower() == "h2":
            if current_h2 is not None and h3_count >= 3:
                offenders.append(f"{h3_count} under “{current_h2[:48]}”")
            current_h2 = re.sub(r"<[^>]+>", "", inner).strip()
            h3_count = 0
        else:
            h3_count += 1
    if current_h2 is not None and h3_count >= 3:
        offenders.append(f"{h3_count} under “{current_h2[:48]}”")

    if offenders:
        return CheckResult(
            id="25", tier="T2",
            name="3+ H3s under one H2 — confirm they are coherent subheadings",
            passed=False,
            detail=f"{len(offenders)} section(s): {'; '.join(offenders[:3])} — keep only if these are clear, logical subheadings of the H2; demote if merely a list or off the H2's core subject (file 28)",
            hard_fail=False,  # soft: surfaces as a warning, never blocks the gate.
        )
    return CheckResult(
        id="25", tier="T2",
        name="No H2 over-structured with 3+ H3s",
        passed=True,
        hard_fail=False,
    )


# ---------------------------------------------------------------------------
# Runner.
# ---------------------------------------------------------------------------

def _page_class_for(path: Path) -> str | None:
    """Resolve a draft's page class from its filename.

    Drafts are named drafts/{wp_id}_{slug}.html, and page-class routing lives
    in scripts/page_runtime_metadata.py SLUG_PAGE_CLASS_OVERRIDES. Returns None
    when the slug is not registered.
    """
    stem = path.stem
    slug = stem.split("_", 1)[1] if "_" in stem and stem.split("_", 1)[0].isdigit() else stem
    try:
        from page_runtime_metadata import SLUG_PAGE_CLASS_OVERRIDES
    except ImportError:
        return None
    return SLUG_PAGE_CLASS_OVERRIDES.get(slug)


# Structure checks that do not apply to hub pages. Hubs are navigational
# taxonomies, not linear articles: their body IS a set of grouped guide lists,
# so 3+ H3s under an H2 is the intended shape rather than an over-structuring
# signal (check 25), and a trailing "Related Guides" block duplicates the
# "Key <topic> Guides" section that defines the page (check 16).
HUB_EXEMPT_CHECK_IDS = {"16", "25"}


def audit_file(path: Path) -> ArticleAudit:
    raw = path.read_text(encoding="utf-8")
    meta = _extract_metadata(raw)
    body = _body_after_metadata(raw)
    body_excl_sources = _strip_sources_section(body)
    prose = _prose_text(body)
    wc = len(prose.split())

    audit = ArticleAudit(
        path=str(path),
        title=meta["title"],
        post_id=meta["post_id"],
        author=meta["author"],
        featured_media=meta["featured_media"],
        template=meta["template"],
        word_count=wc,
    )

    audit.checks = [
        check_em_dashes(body_excl_sources),
        check_first_person_density(prose, wc),
        check_you_density(prose, wc),
        check_we_density(prose, wc),
        check_i_think_opens(prose),
        check_ai_fingerprints(prose),
        check_padded_evaluation(prose),
        check_generic_anchors(raw),
        check_banned_openings(body),
        check_word_count(wc),
        check_featured_image(meta["featured_media"]),
        check_no_body_hero(body),
        check_template(meta["template"]),
        check_author(meta["author"]),
        check_internal_links(body),
        check_faq_accordion(raw, body),
        check_methodology(body),
        check_sources(body),
        check_keyword_h2s(meta["title"], body),
        check_paragraph_length(body),
        check_lead_paragraph_no_strong(body),
        check_block_comment_json_no_raw_html(raw),
        check_no_strong_in_auto_bolded_table_cells(body),
        check_table_cell_brevity(body),
        check_h3_density_per_h2(body),
    ]

    if _page_class_for(path) == "hub":
        audit.checks = [c for c in audit.checks if c.id not in HUB_EXEMPT_CHECK_IDS]

    return audit


def _square(score: int, max_score: int = 21) -> str:
    """Score colour square.

    The brackets scale to whatever the current max is, so adding a check (e.g.,
    /20 -> /21) does not silently change which articles get the green tick:
        \u2705 : full pass (== max_score)
        \uD83D\uDFE8 : within 1 of max (15..max_score-1 historically)
        \uD83D\uDFE7 : 10..14
        \uD83D\uDFE5 : 5..9
        \u2B1B : 0..4
    """
    if score >= max_score:
        return "\u2705"
    if score >= 15:
        return "\U0001F7E8"
    if score >= 10:
        return "\U0001F7E7"
    if score >= 5:
        return "\U0001F7E5"
    return "\u2B1B"


def print_report(a: ArticleAudit) -> None:
    verdict = "PASS" if a.gate_passed else "FAIL"
    print("=" * 80)
    print(f"{a.title or a.path}")
    print(f"  file={a.path}")
    print(f"  post_id={a.post_id} author={a.author} FM={a.featured_media} template={a.template}")
    print(f"  words={a.word_count}  score={_square(a.score, a.max_score)} {a.score}/{a.max_score}  GATE: {verdict}")
    print()
    for c in a.checks:
        mark = "\u2713" if c.passed else "\u2717"
        hf = "" if c.hard_fail else " [soft]"
        print(f"  {mark} [{c.tier}] {c.id}. {c.name}{hf}")
        if not c.passed and c.detail:
            print(f"      \u2514\u2500 {c.detail}")
    print()
    print("  Reminder: Tier 3 editorial checks (info gain per section, authored")
    print("  authority, evaluative bite, concrete scenes) are NOT mechanical and")
    print("  must still be reviewed against editorial-os/16-pre-publish-gate.md")
    print("  §Check 1a, §Check 12a, §Check 13a.")
    print()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts", default="drafts", help="Drafts directory path")
    ap.add_argument("--slug", help="Limit to files whose name contains this substring")
    ap.add_argument("--json", help="Write JSON report to this path")
    ap.add_argument("--quiet", action="store_true", help="Summary only")
    ap.add_argument(
        "--gate-format",
        action="store_true",
        help="Emit 'HARD FAIL: <check> - <detail>' lines per failure for "
             "Bernstein gate consumption (in addition to normal output).",
    )
    args = ap.parse_args()

    drafts_dir = Path(args.drafts)
    if not drafts_dir.is_dir():
        print(f"ERROR: drafts dir not found: {drafts_dir}", file=sys.stderr)
        return 2

    files = sorted(drafts_dir.glob("*.html"))
    if args.slug:
        files = [f for f in files if args.slug in f.name]
    if not files:
        print("No article files matched.", file=sys.stderr)
        return 1

    audits = [audit_file(f) for f in files]

    if not args.quiet:
        for a in audits:
            print_report(a)

    # Gate-format output: emit a HARD FAIL line per failed check so Bernstein's
    # parseHardFails() regex (HARD FAIL: <check> - <detail>) picks them up.
    if args.gate_format:
        for a in audits:
            for check in a.checks:
                if not check.passed:
                    detail = check.detail or "(no detail)"
                    # Only checks that actually block the gate may emit the
                    # HARD FAIL prefix — that string is what Bernstein's
                    # parseHardFails() consumes. Soft checks (hard_fail=False)
                    # are advisory by definition and were previously reported
                    # as blocking, which contradicted gate_passed.
                    label = "HARD FAIL" if check.hard_fail else "SOFT"
                    print(f"{label}: {check.id}. {check.name} - {detail}")

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Article':<55}{'Score':<10}{'Gate':<6}{'Words':<7}")
    for a in audits:
        title = (a.title or Path(a.path).name)[:54]
        sc = f"{_square(a.score, a.max_score)} {a.score}/{a.max_score}"
        gate = "PASS" if a.gate_passed else "FAIL"
        print(f"{title:<55}{sc:<10}{gate:<6}{a.word_count:<7}")

    if args.json:
        Path(args.json).write_text(
            json.dumps([a.to_dict() for a in audits], indent=2, default=str),
            encoding="utf-8",
        )
        print(f"\nJSON written to {args.json}")

    # Exit non-zero if any article fails the gate — useful for CI.
    return 0 if all(a.gate_passed for a in audits) else 1


if __name__ == "__main__":
    sys.exit(main())
