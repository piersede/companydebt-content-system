# 24. Content Registry and Entity Ownership

Governance layer for anti-cannibalisation, entity ownership, and structured metadata. This file defines the system that sits above the CMS and below the editorial workflow — the operational source of truth for what each URL is allowed to do.

---

## 24.1 Core principle

One entity, one canonical owner URL. Every major insolvency procedure, creditor-action mechanism, director-risk concept, and distress state must have exactly one canonical owner page on the site.

The existing sitemap is treated as the immutable taxonomy. Governance is applied through an overlay that attaches metadata to each sitemap node. You do not restructure the site to control overlap; you control overlap by enforcing what each existing URL is allowed to do.

---

## 24.2 Entity registry

The entity registry is the single place where Company Debt defines concept-level ownership. It must include entities across:

- **Formal procedures:** CVA, administration, pre-pack, liquidation (CVL / compulsory), receivership, dissolution/strike-off
- **Creditor actions:** statutory demands, winding-up petitions, CCJs, enforcement agents/bailiffs, freezing orders, validation orders
- **Tax distress mechanisms:** Time to Pay, HMRC enforcement steps, security bonds, personal liability notices, joint and several VAT liability
- **Director exposure:** personal guarantees, wrongful trading, preferences/undervalue transactions, disqualification, misfeasance
- **Distress states:** cash flow distress, ceased trading, insolvency tests, creditor pressure escalation
- **Special programmes:** Bounce Back Loans / CBILS treatment and misuse risk

### Enforcement rules

- One canonical owner URL per entity
- One "supporting set" per entity: allowed spoke pages and comparison pages
- One "do not compete" constraint set: pages that reference the entity but may not attempt to rank as the primary explainer
- Only ENTITY_OWNER pages may fully define an entity; child pages must summarise and route back

---

## 24.3 Content object types

Every page must be assigned exactly one content object type as a mandatory CMS field:

| Type | Purpose | Scope limit |
|---|---|---|
| HUB | Navigation and distribution | Must not compete with entity owners; no full definitions |
| ENTITY_OWNER | Canonical definitional page for a procedure/solution | Owns the entity; all other pages route here |
| ENTITY_MODIFIER | Cost/timeline/comparison/failure mode subpages | Narrow scope; one modifier intent per page |
| TRIGGER | Distress symptom pages ("can't pay X", frozen account) | Route to solutions; do not redefine procedures |
| ENFORCEMENT | Legal artefacts (statutory demands, petitions, bailiffs) | What was served, deadlines, options, risks |
| DIRECTOR_RISK | Duties, guarantees, disqualification, antecedent transactions | Liability concept, statute, mitigation |
| TEMPLATE | Operational assets (letters, checklists) | Utility + routing to strategy pages; not decision guides |
| CASE_STUDY | Anonymised resolution examples with evidence pack | Must not cannibalise entity owners |
| B2B_SERVICE | Creditor/lender/bank/solicitor/accountant facing | Commercial route with declared relationship |
| NEWS_COMMENTARY | Topical authority | Must not cannibalise owners; clearly date-stamped |

---

## 24.4 Page metadata schema

Every page in the registry must carry:

| Field | Purpose |
|---|---|
| node_id | Stable key derived from URL (does not change when titles change) |
| node_class | Content object type from §24.3 |
| primary_entity | The single owned concept |
| primary_intent | Job-to-be-done: diagnose / compare / comply / execute / contact |
| audience_primary | Director / Creditor / Adviser-referrer / Sector-operator |
| decision_stage | Early warning / Active pressure / Formal procedure / Closure / Post-event / Creditor-side |
| allowed_overlap | Entities this page may cover secondarily (explicit whitelist, max 5) |
| overlap_exclusions | Entities this page must not attempt to own (explicit blacklist) |
| entity_owner_url | The canonical owner URL for this page's primary entity |
| citations_required | Yes/No + primary-source list requirements |
| reviewer_requirement | IP review / editorial-only |
| trust_pack_required | Mandatory components (byline, reviewer, methodology, last-reviewed date) |
| freshness_tier | See `25-update-logic.md` |
| internal_link_requirements | Mandatory links to parent hub + next-step pages |
| commercial_alignment | Allowed CTA type and service route mapping |

---

## 24.5 Intent ownership

Entity ownership alone is not sufficient. Intent ownership prevents query-stage confusion.

### Four intent classes

Every page is assigned exactly one primary intent:

1. **Definition intent:** "What is X?" and "How does X work?"
2. **Decision intent:** "Should I choose X or Y?" and "Which is right?"
3. **Execution intent:** "How to do X", "documents needed", "timeline/cost"
4. **Escalation intent:** "What happens if...", "can they...", "risks/liability"

### Scope boundaries

- A definition page can include a short "when to choose" section but must route to decision pages for comparisons
- Decision pages can summarise each option but must route to definition pages for mechanics and to execution pages for steps
- Execution pages can give step-by-step but must not attempt to become the canonical definition
- Escalation pages can explain consequences but must route to the applicable procedure owner

---

## 24.6 Anti-cannibalisation rules

### Required overlap controls per page

- Primary entity: exactly one
- Secondary entities allowed: maximum of five, pre-approved
- Prohibited entities: explicit list (especially those owned by sibling pages)
- Required internal links out: mandatory links to (a) entity owner, (b) parent hub, (c) relevant decision/next-step page
- Prohibited internal anchors: phrases that cause "accidental ownership" (e.g., a scenario page using "What is a CVA?" as a primary H2)

### Pre-publication checks

Before publication, verify:
1. **Semantic overlap check:** does the page's H2/H3 set match another canonical owner's outline pattern?
2. **Internal link compliance check:** does the page contain the required links to canonical owners?

### High-risk overlap pairs

These pairs are prone to cannibalisation and must have explicit ownership boundaries:

- process owner vs "Can I...?" subpages
- procedure page vs comparison page
- creditor action page vs definition page
- "company bankruptcy" vs "insolvency vs bankruptcy"
- liquidation vs CVL vs voluntary liquidation
- statutory demand vs winding-up petition

---

## 24.7 Commissioning protocol

New content should rarely be new URLs. Most growth should occur through:
- expanding sections inside canonical owners
- adding spokes under an existing hub when a new scenario is distinct
- adding comparison pages only when both entities already have owners

Every new content brief must declare:
- entity name + owner URL (existing or new)
- intent class + explicit "not this intent" exclusions
- "competes with" declaration: list of existing pages covering similar ground
- routing plan: where the page sends the user next
- evidence plan: which primary sources must be cited

---

## 24.8 Consolidation playbook

When overlap exists:

1. Choose the canonical owner (usually the most central procedure/definition page)
2. Merge the strongest unique sections of non-canonical pages into the owner
3. 301 redirect non-canonical URLs where appropriate
4. Update internal links so hubs route to the canonical owner
5. Add a scope statement to both canonical and merged pages to prevent re-expansion

Do not rely on informal agreement. Consolidation is a content maintenance function, not a one-time cleanup.

---

## 24.9 Retrieval metadata

For LLM and machine retrieval, every high-risk page should include:

| Field | Purpose |
|---|---|
| one_sentence_answer | Page purpose in one sentence |
| director_action_next_72h | Immediate next steps for a director under pressure |
| key_risks | Primary risks if the reader does nothing |
| what_this_page_does_not_cover | Explicit scope exclusion |

These fields keep retrieval outputs anchored to the canonical owner and reduce hallucinated context.
