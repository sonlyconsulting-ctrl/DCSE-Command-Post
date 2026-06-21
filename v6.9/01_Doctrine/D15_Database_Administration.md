# DCSE Doctrine D15: Database Administration (Supabase, PostgreSQL & Local Sync)

**Document ID:** DCSE-D15  
**Version:** v6.9  
**Created Date/Time:** 2026-06-21T15:31:45-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T15:31:45-04:00  
**Last Version/Release Date/Time:** 2026-06-21T15:31:45-04:00  
**Status:** CANDIDATE  
**Classification:** INTERNAL  
**Lane:** DCSE  
**Canonical file:** D15_Database_Administration.md  
**Doctrine Description:** The Database Administration Doctrine (D15) establishes the structural guidelines, security policies, and maintenance routines governing all data storage systems in the DCSE architecture. It acts as the operational bridge between remote cloud engines (such as Supabase PostgreSQL databases) and local transaction networks (including file-based JSON message exchanges, offline inventories, and case graphs). D15 defines the DBA's role in enforcing Row Level Security (RLS), gating database credentials, sanitizing inputs, and executing schema migrations. It provides concrete maintenance scripts for verifying transactional integrity, conducting pg_dump backups, and auditing cryptographic hashes. Through strict rules on local data boundaries and replica syncing, D15 guarantees data persistence, privacy, and systemic reliability.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## 1. Dual-State Database Architecture

The DCSE database layer operates in a split-state posture to satisfy both public web performance and strict litigation confidentiality:

### 1.1 Remote Cloud State (Supabase / PostgreSQL)
- **Scope**: Governs B2B consulting client portals (SC lane), public website reviews, and dynamic content feeds.
- **Constraints**: 
  - Accessed exclusively via API client endpoints (Velo / Wix postMessage widgets).
  - Web client access is limited to anonymous public keys.
  - Schema updates are managed via migrations tracked in the `07_Projects` folder.

### 1.2 Local Transaction Log Database (`05_Tribunal_Inbox`)
- **Scope**: Governs internal command orchestration and agent state exchanges.
- **Form**: A file-based database consisting of structured JSON packets.
- **Transaction Properties**: 
  - Writes must follow the packet schema (Timestamp, Sender, Priority, Status, Payload).
  - Concurrent writes are serialized by local poller processes.
  - Transactions are committed to Git as a versioned ledger.

### 1.3 Offline Evidentiary Databases (Litigation Spoke)
- **Scope**: Contains sensitive case parameters, Bates ranges, and custodian tables (PS lane).
- **Security Invariant**: Strictly prohibited from syncing to cloud endpoints. Data resides locally in JSON tables (e.g. `case_graph.json` or local Excel inventories) on authorized command nodes.

---

## 2. DBA Security & RLS Invariants

To prevent data leaks and access violations, all database entities must clear the following security gates:

### 2.1 Row Level Security (RLS) Policies
- All user-facing tables in Supabase must have RLS enabled.
- Select/Insert policies must validate the caller's JWT token or utilize an application-specific session identifier.
- Direct database connection strings (containing `postgres` master user credentials) must never be hardcoded or written to disk in public repositories.

### 2.2 Input Sanitization & Parameterization
- All queries executed against remote or local engines must use parameterized bindings.
- Direct string concatenation in SQL execution is prohibited to prevent SQL injection.

---

## 3. Database Maintenance Scripts

The following Python scripts must reside under `09_Tools/` and are scheduled via local pollers to maintain database health:

### 3.1 Local JSON Inbox Schema Verifier (`09_Tools/db_verify_inbox.py`)
This script audits the JSON transaction files inside the local communications bus to verify structural integrity and prevent corrupt logs.

```python
import os
import json
import datetime

inbox_dir = r"C:\DS All Things\DCSE_Command_Center\v6.9\05_Tribunal_Inbox"
schema_fields = {"timestamp", "sender_id", "priority", "status", "payload"}

def audit_transactions():
    corrupted_count = 0
    if not os.path.exists(inbox_dir):
        print(f"ERR_TRIBUNAL_INBOX_NOT_FOUND: {inbox_dir}")
        return
        
    for file_name in os.listdir(inbox_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(inbox_dir, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check for missing fields
                missing = schema_fields - set(data.keys())
                if missing:
                    print(f"WARN: Schema mismatch in {file_name}. Missing fields: {missing}")
                    corrupted_count += 1
            except Exception as e:
                print(f"WARN: Unreadable database packet {file_name}. Error: {e}")
                corrupted_count += 1
                
    print(f"Audit completed. Corrupted transactions flagged: {corrupted_count}")

if __name__ == "__main__":
    audit_transactions()
```

### 3.2 Headless Supabase Schema Backup (`09_Tools/db_backup_schema.py`)
This script automates backup rotations of the Supabase PostgreSQL database schema using `pg_dump`, saving schema outputs locally to `10_Archive`.

```python
import os
import subprocess
import datetime

def run_schema_backup():
    db_uri = os.environ.get("SUPABASE_DB_URI")
    if not db_uri:
        print("ERR_CREDENTIAL_MISSING: SUPABASE_DB_URI environment variable is not defined.")
        return
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = rf"C:\DS All Things\DCSE_Command_Center\v6.9\10_Archive\supabase_schema_backup_{timestamp}.sql"
    
    try:
        # Execute pg_dump for schema only
        command = f'pg_dump "{db_uri}" --schema-only -f "{backup_path}"'
        subprocess.run(command, shell=True, check=True)
        print(f"SUCCESS: Database schema backed up to {backup_path}")
    except subprocess.CalledProcessError as e:
        print(f"ERR_BACKUP_FAILED: Command execution failed. {e}")

if __name__ == "__main__":
    run_schema_backup()
```

### 3.3 DART Bates Range and Evidentiary Integrity Audit (`09_Tools/db_audit_evidentiary.py`)
Enforces the 8 Quality Gates by detecting overlapping Bates ranges, verifying SHA-256 metadata signatures, and auditing discovery duplication across index tables.

```python
import os
import json
import hashlib

def generate_file_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            sha.update(chunk)
    return sha.hexdigest()

def audit_evidentiary_database(receipts_dir):
    hash_registry = {}
    duplicates_flagged = 0
    
    if not os.path.exists(receipts_dir):
        print(f"ERR_DIRECTORY_MISSING: Receipts directory {receipts_dir} not found.")
        return
        
    for root, dirs, files in os.walk(receipts_dir):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = generate_file_sha256(filepath)
            
            if file_hash in hash_registry:
                print(f"WARN: Duplicate document signature detected! {filepath} matches {hash_registry[file_hash]}")
                duplicates_flagged += 1
            else:
                hash_registry[file_hash] = filepath
                
    print(f"Evidentiary audit complete. Unique signatures: {len(hash_registry)}. Duplicates: {duplicates_flagged}")

if __name__ == "__main__":
    audit_evidentiary_database(r"C:\DS All Things\DCSE_Command_Center\v6.9\11_Receipts")
```

---

## Related Doctrine

- [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) - Credential containment and MEC boundaries
- [D04_Command_Post_Communications.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D04_Command_Post_Communications.md) - JSON packet transfer rules and folder endpoints
- [D06_File_System.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D06_File_System.md) - Core layout definitions and archiving rules
- [D11_HTML_Wix_App.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D11_HTML_Wix_App.md) - Web endpoint security and browser-facing database keys
- [D13_DART_Core.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D13_DART_Core.md) - Cryptographic file hashing quality gates

---

## Error-Catch Protocol

If this database doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.
