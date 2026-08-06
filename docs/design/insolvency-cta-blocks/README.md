# Handoff: Insolvency Test — CTA Blocks

## Overview
Six CTA components that promote the "Insolvency Test" (4-question lead-gen tool at `Insolvency Test - Multi-Step Rebuild.html`) from within articles/pages on the CompanyDebt-style site. One full hero-style block (recommended primary placement), one compact block for mid-article use, and four laptop/browser-mockup explorations of the full block that were reviewed but not chosen as final.

## About the Design Files
The bundled HTML file is a **design reference built in HTML** — it shows intended look, spacing, responsive behavior and copy, not production code to copy directly. Recreate these designs in the target codebase's existing environment (React components, WordPress template, whatever the site already uses) using its established patterns, componentry and CSS approach — don't ship this raw HTML as-is.

## Fidelity
**High-fidelity.** Colors, typography, spacing and copy are final for the two primary blocks (Recommended Full Block, Compact Mid-Article Block). Recreate pixel-accurately. Versions 1–4 (laptop/browser explorations) are decision-support comparisons, not committed designs — see note below.

## Screens / Views

### 1. Recommended Full Block (primary — build this one)
**Purpose:** Full-width hero-style CTA driving traffic to the insolvency test from key pages.
**Layout:** Outer wrapper centers a card: `width: calc(100% - 64px); max-width: 1380px; margin: 24px auto;` — must not use a fixed left margin, must stay centered at all viewport widths. Card: `border-radius: 22px; padding: 54px 72px 52px; background: #fbfcfd; border: 1px solid rgba(0,40,86,.14)`.
Two stacked rows inside the card:
1. **Meta row** (`display:flex; align-items:center; gap:30px; margin-bottom:35px`): eyebrow label + timing indicator.
2. **Main row** (`display:grid; grid-template-columns: minmax(0,620px) minmax(380px,440px); justify-content:space-between; align-items:center; gap:72px`): left = copy/CTA column, right = laptop image, vertically centered against the left column.

**Components:**
- Eyebrow: "FREE ONLINE TEST", 16px/22px, weight 800, uppercase, letter-spacing .03em, color `#ff6600`.
- Timing indicator: clock icon (16×16, stroke `#ff6600`) + "4 questions · 2 minutes", 16px/22px, weight 700, color `#52606d`.
- Heading: "Could Your Company Be Insolvent?", 52px/1.08 line-height, letter-spacing -.02em, weight 800, color `#002856`, margin-bottom 24px.
- Body copy (2 paragraphs, 21px/32px, weight 400, color `#52606d`, max-width 620px): "Answer four short questions about cash flow and creditor pressure." / "See which warning signs apply and what options may be available." Gap between paragraphs 10px; margin below second paragraph 38px.
- Button: "Check my company's position" + arrow icon (18×18, right-pointing arrow, 11px gap from text). `background:#ff6600; color:#fff; border-radius:12px; min-height:64px; width:fit-content; min-width:360px; padding:18px 28px; font-size:20px; font-weight:700`. Hover: darken to `#e65c00`, arrow nudges 3px right (no button movement, no scale/bounce). Include a visible keyboard focus ring.
- Reassurance text below button (margin-top 22px, 16px/24px, color `#52606d`): "See your result online and receive a copy by email." then, on its own line (margin-top 4px, bold, color `#002856`): "We only call if you ask."
- Visual: laptop mockup image (`assets/laptop-mockup-cropped.png`), max-width 430px, showing the test's real first question and four answer options on-screen, vertically centered against the left column.

**Interactions:** Link navigates to the insolvency test tool. Button hover/focus states as above. No animation beyond the button hover.

