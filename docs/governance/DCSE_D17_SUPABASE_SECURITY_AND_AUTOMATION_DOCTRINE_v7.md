# RECLASSIFIED: Historical D17 Mislabel — Not Canonical D17

**Status:** SUPERSEDED / NONCANONICAL COMPATIBILITY NOTICE  
**Reclassified:** 2026-08-07  
**Authority basis:** DCS v7.2 Master Profile source reconciliation  

This repository path previously contained a July 29, 2026 document titled **“DCSE D17 Supabase Security and Automation Doctrine v7.”** That title conflicted with the promoted and canonical D17 identity.

## Canonical D17

The governing D17 is:

- **Title:** D17 — DART Universal Assurance Methodology
- **Canonical source:** `governance/v7.1/source/doctrines/D17_DART_Universal_Methodology.md`
- **Promoted Supabase directive key:** `D17`
- **Promoted source checksum:** `568a8f2b3b2f8a960ebcf30dc94679dbb66f94a51aa2a51a0a0f86dc1da633f1`
- **Verified asset-registry SHA-256:** `12186A59C0AEE0F83E08DBAB6E78ECFDC868E2078DE4835544164EDADBDE2392`

D17 is the universal DCSE DART assurance methodology and is not a Supabase/database-security doctrine.

## Database / Supabase Governance

The former content at this path governed Supabase security, RLS, migrations, database functions, automation gates, rollback, and related DBA controls. Those subjects are governed by **D15 — Database Administration** and any explicitly authorized D15 implementation supplements.

The former content remains recoverable through Git history for provenance. It SHALL NOT be loaded, cited, compiled, or treated as D17 authority by any runtime, reviewer, RAG process, context compiler, doctrine registry, or Master Profile build.

## Machine Rule

```json
{
  "path": "docs/governance/DCSE_D17_SUPABASE_SECURITY_AND_AUTOMATION_DOCTRINE_v7.md",
  "classification": "HISTORICAL_MISLABEL_TOMBSTONE",
  "canonical_d17": "governance/v7.1/source/doctrines/D17_DART_Universal_Methodology.md",
  "database_governance": "D15",
  "load_as_doctrine": false,
  "compile_as_d17": false,
  "stop_gate_if_treated_as_d17": true
}
```

**Structure Precedes Scale.**
