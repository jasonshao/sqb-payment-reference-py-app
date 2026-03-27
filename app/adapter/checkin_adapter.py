from app.adapter.base_client import SqbApiClient
from app.protocol.models import CheckinRequest


class SqbCheckinAdapter:
    def __init__(self, client: SqbApiClient) -> None:
        self.client = client

    def checkin(self, req: CheckinRequest, terminal_key: str) -> dict:
        return self.client.post("/terminal/checkin", req.model_dump(), terminal_key)
