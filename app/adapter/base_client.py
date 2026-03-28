from typing import Any, Callable

import httpx

from app.core.config import Settings
from app.support.signing import build_authorization, dumps_body, md5_sign

Sender = Callable[[str, dict[str, str], dict[str, Any]], dict[str, Any]]


class SqbApiClient:
    def __init__(self, settings: Settings, sender: Sender | None = None) -> None:
        self.settings = settings
        self.sender = sender or self._default_sender

    def _default_sender(self, path: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.sqb_use_stub_transport:
            try:
                with httpx.Client(
                    base_url=self.settings.sqb_base_url,
                    timeout=self.settings.sqb_timeout_seconds,
                ) as client:
                    response = client.post(path, headers=headers, json=payload)
                body = response.json()
                if isinstance(body, dict):
                    body.setdefault("http_status", response.status_code)
                    return body
                return {
                    "http_status": response.status_code,
                    "result_code": "500",
                    "error_message": "invalid json body",
                }
            except httpx.HTTPError as exc:
                status_code = exc.response.status_code if exc.response is not None else 599
                return {"http_status": status_code, "result_code": "500", "error_message": str(exc)}

        if path == "/terminal/activate":
            terminal_sn = f"TSN-{payload['device_id']}"
            return {
                "http_status": 200,
                "result_code": "200",
                "biz_response": {
                    "result_code": "TERMINAL_ACTIVATE_SUCCESS",
                    "data": {"terminal_sn": terminal_sn, "terminal_key": f"key-{terminal_sn}"},
                },
            }
        if path == "/terminal/checkin":
            return {
                "http_status": 200,
                "result_code": "200",
                "biz_response": {
                    "result_code": "TERMINAL_CHECKIN_SUCCESS",
                    "data": {
                        "terminal_sn": payload["terminal_sn"],
                        "terminal_key": f"key-{payload['terminal_sn']}",
                    },
                },
            }
        if path == "/upay/v2/pay":
            return {
                "http_status": 200,
                "result_code": "200",
                "biz_response": {
                    "result_code": "USERPAYING",
                    "data": {"order_status": "USERPAYING"},
                },
            }
        if path == "/upay/v2/query":
            return {
                "http_status": 200,
                "result_code": "200",
                "biz_response": {
                    "result_code": "ORDER_NOT_PAID",
                    "data": {"order_status": "CREATED"},
                },
            }
        if path == "/upay/v2/precreate":
            return {
                "http_status": 200,
                "result_code": "200",
                "biz_response": {
                    "result_code": "PRECREATE_SUCCESS",
                    "data": {"order_status": "CREATED"},
                },
            }
        if path == "/upay/v2/refund":
            return {
                "http_status": 200,
                "result_code": "200",
                "biz_response": {
                    "result_code": "REFUND_SUCCESS",
                    "data": {"order_status": "REFUNDED"},
                },
            }
        if path == "/upay/v2/cancel":
            return {
                "http_status": 200,
                "result_code": "200",
                "biz_response": {
                    "result_code": "CANCEL_SUCCESS",
                    "data": {"order_status": "CANCELED"},
                },
            }
        return {"http_status": 200, "result_code": "200", "biz_response": {"result_code": "UNKNOWN", "data": {}}}

    def post(self, path: str, payload: dict[str, Any], *, signatory_sn: str, sign_key: str) -> dict[str, Any]:
        body = dumps_body(payload)
        signature = md5_sign(body, sign_key)
        authorization = build_authorization(signatory_sn=signatory_sn, signature=signature)
        headers = {"Authorization": authorization, "Content-Type": "application/json"}
        return self.sender(path, headers, payload)
