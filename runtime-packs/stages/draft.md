# Stage Pack: Draft

Goal:

- produce a full first draft that is clear, authored, evidence-disciplined, and decision-useful

Rules:

- write the full argument before auditing
- keep director impact and personal consequences visible throughout
- turn facts into consequences
- avoid filler, generic transitions, and anonymous summary tone
- if support is weak, narrow the claim rather than padding around it
- keep human-authorship markers explicit: concrete scenes, lived operational friction, evaluative bite
- avoid taxonomy-engine prose -- if the page reads like a neutral category overview, rewrite it
- make sure at least a few lines sound distinctly authored rather than safely competent

## Gate-aware constraints (so the draft starts clean)

Bake these in as you write. They are the same constraints the humanise pass and
`article_audit.py` enforce; getting them right in the draft means less to undo
later.

- **No em dashes anywhere in prose** (hard AI signal). Commas, colons, full
  stops. Hyphenated compounds are fine.
- **Openings (P1-P3) avoid banned patterns**: no "This page is for/about", "In
  today's", "When it comes to", "Whether you are", rhetorical throat-clearing,
  or a delayed/generic first line. Open on a concrete claim or observation.
- **`you` density high (>= 8/1k); `we/our/us` natural (~3-4/1k), not padded**
  (the 5/1k audit floor is a known over-shoot for the company-authored voice --
  a 3-4/1k page is correct). First-person `I/me/my` under 5/1k, and never open a
  sentence with "I think".
- **Write self-standing sentences** so no `<p>` runs over ~400 chars / ~4
  rendered lines; a paragraph that has to be split later should split cleanly at
  a sentence boundary, not mid-clause.
- **Lead paragraph carries no `<strong>`/`<b>`** (the theme auto-bolds it).
- No AI fingerprints, no padded evaluation phrases ("plays a crucial role",
  "when it comes to"), no generic anchor text ("click here", "read more").

## Structure and end-matter the gate checks

- **Header comment, canonical format** (the audit regex needs every field or it
  parses nothing): `<!-- POST ID: <id> / TYPE: pages|posts / AUTHOR: 34 / FM:
  <featured_media_id> / TEMPLATE: <template.php> -->`. Templates accepted:
  take-the-test-template.php (guide pages) or post-sectors.php (sector posts).
- **FAQ as the `ub/content-toggle` accordion**, and the **FAQ H2 must begin with
  "Frequently Asked Questions" or "FAQ"** (the audit anchors on that). accordion
  `panelTitle` uses `<` built via chr(92); never raw `<strong>` (renders as
  literal junk), never double-backslash. Block-comment JSON attrs use `<`
  escapes generally.
- **Related Guides is the FINAL H2**, immediately after FAQ, and its heading text
  contains the exact phrase "Related Guides". Nothing else may be an H2 after it.
- **Methodology & Disclosure and Sources & References** sit in `<aside>` blocks
  OUTSIDE the H2 hierarchy (styled labels, not h2). Both are required end-matter,
  along with the review/verification date. Name the reviewing IP only once a
  genuine sign-off exists (human-expert authorship gate).
- **Keyword-rich H2s**: at least ~30% of H2s contain a title keyword.
- No hero/featured image inside the body; keep table cells concise and free of
  `<strong>` in `<th>` or the first-column `<td>` (the theme auto-bolds those).

## Definition of done (before handing to review)

- Full argument written, authored voice present, claims evidence-disciplined.
- `article_audit.py` would fail on at most the two documented exceptions
  (we/our density floor, soft 3+ H3 advisory). Any structural or opening-pattern
  fail should not survive the draft.
