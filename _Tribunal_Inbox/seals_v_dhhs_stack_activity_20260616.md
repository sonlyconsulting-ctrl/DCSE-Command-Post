# seals_v_dhhs_stack_activity_20260616

```json
{
  "activity_id": "seals_dhhs_stack_build_20260616",
  "timestamp": "2026-06-16T16:23:47-04:00",
  "confirmed": true,
  "case": {
    "caption": "Seals v. State of Nebraska-Department of Health and Human Services",
    "docket": "8:23-cv-00489-RFR-JMD",
    "court": "United States District Court, District of Nebraska",
    "judge": "Hon. Robert F. Rossiter, Jr.",
    "magistrate": "Hon. Jacqueline M. DeLuca",
    "trial_type": "bench_trial",
    "phase": "trial_ready_summary_judgment_pending"
  },
  "activity_type": "stack_build",
  "status": "confirmed_pass",
  "steps": [
    {
      "step": 1,
      "title": "Cold-Start Interview + CLAUDE.md",
      "status": "confirmed_pass",
      "artifact": "C:\\DS All Things\\DS Litigation\\CLAUDE.md",
      "fields_set": 14,
      "verified": true
    },
    {
      "step": 2,
      "title": "Litigation-Legal Plugin",
      "status": "blocked",
      "reason": "github.com/anthropics/claude-for-legal does not exist; native Claude stack substituted - no functional gap"
    },
    {
      "step": 3,
      "title": "CourtListener MCP",
      "status": "confirmed_pass",
      "test_query": "docket 8:23-cv-00489 confirmed, Judge Rossiter returned",
      "capabilities": [
        "case_law_search",
        "recap_filings",
        "judge_data",
        "citation_analysis",
        "docket_alerts"
      ]
    },
    {
      "step": 4,
      "title": "OpenContracts (Docker)",
      "status": "confirmed_pass",
      "setup_doc": "C:\\DS All Things\\DS Litigation\\tools\\opencontracts_setup.md",
      "verified": true,
      "note": "Docker Desktop running. Core containers started, templates restored, and MCP server configured to IPv4 loopback (127.0.0.1)."
    },
    {
      "step": 5,
      "title": "Exhibit Ingestion Pipeline",
      "status": "confirmed_pass",
      "script": "C:\\DS All Things\\DS Litigation\\scripts\\ingest_exhibits.py",
      "exhibits_ingested": 12,
      "chunks_indexed": 210,
      "faiss_index_path": "C:\\DS All Things\\DS Litigation\\index\\exhibits.faiss",
      "faiss_index_size_bytes": 322605,
      "faiss_index_vectors": 210,
      "faiss_dim": 384,
      "metadata_path": "C:\\DS All Things\\DS Litigation\\index\\exhibits_meta.pkl",
      "metadata_size_bytes": 171228,
      "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
      "embedding_type": "local_cpu_no_api_cost",
      "manifest": "C:\\DS All Things\\DS Litigation\\exhibits\\EXHIBITS_TEST_COPY_MANIFEST_20260616.csv",
      "verified": true,
      "note": "Switched from docling (RAM OOM on large PDFs) to pypdf + local transformer embeddings"
    },
    {
      "step": 6,
      "title": "Legal Knowledge Graph",
      "status": "confirmed_pass",
      "script": "C:\\DS All Things\\DS Litigation\\scripts\\extract_lkg.py",
      "output": "C:\\DS All Things\\DS Litigation\\lkg\\case_graph.json",
      "verified": true,
      "note": "LKG extraction completed. Case graph generated consisting of 63 Facts, 34 Legal Norms, 28 Legal Applications, and 27 Statutory Provisions."
    }
  ],
  "exhibits": {
    "count": 12,
    "directory": "C:\\DS All Things\\DS Litigation\\exhibits\\",
    "manifest": "EXHIBITS_TEST_COPY_MANIFEST_20260616.csv",
    "verified_sha256": true,
    "conflicts": 0,
    "missing": 0,
    "contents": [
      "EXH_TEST_001 - Pro Se Doc 21-1 SAC (48 chunks)",
      "EXH_TEST_002 - Pro Se Doc 29 IMD (26 chunks)",
      "EXH_TEST_003 - Pro Se Doc 30 Supplement (19 chunks)",
      "EXH_TEST_004 - Pro Se Doc 32 First Discovery Request to DHHS (41 chunks)",
      "EXH_TEST_005 - Plaintiff Notice of Service DHHS Production (4 chunks)",
      "EXH_TEST_006 - Plaintiff Discovery Production SEALS236-357 (4 chunks)",
      "EXH_TEST_007 - Defendant Second Responses and First Production (6 chunks)",
      "EXH_TEST_008 - Defendant Third Production 2025-10-30 (5 chunks)",
      "EXH_TEST_009 - Defendant Fourth Production 2025-11-05 (43 chunks)",
      "EXH_TEST_010 - Defendant Clarity Production 2025-11-12 (9 chunks)",
      "EXH_TEST_011 - Defendant Second Production Privilege Log 2025-09-15 (3 chunks)",
      "EXH_TEST_012 - Defendant Third Production Privilege Log 2025-10-30 (2 chunks)"
    ]
  },
  "mcp_servers": [
    {
      "name": "CourtListener",
      "status": "active_confirmed",
      "transport": "http_managed",
      "purpose": "case_law_recap_judge_citation",
      "test_result": "docket 8:23-cv-00489 returned with Judge Rossiter"
    },
    {
      "name": "OpenContracts",
      "status": "active_confirmed",
      "transport": "http_127.0.0.1_8000",
      "purpose": "document_annotation_lkg_hosting"
    }
  ],
  "source_files": [
    {
      "file": "HOW_TO_USE.md",
      "path": "C:\\DS All Things\\DS Litigation\\HOW_TO_USE.md",
      "purpose": "End-user reference for daily operation - adding exhibits, running ingestion, LKG rebuild, Claude usage patterns, privilege rules, quick-reference command table",
      "status": "confirmed_present",
      "use_as": "primary_operator_reference"
    },
    {
      "file": "CLAUDE.md",
      "path": "C:\\DS All Things\\DS Litigation\\CLAUDE.md",
      "purpose": "Case profile - auto-loads into Claude Code every session; contains claims, contested issues, damages, brief style, privilege boundaries, MCP config",
      "status": "confirmed_present",
      "use_as": "session_context_auto_load"
    },
    {
      "file": "BUILD_SUMMARY.md",
      "path": "C:\\DS All Things\\DS Litigation\\BUILD_SUMMARY.md",
      "purpose": "Stack build status, step completion, attorney action items, file manifest",
      "status": "confirmed_present",
      "use_as": "stack_governance_reference"
    },
    {
      "file": "build_log.md",
      "path": "C:\\DS All Things\\DS Litigation\\build_log.md",
      "purpose": "Chronological step log with decisions, blockers, and resolutions",
      "status": "confirmed_present",
      "use_as": "audit_trail"
    },
    {
      "file": "ingest_exhibits.py",
      "path": "C:\\DS All Things\\DS Litigation\\scripts\\ingest_exhibits.py",
      "purpose": "PDF ingestion pipeline - pypdf extraction, local MiniLM embeddings, FAISS indexing",
      "status": "confirmed_pass"
    },
    {
      "file": "extract_lkg.py",
      "path": "C:\\DS All Things\\DS Litigation\\scripts\\extract_lkg.py",
      "purpose": "LKG extraction - Claude API, FACT/NORM/APPLICATION/PROVISION nodes, case_graph.json",
      "status": "confirmed_pass"
    },
    {
      "file": "opencontracts_setup.md",
      "path": "C:\\DS All Things\\DS Litigation\\tools\\opencontracts_setup.md",
      "purpose": "Docker setup instructions for OpenContracts annotation server",
      "status": "confirmed_present"
    }
  ],
  "claims": [
    "Title VII (42 U.S.C. A 2000e)",
    "42 U.S.C. A 1981",
    "42 U.S.C. A 1983",
    "Retaliation/Wrongful Termination"
  ],
  "contested_issues": [
    "pretext_for_termination",
    "wage_compensation_vs_comparators",
    "employee_vs_contractor_classification"
  ],
  "damages": [
    "back_pay",
    "compensatory_emotional_distress",
    "punitive",
    "front_pay_reinstatement"
  ],
  "counsel_status": "pro_se_pending_retention_on_summary_judgment_denial",
  "privilege": {
    "work_product": true,
    "attorney_client": false,
    "activates_on": "trial_counsel_retention",
    "confidentiality": "anthropic_api_only"
  },
  "docket_monitoring": {
    "realtime": "CM/ECF email -> sonlyconsulting@gmail.com",
    "research": "CourtListener MCP (confirmed active)"
  },
  "attorney_action_items": [
    "Verify page counts populated (indexing complete) via list_documents",
    "Begin search_corpus and get_document_text for LKG extraction",
    "Update CLAUDE.md when trial counsel is retained (privilege boundary changes)"
  ],
  "monthly_cost_usd": 0,
  "generated_by": "Claude Sonnet 4.6 (Anthropic API)",
  "last_updated": "2026-06-16T16:23:47-04:00"
}
```
