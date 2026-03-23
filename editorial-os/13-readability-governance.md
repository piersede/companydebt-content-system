# Readability Governance

Hard rules for paragraph length, punctuation, emphasis, and web formatting across all Company Debt content.

## 1. Paragraph length

### Rule
Keep paragraphs short. Default to 2 or 3 lines maximum in published article formatting.

### Why this matters
Web readers scan. Dense paragraphs signal "skip this." Short paragraphs signal "this is manageable." Every paragraph over 3 lines is a paragraph the reader is more likely to abandon.

### Specific limits
- Maximum 3 rendered lines at standard article width (680px)
- Maximum approximately 250-300 characters per paragraph as a rough guide
- Use a blank line between every paragraph
- Break dense reasoning into separate short paragraphs
- If a paragraph contains two distinct ideas, split it into two paragraphs

### Detection
If a paragraph contains more than one core idea, or if it exceeds 3 rendered lines, it needs splitting.

### What not to do
Do not split paragraphs in ways that break the logical flow. The split point should feel natural. If splitting makes the text worse, keep the paragraph and tighten the wording instead.

### Intent payoff
Every paragraph must pay off the reader's intent quickly. The first sentence should deliver the point or decision-useful fact; supporting detail follows. If a reader stops reading after the first sentence of any paragraph, they should still have gained something. Do not bury the payoff at the end of a paragraph behind setup, context, or throat-clearing.

Detection: if the first sentence of a paragraph could be removed without losing its core claim, the paragraph is back-loaded and needs restructuring. Lead with the answer, not the question.

## 2. Em dash rules

### Rule
Avoid em dashes unless absolutely necessary. Default to full stops, commas, or a colon.

### Why this matters
Em dashes are an AI writing signature. Overuse makes content feel synthetic. Human web editors use them sparingly. AI uses them as a structural crutch.

### Replacement hierarchy
When you encounter an em dash, replace it with (in order of preference):
1. A full stop and a new sentence
2. A comma
3. A colon
4. Parentheses (for genuinely parenthetical asides)
5. Restructure the sentence to eliminate the need

### Acceptable em dash use
Em dashes are acceptable:
- In citation formats within Sources sections
- In rare cases where no other punctuation creates the right pause and the em dash genuinely improves readability
- Maximum 1 per article. Zero is preferred

### Banned patterns
- Paired em dashes around parenthetical lists ("email, SMS, WhatsApp, and voice")
- Em dash before "and" or "but" joining clauses
- Em dash as a sentence joiner between two independent clauses
- Em dash before an elaboration or qualification
- Em dash as a stylistic crutch to avoid writing two clean sentences

## 3. Emphasis rules

### Rule
Use bolding and italics very sparingly. Do not use them decoratively.

### When bold is acceptable
- **Lead terms in structured lists:** The bold word or phrase at the start of a list item that names the concept, followed by explanatory text. This is the primary editorial use of bold.
- **Table headers**
- **Critical terms on first introduction** (once per term, not repeatedly through the article)
- **Summary verdict lines** where the emphasis is editorially necessary and the sentence cannot carry it alone
- **Decision-critical phrases** in fit/misfit guidance (e.g., "If your bottleneck is **internal visibility**, Karbon addresses it directly")

### When bold is not acceptable
- Scattering bold through body text to simulate emphasis
- Bolding product names, feature names, or category names in running prose
- Using bold as a substitute for strong sentence construction
- Decorative emphasis that adds visual noise without aiding comprehension
- Bolding more than one phrase per paragraph (except in structured lists)
- Re-bolding a term that was already bolded earlier in the article

### When italic is acceptable
- **Editorial asides and caveats** that shift the reading of a sentence (e.g., "This is true *if* the practice has already outgrown spreadsheets")
- **Publication and source titles** (e.g., *Glassdoor UK*)
- **Technical terms on first use** where the term itself is the subject
- **Genuine emphasis** where a human editor would italicise and the sentence reads differently without it

### When italic is not acceptable
- Decorative emphasis
- Softening language ("might", "perhaps")
- Any use that adds typographic clutter without improving comprehension
- Italicising entire sentences or clauses (italic a word or short phrase, not a block)

### Preference order for emphasis
1. Write a stronger sentence (best option)
2. Use a subhead to highlight the point
3. Use a short standalone paragraph
4. Use bold (last resort, sparingly)

### Bold/italic rendering note
Bold renders at font-weight 650 in Company Debt blog articles, slightly heavier than semi-bold. Italics use the standard italic variant. Both inherit the surrounding text colour (primary for headings and body, tertiary for sources). Do not rely on emphasis to carry meaning that the sentence cannot carry without it.

## 4. Human formatting rule

### Rule
Format like a good human web editor. Not like AI trying to look polished.

### What this means in practice
- Strong headings that tell the reader what they will learn
- Short paragraphs (2-3 lines)
- Restrained emphasis (minimal bold, minimal italic)
- Minimal typographic fuss
- Clear sections with visual breathing room
- Lists only when they genuinely improve comprehension (not as default structure)
- No decorative formatting

### AI formatting signatures to avoid
- Excessive use of bold within body text
- Em dashes as structural punctuation
- Long paragraphs that look like essay writing
- Stacking multiple ideas into one dense paragraph
- Formatting that feels "typographically busy"
- Lists used as a crutch to avoid writing proper paragraphs
- Headers that label topics rather than communicate content

## 5. List usage rules

