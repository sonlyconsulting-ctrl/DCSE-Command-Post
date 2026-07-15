# Role Access Matrix
**Version:** 1.0
**Date:** 2026-07-15

---

## Role Hierarchy

```
DCS Authority
  └── DCSE Administrator
        └── SC Product Administrator
              ├── Persona Owner
              │     └── Family Administrator
              │           ├── Parent
              │           │     ├── Adult Family Member
              │           │     └── Child Profile
              │           └── Product Reviewer
              ├── Asset Reviewer
              ├── Read Only
              └── Agent Service Account
```

---

## Permissions by Role

| Action | DCS | DCSE Admin | SC Product Admin | Persona Owner | Family Admin | Parent | Child | Reviewer | Read Only | Agent |
|--------|-----|------------|-----------------|---------------|--------------|--------|-------|----------|-----------|-------|
| Promote persona to approved/active | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| Promote persona to review | YES | YES | NO | YES | NO | NO | NO | NO | NO | NO |
| Register new persona | YES | YES | YES | NO | NO | NO | NO | NO | NO | NO |
| Change privacy_class | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| Override identity_mask | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| Approve asset | YES | YES | NO | NO | NO | NO | NO | NO | NO | NO |
| Deploy asset | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| Register asset | YES | YES | YES | YES | NO | NO | NO | NO | NO | NO |
| View protected personas | YES | YES | NO | NO | NO | NO | NO | NO | NO | NO |
| View classified assets | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| View family assets | YES | YES | YES | YES | YES | YES | NO | NO | NO | NO |
| View child content | YES | YES | YES | YES | YES | YES | YES (age-gated) | NO | NO | NO |
| Push to main branch | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| Merge PR | YES | NO | NO | NO | NO | NO | NO | NO | NO | NO |
| Approve own output | NO | NO | NO | NO | NO | NO | NO | NO | NO | NO |

---

## Current RLS Enforcement (Supabase)

| Table | Anon | Authenticated | Service Role |
|-------|------|---------------|--------------|
| personas | NONE | SELECT (release_posture filter) | ALL |
| assets | NONE | SELECT | ALL |
| persona_modules | NONE | SELECT (persona filter) | ALL |
| products | SELECT | SELECT | ALL |

**Gap:** No row-level separation by dcs_lane or privacy_class. Migration 001/002 adds these columns; RLS policies need subsequent update by DCS authority.

---

## PS Firewall Integration

Any action that would surface PS (personal/sensitive) content in:
- A dispatch packet
- A GitHub artifact
- A public-facing asset
- A child-accessible product

...is BLOCKED regardless of role.

PS content includes: employment/career material, legal claims, personal financial data, health information, family location data.
