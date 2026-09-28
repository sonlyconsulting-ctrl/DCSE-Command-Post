# DCSE Doctrine D09: Brand Identity Governance v7.2 RC1 Candidate

**Document ID:** DCSE-D09-v7.2-RC1-CANDIDATE  
**Version:** v7.2 RC1 (reconciled candidate, 2026-09-19)  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to entity and product profile  
**Authority holder:** DCS  
**Prepared date:** 2026-09-19
**Candidate lineage:** v7.1 RC3 (2026-08-03), compared to main v7.2 D09 carried-forward and proposed PR #158 brand-motion changes  
**Source doctrine:** `governance/v7.1/source/doctrines/D09_Brand_Identity.md`  
**Source SHA-256:** `4d6ec4f7dae479cbbd342876dbb1b0e7d43af622dd1c9741897f162462328244`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE. The 2026-09-19 DCS CTJ image selection is an asset-level direction, not blanket doctrine promotion. D05/D21/D22 gates remain.  

## 1. Purpose

D09 governs names, marks, visual systems, design tokens, logos, typography, imagery, motion identity, asset rights, and cross-channel brand consistency for DCSE entities and products.

D09 defines governance and registry contracts. It does not freeze every palette, font, logo, or product identity into permanent doctrine.

## 2. Governing principles

1. Each brand asset has a verified owner, scope, version, status, and source.
2. Entity identities remain isolated unless an approved relationship permits co-branding.
3. Accessibility and usability control over decorative preference.
4. Trademark symbols reflect verified status, not aspiration.
5. Generated assets require provenance, rights review, and identity consistency.
6. A palette is a versioned brand profile, not a universal enterprise constant.
7. Public output must not expose internal candidate, lane, or governance metadata.
8. Brand drift is measured against the applicable profile, not model memory.
9. A brand update requires impact analysis across dependent artifacts.
10. Missing D09 isolates brand-dependent release, not unrelated product work.

## 3. Brand registry

```yaml
brand_profile:
  brand_id: ""
  legal_or_operating_owner: ""
  entity: ""
  product_or_program: ""
  public_name: ""
  controlled_terms: []
  abbreviations: []
  prohibited_variants: []
  tagline_refs: []
  mark_records: []
  logo_system_ref: ""
  color_token_ref: ""
  typography_ref: ""
  imagery_profile_ref: ""
  motion_profile_ref: ""
  voice_profile_ref: ""
  accessibility_baseline_ref: ""
  rights_and_license_refs: []
  approved_channels: []
  co_brand_rules: []
  authority_ref: ""
  version: ""
  status: "CANDIDATE | ACTIVE | RETIRED"
```

## 4. Controlled names and marks

- Public names and approved abbreviations come from the active brand profile.
- A model or designer may not rename a controlled entity or product for stylistic variation.
- Trademark and registration symbols require a verified mark record that identifies jurisdiction, status, owner, goods or services, and permitted display.
- A pending or unregistered mark must not use a registration symbol.
- Descriptive text may explain an entity without creating a new public name.
- Domain names, social handles, app names, and package names must reconcile to the brand registry.

## 5. Design token system

```yaml
design_token_set:
  token_set_id: ""
  brand_id: ""
  version: ""
  color_tokens: {}
  typography_tokens: {}
  spacing_tokens: {}
  radius_tokens: {}
  border_tokens: {}
  elevation_tokens: {}
  motion_tokens: {}
  icon_tokens: {}
  chart_tokens: {}
  state_tokens: {}
  dark_mode_tokens: {}
  accessibility_results: []
  source_artifact_ref: ""
  authority_ref: ""
```

Raw values such as hexadecimal colors may appear in the token artifact. Product code consumes semantic tokens such as `surface-primary`, `text-muted`, `action-primary`, `focus-ring`, `success`, `warning`, and `error`.

## 6. Accessibility and inclusive identity

Brand expression must preserve:

- required text and non-text contrast;
- visible keyboard focus;
- distinguishable interactive states beyond color alone;
- readable typography and zoom behavior;
- reduced-motion alternatives;
- text alternatives for meaningful logos and images;
- legibility over backgrounds and media;
- culturally responsible imagery;
- representation without tokenism, stereotype, or identity inference.

A premium aesthetic does not justify low contrast, unreadable text, inaccessible motion, or ambiguous controls.

## 7. Logo and asset governance

```yaml
brand_asset:
  asset_id: ""
  brand_id: ""
  asset_type: "LOGO | LOCKUP | ICON | PATTERN | IMAGE | TEMPLATE | FONT | MOTION"
  variant: ""
  source_ref: ""
  content_sha256: ""
  creator_or_provider: ""
  generation_record_ref: ""
  rights_or_license_ref: ""
  permitted_uses: []
  prohibited_uses: []
  accessibility_text: ""
  version: ""
  lifecycle_state: ""
```

