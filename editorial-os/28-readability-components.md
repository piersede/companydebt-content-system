# 28. Readability Components

Scanning aids and structural patterns that support comprehension on long-form service and advice pages. Sits between file 13 (prose typography) and file 26 (decision-critical callout boxes).

---

## 28.1 Purpose

Components exist to break visual density and help users locate what matters. They do not replace copy depth; they frame it.

Two tiers:

- **Editorial callouts** (§28.3) — opinionated, evidence-gated, decision-shifting. Governed jointly with file 26. Use sparingly.
- **Structural components** (§28.4) — formatting aids (orientation, process flows, navigation). No evidence gate; placement discipline only.

---

## 28.2 Rhythm rules

These rules apply to every page regardless of page class.

1. **Max 3–4 components per page** (editorial callouts + structural combined).
2. **Never two identical component types directly adjacent.** Always return to paragraph copy or a new heading before repeating the same component type.
3. **No component within the first two paragraphs.** Let the reader land before introducing structure.
4. **No component immediately before Methodology or Sources sections.**
5. **After any visual block, return to prose before the next block.** One clear prose section between any two components.
6. **Do not use a component where prose already does the job.** If the section heading and two paragraphs already communicate the point clearly, adding a callout is decoration, not support.

---

## 28.3 Editorial callouts (8 types)

Each type requires an evidence level (see file 26 §26.3) and has specific placement rules (file 26 §26.6).

For full schema (box_type, claim, judgement_shift, evidence_refs, expiry_rule, canonical_links) see **file 26**.

### CompanyDEBT View
- **Class**: `.cd-callout .cd-callout--companydbt-view`
- **Purpose**: Process framing and disciplined multi-route decision guidance
- **Evidence**: B or C
- **Best on**: Entity-owner pages, service pages
- **Not on**: Trigger pages where urgency is the primary frame

### What Most Directors Miss
- **Class**: `.cd-callout .cd-callout--directors-miss`
- **Purpose**: Blind-spot correction
- **Evidence**: A or B
- **Best on**: Director-risk, trigger, procedure pages
- **Not on**: Pages where the "miss" is already obvious from the heading structure

### Risk Warning
- **Class**: `.cd-callout .cd-callout--risk-warning`
- **Purpose**: Imminent danger or statutory deadline
- **Evidence**: A only
- **Best on**: Top-third of enforcement, procedure, director-risk pages
- **Not on**: Pages where the risk is already the primary subject of the heading structure

### Cost Reality
- **Class**: `.cd-callout .cd-callout--cost-reality`
- **Purpose**: Realistic cost drivers and ranges with stated assumptions
- **Evidence**: A or B with assumptions explicit
- **Best on**: Procedure pages, cost modifier pages
- **Not on**: Pages with a full cost table already present

### Legal Exposure
- **Class**: `.cd-callout .cd-callout--legal-exposure`
- **Purpose**: Director liability, disqualification, wrongful trading, preferences
- **Evidence**: A only (statute or case law)
- **Best on**: Director-risk, enforcement, procedure pages
- **QA gate**: Must be reviewed by a licensed IP before publication (file 26 §26.8)

### Recovery Path
- **Class**: `.cd-callout .cd-callout--recovery-path`
- **Purpose**: Structured route through a process with decision forks
- **Evidence**: B or C
- **Best on**: Entity-owner, trigger, hub pages
- **Not on**: Where a process steps module already covers the same ground

### Creditor Perspective
- **Class**: `.cd-callout .cd-callout--creditor-perspective`
- **Purpose**: Creditor incentives and leverage from the creditor's viewpoint
- **Evidence**: A for rights, B or C for behavioural claims
- **Best on**: Enforcement, creditor-facing, procedure pages

### Timeline Reality
- **Class**: `.cd-callout .cd-callout--timeline-reality`
- **Purpose**: Deadlines with consequence
- **Evidence**: A only
- **Best on**: Enforcement, procedure, trigger pages

### HTML template (all callout types)

```html
<!-- wp:group {"className":"cd-callout cd-callout--[type]"} -->
<div class="wp-block-group cd-callout cd-callout--[type]">
  <p class="cd-callout__label">[Label text from table above]</p>
  <p class="cd-callout__title">[Title — specific, not generic]</p>
  <!-- wp:paragraph -->
  <p>[Body — 2–4 sentences. Must shift the reader's judgement. Must not repeat adjacent prose.]</p>
  <!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
```

