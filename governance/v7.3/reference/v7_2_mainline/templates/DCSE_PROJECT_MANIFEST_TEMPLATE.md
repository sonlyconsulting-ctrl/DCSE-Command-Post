# DCSE Project Manifest Template

Use as `DCSE_PROJECT_MANIFEST.yaml` in governed product repositories.

```yaml
dcse_project:
  project_id: ""
  product_name: ""
  entity: ""
  lane: ""
  purpose: ""
  status: ""

  parent_governance:
    repository: "sonlyconsulting-ctrl/DCSE-Command-Post"
    branch: "main"
    master_profile: "governance/v7.2/DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md"
    navigation_standard: "governance/v7.2/DCSE_PARTICIPANT_NAVIGATION_AND_PROJECT_BOOTSTRAP_STANDARD_v1.md"
    product_start_gate: "governance/v7.2/product/DCSE_PRODUCT_START_GATE_AND_BUILD_DECLARATION_STANDARD_v1.md"
    shared_media_standard: "governance/v7.2/media/DCSE_SHARED_MEDIA_ASSET_STANDARD_v1.md"

  repository:
    full_name: ""
    authority_branch: ""
    starting_commit: ""

  build_contract:
    work_mode: "NEW_BUILD|MODIFY|PACKAGE|CAMPAIGN|HOTFIX|MIGRATION|REVIEW"
    source_baseline: ""
    current_release_state: ""
    preserve:
      - ""
    prohibited_changes:
      - ""
    supersession_target: ""
    reuse_search_completed: false

  product_start:
    declaration: "DCSE_PRODUCT_START_DECLARATION.yaml"
    gate_state: "READY|PARTIAL|START_GATE_BLOCKED"
    dcs_e_escalation: false
    escalation_reasons: []

  audience:
    personas: []
    problem_or_outcome: ""
    success_metric: ""

  journey:
    entry_point: ""
    primary_critical_path: []
    key_pages_or_states: []
    failure_recovery_path: ""
    operator_admin_path: ""

  destination:
    type: ""
    primary_url: ""
    canonical_host_or_slug: ""
    development_url: ""
    preview_url: ""
    production_url: ""
    url_state: "VERIFIED|RESERVED|TBD_BY_DCS_E|NOT_APPLICABLE"
    cta: ""
    checkout_or_access_handoff: ""
    contact_path: ""

  brand:
    brand_reference: ""
    voice_tone_reference: ""
    logo_wordmark_assets: []
    persona_assets: []
    hero_assets: []
    background_assets: []
    source_reference_assets: []
    approved_current_image_use: []
    prohibited_elements: []
    asset_usage_map: {}

  assets:
    manifest: "assets/DCSE_MEDIA_ASSET_MANIFEST.json"
    binary_storage: ""
    shared_media_standard: "governance/v7.2/media/DCSE_SHARED_MEDIA_ASSET_STANDARD_v1.md"
    required_delivery_variants: []
    archive_retention: ""

  deliverables:
    inventory: []
    package_structure: ""
    naming_convention: ""
    customer_facing_files: []
    internal_only_files: []
    delivery_or_download_method: ""
    version_label: ""
    packaging_acceptance: []

  content:
    source_of_truth: ""
    core_message: ""
    claims_evidence: []
    preserve_wording: []
    seo_aeo_geo: ""
    legal_compliance: []

  architecture:
    runtime_surfaces: []
    databases: []
    storage: []
    integrations: []
    auth_access: ""
    environment_variable_names: []
    browser_server_boundary: ""
    upstream_dependencies: []
    downstream_impacts: []
    shared_components_or_schemas: []
    backward_compatibility: ""

  constraints:
    target_date: ""
    time_to_market_priority: ""
    budget_boundary: ""
    quotas_rate_limits: []
    performance_capacity: ""
    technical_vendor_constraints: []
    execution_boundary: ""

  instructions:
    project_instructions: ""
    methodologies: []
    doctrine_overlays: []

  tasks:
    root: ""
    active_task_id: ""

  security:
    classification: ""
    secrets_location: "approved secret store"
    ps_exposure: "none"

  validation:
    commands: []
    device_browser_targets: []
    accessibility_target: ""
    performance_expectations: ""
    qa_compliance_checks: []
    acceptance_criteria: []
    evidence_destination: ""

  promotion:
    authority: "DCS Level 0 or verified delegation"
    rollback_reference: ""
```