Source files, exports, responsive variants, monochrome variants, and public derivatives retain lineage. A screenshot or generated approximation does not replace the canonical logo source.

## 8. Generated and external assets

AI-generated, stock, commissioned, and third-party assets require:

- source and provider;
- prompt or brief reference where applicable;
- creation date;
- license and permitted-use review;
- likeness, identity, and consent review;
- trademark and confusing-similarity review;
- disclosure requirements;
- content hash;
- human or governed acceptance evidence.

Generated output must not imitate a living artist, protected character, logo, celebrity, or real person's likeness without verified authority.

## 9. Co-branding and product variation

Co-branding records define hierarchy, spacing, attribution, shared palette, audience, channel, and ownership. One entity's palette or voice must not silently overwrite another's identity.

Product-specific profiles may extend enterprise design foundations. Extensions must identify inherited tokens, overridden tokens, accessibility evidence, and reason.

## 10. Change, drift, and retirement

Brand changes require:

1. exact source and proposed diff;
2. affected asset inventory;
3. accessibility assessment;
4. trademark and rights assessment;
5. code and content dependency analysis;
6. migration plan;
7. rollback or coexistence plan;
8. D05 authority and D22 reconciliation.

Retired assets remain identifiable so old publications and evidence can be interpreted accurately.

## 11. Brand validation receipt

```yaml
brand_validation_receipt:
  receipt_id: ""
  artifact_ref: ""
  brand_profile_ref: ""
  token_set_ref: ""
  controlled_name_result: ""
  mark_result: ""
  accessibility_result: ""
  rights_result: ""
  asset_lineage_result: ""
  drift_result: ""
  findings: []
  disposition: "PASS | PASS_WITH_CORRECTIONS | FAIL | INSUFFICIENT_EVIDENCE"
```

## 12. Runtime interfaces

```text
resolve_brand_profile(entity, product, channel) -> BrandProfile
resolve_design_tokens(profile, mode) -> DesignTokenSet
validate_brand_asset(asset, profile) -> BrandValidationReceipt
detect_brand_drift(scope, profile) -> DriftReport
plan_brand_migration(old_profile, new_profile) -> MigrationPlan
```

## 13. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D09-001 | Product palette changes | Versioned profile changes without doctrine rewrite. |
| D09-002 | Registration symbol lacks verified record | Public use fails. |
| D09-003 | Model renames a controlled product | Drift test fails. |
| D09-004 | Text contrast is insufficient | Accessibility result fails. |
| D09-005 | State differs only by color | Interaction identity fails. |
| D09-006 | Generated logo resembles protected mark | Release remains blocked pending rights review. |
| D09-007 | Real-person likeness lacks consent | Intended use fails. |
| D09-008 | Asset has no source lineage | Disposition is INSUFFICIENT_EVIDENCE. |
| D09-009 | Public page exposes candidate status | Validation fails. |
| D09-010 | Product extends enterprise tokens | Inheritance and overrides are recorded. |
| D09-011 | Two entities are co-branded | Approved hierarchy and ownership apply. |
| D09-012 | Dark mode is added | Contrast and state tokens are tested separately. |
| D09-013 | Motion ignores reduced-motion preference | Accessibility result fails. |
| D09-014 | Old logo remains in archive | It remains identifiable as retired, not deleted silently. |
| D09-015 | New palette affects applications | Dependency migration plan is required. |
| D09-016 | Stock asset license is unclear | Release is INSUFFICIENT_EVIDENCE. |
| D09-017 | D09 is unavailable | Brand-dependent release is isolated. |
| D09-018 | All criteria pass | Receipt returns PASS without promotion. |

## 14. Source correction record

| Source condition | RC3 correction |
| --- | --- |
| One fixed palette treated as universal | Versioned entity and product brand profiles. |
| Controlled terms listed without records | Registry-backed names and mark status. |
| No accessibility contract | Contrast, focus, motion, typography, and state controls. |
| No asset rights or provenance | Brand asset lineage and license contracts. |
| No change lifecycle | Drift, migration, rollback, and retirement controls. |
| Blanket halt | Brand-dependent affected-action isolation. |

## 15. Candidate status

This candidate does not replace active D09 or authorize a name, mark, palette, asset, public release, or promotion until exact DCS promotion and D22 reconciliation.

---
## 16. v7.2 reconciliation: authority, precedence, and parent-child inheritance

