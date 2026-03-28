from pydantic import BaseModel


class NotifyPayload(BaseModel):
    event: str | None = None
    terminal_sn: str
    client_sn: str
    status: str | None = None
    order_status: str | None = None
    sn: str | None = None
    total_amount: str | None = None
    net_amount: str | None = None
    settlement_amount: str | None = None
    subject: str | None = None
    finish_time: str | None = None
