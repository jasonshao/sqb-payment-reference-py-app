from fastapi.testclient import TestClient

from app.main import app
from app.support.signing import md5_sign

client = TestClient(app)


def test_activate_then_checkin() -> None:
    activate = client.post("/terminal/activate", json={"terminal_sn": "T1", "terminal_name": "POS-1"})
    assert activate.status_code == 200

    checkin = client.post("/terminal/checkin", json={"terminal_sn": "T1"})
    assert checkin.status_code == 200
    assert checkin.json()["terminal_sn"] == "T1"


def test_notify_verify_then_success() -> None:
    client.post("/terminal/activate", json={"terminal_sn": "NT1", "terminal_name": "N-1"})
    body = '{"event":"payment","terminal_sn":"NT1","client_sn":"C1","status":"PAID","amount":100}'
    signature = md5_sign(body, "key-NT1")

    resp = client.post("/notify", content=body, headers={"X-SQB-Signature": signature})
    assert resp.status_code == 200
    assert resp.text == "success"


def test_notify_rejects_malformed_payload() -> None:
    resp = client.post("/notify", content="{not-json}", headers={"X-SQB-Signature": "bad-signature"})
    assert resp.status_code == 400
    assert resp.json() == {"detail": "malformed payload"}