### When to use lists
- When presenting genuinely parallel items (features, criteria, steps)
- When the items are more scannable as a list than as prose
- When the reader needs to compare or check off items

### When not to use lists
- When the items are part of an argument that needs narrative flow
- When using a list to avoid writing proper explanatory paragraphs
- When the list is just a reformatted paragraph
- When the items are not genuinely parallel

### List formatting
- Use bullet lists for unordered items
- Use numbered lists only for sequential steps or ranked items
- Keep list items short (one line where possible)
- Do not nest lists more than one level deep in article content

## 6. Section breathing room

### Rule
Each section should visually breathe. Avoid walls of text.

### What this means
- A section that is entirely dense paragraphs needs breaking up
- A section should have a mix of paragraph lengths (but none over 3 lines)
- Use subheads to pace the article
- A reader scrolling through should see clear visual breaks every few paragraphs

### What to avoid
- Sections that are one continuous block of text
- Back-to-back long paragraphs
- Sections without any structural relief (a subhead, a list, a short standalone sentence)

## 7. External link rules

### Rule
External links to credible sources strengthen evidence and trust. Use them where they genuinely support a claim or help the reader verify information. Every external link opens in a new tab (`target="_blank"`) and displays a subtle arrow indicator (↗) so the reader knows they are leaving the site.

### When to use external links
- **Source citations:** Link directly to the data source when citing salary figures, policy changes, adoption statistics, or other verifiable claims
- **Product documentation:** Link to a competitor's pricing page, feature page, or documentation when making claims about their capabilities
- **Regulatory references:** Link to GOV.UK or HMRC guidance when referencing tax deadlines, NIC changes, or compliance requirements
- **Industry reports:** Link to reports, surveys, or benchmarks that support editorial claims

### When not to use external links
- Do not link for the sake of linking. Every external link should help the reader verify or explore a specific claim.
- Do not link to competitor homepages generically. Link to the specific page that supports your claim (pricing page, feature comparison, documentation).
- Do not link to paywalled content without noting it.
- Do not add more than 3-5 external links per 1,000 words of body content (same density cap as internal links).

### Link text quality
- Anchor text should describe what the reader will find, not generic text like "click here" or "source"
- **Good:** "Glassdoor UK salary data for accounts administrators"
- **Bad:** "source" or "click here"
- For inline source citations in the Sources section, the domain name or publication title is acceptable anchor text

### Markup
External links must use `target="_blank"` for new-tab behaviour. The CSS handles the visual indicator automatically. In WordPress block markup:
```html
<a href="https://example.com/page" target="_blank" rel="noopener">anchor text</a>
```

## 8. Contractions

### Rule
Use natural contractions. Company Debt content should sound like a knowledgeable person writing, not a formal document.

### Required contractions
Use these instead of the expanded form:
- isn't (not "is not")
- doesn't (not "does not")
- don't (not "do not")
- won't (not "will not")
- can't (not "cannot")
- shouldn't (not "should not")
- wouldn't (not "would not")
- couldn't (not "could not")
- wasn't (not "was not")
- weren't (not "were not")
- hasn't (not "has not")
- haven't (not "have not")
- hadn't (not "had not")
- it's (not "it is" — when used as contraction, not possessive)
- that's (not "that is")
- there's (not "there is")
- you'll (not "you will")
- you're (not "you are")
- we've (not "we have")
- we're (not "we are")
- they're (not "they are")

### Exception
Do not contract in:
- legal or compliance disclaimers
- formal attribution ("This is a desk-based review")
- emphasis through deliberate formality ("This tool is not weak" — intentional weight)

### Detection
Any "is not", "does not", "do not", "will not", "cannot" in body prose is a readability flag unless it falls under an exception above.

## 9. Heading capitalisation

### Rule
All H1, H2, and H3 headings use title case. Capitalise every word above three characters. Keep short function words lowercase unless they begin the heading.

### Words to keep lowercase (unless first word)
a, an, the, and, or, but, for, in, on, of, to, is, it, vs, not, via, nor, so, yet, at, by, up

### Examples
- **Good:** "Five Things to Check Before Choosing Document Collection Software"
- **Good:** "Liscio: Client Messaging, Not Automated Document Collection"
- **Bad:** "Five things to check before choosing document collection software"

### Table column headers
Table column header text also follows title case. Additionally, all table column headers must be left-aligned (text-align: left).

### Detection
Any H2 or H3 where the second word or later is lowercase and longer than 3 characters is a formatting flag.

## 10. Readability governance checklist

Before finalising any article:

- [ ] No paragraph exceeds 3 rendered lines
- [ ] Every paragraph pays off intent in its first sentence (no back-loaded paragraphs)
- [ ] Blank line between every paragraph
- [ ] Maximum 1 em dash in the entire article (zero preferred)
- [ ] Bold used for lead terms in lists and decision-critical phrases only (not scattered through prose)
- [ ] No decorative italic
- [ ] No bold phrase repeated (each term bolded once, on first introduction)
- [ ] External links use `target="_blank"` and descriptive anchor text
- [ ] External link density does not exceed 3-5 per 1,000 words
- [ ] Lists used only where they genuinely improve comprehension
- [ ] Every section has visual breathing room
- [ ] Subheads are specific and informative, not generic labels
- [ ] The article looks like it was formatted by a human web editor
- [ ] No AI formatting signatures present
- [ ] All headings (H1, H2, H3) use title case
- [ ] All table column headers are left-aligned and use title case
- [ ] Natural contractions used throughout (no "is not", "does not" etc. in body prose)
