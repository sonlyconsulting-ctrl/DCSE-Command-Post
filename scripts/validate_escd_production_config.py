#!/usr/bin/env python3
"""Strict ESCD production deployment configuration gate.

This validator intentionally has no local .env fallback and does not synthesize
DDNA bindings. It is intended to run in the actual deployment environment.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

EXPECTED_HOST = "nevgdyfpxdaloacuutal.supabase.co"
REQUIRED_VARS = (
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "SUPABASE_SERVICE_ROLE_KEY",
    "DDNA_SUPABASE_URL",
    "DDNA_SUPABASE_SERVICE_ROLE_KEY",
)


def fail(message: str) -> None:
    print(f"[GATE FAILED] {message}")
    raise SystemExit(1)


def request_json(url: str, headers: dict[str, str]) -> tuple[int, object]:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
        return resp.status, json.loads(raw or "{}")


def validate_config() -> None:
    missing = [name for name in REQUIRED_VARS if not str(os.environ.get(name) or "").strip()]
    if missing:
        fail("Missing required production variables: " + ", ".join(missing))

    supabase_url = os.environ["SUPABASE_URL"].rstrip("/")
    ddna_url = os.environ["DDNA_SUPABASE_URL"].rstrip("/")
    if urllib.parse.urlparse(supabase_url).hostname != EXPECTED_HOST:
        fail("SUPABASE_URL does not target SC-Command-Post")
    if urllib.parse.urlparse(ddna_url).hostname != EXPECTED_HOST:
        fail("DDNA_SUPABASE_URL does not target SC-Command-Post")

    service_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    ddna_key = os.environ["DDNA_SUPABASE_SERVICE_ROLE_KEY"]

    headers = {"apikey": service_key, "Authorization": f"Bearer {service_key}"}
    status, _ = request_json(f"{supabase_url}/rest/v1/", headers)
    if status != 200:
        fail(f"Supabase Data API returned {status}")

    ddna_headers = {
        "apikey": ddna_key,
        "Authorization": f"Bearer {ddna_key}",
        "Accept-Profile": "dcse_cp",
    }
    status, _ = request_json(f"{ddna_url}/rest/v1/ddna_source_queue?select=id&limit=1", ddna_headers)
    if status != 200:
        fail(f"DDNA dcse_cp returned {status}")

    status, bucket = request_json(f"{supabase_url}/storage/v1/bucket/escd-files", headers)
    if status != 200 or not isinstance(bucket, dict):
        fail("escd-files Storage bucket unavailable")
    if bool(bucket.get("public")):
        fail("escd-files Storage bucket must remain private")

    print("[GATE PASSED] Strict ESCD production configuration verified.")


if __name__ == "__main__":
    validate_config()
