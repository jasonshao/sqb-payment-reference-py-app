from app.adapter.base_client import SqbApiClient
from app.protocol.models import ActivateRequest


class SqbActivateAdapter:
    def __init__(self, client: SqbApiClient) -> None:
        self.client = client

    def activate(self, req: ActivateRequest) -> dict:
        return self.client.post("/terminal/activate", req.model_dump(), self.client.settings.sqb_vendor_key)