---

## 28.4 Structural components (10 types)

No evidence gate. Placement discipline applies.

### Key Takeaway
- **Class**: `.cd-key-takeaway`
- **Purpose**: 1–3 sentence summary after a complex section
- **Use after**: Dense legal/process sections, multi-option explanations
- **Not after**: Simple sections, nor immediately before or after another callout
- **Max per page**: 2
- **HTML**:
```html
<!-- wp:group {"className":"cd-key-takeaway"} -->
<div class="wp-block-group cd-key-takeaway">
  <p class="cd-key-takeaway__label">Key Takeaway</p>
  <!-- wp:paragraph -->
  <p>[1–3 sentences. Summary only. No new claims.]</p>
  <!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
```

### Process Steps
- **Class**: `.cd-process-steps` + `cd-process-steps__item`, `__number`, `__content`, `__title`, `__body`
- **Purpose**: Numbered sequence for "what happens next" or service process sections
- **Use**: 3–6 steps. Where a process needs to feel clear and reassuring.
- **Not**: Where process is already covered by H3 subheadings in the same section. Not adjacent to another step module.
- **Max per page**: 1 (2 only on very long pages where processes are clearly distinct)
- **HTML**:
```html
<!-- wp:html -->
<ol class="cd-process-steps">
  <li class="cd-process-steps__item">
    <span class="cd-process-steps__number">1</span>
    <div class="cd-process-steps__content">
      <p class="cd-process-steps__title">[Step title]</p>
      <p class="cd-process-steps__body">[1–2 sentences]</p>
    </div>
  </li>
</ol>
<!-- /wp:html -->
```

### Inline CTA
- **Class**: `.cd-inline-cta` + `__headline`, `__body`, `__button`
- **Purpose**: High-intent call to action placed within main content
- **Use after**: High-intent sections (director risk, rescue options, immediate action)
- **Not**: Within two components of another CTA. Not at the very top or bottom of the page.
- **Max per page**: 1
- **HTML**:
```html
<!-- wp:group {"className":"cd-inline-cta"} -->
<div class="wp-block-group cd-inline-cta">
  <p class="cd-inline-cta__headline">[Short, specific headline]</p>
  <p class="cd-inline-cta__body">[1–2 sentences. Helpful, not salesy.]</p>
  <a href="/contact/" class="cd-inline-cta__button">Speak to an adviser</a>
</div>
<!-- /wp:group -->
```

### Do / Don't Panel
- **Class**: `.cd-do-dont` + `__do`, `__dont`, `__label`
- **Purpose**: Practical advice and director behaviour comparison
- **Use**: 3–5 rows each side. Practical risk reduction.
- **Not**: Adjacent to a table or another comparison component. Not more than once per page.
- **HTML**:
```html
<!-- wp:html -->
<div class="cd-do-dont">
  <div class="cd-do-dont__do">
    <p class="cd-do-dont__label">Do</p>
    <ul>
      <li>[Action]</li>
    </ul>
  </div>
  <div class="cd-do-dont__dont">
    <p class="cd-do-dont__label">Don't</p>
    <ul>
      <li>[Action to avoid]</li>
    </ul>
  </div>
</div>
<!-- /wp:html -->
```

### Card Grid
- **Class**: `.cd-card-grid` + `__card`, `__icon`, `__title`, `__body`
- **Purpose**: Grouped themes — causes, risks, pressure points, stakeholder concerns
- **Use**: 4–6 cards. Two or three columns on desktop, stacks on mobile.
- **Not**: Adjacent to another card grid. Not more than 6 cards (use subheadings instead).
- **HTML**:
```html
<!-- wp:html -->
<div class="cd-card-grid">
  <div class="cd-card-grid__card">
    <span class="cd-card-grid__icon">&#9670;</span>
    <p class="cd-card-grid__title">[Card title]</p>
    <p class="cd-card-grid__body">[1–2 sentences]</p>
  </div>
</div>
<!-- /wp:html -->
```

