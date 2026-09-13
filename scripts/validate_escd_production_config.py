#!/usr/bin/env python3
"""
Preflight configuration validator for ESCD Production Deployment Gate.
Validates presence and connectivity of required environment variables without leaking secrets.
"""
import os
import sys
import urllib.request
import urllib.error

REQUIRED_VARS = [
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "SUPABASE_SERVICE_ROLE_KEY",
    "DDNA_SUPABASE_URL",
    "DDNA_SUPABASE_SERVICE_ROLE_KEY"
]

def load_env_if_local():
    # If variables are not in os.environ, check local .env.local for local testing
    env_file = r"C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\DCSE_ASSET_PORTAL_APP\apps\web\.env.local"
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k.startswith("NEXT_PUBLIC_"):
                    clean_k = k.replace("NEXT_PUBLIC_", "")
                    if clean_k not in os.environ:
                        os.environ[clean_k] = v
                if k not in os.environ:
                    os.environ[k] = v

    if "DDNA_SUPABASE_URL" not in os.environ and "SUPABASE_URL" in os.environ:
        os.environ["DDNA_SUPABASE_URL"] = os.environ["SUPABASE_URL"]
    if "DDNA_SUPABASE_SERVICE_ROLE_KEY" not in os.environ and "SUPABASE_SERVICE_ROLE_KEY" in os.environ:
        os.environ["DDNA_SUPABASE_SERVICE_ROLE_KEY"] = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

def validate_config():
    load_env_if_local()
    missing = []
    for var in REQUIRED_VARS:
        val = os.environ.get(var)
        if not val or not val.strip():
            missing.append(var)
        else:
            # Report presence and length safely without exposing secret
            print(f"[CHECK] {var}: PRESENT (len={len(val)})")

    if missing:
        print(f"[GATE FAILED] Missing required deployment variables: {missing}")
        sys.exit(1)

    # Validate Supabase connectivity
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}

    try:
        req = urllib.request.Request(f"{url}/rest/v1/", headers=headers)
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print(f"[CHECK] Supabase Root API: REACHABLE (status={resp.status})")
    except Exception as e:
        print(f"[GATE FAILED] Supabase API unreachable: {e}")
        sys.exit(1)

    # Validate DDNA PostgREST schema dcse_cp
    ddna_url = os.environ["DDNA_SUPABASE_URL"]
    ddna_key = os.environ["DDNA_SUPABASE_SERVICE_ROLE_KEY"]
    ddna_headers = {
        "apikey": ddna_key,
        "Authorization": f"Bearer {ddna_key}",
        "Accept-Profile": "dcse_cp"
    }
    try:
        req = urllib.request.Request(f"{ddna_url}/rest/v1/ddna_source_queue?limit=1", headers=ddna_headers)
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print(f"[CHECK] DDNA Schema (dcse_cp): REACHABLE (status={resp.status})")
    except Exception as e:
        print(f"[GATE FAILED] DDNA Schema dcse_cp unreachable: {e}")
        sys.exit(1)

    # Validate Storage bucket escd-files
    try:
        req = urllib.request.Request(f"{url}/storage/v1/bucket/escd-files", headers=headers)
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print(f"[CHECK] Storage Bucket (escd-files): VERIFIED (status={resp.status})")
    except Exception as e:
        print(f"[GATE FAILED] Storage bucket escd-files check failed: {e}")
        sys.exit(1)

    print("[GATE PASSED] All production environment requirements satisfied.")

if __name__ == "__main__":
    validate_config()