This RC1 is a **candidate consolidation**, not a restatement of operative v7.2 authority. The repository's `governance/v7.2/doctrines/D09_Brand_Identity_v7-2.md` remains the carried-forward operative source subject to the v7.2 controller until an exact DCS decision, independent review, and D05/D22 reconciliation. The original v7.1 RC3 file on `agent/v71-master-profile-rc3-manual` is candidate lineage. The proposed ident text in PR #158 is not automatically operative or merged by referencing it.

A product brand profile SHALL declare `parent_brand_id`, inherited SC tokens/typography, explicit scoped overrides with rationale, source/asset identifiers, approved use, accessibility test receipts, version, approver and promotion state. A child shall not modify its parent's global tokens. Inherited SC color anchors are gold `#D4AF37`, navy `#0A192F` or `#1B3A57`, and silver `#C0C0C0` until the approved SC profile selects specific roles. CTJ's currently selected shared UI navy `#061A33` is a **child-specific variant**, not a silent SC-wide navy replacement. The three alternative light canvas/commerce palettes remain distinct **unselected candidates**, not automatic changes to approved CTJ identity.

CTJ family / Unified specific decision is tracked separately (CTJ identity PR #156 and its subsequent supersession comment, issue #157). CTJ proper uses DCS-selected first circular full lockup. Unified uses the later **user-designated final 16:9 CTJ Unified Logo**, with no first-line tagline and the sole `CLARITY • PERSPECTIVE • ACTION` tagline below `The Unified Path`; it supersedes the earlier side-by-side right-panel *direction reference* as the identity end plate. The latest binary's exact hash, persistent authorized retrieval, rights and release status must be verified before using it as an approved technical master. “Executive Suite” is an audience hypothesis, **not an approved product name**.

### 16.1 Logo, icon, hero, and motion usage
- **Logo/lockup:** approved symbol plus readable complete name for first-contact identity, covers and formal attribution.
- **Icon:** purpose-made, tested derivative without illegible miniature wording for favicon, navigation and compact controls. The existence of an older simplified mockup does not mean the final icon is approved.
- **Product hero:** approved large-format narrative artwork specific to a product; it does not replace the parent logo or compact icon. A screenshot, generated near-match or re-render cannot be silently promoted as the exact canonical source.
- **Motion ident:** a brand/product primary-logo package SHALL include a 6–8-second illustrative motion-ident production requirement or a specific DCS-approved exception, with `motion_profile_ref`, original-logo end-plate identity and asset lineage. Existing brands lacking an ident become a tracked backlog, not falsely described as ident-complete; this addition does not retroactively unpublish unrelated approved work. D12 controls video rules and short-ident exception; D18 controls implementation; D19 controls new visual derivatives. A production prompt is not a rendered video.

### 16.2 Typography and controlled terms
The v7.2 carried-forward D11 token stack records SC display `Cormorant Garamond, Georgia, serif`, labels/subheaders `Barlow Condensed, Arial Narrow, sans-serif`, data `DM Mono, monospace`. D11 RC3's removal of **fixed universal fonts** SHALL NOT be read as evidence that the established SC typography was revoked. The active SC brand profile retains these inherited default roles until an explicitly approved versioned alternative; the precise typeface depicted in a raster CTJ logo remains **UNKNOWN** without an editable source. Inter is an implementation/body-text candidate where found, not a universally ratified brand font.

D09 legacy lists `GET YOUR THINK ON!™` as a public mark; D12's inherited blanket public suppression and D07's public-content handling differ. **Conflict unresolved**: decide applicability by exact current DCS term/mark records and intended channel, do not claim blanket public authorization or blanket prohibition from these competing historic passages. DCS must ratify the mark/channel usage contract before extending or withdrawing that term in public copy. “SS” and “TI” legacy expansions that differ from current enterprise entity routing are historic provenance, not permission for cross-lane leakage.

### 16.3 Executable validation
A brand-related deliverable SHALL resolve its current profile and actual source binary before release; absence from current chat is `ACCESS_UNKNOWN`, not verified global absence. Logo/video rendering SHALL pass text/geometry match, explicit product attribution, applicable rights, small/large size, contrast and reduced motion checks. Brand change must enumerate child products and media derivatives affected and test non-interference on unrelated entity profiles.

Additional v7.2 challenge cases: `D09-019` missing approved binary => no fabricated substitute; `D09-020` child overrides parent without profile => drift fail; `D09-021` short-ident prompt exists but no rendered master => media production remains pending; `D09-022` logo used as unreadable favicon => icon-size QA fails; `D09-023` newer DCS logo selection conflicts with older mockup => newest exact, verified decision controls after identity reconciliation, with previous artifacts preserved as lineage; `D09-024` source file or proposal exists without signed promotion => no authority upgrade.

**Status:** V7.2 RC1 CANDIDATE; brand-specific approved user decisions retain only their explicitly stated scope. No destructive retirement, public deployment, or doctrine promotion follows from this candidate.
