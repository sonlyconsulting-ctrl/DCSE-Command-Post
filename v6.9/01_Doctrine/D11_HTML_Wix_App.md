# DCSE Doctrine D11: HTML, Wix, and App Governance

**Document ID:** DCSE-D11  
**Version:** v6.9  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T15:22:37-04:00  
**Last Version/Release Date/Time:** 2026-06-21T15:22:37-04:00  
**Status:** CANDIDATE  
**Classification:** INTERNAL  
**Lane:** ALL  
**Canonical file:** D11_HTML_Wix_App.md  
**Doctrine Description:** The HTML, Wix, and App Governance Doctrine (D11) regulates the implementation of web assets, standalone interactive modules, and Wix-embedded widgets. It defines secure iframe sandboxing, postMessage dynamic sizing communication, and CSS styling token stacks. D11 ensures responsive layout standards across mobile, tablet, and desktop breakpoints while enforcing credential safety in browser-facing code.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## Part 1: Standalone Interactive Modules

Interactive HTML modules (calculators, review interfaces, dashboards, decision engines) function as standalone software apps running in local or hosted environments.

### 1.1 UI State Management
- **Explicit State Schema**: Every interactive module must maintain an explicit, serializable state object (draft, review, confirmed, rejected, conflict, blocked, archived).
- **No Silenced Failures**: Visual alerts must appear for validation errors, write failures, and connection drops. Standardize success indicators (`--accent-success`), info banners (`--accent-info`), and warnings/errors (`--accent-alert`).
- **Data Boundaries**: When communicating with backend services (such as Supabase):
  - Utilize only public-safe anonymous keys in browser-facing code.
  - Ensure all database writes are routed through row-level security (RLS) policies.
  - Sanitize and escape all untrusted user data before rendering to prevent Cross-Site Scripting (XSS) attacks.

### 1.2 Layout Rules
- Avoid card-nesting (do not nest cards inside other cards). Keep cards at an 8px border radius or less.
- Control densities: use compact, data-dense layouts for internal dashboards and workspaces, but retain generous breathing room for consumer-facing tools.

---

## Part 2: Wix-Embedded Modules

When embedding interactive widgets or custom HTML modules in Wix pages, strict containment and integration protocols apply to maintain performance and visual parity.

### 2.1 iframe Container Isolation
- **Secure Sandboxing**: Embed modules within custom iFrame components (HTML widgets) using strict sandbox settings: `sandbox="allow-scripts allow-downloads allow-forms allow-same-origin"`.
- **Explicit PostMessage Protocol**: Communication between the parent Wix page (via Wix Velo) and the embedded iframe must occur exclusively through `window.postMessage`.
  - Validate the origin of incoming messages on both sides to prevent cross-origin scripting issues.
  - Reject messages that do not contain a verified schema format.

### 2.2 Sizing and Fit Standard
- **No Fixed Heights**: Prevent double scrollbars by utilizing dynamic height adjustments. Embedded modules must send their height changes to the parent Wix page via postMessage, allowing the Wix container to resize dynamically.
- **Wix Styling Parity**: Embedded elements must match Wix styles, importing and utilizing Wix CSS variables or inheriting fonts and colors dynamically.

---

## Part 3: Responsiveness Best Practices

All content pages and interactive tools must render flawlessly across all standard screen sizes (mobile, tablet, laptop, and desktop).

### 3.1 Fluid Layout Standards
- **Use Flexbox and Grid**: Absolutely no hardcoded pixel widths (`width: 800px`) on main containers. Use `max-width: 100%`, flexbox layouts, or CSS grid.
- **Breakpoints**: Standardize media queries around the following breakpoints:
  - Mobile Portrait: `< 480px`
  - Tablet/Mobile Landscape: `481px - 768px`
  - Laptop: `769px - 1024px`
  - Desktop: `> 1025px`
- **Fluid Typography**: Use relative units (`rem`, `em`, `vh`, `vw`, `clamp()`) for font-sizes and padding to scale layout proportions smoothly.
- **Overflow Prevention**: Apply `box-sizing: border-box` globally and configure `overflow: hidden` or `overflow-x: auto` on container levels where overflow risks exist.

---

## Part 4: Technical Consistency Standards

Consistency across files, lanes, and visual builds prevents brand degradation and errors.

### 4.1 Reconciled Brand Token Stack
- **Standardized Fonts**:
  - Display Font (H1/H2): `'Cormorant Garamond', Georgia, serif`
  - UI Labels & Subheaders: `'Barlow Condensed', 'Arial Narrow', sans-serif`
  - Monospace (Code/Data): `'DM Mono', monospace`
- **Standardized Color Map**:
  - DCSE Blue (Structure/Clinical): `#0A192F`
  - SC Gold (Warmth/Approachability): `#D4AF37`
  - PS Dark (Litigation/Court Register): `#333333`
  - SS Earth (Soulful/Narrative): `#D2691E` & `#8B4513`
  - Emerald (Growth/Transformation): `#50C878`
  - Silver (Modern/Technical): `#C0C0C0`

> **Canonical palette source**: [D09_Brand_Identity.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D09_Brand_Identity.md) Section 3. This section extends the canonical palette with implementation-specific CSS tokens.
- **Visual Motion**:
  - Animation cycles must remain interruptible.
  - Standardize keyframes (e.g. Sonly Flip: 11.7s cycle, 2s delay).
  - Respect user settings: always wrap animations in `@media (prefers-reduced-motion: reduce)` media queries.

### 4.2 Code & Copywriting Invariants
- **Em and En Dash Compliance**: Never allow em dashes (`—`) or en dashes (`–`) in HTML text strings, meta tags, or document markup. Standardize date ranges to use hyphens (`-`) or the word "to".
- **Semantic HTML**: Prioritize semantic tags (`header`, `main`, `section`, `article`, `nav`, `footer`) over generic `div` selectors to guarantee structural accessibility (WCAG 2.2 AA).
- **Footer Rule**: The standard footer layout requires candidate/release metadata and the controlling entity name to be clearly visible on drafts, while public pages must suppress internal labels.
- **Credential Safety**: Run pre-commit checks to ensure no API keys, private database connection strings, or system passwords exist in the code markup.

---

## Related Doctrine

- [D09_Brand_Identity.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D09_Brand_Identity.md) - Canonical brand color palette (this file extends with CSS tokens)
- [D07_Campaign_Governance.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D07_Campaign_Governance.md) - Campaign assets must follow HTML/Wix standards

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.
