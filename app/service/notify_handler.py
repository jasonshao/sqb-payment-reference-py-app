import json

from app.protocol.notify_payload import NotifyPayload
from app.support.callback_verifier import SqbCallbackVerifier
from app.support.notify_deduplicator import SqbNotifyDeduplicator


class SqbNotifyHandler:
    def __init__(
        self,
        verifier: SqbCallbackVerifier,
        deduplicator: SqbNotifyDeduplicator,
    ) -> None:
        self.verifier = verifier
        self.deduplicator = deduplicator

    def handle(self, body: str, signature: str) -> tuple[bool, str]:
        payload = NotifyPayload.model_validate_json(body)

        if not self.verifier.verify(body, signature):
            return False, "invalid signature"

        dedup_key = f"{payload.sn or payload.client_sn}:{payload.order_status or payload.status}"
        if self.deduplicator.is_duplicate(dedup_key):
            return True, "duplicate"

        _ = json.loads(body)
        return True, "success"
