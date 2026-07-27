# Skill Architecture — DCSE V7 Phase C

**Atomic Skills** — Single capability, tested in isolation, composable
```json
{
  "skill_id": "SKILL-FILE-READ-001",
  "type": "atomic",
  "lane": "SC",
  "capability": "read_files",
  "requires": ["filesystem_access"],
  "provides": ["file_content"],
  "version": "1.0"
}
```

**Composite Skills** — Combine atomic skills into workflows
```json
{
  "skill_id": "SKILL-CODE-REVIEW-001",
  "type": "composite",
  "atomic_skills": ["SKILL-FILE-READ-001", "SKILL-GREP-SEARCH-001", "SKILL-LINT-CHECK-001"],
  "lane": "SC",
  "version": "1.0"
}
```

**Lane Skills** — Authorized for specific authorization lanes
- `SC`: Software Construction (code, migrations, builders)
- `DCSE`: Decision/Governance (rules, workflows, acceptance)
- `SYSTEM`: System Architecture (core infrastructure)
- `RAG`: Knowledge/Research (documentation, patterns)
- `DDNA`: Data/Analytics (metrics, reporting)

**Runtime Skill Loading** — Dynamic resolution at execution time
1. Worker requests skills for task
2. Dispatcher loads from skill registry
3. Verify worker authorization for lane
4. Inject into execution context
5. Worker calls skills via SDK

**Versioning & Promotion**
```
Draft → Tested → Stable → Promoted → Deprecated → Archived
```

---

## Success Criteria

✅ Atomic skill registry with 50+ base skills
✅ Composite skill templates (code review, migration, testing, deployment)
✅ Lane-based access control (SC, DCSE, SYSTEM, RAG, DDNA)
✅ Runtime skill loading mechanism
✅ Versioning and promotion workflow
✅ Inheritance model (child skills extend parent)
✅ Skill retirement protocol

**Next:** Workflow Engine (Phase D)
