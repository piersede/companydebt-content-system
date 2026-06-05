"""Recommended display-format taxonomy for audit nuggets (UK insolvency / company-debt domain).

Every verified nugget the audit surfaces should carry a
``recommended_display_format`` so the recommendation step proposes the SMALLEST
useful edit (a definition, an ordered step list, a risk callout, a table cell, an
FAQ) rather than a prose dump or a rewrite. This drives
``reports/06-recommended-edits.md``.

The taxonomy is page-builder-aware, but for the company-insolvency / debt-advice
domain rather than commercial product comparison. There are no "providers" or
product cards here: the facts are statutory, procedural, cost, timeline,
liability and consequence claims aimed at a UK company director deciding what to
do. So the formats favour definitions, ordered process steps, risk callouts,
route-comparison tables, key-takeaways and FAQs, with every hard fact carrying a
primary source (GOV.UK / The Insolvency Service / legislation.gov.uk).
"""

from __future__ import annotations

# Canonical formats. Order is roughly "highest extractability / smallest edit"
# first. Keep in sync with the recommendation prompt (prompts.RECOMMEND_EDITS).
DISPLAY_FORMATS: list[str] = [
    "top_summary_block",            # concise direct answer near the top
    "definition_block",            # define a term/route (callout: note/info)
    "process_steps",               # ordered "how it works" steps, not prose
    "comparison_table_cell",       # a value into an existing route/cost table cell
    "comparison_table_column",     # a NEW column in a route-comparison table
    "comparison_table_footnote",   # qualifier/condition under a table
    "warning_callout",             # director risk / liability / pitfall (callout: warning)
    "key_takeaways",               # consequence / "what this means" summary box
    "faq",                         # answers a real follow-up query, self-contained
    "source_note",                 # visible primary source + last-checked line
    "methodology_note",            # how-we-checked / evidence basis
    "verification_needed_report",  # unresolved/contradicted -> queue, NOT page copy
]

# Default format by nugget category. The recommender may override per nugget, but
# these are sane starting points. The category keys are the closed vocabulary the
# extractor must choose from (extract.ALLOWED_CATEGORIES derives from this dict).
DEFAULT_FORMAT_BY_CATEGORY: dict[str, str] = {
    "Definition / Terminology": "definition_block",
    "Process / Steps": "process_steps",
    "Eligibility / Criteria": "comparison_table_column",
    "Cost / Fees": "comparison_table_cell",
    "Timeline / Duration": "comparison_table_cell",
    "Director Liability / Personal Risk": "warning_callout",
    "Consequences / Aftermath": "key_takeaways",
    "Route Comparison": "comparison_table_column",
    "Alternatives / Options": "comparison_table_column",
    "Creditor / HMRC Treatment": "definition_block",
    "Legal / Regulatory": "source_note",
    "Risks / Pitfalls": "warning_callout",
    "Statistics / Data": "comparison_table_cell",
    "FAQs / User Questions": "faq",
}


def default_format(category: str) -> str:
    """Best-guess display format for a nugget category."""
    return DEFAULT_FORMAT_BY_CATEGORY.get(category, "definition_block")


# Aliases: accept legacy / doc tokens and normalise to a canonical format so
# stray values from older prompts or pasted material still resolve. The
# credit-card provider-card tokens have no home in this domain; map them to the
# nearest insolvency-appropriate shape rather than dropping silently.
FORMAT_ALIASES: dict[str, str] = {
    "terms_table_column": "comparison_table_column",
    "terms_table_cell": "comparison_table_cell",
    "provider_card_field": "key_takeaways",
    "provider_card_caveat": "warning_callout",
    "provider_card_verdict_lead": "top_summary_block",
    "also_considered_section": "comparison_table_column",
    "eligibility_section": "comparison_table_column",
    "pros_cons_note": "key_takeaways",
}


def normalise_format(fmt: str) -> str:
    """Map a legacy/alias token to a canonical DISPLAY_FORMATS value. Unknown
    tokens are returned unchanged so the caller can validate and fall back."""
    f = (fmt or "").strip()
    return FORMAT_ALIASES.get(f, f)


def split_formats(value: str) -> list[str]:
    """Parse a compound display-format string ("a + b", "a, b", "a | b") into a
    list of canonical formats. A fact can legitimately have two homes (e.g. a
    route-comparison column AND a warning callout). Unknown tokens are dropped."""
    import re as _re

    valid = set(DISPLAY_FORMATS)
    out: list[str] = []
    for part in _re.split(r"[+,|/]", value or ""):
        canon = normalise_format(part)
        if canon in valid and canon not in out:
            out.append(canon)
    return out
