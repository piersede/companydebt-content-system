# 24. Content Registry and Entity Ownership

Governance layer for anti-cannibalisation, entity ownership, and structured metadata. This file defines the system that sits above the CMS and below the editorial workflow.

---

## 24.1 Core principle

One entity, one canonical owner URL. Every major insolvency procedure, creditor-action mechanism, director-risk concept, and distress state must have exactly one canonical owner page on the site.

The sitemap is treated as the immutable taxonomy. Governance is applied through an overlay that attaches metadata to each sitemap node. Do not restructure the site to control overlap. Control overlap by enforcing what each URL is allowed to do.

---

## 24.2 Entity registry

The entity registry is the single place where Company Debt defines concept-level ownership. It must include entities across:

- formal procedures
- creditor actions
- tax-distress mechanisms
- director exposure
- distress states
- special programmes

### Enforcement rules

- one canonical owner URL per entity
- one supporting set per entity
- one do-not-compete constraint set
- only entity-owner pages may fully define an entity

---

## 24.3 Content object types

Every page must be assigned exactly one content object type as a mandatory CMS field:

| Type | Purpose | Scope limit |
|---|---|---|
| HUB | Navigation and distribution | Must not compete with entity owners |
| ENTITY_OWNER | Canonical definitional page | Owns the entity |
| ENTITY_MODIFIER | Cost, timeline, comparison, failure-mode subpages | Narrow scope |
| TRIGGER | Distress symptom pages | Route to solutions |
| ENFORCEMENT | Legal artefacts and actions | Deadlines, options, risks |
| DIRECTOR_RISK | Duties, guarantees, disqualification, liability | Liability concept and mitigation |
| TEMPLATE | Operational assets | Utility plus routing |
| CASE_STUDY | Anonymised resolution examples | Must not cannibalise owners |
| B2B_SERVICE | Creditor, lender, bank, solicitor, or accountant-facing | Commercial route with declared relationship |
| NEWS_COMMENTARY | Topical authority | Must not cannibalise owners |

---

## 24.4 Page metadata schema

Every page in the registry must carry:

- `node_id`
- `node_class`
- `primary_entity`
- `primary_intent`
- `audience_primary`
- `decision_stage`
- `allowed_overlap`
- `overlap_exclusions`
- `entity_owner_url`
- `citations_required`
- `reviewer_requirement`
- `trust_pack_required`
- `freshness_tier`
- `internal_link_requirements`
- `commercial_alignment`

---

## 24.5 Intent ownership

Every page is assigned exactly one primary intent:

1. definition
2. decision
3. execution
4. escalation

### Scope boundaries

- definition pages may summarise choice logic but must route to decision pages
- decision pages may summarise options but must route to definition and execution pages
- execution pages must not become canonical definitions
- escalation pages must route to the applicable procedure owner

---

## 24.6 Anti-cannibalisation rules

Required overlap controls per page:

- exactly one primary entity
- maximum five approved secondary entities
- explicit prohibited entities
- mandatory internal links to canonical owners, parent hubs, and next-step pages
- no H2 or H3 structures that accidentally claim canonical ownership for a sibling topic

### Pre-publication checks

Before publication, verify:

1. semantic overlap against canonical owner patterns
2. internal-link compliance to canonical owners

---

## 24.7 Commissioning protocol

Every new content brief must declare:

- entity name and owner URL
- intent class and scope exclusions
- competing pages
- routing plan
- evidence plan

New content should usually extend existing owners or add spokes under an existing hub rather than create unnecessary new URLs.

---

## 24.8 Consolidation playbook

When overlap exists:

1. choose the canonical owner
2. merge the strongest unique sections into it
3. redirect non-canonical URLs where appropriate
4. update internal links
5. add scope statements to prevent future re-expansion

---

## 24.9 Retrieval metadata

For high-risk pages, keep these fields available:

- `one_sentence_answer`
- `director_action_next_72h`
- `key_risks`
- `what_this_page_does_not_cover`

These fields help keep retrieval anchored to the canonical owner.
