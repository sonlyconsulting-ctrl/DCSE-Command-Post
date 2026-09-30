import pytest
from pathlib import Path
from apps.escd.runtime.protocol_bridge import get_bridge, ESCDProtocolBridgeError

def test_bridge_loads_protocol():
    bridge = get_bridge()
    proto = bridge.load_protocol()
    assert proto["revision"] == "DCSE-SPEC-SHARED-ACTION-PROTOCOL-v1"
    assert proto["authority"] == "DCS"
    assert proto["status"] == "CANDIDATE"

def test_bridge_resolves_task_contract():
    bridge = get_bridge()
    contract = bridge.resolve_task_contract(
        task_id="TASK-TEST-001",
        handoff_id="HO-TEST-001",
        authorized_scope="Testing ESCD protocol integration",
        lane="operational"
    )
    assert contract["task_id"] == "TASK-TEST-001"
    assert contract["authorizing_authority"] == "DCS"
    assert contract["applicable_dart_route"] == "Command Post / SC (Discovery, Assess, Refine, Transfer)"
    assert contract["authorization_continuity_verified"] is True

def test_bridge_resolves_ps_dart_route():
    bridge = get_bridge()
    contract = bridge.resolve_task_contract(
        task_id="TASK-PS-001",
        handoff_id="HO-PS-001",
        authorized_scope="Litigation forensic review",
        lane="protected_ps"
    )
    assert contract["applicable_dart_route"] == "Protected PS (Discovery, Attack, Rebuttal, Trial)"

def test_bridge_evaluates_acceptance():
    bridge = get_bridge()
    root = Path(__file__).resolve().parents[3]
    valid_file = root / "governance" / "v7.2" / "implementations" / "DCSE_SPEC_SHARED_ACTION_PROTOCOL_v1.md"
    result = bridge.evaluate_acceptance([valid_file])
    assert result["passed"] is True
    assert result["returncode"] == 0
