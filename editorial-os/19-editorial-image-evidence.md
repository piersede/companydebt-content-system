# 19. Editorial Image Evidence System

Images are not decoration. They are proof of work. Every visual asset on a Company Debt page must advance a claim, answer a reader question, or provide evidence that text alone cannot deliver.

This system is adapted from a forensic audit of Pack Hacker's editorial image architecture and translated for business comparison content (credit cards, software, financial services).

## 19.1 Core principle: claim-then-verify

Every substantive claim in a review or comparison should be followed by a visual asset that proves or illustrates the claim. The pattern is:

1. Make a specific editorial claim in prose (e.g. "the rewards dashboard breaks cashback into clear spending categories").
2. Follow immediately with a screenshot, annotated image, or data visualisation that lets the reader verify the claim without trusting the writer's word alone.

This is not optional for review-type content. It is the baseline expectation.

## 19.2 Visual rhythm and density

Target one visual asset every 120-150 words in review and comparison content. This interval prevents text fatigue and keeps evidence close to claims.

| Page type | Target image count | Visual focus |
|---|---|---|
| Single product review | 8-12 assets | Forensic screenshots, annotated UI, fee breakdowns |
| Comparison/roundup guide | 6-10 assets | Side-by-side comparisons, scorecards, data tables |
| Brand/category hub | 4-6 assets | Product card art, quick-compare widgets |
| Informational guide | 2-4 assets | Contextual illustrations, workflow diagrams |

Images must not cluster at the top. Distribute them through the full article so visual proof appears at the point where the claim is made.

## 19.3 Proof visual types for digital and financial products

Physical product sites use product photography. Business comparison sites use forensic screenshots. The translation:

| Physical product equivalent | Business comparison equivalent | Implementation |
|---|---|---|
| Environmental hero shot | Main dashboard overview | High-res, logged-in screenshot of the primary UI |
| Material texture detail | Pricing/fee disclosure table | Screenshot of the actual fee schedule within the account |
| Internal organisation shot | Onboarding/setup flow | Sequence of screenshots showing friction or ease of setup |
| Functional/action shot | Reporting/analytics view | Annotated view of a real report being generated |
| Scale/context shot | Mobile vs desktop view | Side-by-side comparison of the same feature on different platforms |
| Timeline-of-use wear shot | Support response logs | Screenshot with timestamped response from live chat |

**Hard rule:** Screenshots must never be taken from the public marketing site. They must represent the actual user experience behind a login. If logged-in access is not available, mark the image with `[MARKETING ASSET — NOT LOGGED-IN VIEW]`.

## 19.4 Page-type playbooks

### A. Single product forensic review

Required assets:

| Asset | Description | Purpose |
|---|---|---|
| Entry hero | Logged-in view of the primary screen | Establishes authority and access |
| Friction audit | Step-by-step application/onboarding sequence | Shows real time investment |
| Transparency shot | Hidden fees menu or actual fee deduction | Builds trust through disclosure |
| Utility macro | Close-up of key mobile or desktop feature | Shows ergonomics and functionality |
| Support evidence | Screenshot of real interaction with support | Proves support quality claims |

### B. Comparison/roundup guide

- **Scoreboard template:** Each product gets a standardised graphical badge with category breakdowns (fees, ease of use, features).
- **Gap analysis visual:** Side-by-side screenshots comparing a specific feature across the top picks.
- **Selection badge:** Branded icon for "Best Overall", "Best for Start-ups", etc.

### C. Brand/category hub

- **Visual grid:** Standardised product images (card art, app icons) paired with key offer in readable type.
- **Quick-compare widget:** Visual tool allowing selection of 2-3 products for high-level comparison.

## 19.5 Capture and annotation standards

1. **Logged-in only.** No marketing site screenshots for review content.
2. **Standardised viewport.** Desktop screenshots at 1920x1080. Mobile screenshots at standard device widths.
3. **Consistent annotation style.** Use brand-approved colours and line weights for arrows, boxes, and overlays. One colour for positive features, another for friction points.
4. **Privacy protocol.** Pixelate or blur all PII (account numbers, names, balances) with a consistent filter.

## 19.6 Image metadata and SEO protocol

### Filenaming
Pattern: `[product]-[feature]-[intent].webp`

Example: `square-pos-inventory-tracking-tutorial.webp`

### Alt text
Must describe the action or benefit shown, not just the interface.

- Bad: "Screenshot of Square inventory page"
- Good: "Square POS inventory tracking screen showing low-stock alert notifications for a retail business"

### Captions
Every screenshot must have a unique caption that highlights the claim being verified. Format as a bolded lead-in followed by a descriptive sentence.

### Proximity to headings
Images should immediately follow the relevant H2/H3 tag to reinforce the topical authority of the section.

## 19.7 Technical performance protocol

| Requirement | Standard |
|---|---|
| Format | WebP or AVIF via CDN, with JPG/PNG fallback |
| Lazy loading | `loading="lazy"` on all images except above-fold hero |
| Dimensions | Always include `width` and `height` attributes to prevent CLS |
| Responsive delivery | `srcset` with multiple size variations; `sizes` attribute matching layout |
| Hero priority | `fetchpriority="high"` on above-fold hero image |
| Schema integration | Every review must include Review schema pointing to the primary screenshot as the `image` property |

## 19.8 Advanced visual tactics

These go beyond baseline requirements and should be implemented as capacity allows:

1. **Forensic receipt audit.** For payment processors and credit cards, perform a real transaction and screenshot the settlement. Provides irrefutable proof that text tables cannot match.
2. **Live speed tests.** For software, use short looping GIFs showing the actual time to complete key actions.
3. **Integration proof.** Instead of listing integrations, screenshot the "Integration Active" toggle within the software settings.
4. **Historical UI archive.** For products with major updates, maintain comparison images showing the old vs current interface. Signals ongoing maintenance to search engines.
5. **Real-world context shots.** Occasionally show a business owner using the product in a real office environment. Grounds digital services in reality.
