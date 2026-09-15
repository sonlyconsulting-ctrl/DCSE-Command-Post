#!/usr/bin/env python3
"""Conservative anti-drift checks for changed Supabase SQL migrations."""
from __future__ import annotations

import pathlib
import re
import sys

EXPOSED = r"(?:public|api|ps_learner)"
CLIENT = r"(?:public|anon|authenticated)"


def statements(sql: str) -> list[str]:
    return [s.strip() for s in re.split(r";\s*(?:\n|$)", sql) if s.strip()]


def validate(path: pathlib.Path) -> list[str]:
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
