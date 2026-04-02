# 26. Call-Out Box Governance

Hard rules for structured call-out boxes in insolvency and debt content. Call-out boxes are not decoration. They are decision-critical interventions and often carry a higher evidence burden than body copy.

---

## 26.1 Core principle

Every call-out box must shift the reader's judgement.

If it repeats nearby copy, it fails.
If it introduces a claim without evidence, it fails.
If it uses sales language, it fails.

---

## 26.2 Approved call-out types

### 1. CompanyDEBT View

- purpose: process framing and disciplined multi-route decision guidance
- tone: authoritative and grounded, never sales-led
- evidence level: B or C
- placement: entity-owner pages and service pages

### 2. What Most Directors Miss

- purpose: blind-spot correction
- tone: direct, slightly urgent, protective
- evidence level: A or B
- placement: director-risk, trigger, and procedure pages

### 3. Risk Warning

- purpose: imminent danger and deadline intervention
- tone: calm but firm
- evidence level: A only
- placement: top third of enforcement, procedure, and director-risk pages

### 4. Cost Reality

- purpose: realistic cost drivers and ranges
- tone: transparent and assumption-led
- evidence level: A or B with assumptions
- placement: procedure pages and cost modifiers

### 5. Legal Exposure

- purpose: director liability, disqualification, wrongful trading, preferences, undervalue transactions
- tone: clinical and statutory-led
- evidence level: A only
- placement: director-risk, enforcement, and procedure pages

### 6. Recovery Path

- purpose: structured route through a process with decision forks
- tone: calm, methodical, protective
- evidence level: B or C
- placement: entity-owner, trigger, and hub pages

### 7. Creditor Perspective

- purpose: creditor incentives and leverage from the creditor viewpoint
- tone: objective and fair
- evidence level: A for rights, B or C for behavioural claims
- placement: enforcement, creditor-facing, and procedure pages

### 8. Timeline Reality

- purpose: deadlines with consequence
- tone: precise and consequence-first
- evidence level: A only
- placement: enforcement, procedure, and trigger pages

---

## 26.3 Evidence ladder

| Level | Required for | Source standard |
|---|---|---|
| A | Statutory thresholds, deadlines, formal definitions, director liability, creditor priority | statute, case law, government guidance |
| B | Professional conduct and regulator guidance | SIPs, ethics codes, RPB or FCA guidance |
| C | Contextual interpretations aligned with formal guidance | reasoning basis stated explicitly |
| D | Anonymised case insights | method, consent, and date stated |

---

## 26.4 Box schema

Every box must include:

- `box_type`
- `title`
- `claim`
- `judgement_shift`
- `evidence_level`
- `evidence_refs`
- `audience_lane`
- `placement`
- `expiry_rule`
- `canonical_links`

---

## 26.5 Fail conditions

Any of these blocks publication:

1. repeats body copy
2. unqualified cost or timeline claim
3. new claim without evidence
4. sales language
5. mixed audience with no clear lane
6. non-canonical links where a canonical owner exists
7. fear-led framing with no legal grounding

---

## 26.6 Placement rules

Top-third placement is required for:

- enforcement pages using risk or timeline boxes
- procedure pages with director-liability implications
- director-risk pages
- immediate cash-flow triage pages

Pre-CTA placement is required on pages with a commercial CTA.

---

## 26.7 Page-type mapping

| Page type | Primary box types | Secondary box types |
|---|---|---|
| ENFORCEMENT | Risk Warning, Timeline Reality | Creditor Perspective |
| ENTITY_OWNER | CompanyDEBT View, Recovery Path | Cost Reality |
| DIRECTOR_RISK | Legal Exposure, What Most Directors Miss | Risk Warning |
| TRIGGER | Recovery Path, Cost Reality | What Most Directors Miss |
| CASE_STUDY | Case insight format | CompanyDEBT View |
| B2B_SERVICE | CompanyDEBT View | Creditor Perspective |

---

## 26.8 QA escalation

Any `Legal Exposure`, `Risk Warning`, or `Timeline Reality` box that references:

- director liability or disqualification
- enforcement thresholds or statutory deadlines
- creditor priority or preferential-payment rules

must be reviewed by a licensed insolvency practitioner or similarly qualified reviewer before publication.
