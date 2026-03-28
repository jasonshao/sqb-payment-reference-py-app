import json

from pydantic import ValidationError

from app.protocol.notify_payload import NotifyPayload
from app.support.callback_verifier import SqbCallbackVerifier
from app.support.notify_deduplicator import SqbNotifyDeduplicator
from app.support.terminal_credential_store import TerminalCredentialStore


class SqbNotifyHandler:
    def __init__(
        self,
        verifier: SqbCallbackVerifier,
        deduplicator: SqbNotifyDeduplicator,
        credential_store: TerminalCredentialStore,
    ) -> None:
        self.verifier = verifier
        self.deduplicator = deduplicator
        self.credential_store = credential_store

    def handle(self, body: str, signature: str) -> tuple[bool, str]:
        try:
            payload = NotifyPayload.model_validate_json(body)
        except ValidationError:
            return False, "malformed payload"
        terminal_key = self.credential_store.get_key(payload.terminal_sn)
        if not terminal_key:
            return False, "unknown terminal"

        if not self.verifier.verify(body, terminal_key, signature):
            return False, "invalid signature"

        dedup_key = f"{payload.event}:{payload.client_sn}:{payload.status}"
        if self.deduplicator.is_duplicate(dedup_key):
            return True, "duplicate"

        _ = json.loads(body)
        return True, "success"
