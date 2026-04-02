# 26. Call-Out Box Governance

Hard rules for structured call-out boxes in insolvency and debt content. Call-out boxes are not decoration — they are decision-critical interventions that carry the same evidence burden as body copy, often higher.

---

## 26.1 Core principle

Every call-out box must shift the reader's judgement. If it repeats what the surrounding copy says, it fails. If it introduces a claim without evidence, it fails. If it uses sales language, it fails.

---

## 26.2 Approved call-out types

Eight types are approved. No other box types may be created without updating this governance file.

### 1. CompanyDEBT View

**Purpose:** Process framing and disciplined multi-route decision guidance.
**Tone:** Authoritative, grounded in workflow expertise, never sales-led.
**Evidence level:** B or C (professional conduct/ethics or contextual interpretation aligned with statute).
**Placement:** Entity owner pages and service pages.
**Required:** One-sentence judgement shift that adds perspective beyond the surrounding prose.

### 2. What Most Directors Miss

**Purpose:** Blind spot correction. Names a specific misconception, then corrects it.
**Tone:** Direct, slightly urgent, protective.
**Evidence level:** A or B (statutory or professional guidance).
**Placement:** Director risk pages, trigger pages, procedure pages.
**Required:** Misconception stated explicitly, followed by correction with source.

### 3. Risk Warning

**Purpose:** Stop-and-verify intervention for imminent danger.
**Tone:** Calm but firm. Not fear-mongering.
**Evidence level:** A only (statutory threshold or deadline).
**Placement:** Top third of enforcement, procedure, and director risk pages.
**Required:** Specific deadline or threshold with statutory citation.

### 4. Cost Reality

**Purpose:** Cost drivers and realistic ranges, not bait pricing.
**Tone:** Transparent, assumption-led.
**Evidence level:** A or B with stated assumptions.
**Placement:** Procedure pages, modifier pages (cost subpages).
**Required:** Assumptions stated; no unqualified cost claims.

### 5. Legal Exposure

**Purpose:** Director liability, disqualification risk, wrongful trading, preferences, undervalue transactions.
**Tone:** Clinical, statutory-led.
**Evidence level:** A only (statute, case law, or government guidance).
**Placement:** Director risk pages, enforcement pages, procedure pages.
**Required:** Licensed IP or qualified reviewer sign-off before publication.

### 6. Recovery Path

**Purpose:** Structured route through a process with decision forks.
**Tone:** Calm, methodical, protective.
**Evidence level:** B or C, aligned with government guidance.
**Placement:** Entity owner pages, trigger pages, hub pages.
**Required:** Multiple paths presented; no inflated recovery promises.

### 7. Creditor Perspective

**Purpose:** Creditor incentives and leverage, presented from the creditor's viewpoint.
**Tone:** Objective, fair.
**Evidence level:** A for rights (statutory); B or C for behavioural claims.
**Placement:** Enforcement pages, creditor-facing pages, procedure pages.
**Required:** Distinguishes creditor rights from creditor likely behaviour.

### 8. Timeline Reality

**Purpose:** Deadlines with consequences. Not "fast" or "slow" — specific timeframes with what happens when they expire.
**Tone:** Precise, consequence-first.
**Evidence level:** A only (statutory deadlines, procedural timeframes).
**Placement:** Enforcement pages, procedure pages, trigger pages.
**Required:** Every timeline claim backed by primary source.

---

## 26.3 Evidence ladder for call-out boxes

Call-out boxes carry a stricter evidence requirement than body copy because they are visually prominent and often the first thing a reader in distress focuses on.

| Level | Required for | Source standard |
|---|---|---|
| A | Statutory thresholds/deadlines, formal procedure definitions, director liability claims, creditor priority order | Insolvency Act 1986, Companies Act 2006, government guidance, case law |
| B | Professional conduct/ethics claims about IPs, regulator guidance | SIPs, Insolvency Code of Ethics, RPB guidance, FCA guidance |
| C | Contextual interpretations aligned with statute or government guidance | Must be explicitly framed as interpretation; reasoning basis stated |
| D | Anonymised case insights | Method, consent, and date must be stated; no identifying details |

---

## 26.4 Call-out box schema

Every call-out box must include:

| Field | Requirement |
|---|---|
| box_type | One of the 8 approved types |
| title | Follows naming pattern for the type |
| claim | One sentence: the core assertion |
| judgement_shift | One sentence: what this changes about the reader's understanding |
| evidence_level | A, B, C, or D |
| evidence_refs | Source citations meeting the evidence level requirement |
| audience_lane | Which sub-persona this primarily serves |
| placement | Top third / Mid / Pre-CTA / Post-CTA |
| expiry_rule | When this box's claims need re-verification |
| canonical_links | Maximum 2 internal links to canonical owner pages |

---

## 26.5 Fail conditions (hard gates)

Any of these blocks publication:

1. **Repeats body copy** — the box says nothing the surrounding prose does not already say
2. **Unqualified cost or timeline claim** — cost or timeline stated without assumptions or source
3. **New claim without evidence** — introduces a factual assertion not backed by a source at the required evidence level
4. **Sales language** — any language that reads as promotional rather than informational
5. **Mixed audience** — tries to address multiple sub-personas without clarity about who it serves
6. **Non-canonical links** — links to non-owner pages when an entity owner exists
7. **Fear-led without legal framing** — uses fear as a motivator without grounding the risk in statute or case law

---

## 26.6 Placement rules

### Top-third placement required for:
- enforcement pages (Risk Warning, Timeline Reality)
- procedure pages with director liability implications (Legal Exposure)
- director risk pages (What Most Directors Miss, Legal Exposure)
- immediate cash flow triage pages (Recovery Path)

Top-third boxes must appear after the first definitional paragraph and before the deep explanation begins.

### Pre-CTA placement required for:
- any page with a commercial CTA (CompanyDEBT View or Recovery Path must precede the CTA)

---

## 26.7 Page-type to box-type mapping

| Page type | Primary box types | Secondary box types |
|---|---|---|
| ENFORCEMENT | Risk Warning, Timeline Reality | Creditor Perspective |
| ENTITY_OWNER | CompanyDEBT View, Recovery Path | Cost Reality |
| DIRECTOR_RISK | Legal Exposure, What Most Directors Miss | Risk Warning |
| TRIGGER | Recovery Path, Cost Reality | What Most Directors Miss |
| CASE_STUDY | (case insight format) | CompanyDEBT View |
| B2B_SERVICE | CompanyDEBT View | Creditor Perspective |

---

## 26.8 QA escalation

Any call-out box of type **Legal Exposure**, **Risk Warning**, or **Timeline Reality** that references:
- director liability or disqualification
- enforcement thresholds or statutory deadlines
- creditor priority or preferential payment rules

must be reviewed by a licensed insolvency practitioner or qualified reviewer before publication. Editorial-only review is not sufficient for these box types.
