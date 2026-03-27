from pydantic import BaseModel


class NotifyPayload(BaseModel):
    event: str
    terminal_sn: str
    client_sn: str
    status: str
    amount: int | None = None