### Orientation Block
- **Class**: `.cd-orientation-block` + `__label`
- **Purpose**: "Who this is for" and/or "When to act" — confirms relevance near page top
- **Use**: Once, near the top of pages where the audience needs quick confirmation
- **Not**: If the page already has a strong opening summary that does this job. Not both "who this is for" and "when to act" on short pages — pick one.
- **HTML**:
```html
<!-- wp:group {"className":"cd-orientation-block"} -->
<div class="wp-block-group cd-orientation-block">
  <p class="cd-orientation-block__label">Who This Page Is For</p>
  <!-- wp:list -->
  <ul>
    <li>[Audience item]</li>
  </ul>
  <!-- /wp:list -->
  <p><strong>Not for:</strong> [exclusion if useful]</p>
</div>
<!-- /wp:group -->
```

### On This Page (anchor nav)
- **Class**: `.cd-on-this-page` [+ `--sticky` modifier for desktop sticky]
- **Purpose**: Jump menu for long-form pages
- **Use**: Long pages only (5+ major sections). Desktop sticky if it does not interfere with the existing sidebar.
- **Not**: On short pages. Do not include every heading — only main decision points (5–7 anchors max).
- **HTML**:
```html
<!-- wp:html -->
<div class="cd-on-this-page">
  <p class="cd-on-this-page__label">On This Page</p>
  <nav>
    <ul>
      <li><a href="#section-id">[Anchor label]</a></li>
    </ul>
  </nav>
</div>
<!-- /wp:html -->
```

### Question Section
- **Class**: `.cd-question-section`
- **Purpose**: Heading treatment for question-led sub-sections within dense explanatory passages
- **Use**: Apply as an additional class on an existing `<h3>` element. 2–4 questions per section.
- **Not**: Do not convert an entire page to question format. Not on H2 headings.
- **HTML**: Apply as an additional class: `<h3 class="wp-block-heading cd-question-section">Can a care home…?</h3>`

### Decision List
- **Class**: `.cd-decision-list`
- **Purpose**: Styled bullet list for warning signs, first steps, director duties, documents needed
- **Use**: 5–7 items. Where the user needs to identify, compare, or act.
- **Not**: Multiple decision lists back to back without intervening paragraph copy. Not for narrative lists.
- **HTML**:
```html
<!-- wp:html -->
<ul class="cd-decision-list">
  <li>[Item]</li>
</ul>
<!-- /wp:html -->
```

### FAQ Accordion wrapper
- **Class**: `.cd-faq-accordion`
- **Purpose**: Outer wrapper for the existing `ub/content-toggle-block` FAQ sections
- **Use**: Wrap the outer `<!-- wp:ub/content-toggle-block -->` comment group with a `wp:group` carrying this class.
- **Not**: Do not use immediately after another highly interactive component.

---

## 28.5 Page-type component stacks

Choose 2–3 from the recommended stack for the page class. Never all.

| Page class | Primary components | Secondary |
|---|---|---|
| `distress_use_case` | Orientation Block, Risk Warning, Recovery Path | Process Steps, Inline CTA |
| `entity_owner` | CompanyDEBT View, Recovery Path, Process Steps | Key Takeaway, On-This-Page |
| `director_risk` | Legal Exposure, What Most Directors Miss, Do/Don't | Risk Warning, Timeline Reality |
| `enforcement` | Risk Warning, Timeline Reality, Process Steps | Creditor Perspective |
| `trigger` | Recovery Path, Cost Reality, Process Steps | Orientation Block |
| `process_guide` | Process Steps, On-This-Page, Key Takeaway | Risk Warning |
| `pricing_cost` | Cost Reality, Do/Don't, Key Takeaway | CompanyDEBT View |
| `legal_compliance` | Legal Exposure, What Most Directors Miss, Do/Don't | Timeline Reality |
| `recovery_strategy` | Recovery Path, Key Takeaway, Orientation Block | Inline CTA |
| `case_insight` | CompanyDEBT View, Key Takeaway, Process Steps | Creditor Perspective |

---

## 28.6 QA checklist

Before publishing any page with components:

- [ ] No two identical component types adjacent
- [ ] No component in the first two paragraphs
- [ ] No component immediately before Methodology or Sources
- [ ] Total components ≤ 4
- [ ] Any Legal Exposure or Risk Warning callout reviewed by licensed IP (file 26 §26.8)
- [ ] Evidence level confirmed for all editorial callouts (file 26 §26.3)
- [ ] Components support comprehension — not placed for decoration
