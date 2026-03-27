from dataclasses import dataclass
from typing import Any

from app.protocol.status import OrderStatus


@dataclass(slots=True)
class ParsedResult:
    transport_ok: bool
    api_ok: bool
    order_status: OrderStatus
    final: bool
    success: bool
    reason: str | None
    raw: dict[str, Any]
