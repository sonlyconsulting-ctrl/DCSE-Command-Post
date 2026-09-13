#!/usr/bin/env python3
"""
Storage round-trip verification:
Upload -> Persist -> Retrieve -> Compare SHA-256 -> Delete cleanup
"""
import urllib.request
import os
import hashlib
import json

def get_credentials():
    url = os.environ.get("SUPABASE_URL") or os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not (url and key):
        env_file = r"C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\DCSE_ASSET_PORTAL_APP\apps\web\.env.local"
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not url and line.startswith("NEXT_PUBLIC_SUPABASE_URL="):
                        url = line.split("=", 1)[1].strip().strip('"').strip("'")
                    elif not key and line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
    return url, key

def run_roundtrip():
    url, key = get_credentials()
    assert url and key, "Missing credentials"
    test_content = b"Hello ESCD Governed Storage - SHA-256 Verification"
    expected_sha = hashlib.sha256(test_content).hexdigest()
    path = "roundtrip_test/test_doc.txt"

    print("[1] Uploading test object to escd-files...")
    req = urllib.request.Request(
        f"{url}/storage/v1/object/escd-files/{path}",
        data=test_content,
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "text/plain",
            "x-upsert": "true"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        upload_res = resp.read().decode("utf-8")
        print(f"    Upload response: {upload_res}")

    print("[2] Retrieving object from authenticated endpoint...")
    get_req = urllib.request.Request(
        f"{url}/storage/v1/object/authenticated/escd-files/{path}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}"
        }
    )
    with urllib.request.urlopen(get_req) as resp:
        retrieved = resp.read()
        retrieved_sha = hashlib.sha256(retrieved).hexdigest()
        print(f"    Retrieved {len(retrieved)} bytes.")
        print(f"    Expected SHA:  {expected_sha}")
        print(f"    Retrieved SHA: {retrieved_sha}")
        assert retrieved_sha == expected_sha, "SHA-256 mismatch!"
        print("    [MATCH CONFIRMED]")

    print("[3] Deleting object from escd-files for cleanup...")
    del_payload = json.dumps({"prefixes": [path]}).encode("utf-8")
    del_req = urllib.request.Request(
        f"{url}/storage/v1/object/escd-files",
        data=del_payload,
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        method="DELETE"
    )
    with urllib.request.urlopen(del_req) as resp:
        del_res = resp.read().decode("utf-8")
        print(f"    Delete response: {del_res}")

    print("[ROUNDTRIP PASSED] Upload, SHA-256 verification, and deletion successful.")

if __name__ == "__main__":
    run_roundtrip()
