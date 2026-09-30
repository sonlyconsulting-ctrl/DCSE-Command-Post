import pytest
import json
from pathlib import Path
from apps.escd.runtime.protocol_bridge import get_bridge, ESCDProtocolBridgeError

VALID_AUTH = {
    "authorizing_authority": "DCS",
    "authorized_scope": "Integration and test of ESCD shared protocol",
    "active": True,
}

def test_bridge_dynamically_loads_protocol_metadata():
    bridge = get_bridge()
    proto = bridge.load_protocol()
    assert proto["revision"] == "DCSE-SPEC-SHARED-ACTION-PROTOCOL-v1"
    assert "DCS" in proto["authority"]
    assert proto["status"] == "CANDIDATE"

def test_bridge_rejects_missing_authorization_record():
    bridge = get_bridge()
    with pytest.raises(ESCDProtocolBridgeError, match="Existing authorization record is required"):
        bridge.resolve_task_contract(
            task_id="TASK-UNAUTH-01",
            handoff_id="HO-01",
            requested_scope="Unchecked work",
            lane="operational",
            auth_record=None,
        )

def test_bridge_rejects_scope_expansion():
    bridge = get_bridge()
    with pytest.raises(ESCDProtocolBridgeError, match="Scope expansion detected"):
        bridge.resolve_task_contract(
            task_id="TASK-EXPAND-01",
            handoff_id="HO-01",
            requested_scope="Deploy live production website to public internet",
            lane="operational",
            auth_record=VALID_AUTH,
        )

def test_bridge_rejects_invalid_lane_without_guessing():
    bridge = get_bridge()
    with pytest.raises(ESCDProtocolBridgeError, match="Invalid lane 'litigation_notes'"):
        bridge.resolve_task_contract(
            task_id="TASK-LANE-01",
            handoff_id="HO-01",
            requested_scope="Integration and test of ESCD shared protocol",
            lane="litigation_notes",  # Should reject even if text mentions litigation
            auth_record=VALID_AUTH,
        )

def test_bridge_routes_protected_ps_only_on_explicit_lane():
    bridge = get_bridge()
    contract = bridge.resolve_task_contract(
        task_id="TASK-PS-01",
        handoff_id="HO-01",
        requested_scope="Integration and test of ESCD shared protocol",
        lane="protected_ps",
        auth_record=VALID_AUTH,
    )
    assert contract["applicable_dart_route"] == "Protected PS (Discovery, Attack, Rebuttal, Trial)"

def test_bridge_routes_commercial_on_operational_lane():
    bridge = get_bridge()
    contract = bridge.resolve_task_contract(
        task_id="TASK-OP-01",
        handoff_id="HO-01",
        requested_scope="Integration and test of ESCD shared protocol",
        lane="operational",
        auth_record=VALID_AUTH,
    )
    assert contract["applicable_dart_route"] == "Command Post / SC (Discovery, Assess, Refine, Transfer)"

def test_dispatch_and_complete_authorized_task_with_persisted_receipt(tmp_path):
    bridge = get_bridge()
    bridge.receipts_dir = tmp_path

    root = Path(__file__).resolve().parents[3]
    valid_file = root / "governance" / "v7.2" / "implementations" / "DCSE_SPEC_SHARED_ACTION_PROTOCOL_v1.md"

    receipt = bridge.dispatch_and_complete_task(
        task_id="TASK-DEMO-001",
        handoff_id="HO-DEMO-001",
        requested_scope="Integration and test of ESCD shared protocol",
        lane="operational",
        auth_record=VALID_AUTH,
        target_files=[valid_file],
        remote_sha="3d4baeb1c03d38db9048e618ef80472258260e8a",
    )
    assert receipt["status"] == "ACCEPTED"
    assert receipt["contract"]["authorization_continuity_verified"] is True
    assert Path(receipt["persisted_path"]).is_file()

    # Verify retrieval
    retrieved = bridge.retrieve_evidence_receipt("TASK-DEMO-001")
    assert retrieved is not None
    assert retrieved["receipt_id"] == "RECEIPT-TASK-DEMO-001"
    assert retrieved["remote_commit_sha"] == "3d4baeb1c03d38db9048e618ef80472258260e8a"

