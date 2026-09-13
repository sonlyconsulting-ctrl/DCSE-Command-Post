from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "web" / "app.html"
MVP = ROOT / "web" / "mvp.html"
API = ROOT / "api" / "mvp.py"
SERVICE = ROOT / "runtime" / "mvp_data.py"
REPO = ROOT / "runtime" / "repository.py"


def test_ddna_schema_is_dcse_cp_not_legacy():
    code = SERVICE.read_text(encoding="utf-8")
    assert "dcse_ddna_legacy" not in code
    assert "dcse_cp" in code
    assert "list_ddna_sources" in code
    assert "create_ddna_source" in code
    assert "patch_ddna_source" in code
    assert "delete_ddna_source" in code


def test_asset_crud_in_runtime():
    code = SERVICE.read_text(encoding="utf-8")
    assert "list_assets" in code
    assert "create_asset" in code
    assert "patch_asset" in code
    assert "delete_asset" in code
    assert "dcse_asset_registry" in code


def test_file_attachment_in_runtime():
    code = SERVICE.read_text(encoding="utf-8")
    assert "save_file_attachment" in code
    assert "evidence_refs" in code
    assert "escd-files" in code


def test_repository_supports_delete():
    code = REPO.read_text(encoding="utf-8")
    assert "def delete_item" in code


def test_api_handlers_support_crud_and_upload():
    code = API.read_text(encoding="utf-8")
    assert "/api/mvp/upload" in code
    assert "save_file_attachment" in code
    assert "/api/mvp/assets" in code
    assert "/api/mvp/ddna" in code
    assert "def do_DELETE" in code
    assert "def do_PUT" in code


def test_ui_surfaces_have_crud_forms_and_modal():
    for page in (APP, MVP):
        html = page.read_text(encoding="utf-8")
        # All tabs present
        for tab in ("Chat", "Tasks", "Ideas", "Assets", "DDNA"):
            assert tab in html
        # Detail & CRUD Modal
        assert 'id="recordModal"' in html
        assert 'id="modalSaveBtn"' in html
        assert 'id="modalDeleteBtn"' in html
        assert 'id="modalUploadBtn"' in html
        # Add Asset form
        assert 'id="addAsset"' in html
        assert 'id="assetFileName"' in html
        # Add DDNA form
        assert 'id="addDDNA"' in html
        assert 'id="ddnaTitle"' in html
        # File inputs on forms
        assert 'id="taskInitialFile"' in html
        assert 'id="ideaInitialFile"' in html
        assert 'id="assetInitialFile"' in html
        assert 'id="ddnaInitialFile"' in html
        # Edit & Details button in list rendering
        assert "Edit & Details" in html
        assert "uploadFileToRecord" in html
