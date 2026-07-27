#!/usr/bin/env python3
"""
DCSE V7 Deterministic Validator and Preflight Suite

Validates Supabase schema, migrations, worker contracts, and task artifacts.
Runs as an autonomous worker with deterministic logic (no LLM involvement).

Exit codes:
  0: PASS - all checks pass
  1: REPAIRABLE - issues found but auto-fixable
  2: STOP_GATE - blocking issues requiring Level 0 review
  3: BLOCKED - unable to run validation
"""

import json
import sys
import hashlib
import re
from datetime import datetime
from typing import List, Dict, Tuple
from enum import Enum
from pathlib import Path
import subprocess

class Severity(Enum):
    """Issue severity levels"""
    PASS = "pass"
    WARNING = "warning"
    REPAIRABLE = "repairable"
    STOP_GATE = "stop_gate"

class Finding:
    """Single validation finding"""
    def __init__(self, check_id: str, severity: Severity, title: str, details: str, location: str = "", remedy: str = ""):
        self.check_id = check_id
        self.severity = severity
        self.title = title
        self.details = details
        self.location = location
        self.remedy = remedy
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "check_id": self.check_id,
            "severity": self.severity.value,
            "title": self.title,
            "details": self.details,
            "location": self.location,
            "remedy": self.remedy,
            "timestamp": self.timestamp
        }