**Responsive (breakpoint 900px):** Single column — order: meta row → heading → copy → button → reassurance → laptop image (laptop goes last, `order:99`, margin-top 24px, max-width 270px). Card: `width: calc(100% - 32px); margin:16px auto; padding:28px 24px 32px; border-radius:18px`. Type scales down: eyebrow/timing 14px, heading 35px/1.15, body 18px/27px, reassurance 15px/23px. Button becomes full-width, `min-height:56px`, `font-size:18px`.

### 2. Compact Mid-Article Block
**Purpose:** Lower-commitment CTA to drop inline within article body copy without competing with surrounding content.
**Layout:** `width:640px` (fluid down to `max-width:400px` below 480px), `border:1px solid rgba(0,40,86,.14)`, `border-radius:14px`, `padding:30px 40px`, white background. No image, no icon, no second button.
**Components:**
- Title: "Not Sure Where Your Company Stands?", 24px, weight 800, color `#002856`.
- Body: "Answer four questions in about two minutes and see which warning signs apply and what your company may be able to do next." 16px, color `#52606d`, max-width 480px.
- Button: "Check My Company's Position →", `background:#ff6600; border-radius:14px; padding:20px 40px; font-size:18px; weight:800`. Hover darkens to `#e65c00`.
- Reassurance line: "Estimates are fine · **We only call if you ask us to**" (second clause bold, navy). On screens ≤480px the middot separator is dropped and the two phrases stack on separate lines instead.
**Responsive (≤480px):** Button becomes full-width, centered text.

### 3–6. Laptop/Browser Exploration Versions (reference only — not committed)
Four variations reviewed when deciding how to present the laptop visual in the full block: (1) small laptop image contained fully in the right column, (2) a browser-window mockup of the test screen instead of a physical laptop, (3) a smaller laptop floating in open space with the timing badge stacked above it, (4) a laptop image deliberately cropped/bled off the card's right edge (`overflow:hidden` on the card clips the image). These share a `.v-card` layout (56%/36% two-column grid, 8% gap) and stack to one column below 680px. **Version 1's visual treatment is what was carried into the Recommended Full Block above** — versions 2–4 are included for context on the exploration but were not selected. Full markup/CSS is in the bundled HTML if useful as reference.

## Design Tokens
- Colors: navy `#002856`, navy-dark `#102a43`, orange (brand accent/CTA) `#ff6600`, orange-hover `#e65c00`, body text `#2a2a2e`, grey/secondary text `#52606d`, page background `#f4f6f8`, hairline border `rgba(0,40,86,.14)`.
- Spacing scale (8-step, used throughout the site's other insolvency-test screens): 10 / 20 / 30 / 40 / 52 / 64px.
- Type scale (site-wide base, used on the smaller blocks): 13 / 15 / 16 / 18 / 24 / 32px. The Recommended Full Block uses a bespoke larger hero scale (16 / 21 / 52px) per the latest design review — treat as intentional, not a token violation.
- Border radius: 12–14px on cards and buttons; 999px pill only remains nowhere now (buttons were squared off from pill shape to 14px so wrapped mobile labels don't distort into an oval).
- Shadows: none used — flat, calm, non-promotional styling per the target audience (directors of financially stressed companies) — avoid adding drop shadows or glow effects.

## Assets
- `assets/laptop-mockup-cropped.png` — user-supplied laptop product photo/mockup showing the test's first question on-screen (auto-cropped from the original to remove transparent padding). Use as-is or swap for a higher-resolution asset (~880px source width recommended per design review) if greater screen-content sharpness is needed.

## Files
- `Insolvency Test - CTA Blocks.html` — full HTML/CSS source for all 6 blocks (this is the design reference described above, on a pannable canvas layout for side-by-side comparison — not the shipping page structure).
- `screenshots/` — static renders of each block for quick visual reference:
  - `01-recommended-full-block.png`
  - `02-compact-mid-article-block.png`
  - `03-version1-laptop-contained.png`
  - `04-version2-browser-preview.png`
  - `05-version3-laptop-floating.png`
  - `06-version4-cropped-edge.png`
