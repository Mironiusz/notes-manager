import logging
import sys
from fastapi.testclient import TestClient
from app.main import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("tests")

client = TestClient(app)

def _create_note(title="T", content="C", is_favourite=False) -> dict:
    payload = {"title": title, "content": content, "isFavourite": is_favourite}
    log.info("POST /api/v1/notes payload=%s", payload)
    r = client.post("/api/v1/notes", json=payload)
    log.info("→ status=%s body=%s", r.status_code, r.json())
    assert r.status_code == 201
    return r.json()

def _delete_note(note_id: int) -> None:
    log.info("DELETE /api/v1/notes/%s", note_id)
    r = client.delete(f"/api/v1/notes/{note_id}")
    log.info("→ status=%s", r.status_code)
    assert r.status_code == 204

def test_create_note_returns_201_and_json():
    note = _create_note()
    _delete_note(note["id"])

def test_list_contains_created_note():
    note = _create_note(title="Listed", content="Hello")
    nid = note["id"]

    log.info("GET /api/v1/notes")
    r = client.get("/api/v1/notes")
    log.info("→ status=%s body_len=%s", r.status_code, len(r.json()))
    assert r.status_code == 200
    assert any(n["id"] == nid for n in r.json())

    _delete_note(nid)

def test_patch_note_updates_isFavourite():
    note = _create_note(is_favourite=False)
    nid = note["id"]

    patch = {"isFavourite": True}
    log.info("PATCH /api/v1/notes/%s payload=%s", nid, patch)
    r = client.patch(f"/api/v1/notes/{nid}", json=patch)
    log.info("→ status=%s body=%s", r.status_code, r.json())
    assert r.status_code == 200
    assert r.json()["isFavourite"] is True

    _delete_note(nid)

def test_delete_note_returns_204():
    note = _create_note()
    nid = note["id"]

    _delete_note(nid)

def test_get_deleted_note_returns_404():
    note = _create_note()
    nid = note["id"]
    _delete_note(nid)

    log.info("GET /api/v1/notes/%s (expect 404)", nid)
    r = client.get(f"/api/v1/notes/{nid}")
    log.info("→ status=%s body=%s", r.status_code, r.json())
    assert r.status_code == 404
