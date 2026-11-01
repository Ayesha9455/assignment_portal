import json, os, sys
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app

@pytest.fixture
def setup(tmp_path):
    storage = tmp_path / "subs.json"
    app = create_app(str(storage))
    return app.test_client(), storage

GOOD = {"name": "Ayesha", "reg_no": "SP23-BCS-005",
        "title": "Lab 1", "url": "https://github.com/Ayesha9455/repo"}

def test_valid_submission_is_saved_and_listed(setup):
    client, storage = setup
    r = client.post("/submit", data=GOOD)
    assert r.status_code == 302                      # redirected to the submissions page
    assert "/submissions" in r.headers["Location"]
    assert len(json.loads(storage.read_text())) == 1
    page = client.get("/submissions")
    assert page.status_code == 200
    assert b"SP23-BCS-005" in page.data

def test_missing_registration_number_is_rejected(setup):
    client, storage = setup
    bad = {**GOOD, "reg_no": ""}
    r = client.post("/submit", data=bad)
    assert r.status_code == 400
    assert b"Registration number is required" in r.data
    assert not storage.exists()

def test_invalid_url_is_rejected_and_not_saved(setup):
    client, storage = setup
    bad = {**GOOD, "url": "not a url"}
    r = client.post("/submit", data=bad)
    assert r.status_code == 400
    assert not storage.exists()
