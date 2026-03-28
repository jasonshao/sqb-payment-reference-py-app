from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pay_endpoint_returns_non_final_without_mocked_paid_query() -> None:
    activate = client.post(
        "/terminal/activate",
        json={"app_id": "app-demo", "code": "code-demo", "device_id": "TP1"},
    )
    terminal_sn = activate.json()["terminal_sn"]
    resp = client.post(
        "/payment/pay",
        json={
            "terminal_sn": terminal_sn,
            "client_sn": "ORDER1",
            "total_amount": "100",
            "dynamic_id": "28937492374923",
            "operator": "tester",
            "subject": "coffee",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["final"] is False
