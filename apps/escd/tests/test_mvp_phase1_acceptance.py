from pathlib import Path
import json
import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO

from apps.escd.runtime.mvp_data import (
    MVPServiceError,
    get_canonical_convergence_items,
    list_knowledge,
    search_knowledge,
    create_asset,
    create_ddna_source,
    save_file_attachment,
)
from apps.escd.runtime.repository import SupabaseRLSClient
from apps.escd.api.mvp import handler

ROOT = Path(__file__).resolve().parents[1]
MVP_HTML = ROOT / "web" / "mvp.html"
APP_HTML = ROOT / "web" / "app.html"


def test_knowledge_tab_exists():
    for f in (MVP_HTML, APP_HTML):
        html = f.read_text(encoding="utf-8")
        assert 'id="knowledge"' in html
        assert "Knowledge" in html
        assert "knowledgeSearch" in html


def test_knowledge_record_count_24():
    records = list_knowledge(limit=500)
    assert len(records) == 24, f"Expected 24 canonical knowledge records, found {len(records)}"


def test_knowledge_records_endpoint():
    records = list_knowledge(limit=10)
    assert isinstance(records, list)
    assert len(records) > 0
    first = records[0]
    assert "id" in first
    assert "title" in first
    assert "content" in first
    assert "source" in first


def test_knowledge_search():
    # Search for an existing term
    all_records = list_knowledge(limit=500)
    assert len(all_records) == 24
    term = all_records[0]["title"][:15].strip()
    results = search_knowledge(term)
    assert len(results) >= 1
    assert any(term.lower() in r["title"].lower() or term.lower() in r["content"].lower() for r in results)

    # Empty search returns full list
    assert len(search_knowledge("")) == 24


def test_knowledge_detail_inspector():
    records = list_knowledge(limit=5)
    for r in records:
        assert "authority_classification" in r
        assert "status" in r
        assert "confidence" in r
        assert "provenance" in r
        assert isinstance(r["provenance"], dict)


def test_knowledge_authority_metadata():
    records = list_knowledge(limit=500)
    classifications = set(r.get("authority_classification") for r in records)
    assert "HISTORICAL_RECOVERED" in classifications


def test_malformed_json_handling():
    # Mock handler instance
    mock_handler = handler.__new__(handler)
    mock_handler.headers = {"Content-Length": "15"}
    mock_handler.rfile = BytesIO(b"{invalid json!}")

    with pytest.raises(MVPServiceError) as exc_info:
        mock_handler._read_json()
    assert str(exc_info.value) == "invalid_json"


def test_non_dict_json_handling():
    mock_handler = handler.__new__(handler)
    payload = b'[1, 2, "not a dict"]'
    mock_handler.headers = {"Content-Length": str(len(payload))}
    mock_handler.rfile = BytesIO(payload)

    with pytest.raises(MVPServiceError) as exc_info:
        mock_handler._read_json()
    assert str(exc_info.value) == "invalid_json"


def test_empty_json_handling():
    mock_handler = handler.__new__(handler)
    mock_handler.headers = {"Content-Length": "0"}
    mock_handler.rfile = BytesIO(b"")
    data = mock_handler._read_json()
    assert data == {}


def test_oversized_payload_handling():
    mock_handler = handler.__new__(handler)
    mock_handler.headers = {"Content-Length": "15000000"}  # 15MB
    mock_handler.rfile = BytesIO(b"")

    with pytest.raises(MVPServiceError) as exc_info:
        mock_handler._read_json()
    assert str(exc_info.value) == "payload_too_large"


def test_asset_crud_validation():
    with pytest.raises(MVPServiceError) as exc_info:
        create_asset({})
    assert "asset_file_name_required" in str(exc_info.value)


def test_ddna_crud_validation():
    with pytest.raises(MVPServiceError) as exc_info:
        create_ddna_source({})
    assert "source_title_or_ref_required" in str(exc_info.value)


def test_repository_delete_item_signature():
    client = SupabaseRLSClient("https://nevgdyfpxdaloacuutal.supabase.co", "anon", "token", schema="dcse_cp")
    assert hasattr(client, "delete_item")
    with patch.object(client, "_call", return_value=[]) as mock_call:
        res = client.delete_item("test-id-123")
        assert res is True
        mock_call.assert_called_once_with("DELETE", "escd_items?id=eq.test-id-123")


def test_attachment_size_limit():
    import base64
    huge_data = base64.b64encode(b"A" * (11 * 1024 * 1024)).decode("utf-8")  # 11MB
    with pytest.raises(MVPServiceError) as exc_info:
        save_file_attachment("huge.txt", huge_data)
    assert "file_exceeds_size_limit" in str(exc_info.value)


def test_save_file_attachment_hard_fails_on_storage_error():
    # Verify strict failure semantics: storage error raises MVPServiceError without silent fallback
    with patch("apps.escd.runtime.mvp_data.request.urlopen", side_effect=Exception("Connection refused")):
        with patch("apps.escd.runtime.mvp_data._service_config", return_value=("https://nevgdyfpxdaloacuutal.supabase.co", "mock-key")):
            with pytest.raises(MVPServiceError) as exc_info:
                save_file_attachment("test.txt", "SGVsbG8=")  # "Hello"
            assert "storage_upload_failed" in str(exc_info.value)
