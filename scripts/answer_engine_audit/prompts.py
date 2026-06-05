"""en-GB prompt pack for answer-engine capture (UK company-insolvency / debt domain).

These are written for machine use. The goal at capture time is to elicit the
salient, decision-useful specifics each engine surfaces for the query — the
insolvency routes, statutory rules, costs, timelines, director liability and
consequences a UK company director needs. They are deliberately NOT asking the
engine to be "right"; that is the verification layer's job (which checks claims
against GOV.UK / The Insolvency Service / legislation). Capture is discovery.
"""

from __future__ import annotations


BROAD_ANSWER = """\
You are helping with an editorial coverage audit for an existing UK guide about
company insolvency, company debt, or director responsibilities.

Target keyword: {keyword}
Market: United Kingdom (company / corporate insolvency unless the query is clearly personal)
Language: en-GB

Task:
Give a current, accurate answer to the query as if you were helping a UK company
director understand their situation and options.

Requirements:
- Focus on salient, decision-useful specifics, not generic reassurance.
- Where relevant, name the specific insolvency route or procedure (e.g. Creditors' \
Voluntary Liquidation, Compulsory Liquidation / winding-up petition, Company Voluntary \
Arrangement, Administration, dissolution / strike-off) and what distinguishes it.
- Include what a director actually needs: what the process involves and its order, \
who can start it, eligibility/criteria, typical cost and who pays, realistic timelines, \
the director's personal exposure (personal guarantees, overdrawn director's loan account, \
wrongful or fraudulent trading, misfeasance, disqualification), how creditors and HMRC are \
treated, and the consequences afterwards.
- Anchor statutory points to the governing law where you can (e.g. Insolvency Act 1986, \
Companies Act 2006, Insolvency Rules 2016) and to official bodies (The Insolvency Service, \
Companies House, the courts).
- Be precise; preserve qualifiers such as "usually", "from", "in most cases", "subject to", \
and say when a figure or rule depends on circumstances.
"""


USE_CASE = """\
Target keyword: {keyword}
Language: en-GB

Task:
Answer this specific question with current, decision-useful detail for a UK company
director. Name the relevant insolvency route(s), the governing rule or official source
where one applies, and any figures, thresholds or timelines that justify the answer.
Preserve qualifiers.

Question: {question}
"""


RISK_DRAWBACK = """\
Target keyword: {keyword}
Language: en-GB

Task:
List the main risks, pitfalls and things a UK company director most often gets wrong
or regrets when dealing with this situation.

Focus on failure modes with real consequences: continuing to trade while insolvent
(wrongful trading) and personal liability for the resulting debts, preferring some
creditors over others, an overdrawn director's loan account being called in, personal
guarantees crystallising, misuse of dissolution / strike-off to avoid creditors,
phoenix-company restrictions on reusing a company name (s.216 Insolvency Act 1986),
director disqualification, and HMRC's preferential status and personal liability notices.
State the rule or source behind each where you can.
"""


RECOMMEND_EDITS = """\
You are turning a verified nugget ledger into precise editorial actions for an
existing UK company-insolvency / company-debt guide. Do NOT rewrite the article.
For each verified nugget, recommend the SMALLEST useful edit and tag it with a
recommended_display_format from this list:

top_summary_block, definition_block, process_steps, comparison_table_cell,
comparison_table_column, comparison_table_footnote, warning_callout,
key_takeaways, faq, source_note, methodology_note, verification_needed_report

Rendering rules you MUST respect:
- A statutory, cost, timeline or liability fact must carry its primary source
  (GOV.UK / The Insolvency Service / legislation.gov.uk / Companies House). If the
  page does not already cite one, pair the edit with source_note.
- A fact that defines or disambiguates a term or route -> definition_block.
- A "how it works" sequence -> process_steps (ordered), not a prose paragraph.
- A fact that affects a director's personal risk -> warning_callout.
- A fact that distinguishes routes (cost, timeline, control, who can start it,
  effect on directors) -> comparison_table_cell / comparison_table_column.
- A consequence / "what this means afterwards" fact -> key_takeaways.
- A fact that answers a follow-up query -> faq.
- Anything contradicted or unverifiable -> verification_needed_report, never page copy.

For each nugget return:
- detail (one self-contained line: entity/route + claim + qualifier)
- category
- article_status (present|present_but_weak|missing|outdated|unsupported|buried|contradicted)
- recommended_display_format (from the list above)
- recommended_action (the exact smallest edit, in en-GB plain-English voice)
- needs_primary_verification (true/false)
- priority (low|medium|high|critical)

Keep every recommendation tied to a specific section. Do not parrot another
site's phrasing; preserve our information gain. Be accurate before being
comprehensive: this is YMYL content where a wrong statutory or liability claim is
actively harmful, so prefer to under-claim and flag for verification.
"""


def default_use_cases(keyword: str) -> list[str]:
    """Generic insolvency / debt-advice probes. A page config may override these
    via its own ``priority_questions``."""
    return [
        f"What are the steps involved in {keyword}, and how long does it take?",
        f"How much does {keyword} cost, and who pays for it?",
        f"What are the consequences for company directors of {keyword}, including any "
        f"personal liability?",
        f"When is {keyword} the right option, and what are the alternatives?",
    ]
