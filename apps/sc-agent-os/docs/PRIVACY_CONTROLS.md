# Privacy and Child-Safety Controls
**Version:** 1.0
**Date:** 2026-07-15

---

## Core Privacy Rules

1. **No family or minor content in public GitHub repositories.** Child profiles, parental control data, and family media must not appear in any public-facing code, config, or artifact.

2. **No protected family media in DDNA or RAG.** Family photos, videos, or personal communications may not be submitted to DDNA harvest or indexed as RAG sources.

3. **Identity masking for SNTY and ASP.** These personas require `identity_mask=true`. No personal names, photos, biographical details, or identifiable attributes may appear in any artifact referencing these personas. The SC Agent OS UI must redact all identifying fields when identity_mask=true.

4. **Liberty Mutual reference policy.** Any reference to Liberty Mutual must be treated as factual career context only — not as company endorsement, partnership, or internal access. This information must not appear in SC lane materials, product copy, or public assets.

5. **No public deployment without separate authorization.** Products targeting family personas or containing family content require explicit DCS authorization before any public deployment.

---

## Child-Safety Implementation

### Database Layer
- `child_safe=true` on personas and assets marks content as child-appropriate
- `family_product=true` on personas indicates the persona targets a family context
- Child Profile role has access only to content where `child_safe=true`

### UI Layer (SC Agent OS)
- DDNA Harvest: rejects content if family/child markers detected
- RAG Sources: `protected` privacy_class sources blocked from indexing
- Agent Chat: PS Firewall active in all sessions

### Agent Limits
Agents may NOT:
- Publish child content
- Change privacy_class (could expose protected content)
- Make a product public (parental control bypass)
- Override parental control settings

---

## PS Firewall Rules

| Content Category | Status |
|-----------------|--------|
| PS content in dispatch packets | BLOCKED |
| Employment/career material in SC lane | BLOCKED |
| Pricing in public-facing copy | BLOCKED |
| External brand mentions | BLOCKED |
| Superlatives without evidence | BLOCKED |
| Legal claims | BLOCKED |
| Personal financial data | BLOCKED |
| Family location data | BLOCKED |
| Health information | BLOCKED |
| Identity of masked personas | BLOCKED |

---

## Data Classification Guide

| Class | Examples | Storage | Sharing |
|-------|----------|---------|---------|
| public | SC LP copy, governance docs | GitHub, Vercel | Anyone |
| internal | Agent configs, operational docs | Supabase, GitHub | Authenticated ops |
| family | Family product content | Supabase (RLS) | Family roles only |
| protected | SNTY/ASP persona data | Supabase (service_role) | DCS Authority only |
| classified | Authority governance decisions | Supabase (service_role) | DCS Authority only |
