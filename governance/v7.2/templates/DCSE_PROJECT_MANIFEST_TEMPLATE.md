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
  product_start:
    declaration: "DCSE_PRODUCT_START_DECLARATION.yaml"
    gate_state: "READY|PARTIAL|START_GATE_BLOCKED"
    dcs_e_escalation: false
    escalation_reasons: []
  parent_governance:
    repository: "sonlyconsulting-ctrl/DCSE-Command-Post"
    branch: "main"
    master_profile: "governance/v7.2/DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md"
    navigation_standard: "governance/v7.2/DCSE_PARTICIPANT_NAVIGATION_AND_PROJECT_BOOTSTRAP_STANDARD_v1.md"
  repository:
    full_name: ""
    authority_branch: ""
  instructions:
    project_instructions: ""
    methodologies: []
    doctrine_overlays: []
  tasks:
    root: ""
    active_task_id: ""
  destination:
    type: ""
    primary_url: ""
    url_state: "VERIFIED|RESERVED|TBD_BY_DCS_E|NOT_APPLICABLE"
    cta: ""
    checkout_or_access_handoff: ""
  brand:
    brand_reference: ""
    voice_tone_reference: ""
    persona_assets: []
    background_assets: []
    source_reference_assets: []
  assets:
    manifest: "assets/DCSE_MEDIA_ASSET_MANIFEST.json"
    binary_storage: ""
    shared_media_standard: "governance/v7.2/media/DCSE_SHARED_MEDIA_ASSET_STANDARD_v1.md"
  runtime:
    deployments: []
    databases: []
    storage: []
  security:
    classification: ""
    secrets_location: "approved secret store"
    ps_exposure: "none"
  validation:
    commands: []
    evidence_destination: ""
  promotion:
    authority: "DCS Level 0 or verified delegation"
    rollback_reference: ""
```
