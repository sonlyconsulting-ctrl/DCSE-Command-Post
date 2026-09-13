# ESCD Phase 1 Requirement-to-Test Traceability Matrix

**Task:** ESCD-GOV-20260913-001  
**Lifecycle:** CANDIDATE until canonical Production acceptance completes.

| Requirement | Implementation surface | Automated evidence | Hosted/DCS acceptance |
|---|---|---|---|
| Auth configuration present | Vercel Production + strict validator | production build gate | login |
| Malformed JSON returns 400 | apps/escd/api/mvp.py | test_mvp_http_contract.py | API smoke |
| Tasks/Ideas | /api/mvp/items + UI | pytest contract suite | CRUD smoke |
| Assets | registry + /api/mvp/assets | pytest suite | CRUD smoke |
| DDNA uses dcse_cp | mvp_data.py | pytest + strict validator | hosted DDNA load/search |
| DDNA notes preserved on attachment | finalize/delete helpers | test_mvp_phase1_acceptance.py | attachment smoke |
| Knowledge tab | web app | Playwright | visible hosted tab |
| 24 Knowledge records | canonical registry | pytest + Playwright stub contract | hosted count=24 |
| Private attachment upload | signed upload URL + direct browser PUT | pytest signed-upload contract + Playwright controller syntax | real Storage round-trip |
| Private attachment download | signed download URL | pytest/helper contract | user can open after reload |
| Attachment deletion | DELETE /attachments + metadata cleanup | pytest DDNA deletion regression | Storage + metadata removal |
| Mobile | responsive navigation | Playwright mobile viewport | DCS field test |
| Provider identity | ESCD runtime kernel | provider tests | DCS role question |
| Canonical source | PR to main | GitHub status checks | release SHA recorded |
| Production source parity | Vercel deployment metadata | post-deploy audit | production SHA == canonical release SHA |
