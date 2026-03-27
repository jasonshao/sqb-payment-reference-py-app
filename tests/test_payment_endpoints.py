from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pay_endpoint_returns_non_final_without_mocked_paid_query() -> None:
    client.post("/terminal/activate", json={"terminal_sn": "TP1", "terminal_name": "POS"})
    resp = client.post(
        "/payment/pay",
        json={
            "terminal_sn": "TP1",
            "client_sn": "ORDER1",
            "total_amount": 100,
            "auth_code": "28937492374923",
            "subject": "coffee",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["final"] is False
