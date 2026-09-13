#!/usr/bin/env python3
"""
Provision governed Supabase Storage bucket 'escd-files'.
Configuration:
- Private bucket (public: False)
- Size limit: 10MB (10485760 bytes)
- Permitted MIME types: text, pdf, markdown, json, csv, png, jpeg, webp, zip
"""
import json
import os
import sys
import urllib.request
import urllib.error

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

def provision_bucket():
    url, key = get_credentials()
    if not url or not key:
        print("[ERROR] Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(f"{url}/storage/v1/bucket", headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            buckets = json.loads(resp.read().decode("utf-8"))
            existing = [b.get("id") for b in buckets]
            print(f"[INFO] Existing buckets: {existing}")
    except Exception as e:
        print(f"[ERROR] Failed to list buckets: {e}")
        sys.exit(1)

    bucket_name = "escd-files"
    if bucket_name in existing:
        print(f"[OK] Bucket '{bucket_name}' already exists.")
        return

    payload = {
        "id": bucket_name,
        "name": bucket_name,
        "public": False,
        "file_size_limit": 10485760,
        "allowed_mime_types": [
            "text/plain",
            "text/markdown",
            "text/csv",
            "application/json",
            "application/pdf",
            "image/png",
            "image/jpeg",
            "image/webp",
            "application/zip"
        ]
    }

    post_req = urllib.request.Request(
        f"{url}/storage/v1/bucket",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers
    )
    try:
        with urllib.request.urlopen(post_req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[SUCCESS] Created private bucket '{bucket_name}': {data}")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[ERROR] HTTP {e.code} creating bucket: {err_msg}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error creating bucket: {e}")
        sys.exit(1)

if __name__ == "__main__":
    provision_bucket()