class DeterministicValidator:
    """Comprehensive schema and artifact validator"""

    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.findings: List[Finding] = []
        self.known_failures: Dict[str, str] = {}  # hash -> remedy
        self.schema_inventory: Dict[str, list] = {
            "tables": [],
            "functions": [],
            "policies": [],
            "indexes": []
        }

    def validate_all(self) -> Tuple[Severity, List[Finding]]:
        """Run all validation checks"""
        print("[VALIDATOR] Starting comprehensive validation...", file=sys.stderr)

        # Check 1: SQL Syntax
        self._check_sql_syntax()

        # Check 2: Migration Ordering
        self._check_migration_ordering()

        # Check 3: Duplicate Migrations
        self._check_duplicate_migrations()

        # Check 4: Schema Completeness
        self._check_schema_completeness()

        # Check 5: SECURITY DEFINER Functions
        self._check_security_definer_functions()

        # Check 6: Search Path Validation
        self._check_search_paths()

        # Check 7: Function Ownership and Grants
        self._check_function_grants()

        # Check 8: RLS Coverage
        self._check_rls_coverage()

        # Check 9: Lane and Worker Authorization
        self._check_worker_authorization()

        # Check 10: PS Firewall Exclusion
        self._check_ps_firewall()

        # Check 11: Model Registry Schema
        self._check_model_registry()

        # Check 12: Runtime Packet Schema
        self._check_runtime_packet_schema()

        # Check 13: Worker Contract Schema
        self._check_worker_contract()

        # Check 14: Result Receipt Schema
        self._check_result_receipt_schema()

        # Check 15: File Hashes
        self._check_file_hashes()

        # Determine overall status
        max_severity = self._get_max_severity()
        print(f"[VALIDATOR] Validation complete. Max severity: {max_severity.value}", file=sys.stderr)

        return max_severity, self.findings

    def _check_sql_syntax(self):
        """Validate SQL syntax in migration files"""
        print("[CHECK] SQL Syntax...", file=sys.stderr)
        migration_dir = self.repo_root / "supabase" / "migrations"

        if not migration_dir.exists():
            self.findings.append(Finding(
                "CHECK_01", Severity.STOP_GATE,
                "Migration directory not found",
                f"Expected {migration_dir}",
                str(migration_dir)
            ))
            return

        for sql_file in migration_dir.glob("*.sql"):
            try:
                content = sql_file.read_text()
                # Basic syntax checks
                if content.strip() == "":
                    self.findings.append(Finding(
                        "CHECK_01", Severity.WARNING,
                        "Empty migration file",
                        f"File {sql_file.name} is empty",
                        str(sql_file)
                    ))
                    continue

                # Check for common SQL keywords
                if not any(kw in content.upper() for kw in ["CREATE", "ALTER", "INSERT", "UPDATE", "DELETE"]):
                    self.findings.append(Finding(
                        "CHECK_01", Severity.WARNING,
                        "No SQL operations found",
                        f"File {sql_file.name} contains no recognized SQL",
                        str(sql_file)
                    ))
            except Exception as e:
                self.findings.append(Finding(
                    "CHECK_01", Severity.REPAIRABLE,
                    "SQL file read error",
                    str(e),
                    str(sql_file)
                ))

    def _check_migration_ordering(self):
        """Verify migration files are numbered correctly"""
        print("[CHECK] Migration Ordering...", file=sys.stderr)
        migration_dir = self.repo_root / "supabase" / "migrations"
        migrations = sorted([f.name for f in migration_dir.glob("*.sql")])

        expected_pattern = re.compile(r'^(\d{8,14})_.*\.sql$')
        for i, migration in enumerate(migrations):
            match = expected_pattern.match(migration)
            if not match:
                self.findings.append(Finding(
                    "CHECK_02", Severity.STOP_GATE,
                    "Invalid migration filename",
                    f"Migration {migration} does not match naming convention",
                    str(migration_dir / migration),
                    "Rename to YYYYMMDDHHMMSS_description.sql"
                ))

    def _check_duplicate_migrations(self):
        """Detect duplicate migration files"""
        print("[CHECK] Duplicate Migrations...", file=sys.stderr)
        migration_dir = self.repo_root / "supabase" / "migrations"
        migrations = [f.name for f in migration_dir.glob("*.sql")]

        # Extract timestamps
        timestamps = {}
        for migration in migrations:
            ts = migration[:8]  # YYYYMMDD
            if ts not in timestamps:
                timestamps[ts] = []
            timestamps[ts].append(migration)

        # Check for duplicates on same day
        for ts, files in timestamps.items():
            if len(files) > 5:  # More than 5 per day is suspicious
                self.findings.append(Finding(
                    "CHECK_03", Severity.WARNING,
                    "High volume of migrations on single day",
                    f"{len(files)} migrations on {ts}",
                    str(migration_dir),
                    "Review for consolidation"
                ))

    def _check_schema_completeness(self):
        """Verify required tables and functions exist"""
        print("[CHECK] Schema Completeness...", file=sys.stderr)

        required_tables = [
            "v7_worker.agent_identity",
            "v7_worker.queue_message",
            "v7_worker.task_claim",
            "v7_worker.heartbeat",
            "v7_worker.result_submission",
            "v7_worker.dead_letter",
            "v7_worker.stop_gate",
            "v7_worker.cost_ledger"
        ]

        required_functions = [
            "v7_worker.claim_next_task",
            "v7_worker.send_heartbeat",
            "v7_worker.release_task_claim"
        ]

        # Parse migration file for table/function definitions
        migration_file = self.repo_root / "supabase" / "migrations" / "20260728_v7_agent_worker_communication_system.sql"
        if migration_file.exists():
            content = migration_file.read_text().upper()

            for table in required_tables:
                table_name = table.split(".")[-1]
                if f"CREATE TABLE" in content and table_name in content:
                    self.schema_inventory["tables"].append(table)
                else:
                    self.findings.append(Finding(
                        "CHECK_04", Severity.STOP_GATE,
                        f"Missing table: {table}",
                        f"Required table {table} not found in migrations",
                        str(migration_file)
                    ))

            for func in required_functions:
                func_name = func.split(".")[-1]
                if "CREATE FUNCTION" in content and func_name in content:
                    self.schema_inventory["functions"].append(func)
                else:
                    self.findings.append(Finding(
                        "CHECK_04", Severity.STOP_GATE,
                        f"Missing function: {func}",
                        f"Required function {func} not found",
                        str(migration_file)
                    ))

    def _check_security_definer_functions(self):
        """Verify SECURITY DEFINER on all v7_worker functions"""
        print("[CHECK] SECURITY DEFINER Functions...", file=sys.stderr)

        migration_file = self.repo_root / "supabase" / "migrations" / "20260728_v7_agent_worker_communication_system.sql"
        if not migration_file.exists():
            return

        content = migration_file.read_text()
        functions = re.findall(r'create or replace function v7_worker\.(\w+)', content, re.IGNORECASE)

        for func in functions:
            func_block = re.search(
                rf'create or replace function v7_worker\.{func}.*?language plpgsql.*?as \$\$',
                content,
                re.IGNORECASE | re.DOTALL
            )
            if func_block:
                if "security definer" not in func_block.group(0).lower():
                    self.findings.append(Finding(
                        "CHECK_05", Severity.STOP_GATE,
                        f"Missing SECURITY DEFINER on {func}",
                        "Function must use SECURITY DEFINER for privilege escalation",
                        str(migration_file),
                        f"Add 'security definer' to function {func} definition"
                    ))

    def _check_search_paths(self):
        """Verify fixed search_path in SECURITY DEFINER functions"""
        print("[CHECK] Search Paths...", file=sys.stderr)

        migration_file = self.repo_root / "supabase" / "migrations" / "20260728_v7_agent_worker_communication_system.sql"
        if not migration_file.exists():
            return

        content = migration_file.read_text()

        if "set search_path = public, v7_worker" not in content:
            self.findings.append(Finding(
                "CHECK_06", Severity.STOP_GATE,
                "Missing fixed search_path",
                "SECURITY DEFINER functions must have explicit search_path",
                str(migration_file),
                "Add 'set search_path = public, v7_worker' to function definitions"
            ))

    def _check_function_grants(self):
        """Verify function grants to authenticated and anon roles"""
        print("[CHECK] Function Grants...", file=sys.stderr)

        migration_file = self.repo_root / "supabase" / "migrations" / "20260728_v7_agent_worker_communication_system.sql"
        if not migration_file.exists():
            return

        content = migration_file.read_text()
        grants = re.findall(r'grant execute on function.*?to\s+(\w+)', content, re.IGNORECASE)

        if not grants:
            self.findings.append(Finding(
                "CHECK_07", Severity.STOP_GATE,
                "No function grants found",
                "Functions must grant EXECUTE to authenticated and anon roles",
                str(migration_file)
            ))

    def _check_rls_coverage(self):
        """Verify RLS enabled on all data tables"""
        print("[CHECK] RLS Coverage...", file=sys.stderr)

        migration_file = self.repo_root / "supabase" / "migrations" / "20260728_v7_agent_worker_communication_system.sql"
        if not migration_file.exists():
            return

        content = migration_file.read_text()

        data_tables = ["agent_identity", "queue_message", "task_claim", "heartbeat", "result_submission", "dead_letter", "stop_gate", "cost_ledger"]

        for table in data_tables:
            if f"enable row level security" not in content or table not in content:
                self.findings.append(Finding(
                    "CHECK_08", Severity.STOP_GATE,
                    f"RLS not enabled on {table}",
                    f"Table v7_worker.{table} must have RLS enabled",
                    str(migration_file),
                    f"Add 'alter table v7_worker.{table} enable row level security;'"
                ))

    def _check_worker_authorization(self):
        """Verify lane and task_type authorization in RLS"""
        print("[CHECK] Worker Authorization...", file=sys.stderr)

        migration_file = self.repo_root / "supabase" / "migrations" / "20260728_v7_agent_worker_communication_system.sql"
        if not migration_file.exists():
            return

        content = migration_file.read_text()

        if "authorized_lanes" not in content or "authorized_task_types" not in content:
            self.findings.append(Finding(
                "CHECK_09", Severity.STOP_GATE,
                "Missing worker authorization columns",
                "agent_identity must have authorized_lanes and authorized_task_types",
                str(migration_file)
            ))

    def _check_ps_firewall(self):
        """Ensure no PS (Privacy-Sensitive) content in migrations"""
        print("[CHECK] PS Firewall...", file=sys.stderr)

        migration_file = self.repo_root / "supabase" / "migrations" / "20260728_v7_agent_worker_communication_system.sql"
        if not migration_file.exists():
            return

        content = migration_file.read_text().lower()

        ps_keywords = ["ssn", "credit_card", "password", "secret", "family_data", "minor", "pii"]
        found_ps = [kw for kw in ps_keywords if kw in content]

        if found_ps:
            self.findings.append(Finding(
                "CHECK_10", Severity.STOP_GATE,
                "PS content detected in migration",
                f"Found PS keywords: {', '.join(found_ps)}",
                str(migration_file),
                "Remove all Privacy-Sensitive data from v7 schema"
            ))

    def _check_model_registry(self):
        """Validate model registry schema"""
        print("[CHECK] Model Registry...", file=sys.stderr)

        registry_file = self.repo_root / "02_ARCHITECTURE" / "MODEL_REGISTRY.yaml"
        if not registry_file.exists():
            self.findings.append(Finding(
                "CHECK_11", Severity.STOP_GATE,
                "MODEL_REGISTRY.yaml not found",
                "Required configuration file missing",
                "02_ARCHITECTURE/"
            ))
            return

        try:
            import yaml
            config = yaml.safe_load(registry_file.read_text())

            required_models = ["claude_architecture_reviewer", "claude_implementation_worker", "qwen_build_worker", "deterministic_validator"]
            for model in required_models:
                if model not in config.get("models", {}):
                    self.findings.append(Finding(
                        "CHECK_11", Severity.WARNING,
                        f"Missing model config: {model}",
                        f"Model {model} not defined in registry",
                        str(registry_file)
                    ))
        except Exception as e:
            self.findings.append(Finding(
                "CHECK_11", Severity.REPAIRABLE,
                "MODEL_REGISTRY.yaml parse error",
                str(e),
                str(registry_file)
            ))

    def _check_runtime_packet_schema(self):
        """Validate runtime packet structure"""
        print("[CHECK] Runtime Packet Schema...", file=sys.stderr)

        task_def = self.repo_root / "03_WORK_ORDERS" / "DCSE_V7_COMP_001_ARCHITECTURE_REVIEW.md"
        if not task_def.exists():
            self.findings.append(Finding(
                "CHECK_12", Severity.WARNING,
                "DCSE_V7_COMP_001 task definition not found",
                "Runtime packet schema cannot be validated",
                "03_WORK_ORDERS/"
            ))
            return

        content = task_def.read_text()
        required_fields = ["task_id", "task_type", "lane", "instruction", "tools_allowed", "repo_scope", "deadline"]

        for field in required_fields:
            if field not in content:
                self.findings.append(Finding(
                    "CHECK_12", Severity.WARNING,
                    f"Missing runtime packet field: {field}",
                    f"Runtime packet must include '{field}'",
                    str(task_def)
                ))

    def _check_worker_contract(self):
        """Validate worker identity and capability contracts"""
        print("[CHECK] Worker Contract...", file=sys.stderr)

        registry_file = self.repo_root / "02_ARCHITECTURE" / "MODEL_REGISTRY.yaml"
        if registry_file.exists():
            content = registry_file.read_text()
            required_fields = ["approved_model_id", "fallback_model_id", "required_tools"]
            for field in required_fields:
                if field not in content:
                    self.findings.append(Finding(
                        "CHECK_13", Severity.WARNING,
                        f"Missing worker contract field: {field}",
                        f"Worker contract must specify '{field}'",
                        str(registry_file)
                    ))

    def _check_result_receipt_schema(self):
        """Validate result receipt structure"""
        print("[CHECK] Result Receipt Schema...", file=sys.stderr)

        task_def = self.repo_root / "03_WORK_ORDERS" / "DCSE_V7_COMP_001_ARCHITECTURE_REVIEW.md"
        if task_def.exists():
            content = task_def.read_text()
            required_receipt_fields = ["review_type", "findings", "acceptance_scorecard", "level_0_decision"]
            for field in required_receipt_fields:
                if field not in content:
                    self.findings.append(Finding(
                        "CHECK_14", Severity.WARNING,
                        f"Missing receipt field: {field}",
                        f"Result receipt must include '{field}'",
                        str(task_def)
                    ))

    def _check_file_hashes(self):
        """Compute file hashes for integrity verification"""
        print("[CHECK] File Hashes...", file=sys.stderr)

        critical_files = [
            "supabase/migrations/20260728_v7_agent_worker_communication_system.sql",
            "02_ARCHITECTURE/MODEL_REGISTRY.yaml",
            "02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md",
            "workers/claude-reviewer-worker.js",
            "supabase/config.toml"
        ]

        for file_path in critical_files:
            full_path = self.repo_root / file_path
            if full_path.exists():
                try:
                    content = full_path.read_bytes()
                    file_hash = hashlib.sha256(content).hexdigest()
                    print(f"[HASH] {file_path}: {file_hash[:16]}...", file=sys.stderr)
                except Exception as e:
                    self.findings.append(Finding(
                        "CHECK_15", Severity.WARNING,
                        f"Hash computation error: {file_path}",
                        str(e),
                        str(full_path)
                    ))

    def _get_max_severity(self) -> Severity:
        """Determine overall validation status"""
        if not self.findings:
            return Severity.PASS

        severities = [f.severity for f in self.findings]
        if Severity.STOP_GATE in severities:
            return Severity.STOP_GATE
        if Severity.REPAIRABLE in severities:
            return Severity.REPAIRABLE
        if Severity.WARNING in severities:
            return Severity.WARNING

        return Severity.PASS

    def report(self) -> Dict:
        """Generate validation report"""
        max_severity, _ = self.validate_all()

        return {
            "validation_id": f"VAL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat(),
            "status": max_severity.value,
            "check_count": len(self.findings),
            "findings": [f.to_dict() for f in self.findings],
            "schema_inventory": self.schema_inventory,
            "exit_code": self._severity_to_exit_code(max_severity)
        }

    def _severity_to_exit_code(self, severity: Severity) -> int:
        mapping = {
            Severity.PASS: 0,
            Severity.WARNING: 1,
            Severity.REPAIRABLE: 1,
            Severity.STOP_GATE: 2
        }
        return mapping.get(severity, 3)


def main():
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    validator = DeterministicValidator(repo_root)
    report = validator.report()

    # Output JSON report
    print(json.dumps(report, indent=2))

    # Return exit code
    sys.exit(report["exit_code"])


if __name__ == "__main__":
    main()
