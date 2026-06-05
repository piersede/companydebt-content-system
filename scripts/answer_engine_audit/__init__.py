"""Answer-Engine Coverage Audit System (UK company-insolvency / debt domain).

Captures what major answer engines (OpenAI, Gemini) surface for a query,
normalises the outputs into a verifiable ledger, verifies each hard claim
against authoritative UK sources (GOV.UK / The Insolvency Service /
legislation.gov.uk / Companies House), and diffs that ledger against an existing
page so editors can see what is missing, weak, outdated or buried.

This is editorial QA, not competitor scraping. AI outputs are a DISCOVERY layer
only; authoritative/official pages are the verification layer. Raw witnesses are
preserved immutably per run so provenance is never lost.

Scope: OpenAI + Gemini (Gemini-only where no OpenAI key is set), single live page.
"""

__version__ = "0.1.0"
