"""Shared prompt helpers for Company Debt research workflows."""

from __future__ import annotations

from datetime import datetime


BASE_RESEARCH_STANDARDS = [
    "Use current, authoritative UK sources unless the request explicitly requires otherwise.",
    "Cite the exact source URL and access date for every factual claim.",
    "If a figure cannot be verified from a credible source, flag it explicitly rather than estimating.",
    "Avoid generic category padding. Focus on the requested facts, comparisons, and unresolved gaps.",
]


def build_research_standards(extra_rules: list[str] | None = None) -> str:
    rules = list(BASE_RESEARCH_STANDARDS)
    if extra_rules:
        rules.extend(extra_rules)
    return "\n".join(f"- {rule}" for rule in rules)


def build_article_batch_prompt(articles: list[dict], *, intro: str, extra_rules: list[str] | None = None) -> str:
    today = datetime.now().strftime("%d %B %Y")
    lines = [intro.strip(), "", f"Today's date is {today}.", "", "RESEARCH STANDARDS:", build_research_standards(extra_rules), "", "ARTICLES:"]

    for article in articles:
        lines.append(f"ARTICLE: {article['slug']}")
        lines.append(f"TITLE: {article['title']}")
        lines.append("FACTS NEEDED:")
        for question in article["research_questions"]:
            lines.append(f"- {question}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def build_bundle_prompt(title: str, body: str, *, extra_rules: list[str] | None = None) -> str:
    today = datetime.now().strftime("%d %B %Y")
    lines = [
        f"Research the following topic bundle for Company Debt: {title}.",
        f"Today's date is {today}.",
        "Answer the requested sections directly and preserve the section headings.",
        "",
        "RESEARCH STANDARDS:",
        build_research_standards(extra_rules),
        "",
        body.strip(),
        "",
    ]
    return "\n".join(lines)