def test_dispatch_rejects_on_failed_acceptance(tmp_path):
    bridge = get_bridge()
    bridge.receipts_dir = tmp_path

    # Create temporary file with prohibited em dash
    bad_file = tmp_path / "BAD_ARTIFACT.md"
    bad_file.write_text("# Bad file with em dash \u2014 here", encoding="utf-8")

    with pytest.raises(ESCDProtocolBridgeError, match="Task acceptance evaluation failed"):
        bridge.dispatch_and_complete_task(
            task_id="TASK-FAIL-001",
            handoff_id="HO-FAIL-001",
            requested_scope="Integration and test of ESCD shared protocol",
            lane="operational",
            auth_record=VALID_AUTH,
            target_files=[bad_file],
        )

    # Confirm no completion receipt was created for failed task
    retrieved = bridge.retrieve_evidence_receipt("TASK-FAIL-001")
    assert retrieved is None
def test_mocked_escd_handler_task_lifecycle():
    """
    Mocked handler test: exercises the established ESCD handler entry points
    (/api/mvp/items do_POST and do_PATCH) with mocked repository dependencies.
    Demonstrates handler state transitions and evidence ref handling without
    claiming live external database transactions.
    """
    from io import BytesIO
    from unittest.mock import MagicMock
    from apps.escd.api.mvp import handler

    # 1. Setup mock operator repo adhering to established SupabaseRLSClient interface
    mock_repo = MagicMock()
    mock_item = {
        "id": "item-uuid-001",
        "item_key": "mvp-task-001",
        "title": "Execute Shared Protocol Acceptance Task",
        "status": "active",
        "task_class": "DO",
        "evidence_refs": [],
    }
    mock_repo.create_item.return_value = mock_item
    mock_repo.get_item.return_value = mock_item
    mock_repo.patch_item.side_effect = lambda item_id, update: {**mock_item, **update}

    # 2. Invoke established ESCD handler
    h = handler.__new__(handler)
    h.headers = {"Content-Length": "120"}
    h._auth = lambda: mock_repo
    json_captured = []
    h._json = lambda status, payload: json_captured.append((status, payload))

    # Create task through established route
    h.path = "/api/mvp/items"
    h._read_json = lambda: {
        "kind": "task",
        "title": "Execute Shared Protocol Acceptance Task",
        "notes": "Authorized scope: DDNA protocol verification",
        "priority": 1.0,
    }
    h.do_POST()

    status, resp = json_captured[-1]
    assert status == 201
    assert resp["ok"] is True
    assert resp["item"]["title"] == "Execute Shared Protocol Acceptance Task"

    # 3. Attach verified completion evidence via established ESCD attachment flow
    from apps.escd.runtime.mvp_data import finalize_file_attachment
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("apps.escd.runtime.mvp_data._storage_service_request", lambda *a, **k: ("", {}))
        attachment = finalize_file_attachment(
            storage_path="items/item-uuid-001/DCSE_SPEC_SHARED_ACTION_PROTOCOL_v1.md",
            file_name="DCSE_SPEC_SHARED_ACTION_PROTOCOL_v1.md",
            mime_type="text/markdown",
            size=2500,
            sha256="3d4baeb1c03d38db9048e618ef80472258260e8a" + "0" * 24,
            record_type="item",
            record_id="item-uuid-001",
            repo=mock_repo,
        )
    assert attachment["name"] == "DCSE_SPEC_SHARED_ACTION_PROTOCOL_v1.md"
    assert mock_repo.patch_item.called

    # 4. Complete task under governed transition (_patch_item_governed)
    h._read_json = lambda: {
        "id": "item-uuid-001",
        "status": "completed",
    }
    h.do_PATCH()
    patch_status, patch_resp = json_captured[-1]
    assert patch_status == 200
    assert patch_resp["ok"] is True
    assert patch_resp["item"]["status"] == "completed"
