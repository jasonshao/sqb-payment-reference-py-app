from app.protocol.parsed_result import ParsedResult
from app.protocol.status import OrderStatus


TERMINAL_STATUSES = {
    "CREATED": OrderStatus.CREATED,
    "PAID": OrderStatus.PAID,
    "CANCELED": OrderStatus.CANCELED,
    "REFUNDED": OrderStatus.REFUNDED,
    "PARTIAL_REFUNDED": OrderStatus.PARTIAL_REFUNDED,
    "USERPAYING": OrderStatus.USERPAYING,
    "PENDING": OrderStatus.PENDING,
}


def parse_result(payload: dict) -> ParsedResult:
    transport_ok = payload.get("http_status", 200) == 200
    biz_response = payload.get("biz_response") or {}
    api_result_code = str(payload.get("result_code", "500"))
    biz_result_code = str(biz_response.get("result_code", "")).upper()
    data = biz_response.get("data") or {}

    api_ok = transport_ok and api_result_code == "200"
    status_text = str(
        data.get("order_status")
        or data.get("status")
        or biz_response.get("status")
        or "UNKNOWN"
    ).upper()
    order_status = TERMINAL_STATUSES.get(status_text, OrderStatus.UNKNOWN)

    if not transport_ok or not api_ok:
        order_status = OrderStatus.FAILED
    elif biz_result_code in {"PAY_SUCCESS", "REFUND_SUCCESS"} and order_status == OrderStatus.UNKNOWN:
        order_status = OrderStatus.PAID if biz_result_code == "PAY_SUCCESS" else OrderStatus.REFUNDED
    elif biz_result_code == "CANCEL_SUCCESS" and order_status == OrderStatus.UNKNOWN:
        order_status = OrderStatus.CANCELED
    elif biz_result_code in {"PAY_FAIL", "REFUND_FAIL", "CANCEL_FAIL"}:
        order_status = OrderStatus.FAILED
    elif order_status == OrderStatus.UNKNOWN and biz_result_code in {"PAYING", "USERPAYING"}:
        order_status = OrderStatus.USERPAYING

    success = order_status in {
        OrderStatus.PAID,
        OrderStatus.REFUNDED,
        OrderStatus.PARTIAL_REFUNDED,
        OrderStatus.CANCELED,
    }
    reason = payload.get("error_message") or biz_response.get("error_message")

    return ParsedResult(
        transport_ok=transport_ok,
        api_ok=api_ok,
        order_status=order_status,
        final=order_status.is_final,
        success=success,
        reason=reason,
        raw=payload,
    )
