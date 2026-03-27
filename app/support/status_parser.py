from app.protocol.parsed_result import ParsedResult
from app.protocol.status import OrderStatus


TERMINAL_STATUSES = {
    "PAID": OrderStatus.PAID,
    "PAY_CANCELED": OrderStatus.PAY_CANCELED,
    "REFUNDED": OrderStatus.REFUNDED,
}


def parse_result(payload: dict) -> ParsedResult:
    transport_ok = payload.get("http_status", 200) == 200
    result_code = payload.get("result_code", "500")
    api_ok = result_code == "200"

    biz_response = payload.get("biz_response") or {}
    status_text = str(biz_response.get("status", "PENDING")).upper()
    order_status = TERMINAL_STATUSES.get(status_text, OrderStatus.PENDING)

    if not transport_ok or not api_ok:
        order_status = OrderStatus.FAILED

    success = order_status == OrderStatus.PAID
    reason = payload.get("error_message")

    return ParsedResult(
        transport_ok=transport_ok,
        api_ok=api_ok,
        order_status=order_status,
        final=order_status.is_final,
        success=success,
        reason=reason,
        raw=payload,
    )
