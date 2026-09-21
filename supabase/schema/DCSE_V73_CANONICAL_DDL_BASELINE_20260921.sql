-- ============================================================================
-- DCSE v7.3 CANONICAL DDL BASELINE
-- Canonical Reference: D15 Database Administration & D22 Source Authority
-- Task ID: DCSE-V73-SCHEMA-BASELINE-20260921-01
-- Authority: DCS Level 0 Approved Baseline
-- Date: 2026-09-21
-- Target: PostgreSQL / Supabase (DCSE-DDNA & SC-Command-Post)
-- ============================================================================

-- 1. SCHEMAS
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS dcse_cp;
CREATE SCHEMA IF NOT EXISTS v7_worker;
CREATE SCHEMA IF NOT EXISTS family_vow_go;

-- 2. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA extensions;

-- 3. CUSTOM ENUMS
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'dcse_record_status') THEN
        CREATE TYPE public.dcse_record_status AS ENUM ('RECEIVED', 'VALID', 'INVALID', 'NORMALIZED', 'TRIAGED', 'READY_FOR_LOAD', 'NEEDS_REWORK', 'APPROVED', 'ARCHIVED');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'dcse_review_status') THEN
        CREATE TYPE public.dcse_review_status AS ENUM ('DRAFT', 'IN_REVIEW', 'APPROVED', 'REJECTED', 'ARCHIVED');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'dcse_visibility') THEN
        CREATE TYPE public.dcse_visibility AS ENUM ('INTERNAL', 'PRIVATE', 'SHARED', 'PUBLIC');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'dcse_lifecycle_stage') THEN
        CREATE TYPE public.dcse_lifecycle_stage AS ENUM ('IDEA', 'DRAFT', 'ACTIVE', 'READY', 'PUBLISHED', 'RETIRED');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'dcse_confidentiality') THEN
        CREATE TYPE public.dcse_confidentiality AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'RESTRICTED');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'dcse_object_type') THEN
        CREATE TYPE public.dcse_object_type AS ENUM ('doctrine', 'entity', 'persona', 'profile', 'instruction', 'product', 'service', 'operational_asset', 'workflow', 'app_module', 'business_strategy', 'seo', 'aeo', 'geo', 'content_asset', 'knowledge_file', 'prompt_asset', 'model_configuration', 'ui_component', 'distribution_target', 'creativity_system', 'voice_tone_system', 'layer_module');
    END IF;
END $$;


-- 4. CORE PUBLIC GOVERNANCE & REGISTRY TABLES

