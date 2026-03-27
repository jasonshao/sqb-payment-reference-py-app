from app.adapter.base_client import SqbApiClient
from app.protocol.models import (
    CancelRequest,
    OrderQueryRequest,
    PayRequest,
    PrecreateRequest,
    RefundRequest,
)


class SqbPaymentAdapter:
    def __init__(self, client: SqbApiClient) -> None:
        self.client = client

    def pay(self, req: PayRequest, terminal_key: str) -> dict:
        return self.client.post("/upay/v2/pay", req.model_dump(), terminal_key)

    def query(self, req: OrderQueryRequest, terminal_key: str) -> dict:
        return self.client.post("/upay/v2/query", req.model_dump(), terminal_key)

    def precreate(self, req: PrecreateRequest, terminal_key: str) -> dict:
        return self.client.post("/upay/v2/precreate", req.model_dump(), terminal_key)

    def refund(self, req: RefundRequest, terminal_key: str) -> dict:
        return self.client.post("/upay/v2/refund", req.model_dump(), terminal_key)

    def cancel(self, req: CancelRequest, terminal_key: str) -> dict:
        return self.client.post("/upay/v2/cancel", req.model_dump(), terminal_key)
