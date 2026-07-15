# Governance Gates
**Version:** 1.0
**Date:** 2026-07-15

---

## Gate Definitions

### Gate 0 — Registration
Persona or asset is formally registered in Supabase with required fields.
- **Who can open:** DCSE Admin, SC Product Admin, Persona Owner
- **Who must close:** DCSE Admin

### Gate 1 — Review
Artifact submitted for DCS review. All required fields complete.
- **Who can open:** Any contributor (creates PR in Tribunal Relay)
- **Who must close:** DCS Authority (approves PR)

### Gate 2 — Approval
DCS Authority explicitly approves. Status advances to approved.
- **Who can open:** N/A (automatic from Gate 1)
- **Who must close:** DCS Authority only. Agents blocked.

### Gate 3 — Deployment
Asset deployed to production. Tribunal PR merged.
- **Who can open:** N/A (automatic from Gate 2)
- **Who must close:** DCS Authority only.

### Gate 4 — Archival / Supersession
Terminal state. Asset replaced or retired.
- **Who can open:** DCS Authority
- **Who must close:** N/A

---

## Currently Blocked Actions

| Action | Reason | Unblock Condition |
|--------|--------|-------------------|
| Apply Supabase migrations 001-003 | Requires DCS authorization | DCS explicit approval |
| Merge PR #5 (Tribunal Relay) | Requires DCS merge authorization | DCS merge command |
| Drop TRIB-20260708 dispatch packet | Requires DCS execution | DCS manual drop |
| Deploy SC LP to production | SC brand palette not confirmed | DCS palette confirmation + auth |
| Promote any persona to active | Agent limit | DCS Authority action |
| Approve any asset | Agent limit | DCS Authority action |
| Vercel deploy of SC Agent OS v1.3 | File size vs token limit (technical) | GitHub-Vercel integration OR local deploy |
| Any public deployment of family content | Privacy directive | Separate DCS authorization |

---

## Tribunal Process

1. Agent builds artifact on feature branch
2. PR opened in `dcse-tribunal-relay` repo
3. DCS reviews via GitHub PR interface
4. DCS merges = approval
5. Agent updates Supabase (via service role) after merge confirmed
6. Dispatch packet dropped to `_Tribunal_Inbox` UNC path

---

## Voice Rule (D08 v6.9.1)

All SC lane artifacts must comply: "Lead constructively, no dominating contrast."

Prohibited patterns:
- em-dashes (PROHIBITED in all rendered copy)
- Dashes of any kind in rendered copy
- Superlatives without evidence
- Dominating contrast framing ("the only," "never before")

---

## Agent Limits Summary

An agent may NOT:
1. Approve its own output
2. Promote a persona
3. Promote an asset
4. Publish child content
5. Change privacy classification
6. Make a product public
7. Override parental control
8. Bypass DCS authority
