# ESCD CONNECTOR AND SOURCE ROUTING MATRIX

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Routing principle

Use the authoritative/source-native system for reads and writes whenever available. ESCD may normalize and link state but must not silently replace source authority.

| Source / System | Primary ESCD Use | Read | Draft/Prepare | Write/Execute | Authority Notes |
|---|---|---:|---:|---:|---|
| GitHub | governance, code, issues, PRs, evidence | YES | YES | approval/rule bounded | Current repo authority when verified |
| Supabase / Command Post | operational state, registries, jobs, evidence | YES | YES | server-side bounded | RLS/least privilege; secrets server-side |
| Dedicated DDNA | governed knowledge/provenance | YES | candidate contribution | governed only | No self-promotion by ESCD |
| Tribunal | audit/evidence/receipts | YES | prepare receipts | governed write path | Evidence source, not authority merely by existence |
| Gmail | communications, recruiter/client follow-up | YES | YES | APPROVAL by default | External send consequential |
| Google Calendar | commitments, meetings, deadlines | YES | event proposal | APPROVAL by default | Calendar write changes commitments |
| Google Contacts | identity/recipient resolution | YES | n/a | limited approved update later | Resolve recipients before send |
| Google Drive | files, docs, artifacts | YES | create/edit governed work product | bounded/approval by consequence | Respect source ownership/version |
| Web/Public sources | research/current facts | YES | summarize/cite | no external mutation | Freshness/evidence required |
| Local runtime/Codex | coding/testing/build operations | inspect when available | YES | bounded workspace execution | No secret exposure; no prod without approval |
| ESCD state store | executive/task/job/approval/watch state | YES | YES | YES within policy | Operational source of truth for ESCD-native state |

## Source precedence

For conflicting facts:

1. operative authority/source-native current record
2. verified live operational source
3. versioned evidence/receipt
4. linked external source
5. ESCD derived state
6. model inference

Material contradictions remain visible until resolved.

## Connector execution rules

- Reads may be automatic when authorized and lane-safe.
- Draft creation may be automatic when non-consequential.
- External sends, calendar commitment changes, public publishing, production deploys, spending, destructive operations, and credential changes require explicit approval unless separately delegated.
- Connector failure must not be converted into assumed state.
- Every write records source, actor, timestamp, target, result, and evidence/receipt proportional to consequence.

## Deduplication

Cross-source items must link by stable external IDs, normalized subject/entity/date context, and provenance. ESCD links duplicates rather than deleting source records.

## PS/protected boundaries

Protected material must not be routed into public/recruiting/SC/SS/TI channels without explicit authorization. Connector routing must preserve lane classification before enrichment or model dispatch.

## Acceptance

Tests must cover source precedence, connector unavailable, duplicate detection, wrong-recipient prevention, unauthorized write, stale source, contradictory source, missing evidence, and provenance preservation.