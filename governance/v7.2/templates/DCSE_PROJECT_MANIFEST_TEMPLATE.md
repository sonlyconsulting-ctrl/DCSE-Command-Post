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
  assets:
    manifest: "assets/DCSE_MEDIA_ASSET_MANIFEST.json"
    binary_storage: ""
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
