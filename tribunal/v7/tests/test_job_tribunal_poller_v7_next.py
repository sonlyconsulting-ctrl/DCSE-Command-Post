from pathlib import Path
import json

import pytest

from job_tribunal_poller_v7_next import Envelope, candidate_files
from tribunal_v7_state_machine import GovernanceError


def test_envelope_accepts_multiple_recipients(tmp_path: Path):
    source = tmp_path / "DISPATCH_test.json"
    payload = {
        "DCSE_DISPATCH": {
            "task_id": "DCSE-TEST-001",
            "sender": "ESCD",
            "recipients": ["codex", "claude", "ag"],
            "instruction": "Review the bounded candidate and return the requested artifact.",
            "expected_outputs": ["result.json"],
            "authorization": {"decision": "GO", "approved_by": "DCS", "approved_at": "2026-09-16"},
        }
    }
    source.write_text(json.dumps(payload), encoding="utf-8")
    envelope = Envelope.from_json(payload, source)
    assert envelope.task_id == "DCSE-TEST-001"
    assert envelope.recipients == ("codex", "claude", "ag")
    assert envelope.return_to == "ESCD"


def test_envelope_requires_recipient(tmp_path: Path):
    source = tmp_path / "DISPATCH_test.json"
    payload = {"DCSE_DISPATCH": {"task_id": "DCSE-TEST-002", "sender": "ESCD", "instruction": "Perform bounded work.", "recipients": []}}
    with pytest.raises(GovernanceError):
        Envelope.from_json(payload, source)


def test_candidate_files_only_dispatch_prefix(tmp_path: Path):
    (tmp_path / "DISPATCH_a.json").write_text("{}", encoding="utf-8")
    (tmp_path / "TRIBUNAL_b.json").write_text("{}", encoding="utf-8")
    assert [p.name for p in candidate_files(tmp_path)] == ["DISPATCH_a.json"]
