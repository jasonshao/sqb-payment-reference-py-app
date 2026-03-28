import base64
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi.testclient import TestClient

from app.main import app
from app.bootstrap.dependencies import get_notify_handler, get_settings


private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
).decode("utf-8")

os.environ["SQB_CALLBACK_PUBLIC_KEY"] = public_key
get_settings.cache_clear()
get_notify_handler.cache_clear()

client = TestClient(app)


def test_activate_then_checkin() -> None:
    activate = client.post(
        "/terminal/activate",
        json={"app_id": "app-demo", "code": "code-demo", "device_id": "T1"},
    )
    assert activate.status_code == 200
    terminal_sn = activate.json()["terminal_sn"]

    checkin = client.post("/terminal/checkin", json={"terminal_sn": terminal_sn, "device_id": "T1"})
    assert checkin.status_code == 200
    assert checkin.json()["terminal_sn"] == terminal_sn


def test_notify_verify_then_success() -> None:
    activate = client.post(
        "/terminal/activate",
        json={"app_id": "app-demo", "code": "code-demo", "device_id": "NT1"},
    )
    terminal_sn = activate.json()["terminal_sn"]
    body = (
        '{"event":"trade_status_changed","terminal_sn":"'
        + terminal_sn
        + '","sn":"S1","client_sn":"C1","order_status":"PAID","status":"TRADE_SUCCESS"}'
    )
    signature = base64.b64encode(
        private_key.sign(body.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
    ).decode("utf-8")

    resp = client.post("/notify", content=body, headers={"Authorization": signature})
    assert resp.status_code == 200
    assert resp.text == "success"
