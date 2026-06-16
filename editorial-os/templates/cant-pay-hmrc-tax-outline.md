# Can't Pay HMRC Tax Outline

<!-- H-tag authority: editorial-os/28-htag-semantic-framework.md → Template 13: Specific problem or "Can I" query (HMRC tax-debt variant). If these headings conflict with file 28, file 28 wins. -->

Master H-tag template for "Can't Pay {{TAX}}" pages in the HMRC tax-debt family
(VAT, PAYE, Corporation Tax). Refines `trigger-page-outline.md` for the
specific case where the creditor is HMRC and Time to Pay is the primary lever.

Page class: `trigger`. Verified against the live SERP for "Can't Pay VAT"
(first applied to /hmrc/cant-pay-vat/, post 9443, gate 24/24, June 2026).

Before drafting, define:
- `{{TAX}}` — the tax in arrears (VAT, PAYE, Corporation Tax)
- `{{HELPLINE}}` — the relevant HMRC payment-support number

## Structural rules (non-negotiable)

- Keep every H-tag tight to the core query: `cant pay {{TAX}}`, `unpaid {{TAX}}`,
  `HMRC {{TAX}} debt`, `{{TAX}} time to pay`, `{{TAX}} enforcement`, `{{TAX}} penalties`.
- Time to Pay gets its own H2 BEFORE the enforcement timeline. It is the primary
  user need.
- ONE merged enforcement H2. Do not split "after you miss a payment" and "if the
  debt is not resolved" into two H2s — statutory demands and winding-up must not
  appear as headings twice.
- Adjacent topics (insolvency tests, director duties, wrongful trading, personal
  liability, formal procedures) are BOLD BODY LABELS, never H3s. They have their
  own pages; heading them here cannibalises those pages. Link out instead.
- No em dashes anywhere in the prose.

## Heading blueprint

# H1
Can't Pay {{TAX}}? What Happens and What Directors Should Do

## H2
Quick Answer: What Happens if You Cannot Pay {{TAX}}

## H2
What to Do First If You Cannot Pay {{TAX}}

### H3
File Your {{TAX}} Return on Time

### H3
Contact HMRC Before Enforcement Starts

### H3
Work Out What You Can Afford to Pay

## H2
Can You Get a {{TAX}} Time to Pay Arrangement?
<!-- BODY: do NOT use H3s here — this is facets of one topic, not separate sections.
     Use bold body labels plus one short bullet list:
       - intro: what Time to Pay is
       - **How to apply.** (number + what to say)
       - "Before agreeing, HMRC weigh three things:" + 3-item bullet list
         (business viable / schedule sustainable / compliant on other taxes)
       - **Typical terms.** (6-12 months, interest rate, keep paying current {{TAX}})
       - **Timing matters more than anything.** (call before enforcement)
       - **If HMRC refuses.** (decline/terminate, enforcement resumes, reframes as solvency) -->


## H2
What Happens After You Miss a {{TAX}} Payment?

### H3
HMRC Enforcement Timeline

### H3
Late Payment Interest and Penalties

### H3
Statutory Demands and Winding-Up Petitions

## H2
Can Unpaid {{TAX}} Lead to Insolvency?
<!-- BODY: bold labels, not H3s — cash flow insolvency / HMRC preferential status /
     director duties / wrongful trading risk / when to speak to an insolvency practitioner -->

## H2
What Directors Should Avoid If {{TAX}} Is Unpaid
<!-- BODY: bold labels — do not ignore HMRC / do not miss current returns /
     do not make unrealistic offers / do not keep building debt without a plan /
     do not ignore a statutory demand -->

## H2
Options If You Still Cannot Pay the {{TAX}} Debt

### H3
Extend or Renegotiate Time to Pay

### H3
Business Funding for {{TAX}}

### H3
Insolvency Advice if the Company Cannot Recover

## H2
Frequently Asked Questions

## H2
Methodology and Disclosure

## H2
Sources and References