CREATE TABLE IF NOT EXISTS public.users (
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT,
    display_name TEXT,
    role_name TEXT,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.entities (
    entity_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    entity_code TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    entity_type TEXT,
    positioning TEXT,
    tagline TEXT,
    mission_summary TEXT,
    voice_profile_ref TEXT,
    public_description TEXT,
    internal_description TEXT,
    priority_rank INTEGER,
    active_flag BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.tags (
    tag_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    tag_name TEXT NOT NULL,
    tag_group TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.SourceDocument (
    source_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    external_source_code TEXT,
    source_platform TEXT,
    source_model TEXT,
    source_type TEXT,
    title TEXT,
    file_name TEXT,
    file_type TEXT,
    source_uri TEXT,
    content_type TEXT,
    original_created_at TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    dedupe_hash TEXT,
    rawMetadata JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS public.intake_batches (
    batch_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    intake_label TEXT,
    source_model TEXT,
    run_mode TEXT DEFAULT "full" NOT NULL,
    received_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    received_by UUID,
    file_hash TEXT,
    raw_file_name TEXT,
    status public.dcse_record_status DEFAULT RECEIVED NOT NULL,
    confidence_overview TEXT,
    coverage_status TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS public.intake_batch_sources (
    batch_id UUID NOT NULL,
    source_id UUID NOT NULL,
    PRIMARY KEY (batchId, sourceId)
);

CREATE TABLE IF NOT EXISTS public.raw_json_artifacts (
    raw_json_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    batch_id UUID NOT NULL,
    artifact_name TEXT,
    raw_payload JSONB NOT NULL,
    validation_errors JSONB DEFAULT "[]" NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.ExtractionRun (
    extraction_run_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    batch_id UUID NOT NULL,
    prompt_family TEXT,
    source_model TEXT,
    run_mode TEXT DEFAULT "full" NOT NULL,
    started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMPTZ,
    status public.dcse_record_status DEFAULT RECEIVED NOT NULL,
    summary JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS public.unresolved_items (
    unresolved_item_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    extraction_run_id UUID NOT NULL,
    issue_type TEXT NOT NULL,
    description TEXT NOT NULL,
    recommended_resolution TEXT,
    severity TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.audit_log (
    audit_log_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    actor_user_id UUID,
    action_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_pk TEXT,
    old_value JSONB,
    new_value JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.StagingCandidateRecord (
    staging_candidate_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    extraction_run_id UUID NOT NULL,
    candidate_external_id TEXT,
    object_type public.dcse_object_type NOT NULL,
    canonical_title TEXT NOT NULL,
    brand_code TEXT,
    entity_code TEXT,
    summary TEXT,
    proposedFields JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS public.staging_relationship_candidates (
    staging_relationship_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    extraction_run_id UUID NOT NULL,
    from_candidate_external_id TEXT NOT NULL,
    to_candidate_external_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.staging_duplicate_candidates (
    staging_duplicate_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    extraction_run_id UUID NOT NULL,
    candidate_external_id TEXT NOT NULL,
    possible_match_external_id TEXT,
    reason TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.registry_records (
    record_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    object_type public.dcse_object_type NOT NULL,
    canonical_title TEXT NOT NULL,
    short_title TEXT,
    slug TEXT NOT NULL,
    brand_code TEXT,
    entity_id UUID,
    visibility public.dcse_visibility DEFAULT INTERNAL NOT NULL,
    confidentiality_level public.dcse_confidentiality DEFAULT MEDIUM NOT NULL,
    status public.dcse_record_status DEFAULT VALID NOT NULL,
    lifecycle_stage public.dcse_lifecycle_stage DEFAULT DRAFT NOT NULL,
    version_label TEXT,
    summary TEXT,
    detailed_description TEXT,
    owner_user_id UUID,
    steward_user_id UUID,
    source_of_truth_flag BOOLEAN DEFAULT false NOT NULL,
    source_count INTEGER DEFAULT 0 NOT NULL,
    primary_source_id UUID,
    review_status public.dcse_review_status DEFAULT DRAFT NOT NULL,
    reusable_flag BOOLEAN DEFAULT false NOT NULL,
    monetizable_flag BOOLEAN DEFAULT false NOT NULL,
    public_safe_flag BOOLEAN DEFAULT false NOT NULL,
    internal_only_flag BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    approved_at TIMESTAMPTZ,
    archived_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.record_tags (
    record_id UUID NOT NULL,
    tag_id UUID NOT NULL,
    PRIMARY KEY (recordId, tagId)
);

CREATE TABLE IF NOT EXISTS public.record_sources (
    record_id UUID NOT NULL,
    source_id UUID NOT NULL,
    source_role TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (recordId, sourceId)
);

CREATE TABLE IF NOT EXISTS public.record_relationships (
    relationship_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    from_record_id UUID NOT NULL,
    to_record_id UUID NOT NULL,
    relationship_type TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.RecordRevision (
    revision_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    record_id UUID NOT NULL,
    revision_number INTEGER NOT NULL,
    changed_by UUID,
    change_reason TEXT,
    payload JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS public.doctrines (
    record_id UUID PRIMARY KEY,
    doctrine_code TEXT,
    doctrine_type TEXT,
    governing_scope TEXT,
    doctrine_rule_text TEXT,
    rationale TEXT,
    enforcement_level TEXT,
    exception_policy TEXT,
    qa_gate_reference TEXT
);

CREATE TABLE IF NOT EXISTS public.personas (
    record_id UUID PRIMARY KEY,
    payload JSONB,
    persona_type TEXT,
    demographic_context TEXT,
    psychographic_traits JSONB DEFAULT "[]" NOT NULL,
    pain_points JSONB DEFAULT "[]" NOT NULL,
    aspirations JSONB DEFAULT "[]" NOT NULL,
    use_cases JSONB DEFAULT "[]" NOT NULL,
    monetization_fit TEXT,
    content_fit TEXT,
    experience_level TEXT
);

CREATE TABLE IF NOT EXISTS public.profiles (
    record_id UUID PRIMARY KEY,
    profile_category TEXT,
    audience_type TEXT,
    voice_summary TEXT,
    tone_rules TEXT,
    prohibited_language TEXT,
    visual_preferences TEXT,
    ux_preferences TEXT,
    activation_context TEXT,
    operational_notes TEXT
);

CREATE TABLE IF NOT EXISTS public.instructions (
    record_id UUID PRIMARY KEY,
    instruction_scope TEXT,
    instruction_level TEXT,
    target_model TEXT,
    prompt_text TEXT,
    constraints_text TEXT,
    negative_rules TEXT,
    usage_examples TEXT,
    supersedes_record_id UUID
);

CREATE TABLE IF NOT EXISTS public.products (
    record_id UUID PRIMARY KEY,
    payload JSONB,
    product_family TEXT,
    product_type TEXT,
    product_format TEXT,
    product_stage TEXT,
    audience TEXT,
    transformation_promise TEXT,
    pricing_model TEXT,
    recurring_flag BOOLEAN,
    delivery_method TEXT,
    dependencies JSONB DEFAULT "[]" NOT NULL,
    launch_priority TEXT,
    storefront_ready_flag BOOLEAN DEFAULT false
);

CREATE TABLE IF NOT EXISTS public.services (
    record_id UUID PRIMARY KEY,
    service_category TEXT,
    delivery_type TEXT,
    target_client TEXT,
    problem_solved TEXT,
    engagement_model TEXT,
    price_structure TEXT,
    recurring_flag BOOLEAN,
    intake_requirements TEXT,
    deliverables TEXT,
    success_metrics TEXT
);

CREATE TABLE IF NOT EXISTS public.operational_assets (
    record_id UUID PRIMARY KEY,
    asset_category TEXT,
    asset_format TEXT,
    file_path TEXT,
    preview_path TEXT,
    storage_location TEXT,
    version_text TEXT,
    inventory_status TEXT
);

CREATE TABLE IF NOT EXISTS public.workflows (
    record_id UUID PRIMARY KEY,
    workflow_type TEXT,
    trigger_text TEXT,
    inputs JSONB DEFAULT "[]" NOT NULL,
    steps JSONB DEFAULT "[]" NOT NULL,
    outputs JSONB DEFAULT "[]" NOT NULL,
    automation_level TEXT,
    tools_used JSONB DEFAULT "[]" NOT NULL,
    failure_points JSONB DEFAULT "[]" NOT NULL,
    qa_checks JSONB DEFAULT "[]" NOT NULL,
    deployment_state TEXT
);

CREATE TABLE IF NOT EXISTS public.app_modules (
    record_id UUID PRIMARY KEY,
    app_type TEXT,
    embed_type TEXT,
    standalone_flag BOOLEAN,
    framework TEXT,
    hosting_target TEXT,
    route_or_embed_location TEXT,
    auth_required BOOLEAN,
    data_dependencies JSONB DEFAULT "[]" NOT NULL,
    api_dependencies JSONB DEFAULT "[]" NOT NULL,
    ux_state TEXT,
    testing_status TEXT,
    release_status TEXT,
    production_url TEXT,
    internal_url TEXT
);

CREATE TABLE IF NOT EXISTS public.business_strategies (
    record_id UUID PRIMARY KEY,
    objective TEXT,
    business_problem TEXT,
    strategic_thesis TEXT,
    expected_roi TEXT,
    operating_constraints TEXT,
    dependencies JSONB DEFAULT "[]" NOT NULL,
    target_date TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.seo_objects (
    record_id UUID PRIMARY KEY,
    page_or_asset_name TEXT,
    target_keyword TEXT,
    keyword_cluster TEXT,
    search_intent TEXT,
    funnel_stage TEXT,
    target_url TEXT,
    title_tag TEXT,
    meta_description TEXT,
    internal_links JSONB DEFAULT "[]" NOT NULL,
    schema_markup_needed TEXT,
    rank_tracking_needed BOOLEAN,
    conversion_goal TEXT
);

CREATE TABLE IF NOT EXISTS public.aeo_objects (
    record_id UUID PRIMARY KEY,
    question_cluster TEXT,
    answer_entity TEXT,
    canonical_answer TEXT,
    concise_answer TEXT,
    long_answer TEXT,
    faq_group TEXT,
    authority_signals TEXT,
    source_references JSONB DEFAULT "[]" NOT NULL,
    refresh_cycle TEXT
);

CREATE TABLE IF NOT EXISTS public.geo_objects (
    record_id UUID PRIMARY KEY,
    generative_topic TEXT,
    entity_alignment TEXT,
    authority_claim TEXT,
    evidence_sources JSONB DEFAULT "[]" NOT NULL,
    retrieval_targets JSONB DEFAULT "[]" NOT NULL,
    model_targets JSONB DEFAULT "[]" NOT NULL,
    citation_targets JSONB DEFAULT "[]" NOT NULL,
    trust_signals TEXT,
    update_frequency TEXT
);

CREATE TABLE IF NOT EXISTS public.content_assets (
    record_id UUID PRIMARY KEY,
    content_type TEXT,
    channel TEXT,
    campaign TEXT,
    audience TEXT,
    content_status TEXT,
    publishing_status TEXT,
    repurpose_targets JSONB DEFAULT "[]" NOT NULL
);

CREATE TABLE IF NOT EXISTS public.knowledge_files (
    record_id UUID PRIMARY KEY,
    file_purpose TEXT,
    upload_target TEXT,
    model_target TEXT,
    source_status TEXT,
    canonical_flag BOOLEAN,
    refresh_needed BOOLEAN
);

CREATE TABLE IF NOT EXISTS public.prompt_assets (
    record_id UUID PRIMARY KEY,
    prompt_type TEXT,
    prompt_role TEXT,
    prompt_body TEXT,
    target_model TEXT,
    target_outcome TEXT,
    tested_flag BOOLEAN,
    performance_notes TEXT
);

CREATE TABLE IF NOT EXISTS public.model_configurations (
    record_id UUID PRIMARY KEY,
    model_name TEXT,
    model_provider TEXT,
    role_assignment TEXT,
    primary_use_case TEXT,
    secondary_use_case TEXT,
    prompt_injection_rules TEXT,
    tone_profile TEXT,
    strengths TEXT,
    weaknesses TEXT,
    routing_rules TEXT,
    active_flag BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS public.UiComponent (
    record_id UUID PRIMARY KEY,
    component_type TEXT,
    design_system_group TEXT,
    reusable_flag BOOLEAN,
    dataContract JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS public.distribution_targets (
    record_id UUID PRIMARY KEY,
    target_name TEXT,
    target_type TEXT,
    output_format TEXT,
    publish_method TEXT,
    approval_required BOOLEAN,
    analytics_target TEXT,
    monetization_relation TEXT,
    target_url TEXT
);

CREATE TABLE IF NOT EXISTS public.creativity_systems (
    record_id UUID PRIMARY KEY,
    creativity_type TEXT,
    creative_direction TEXT,
    narrative_mode TEXT,
    emotional_register TEXT,
    originality_level TEXT,
    humor_style TEXT,
    cinematic_influences TEXT,
    cultural_references TEXT,
    visual_language TEXT,
    audio_language TEXT,
    prohibited_creative_patterns TEXT,
    creative_use_cases TEXT
);

CREATE TABLE IF NOT EXISTS public.voice_tone_systems (
    record_id UUID PRIMARY KEY,
    voice_identity TEXT,
    tone_range TEXT,
    reading_level TEXT,
    sentence_style TEXT,
    pacing_style TEXT,
    rhetorical_style TEXT,
    approved_phrases TEXT,
    banned_phrases TEXT,
    linguistic_rules TEXT,
    punctuation_rules TEXT,
    audience_fit TEXT,
    sample_output_reference TEXT,
    default_cta_style TEXT
);

CREATE TABLE IF NOT EXISTS public.layer_modules (
    record_id UUID PRIMARY KEY,
    layer_type TEXT,
    module_type TEXT,
    architectural_role TEXT,
    content_role TEXT,
    data_role TEXT,
    ui_role TEXT,
    interaction_pattern TEXT,
    placement_context TEXT,
    dependency_map JSONB DEFAULT "[]" NOT NULL,
    trigger_conditions TEXT,
    inputs JSONB DEFAULT "[]" NOT NULL,
    outputs JSONB DEFAULT "[]" NOT NULL,
    embedded_flag BOOLEAN,
    standalone_flag BOOLEAN,
    production_status TEXT
);

CREATE TABLE IF NOT EXISTS public.doctrine_to_entity (
    doctrine_record_id UUID NOT NULL,
    entity_id UUID NOT NULL,
    PRIMARY KEY (doctrineRecordId, entityId)
);

CREATE TABLE IF NOT EXISTS public.doctrine_to_product (
    doctrine_record_id UUID NOT NULL,
    product_record_id UUID NOT NULL,
    PRIMARY KEY (doctrineRecordId, productRecordId)
);

CREATE TABLE IF NOT EXISTS public.doctrine_to_instruction (
    doctrine_record_id UUID NOT NULL,
    instruction_record_id UUID NOT NULL,
    PRIMARY KEY (doctrineRecordId, instructionRecordId)
);

CREATE TABLE IF NOT EXISTS public.profile_to_entity (
    profile_record_id UUID NOT NULL,
    entity_id UUID NOT NULL,
    PRIMARY KEY (profileRecordId, entityId)
);

CREATE TABLE IF NOT EXISTS public.profile_to_persona (
    profile_record_id UUID NOT NULL,
    persona_record_id UUID NOT NULL,
    PRIMARY KEY (profileRecordId, personaRecordId)
);

CREATE TABLE IF NOT EXISTS public.persona_to_product (
    persona_record_id UUID NOT NULL,
    product_record_id UUID NOT NULL,
    PRIMARY KEY (personaRecordId, productRecordId)
);

CREATE TABLE IF NOT EXISTS public.product_to_service (
    product_record_id UUID NOT NULL,
    service_record_id UUID NOT NULL,
    PRIMARY KEY (productRecordId, serviceRecordId)
);

CREATE TABLE IF NOT EXISTS public.product_to_app (
    product_record_id UUID NOT NULL,
    app_record_id UUID NOT NULL,
    PRIMARY KEY (productRecordId, appRecordId)
);

CREATE TABLE IF NOT EXISTS public.app_to_component (
    app_record_id UUID NOT NULL,
    component_record_id UUID NOT NULL,
    PRIMARY KEY (appRecordId, componentRecordId)
);

CREATE TABLE IF NOT EXISTS public.asset_to_workflow (
    asset_record_id UUID NOT NULL,
    workflow_record_id UUID NOT NULL,
    PRIMARY KEY (assetRecordId, workflowRecordId)
);

CREATE TABLE IF NOT EXISTS public.workflow_to_product (
    workflow_record_id UUID NOT NULL,
    product_record_id UUID NOT NULL,
    PRIMARY KEY (workflowRecordId, productRecordId)
);

CREATE TABLE IF NOT EXISTS public.content_to_strategy (
    content_record_id UUID NOT NULL,
    strategy_record_id UUID NOT NULL,
    PRIMARY KEY (contentRecordId, strategyRecordId)
);

CREATE TABLE IF NOT EXISTS public.seo_to_content (
    seo_record_id UUID NOT NULL,
    content_record_id UUID NOT NULL,
    PRIMARY KEY (seoRecordId, contentRecordId)
);

CREATE TABLE IF NOT EXISTS public.aeo_to_content (
    aeo_record_id UUID NOT NULL,
    content_record_id UUID NOT NULL,
    PRIMARY KEY (aeoRecordId, contentRecordId)
);

CREATE TABLE IF NOT EXISTS public.geo_to_content (
    geo_record_id UUID NOT NULL,
    content_record_id UUID NOT NULL,
    PRIMARY KEY (geoRecordId, contentRecordId)
);

CREATE TABLE IF NOT EXISTS public.knowledge_file_to_model (
    knowledge_file_record_id UUID NOT NULL,
    model_configuration_record_id UUID NOT NULL,
    PRIMARY KEY (knowledgeFileRecordId, modelConfigurationRecordId)
);

CREATE TABLE IF NOT EXISTS public.prompt_to_model (
    prompt_record_id UUID NOT NULL,
    model_configuration_record_id UUID NOT NULL,
    PRIMARY KEY (promptRecordId, modelConfigurationRecordId)
);

CREATE TABLE IF NOT EXISTS public.prompt_to_product (
    prompt_record_id UUID NOT NULL,
    product_record_id UUID NOT NULL,
    PRIMARY KEY (promptRecordId, productRecordId)
);

CREATE TABLE IF NOT EXISTS public.creativity_to_entity (
    creativity_record_id UUID NOT NULL,
    entity_id UUID NOT NULL,
    PRIMARY KEY (creativityRecordId, entityId)
);

CREATE TABLE IF NOT EXISTS public.creativity_to_product (
    creativity_record_id UUID NOT NULL,
    product_record_id UUID NOT NULL,
    PRIMARY KEY (creativityRecordId, productRecordId)
);

CREATE TABLE IF NOT EXISTS public.voice_tone_to_entity (
    voice_tone_record_id UUID NOT NULL,
    entity_id UUID NOT NULL,
    PRIMARY KEY (voiceToneRecordId, entityId)
);

CREATE TABLE IF NOT EXISTS public.voice_tone_to_profile (
    voice_tone_record_id UUID NOT NULL,
    profile_record_id UUID NOT NULL,
    PRIMARY KEY (voiceToneRecordId, profileRecordId)
);

CREATE TABLE IF NOT EXISTS public.module_to_app (
    layer_module_record_id UUID NOT NULL,
    app_record_id UUID NOT NULL,
    PRIMARY KEY (layerModuleRecordId, appRecordId)
);

CREATE TABLE IF NOT EXISTS public.module_to_workflow (
    layer_module_record_id UUID NOT NULL,
    workflow_record_id UUID NOT NULL,
    PRIMARY KEY (layerModuleRecordId, workflowRecordId)
);

CREATE TABLE IF NOT EXISTS public.module_to_distribution (
    layer_module_record_id UUID NOT NULL,
    distribution_record_id UUID NOT NULL,
    PRIMARY KEY (layerModuleRecordId, distributionRecordId)
);

CREATE TABLE IF NOT EXISTS public.assets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    payload JSONB
);

CREATE TABLE IF NOT EXISTS public.content_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    payload JSONB
);

CREATE TABLE IF NOT EXISTS public.raw_records (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    payload JSONB
);

CREATE TABLE IF NOT EXISTS public.sources (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    payload JSONB
);

CREATE TABLE IF NOT EXISTS public.cp_lanes (
    lane_code TEXT PRIMARY KEY,
    lane_name TEXT NOT NULL,
    description TEXT,
    restricted BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.cp_entities (
    entity_code TEXT PRIMARY KEY,
    entity_name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.pm_projects (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_code TEXT NOT NULL,
    project_name TEXT NOT NULL,
    entity_code TEXT,
    primary_lane TEXT,
    classification TEXT DEFAULT "CONFIDENTIAL" NOT NULL,
    status TEXT DEFAULT "active" NOT NULL,
    priority INTEGER DEFAULT 3 NOT NULL,
    purpose TEXT,
    scope TEXT,
    owner_label TEXT DEFAULT "DCS" NOT NULL,
    ps_lock_flag BOOLEAN DEFAULT false NOT NULL,
    secret_risk_flag BOOLEAN DEFAULT false NOT NULL,
    mixed_lane_flag BOOLEAN DEFAULT false NOT NULL,
    start_date TIMESTAMPTZ,
    target_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.pm_workstreams (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID NOT NULL,
    workstream_code TEXT NOT NULL,
    workstream_name TEXT NOT NULL,
    lane_code TEXT,
    status TEXT DEFAULT "active" NOT NULL,
    priority INTEGER DEFAULT 3 NOT NULL,
    objective TEXT,
    exit_criteria TEXT,
    blocked_flag BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.pm_tasks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID NOT NULL,
    workstream_id UUID,
    task_code TEXT NOT NULL,
    task_title TEXT NOT NULL,
    lane_code TEXT,
    entity_code TEXT,
    status TEXT DEFAULT "not_started" NOT NULL,
    priority INTEGER DEFAULT 3 NOT NULL,
    assigned_to TEXT,
    model_role TEXT,
    task_type TEXT DEFAULT "execution" NOT NULL,
    description TEXT,
    due_date TIMESTAMPTZ,
    ps_lock_flag BOOLEAN DEFAULT false NOT NULL,
    secret_risk_flag BOOLEAN DEFAULT false NOT NULL,
    mixed_lane_flag BOOLEAN DEFAULT false NOT NULL,
    stop_gate_flag BOOLEAN DEFAULT false NOT NULL,
    validation_required BOOLEAN DEFAULT false NOT NULL,
    opus_validation_required BOOLEAN DEFAULT false NOT NULL,
    completion_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.pm_closeouts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID,
    task_id UUID,
    closeout_code TEXT,
    closeout_title TEXT NOT NULL,
    lane_code TEXT,
    status TEXT DEFAULT "draft" NOT NULL,
    verified TEXT,
    likely TEXT,
    unknown TEXT,
    exceptions TEXT,
    blockers TEXT,
    next_actions TEXT,
    run2_status TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.pm_decisions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID,
    decision_code TEXT,
    decision_title TEXT NOT NULL,
    decision_status TEXT DEFAULT "proposed" NOT NULL,
    lane_code TEXT,
    decision_text TEXT NOT NULL,
    rationale TEXT,
    authority_label TEXT DEFAULT "DCS" NOT NULL,
    decided_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.pm_blockers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID,
    task_id UUID,
    blocker_code TEXT,
    blocker_title TEXT NOT NULL,
    lane_code TEXT,
    blocker_status TEXT DEFAULT "open" NOT NULL,
    blocker_description TEXT,
    unblock_condition TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    resolved_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.pm_risks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID,
    task_id UUID,
    risk_code TEXT,
    risk_title TEXT NOT NULL,
    lane_code TEXT,
    severity TEXT DEFAULT "medium" NOT NULL,
    probability TEXT DEFAULT "medium" NOT NULL,
    risk_status TEXT DEFAULT "open" NOT NULL,
    risk_description TEXT,
    mitigation TEXT,
    owner_label TEXT DEFAULT "DCS",
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.pm_artifacts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID,
    task_id UUID,
    artifact_code TEXT,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    lane_code TEXT,
    local_path TEXT,
    source_path TEXT,
    hash_sha256 TEXT,
    version_label TEXT,
    status TEXT DEFAULT "draft" NOT NULL,
    ps_lock_flag BOOLEAN DEFAULT false NOT NULL,
    secret_risk_flag BOOLEAN DEFAULT false NOT NULL,
    mixed_lane_flag BOOLEAN DEFAULT false NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    payload JSONB
);

CREATE TABLE IF NOT EXISTS public.pm_model_handoffs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID,
    task_id UUID,
    from_model TEXT,
    to_model TEXT NOT NULL,
    handoff_type TEXT NOT NULL,
    lane_code TEXT,
    prompt_path TEXT,
    handoff_summary TEXT,
    validation_required BOOLEAN DEFAULT false NOT NULL,
    status TEXT DEFAULT "pending" NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.pm_activity_log (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id UUID,
    task_id UUID,
    event_type TEXT NOT NULL,
    event_title TEXT NOT NULL,
    lane_code TEXT,
    event_detail TEXT,
    created_by_label TEXT DEFAULT "DCS",
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.gotime_intake_quarantine (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    source_type VARCHAR(50) NOT NULL,
    raw_payload JSONB NOT NULL,
    scan_status VARCHAR(50) DEFAULT "PENDING" NOT NULL,
    ps_leakage_flag BOOLEAN DEFAULT false NOT NULL,
    quarantine_reason TEXT,
    promoted BOOLEAN DEFAULT false NOT NULL,
    promoted_to_project_id UUID,
    promoted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 5. COMMAND POST & AGENT RUNTIME TABLES (dcse_cp / v7_worker)

CREATE TABLE IF NOT EXISTS dcse_cp.agent_registry (
    agent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_key TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL,
    provider TEXT NOT NULL,
    status TEXT DEFAULT 'active' NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS dcse_cp.agent_tasks (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_key TEXT UNIQUE NOT NULL,
    assigned_agent_key TEXT REFERENCES dcse_cp.agent_registry(agent_key),
    task_status TEXT DEFAULT 'queued' NOT NULL,
    priority INTEGER DEFAULT 100 NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS dcse_cp.agent_task_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_key TEXT REFERENCES dcse_cp.agent_tasks(task_key) ON DELETE CASCADE,
    agent_key TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS v7_worker.agent_identity (
    worker_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_key TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    enrolled_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS v7_worker.task_claim (
    claim_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_key TEXT NOT NULL,
    worker_id UUID REFERENCES v7_worker.agent_identity(worker_id),
    lease_expires_at TIMESTAMPTZ NOT NULL,
    claim_status TEXT DEFAULT 'claimed' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS v7_worker.heartbeat (
    heartbeat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_key TEXT NOT NULL,
    host_name TEXT NOT NULL,
    status TEXT NOT NULL,
    telemetry JSONB DEFAULT '{}'::jsonb,
    recorded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS v7_worker.result_submission (
    submission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_key TEXT NOT NULL,
    agent_key TEXT NOT NULL,
    result_payload JSONB NOT NULL,
    submitted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS v7_worker.bridge_receipt (
    receipt_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id TEXT UNIQUE NOT NULL,
    source_lane TEXT NOT NULL,
    target_lane TEXT NOT NULL,
    evidence_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS v7_worker.cost_ledger (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_key TEXT NOT NULL,
    model_name TEXT NOT NULL,
    input_tokens INTEGER DEFAULT 0 NOT NULL,
    output_tokens INTEGER DEFAULT 0 NOT NULL,
    cost_usd NUMERIC(10, 6) DEFAULT 0.000000 NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS v7_worker.stop_gate (
    gate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gate_name TEXT UNIQUE NOT NULL,
    is_tripped BOOLEAN DEFAULT false NOT NULL,
    reason TEXT,
    tripped_by TEXT,
    tripped_at TIMESTAMPTZ
);

-- ============================================================================
-- END OF CANONICAL DDL BASELINE
-- ============================================================================
