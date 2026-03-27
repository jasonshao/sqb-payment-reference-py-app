from typing import Any, Callable

from app.core.config import Settings
from app.support.signing import build_authorization, dumps_body, md5_sign

Sender = Callable[[str, dict[str, str], dict[str, Any]], dict[str, Any]]


class SqbApiClient:
    def __init__(self, settings: Settings, sender: Sender | None = None) -> None:
        self.settings = settings
        self.sender = sender or self._default_sender

    def _default_sender(self, path: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
        # Stubbed transport for reference app; replace by real HTTP request in production.
        return {"result_code": "200", "biz_response": {"path": path, "echo": payload}}

    def post(self, path: str, payload: dict[str, Any], sign_key: str) -> dict[str, Any]:
        body = dumps_body(payload)
        signature = md5_sign(body, sign_key)
        authorization = build_authorization(
            client_sn=self.settings.sqb_vendor_sn,
            access_token=self.settings.sqb_access_token,
            signature=signature,
        )
        headers = {"Authorization": authorization, "Content-Type": "application/json"}
        return self.sender(path, headers, payload)
