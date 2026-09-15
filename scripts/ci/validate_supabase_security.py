#!/usr/bin/env python3
"""Conservative anti-drift checks for changed Supabase SQL migrations."""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

EXPOSED = r"(?:public|api|ps_learner)"
CLIENT = r"(?:public|anon|authenticated)"

# Immutable historical-applied migration evidence allowlist
# Keyed by: path + exact SHA-256 + live migration ID + project + evidence ref.
# Exact hash match may bypass current-migration lint only for known already-applied historical migrations.
# Any byte change invalidates exemption.
# All new/current migrations remain fully linted.
HISTORICAL_APPLIED_MIGRATIONS: dict[str, dict[str, str]] = {
    "supabase/migrations/20260914034207_escd_orchestration_exchange_v1.sql": {
        "sha256": "ac9b31fcc130e03e9c043d917e463b561b402196ccb61c96fb8a134f1506527c",
        "live_migration_id": "20260914034207",
        "project": "nevgdyfpxdaloacuutal",
        "evidence_ref": "evidence://supabase/migration/applied/20260914034207",
        "status": "APPLIED_HISTORICAL",
    },
    "supabase/migrations/20260914055827_escd_subject_classification_memory_v1.sql": {
        "sha256": "d42dc9b25e254e2435acfed9fbdb087c86463e89c7096db6223f7f01682ca714",
        "live_migration_id": "20260914055827",
        "project": "nevgdyfpxdaloacuutal",
        "evidence_ref": "evidence://supabase/migration/applied/20260914055827",
        "status": "APPLIED_HISTORICAL",
    },
    "supabase/migrations/20260914060048_escd_orchestration_durable_controls_v1.sql": {
        "sha256": "17714c18b15997bd69acd01db755ea578f339ce2f1063d35001689daf9d66d1e",
        "live_migration_id": "20260914060048",
        "project": "nevgdyfpxdaloacuutal",
        "evidence_ref": "evidence://supabase/migration/applied/20260914060048",
        "status": "APPLIED_HISTORICAL",
    },
    "supabase/migrations/20260914060725_escd_worker_lease_recovery_v1.sql": {
        "sha256": "54965bf3f1014cfab1417f8c457c9443fc5098f2e581a6990de17311d2f2052f",
        "live_migration_id": "20260914060725",
        "project": "nevgdyfpxdaloacuutal",
        "evidence_ref": "evidence://supabase/migration/applied/20260914060725",
        "status": "APPLIED_HISTORICAL",
    },
    "supabase/migrations/20260914195631_escd_provider_anthropic_registry_v1.sql": {
        "sha256": "aa2f821e711cb66df6c96b62bade69c6fa77334e02b949461d1993918a8d7f51",
        "live_migration_id": "20260914195631",
        "project": "nevgdyfpxdaloacuutal",
        "evidence_ref": "evidence://supabase/migration/applied/20260914195631",
        "status": "APPLIED_HISTORICAL",
    },
}


def normalize_migration_key(path: pathlib.Path) -> str:
    posix_path = path.as_posix()
    posix_path = re.sub(r"^\./", "", posix_path)
    if "supabase/migrations/" in posix_path:
        return "supabase/migrations/" + posix_path.split("supabase/migrations/", 1)[1]
    return posix_path


def check_historical_exemption(path: pathlib.Path) -> tuple[bool, str]:
    key = normalize_migration_key(path)
    record = HISTORICAL_APPLIED_MIGRATIONS.get(key)
    if not record:
        return False, "not on historical allowlist"
    raw_bytes = path.read_bytes()
    canonical_bytes = raw_bytes.replace(b"\r\n", b"\n")
    actual_sha = hashlib.sha256(canonical_bytes).hexdigest()
    raw_sha = hashlib.sha256(raw_bytes).hexdigest()
    if actual_sha != record["sha256"] and raw_sha != record["sha256"]:
        return False, f"byte alteration detected (expected {record['sha256']}, got {actual_sha}); exemption invalidated"
    return True, f"historical applied migration verified ({record['live_migration_id']} / {record['project']} / {record['evidence_ref']})"


def statements(sql: str) -> list[str]:
    return [s.strip() for s in re.split(r";\s*(?:\n|$)", sql) if s.strip()]


def validate(path: pathlib.Path) -> list[str]:
    is_exempt, reason = check_historical_exemption(path)
    if is_exempt:
        print(f"::notice file={path}::Bypassing current-migration lint: {reason}")
        return []

    raw = path.read_text(encoding="utf-8")
    sql = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    errs: list[str] = []
    if "dcse-classification:" not in raw.lower():
        errs.append("missing -- dcse-classification header")
    if re.search(r"raw_user_meta_data|user_metadata", sql, re.I):
        errs.append("user-editable metadata used or referenced in authorization DDL")
    if re.search(r"auth\.role\s*\(", sql, re.I):
        errs.append("deprecated auth.role(); use policy TO plus authorization predicate")
    for stmt in statements(sql):
        if re.search(r"alter\s+default\s+privileges", stmt, re.I) and re.search(
            rf"\bgrant\b.*\bto\s+{CLIENT}\b", stmt, re.I | re.S
        ):
            errs.append("client-facing ALTER DEFAULT PRIVILEGES grant is prohibited")
        if re.search(rf"\bgrant\s+all\b.*\bto\s+{CLIENT}\b", stmt, re.I | re.S):
            errs.append("GRANT ALL to PUBLIC/anon/authenticated is prohibited")
    created = re.findall(rf"create\s+table\s+(?:if\s+not\s+exists\s+)?({EXPOSED})\.([a-z_][\w$]*)", sql, re.I)
    for schema, table in created:
        if not re.search(rf"alter\s+table\s+(?:only\s+)?{re.escape(schema)}\.{re.escape(table)}\s+enable\s+row\s+level\s+security", sql, re.I):
            errs.append(f"{schema}.{table} created in an exposed schema without RLS in the same migration")
    if re.search(r"create\s+(?:or\s+replace\s+)?view\s+" + EXPOSED + r"\.", sql, re.I) and not re.search(r"security_invoker\s*=\s*true", sql, re.I):
        errs.append("exposed view lacks security_invoker=true")
    for match in re.finditer(r"security\s+definer", sql, re.I):
        nearby = sql[match.start(): match.start() + 1200]
        if not re.search(r"set\s+search_path\s*=\s*(?:''|pg_catalog)", nearby, re.I):
            errs.append("SECURITY DEFINER lacks an approved fixed search_path")
        if not re.search(r"revoke\s+execute", sql[match.start():], re.I):
            errs.append("SECURITY DEFINER lacks an explicit EXECUTE revoke")
    return errs


def main() -> int:
    paths = [pathlib.Path(p) for p in sys.argv[1:] if p.endswith(".sql")]
    failures = [(p, validate(p)) for p in paths if p.exists()]
    failures = [(p, errors) for p, errors in failures if errors]
    for path, errors in failures:
        for error in sorted(set(errors)):
            print(f"::{ 'error' } file={path}::{error}")
    if failures:
        print(f"Supabase security gate failed for {len(failures)} migration file(s).")
        return 1
    print(f"Supabase security gate passed for {len(paths)} changed migration file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
