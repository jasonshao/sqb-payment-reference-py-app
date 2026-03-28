from app.protocol.status import OrderStatus
from app.support.status_parser import parse_result


def test_status_parser_returns_final_paid() -> None:
    parsed = parse_result(
        {
            "http_status": 200,
            "result_code": "200",
            "biz_response": {"result_code": "PAY_SUCCESS", "data": {"order_status": "PAID"}},
        }
    )
    assert parsed.order_status == OrderStatus.PAID
    assert parsed.final is True
    assert parsed.success is True


def test_status_parser_marks_failed_on_api_error() -> None:
    parsed = parse_result({"http_status": 200, "result_code": "500", "error_message": "oops"})
    assert parsed.order_status == OrderStatus.FAILED
    assert parsed.final is True
    assert parsed.success is False


def test_status_parser_maps_created_as_non_final() -> None:
    parsed = parse_result(
        {
            "http_status": 200,
            "result_code": "200",
            "biz_response": {"result_code": "ORDER_NOT_PAID", "data": {"order_status": "CREATED"}},
        }
    )
    assert parsed.order_status == OrderStatus.CREATED
    assert parsed.final is False
    assert parsed.success is False
